import csv
from zipfile import ZipFile
from io import BytesIO

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.core import serializers
from django.shortcuts import render, redirect
from django.forms import CheckboxSelectMultiple
from django.http import HttpResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from django.urls import reverse
from django.utils.html import format_html

from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from experiment.models import (
    Block,
    Experiment,
    Phase,
    Feedback,
    SocialMediaConfig,
    ExperimentTranslatedContent,
)
from question.admin import QuestionSeriesInline
from experiment.forms import (
    ExperimentForm,
    BlockForm,
    ExportForm,
    TemplateForm,
    SocialMediaConfigForm,
    EXPORT_TEMPLATES,
)
from section.models import Section, Song
from result.models import Result
from participant.models import Participant


class FeedbackInline(admin.TabularInline):
    """Inline to show results linked to given participant"""

    model = Feedback
    fields = ["text"]
    extra = 0


class ExperimentTranslatedContentInline(NestedStackedInline):
    model = ExperimentTranslatedContent
    sortable_field_name = "index"

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class BlockAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "image_preview",
        "block_name_link",
        "block_slug_link",
        "rules",
        "rounds",
        "playlist_count",
        "session_count",
        "active",
    )
    list_filter = ["active"]
    search_fields = ["name"]
    inline_actions = ["export", "export_csv"]
    fields = [
        "name",
        "description",
        "image",
        "slug",
        "url",
        "hashtag",
        "theme_config",
        "language",
        "active",
        "rules",
        "rounds",
        "bonus_points",
        "playlists",
        "consent",
    ]
    inlines = [QuestionSeriesInline, FeedbackInline]
    form = BlockForm

    # make playlists fields a list of checkboxes
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def export(self, request, obj, parent_obj=None):
        """Export block JSON data as zip archive, force download"""

        # Init empty querysets
        all_results = Result.objects.none()
        all_songs = Song.objects.none()
        all_sections = Section.objects.none()
        all_participants = Participant.objects.none()
        all_profiles = Result.objects.none()

        # Collect data
        all_sessions = obj.export_sessions().order_by("pk")

        for session in all_sessions:
            all_results |= session.export_results()
            all_participants |= Participant.objects.filter(pk=session.participant.pk)
            all_profiles |= session.participant.export_profiles()

        for playlist in obj.playlists.all():
            these_sections = playlist.export_sections()
            all_sections |= these_sections
            for section in these_sections:
                if section.song:
                    all_songs |= Song.objects.filter(pk=section.song.pk)

        # create empty zip file in memory
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as new_zip:
            # serialize data to new json files within the zip file
            new_zip.writestr("sessions.json", data=str(serializers.serialize("json", all_sessions)))
            new_zip.writestr(
                "participants.json",
                data=str(serializers.serialize("json", all_participants.order_by("pk"))),
            )
            new_zip.writestr(
                "profiles.json",
                data=str(serializers.serialize("json", all_profiles.order_by("participant", "pk"))),
            )
            new_zip.writestr(
                "results.json",
                data=str(serializers.serialize("json", all_results.order_by("session"))),
            )
            new_zip.writestr(
                "sections.json",
                data=str(serializers.serialize("json", all_sections.order_by("playlist", "pk"))),
            )
            new_zip.writestr(
                "songs.json",
                data=str(serializers.serialize("json", all_songs.order_by("pk"))),
            )

        # create forced download response
        response = HttpResponse(zip_buffer.getbuffer())
        response["Content-Type"] = "application/x-zip-compressed"
        response["Content-Disposition"] = (
            'attachment; filename="' + obj.slug + "-" + timezone.now().isoformat() + '.zip"'
        )
        return response

    export.short_description = "Export JSON"

    def export_csv(self, request, obj, parent_obj=None):
        """Export block data in CSV, force download"""
        # Handle export command from intermediate form
        if "_export" in request.POST:
            session_keys = []
            result_keys = []
            export_options = []
            # Get all export options
            session_keys = [key for key in request.POST.getlist("export_session_fields")]
            result_keys = [key for key in request.POST.getlist("export_result_fields")]
            export_options = [key for key in request.POST.getlist("export_options")]

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(obj.slug)
            # Get filtered data
            block_table, fieldnames = obj.export_table(session_keys, result_keys, export_options)
            fieldnames.sort()
            writer = csv.DictWriter(response, fieldnames)
            writer.writeheader()
            writer.writerows(block_table)
            return response
        # Go back to admin block overview
        if "_back" in request.POST:
            return redirect("/admin/experiment/block")
        # Load a template in the export form
        if "_template" in request.POST:
            selected_template = request.POST.get("select_template")
        else:
            selected_template = "wide"

        initial_fields = {
            "export_session_fields": EXPORT_TEMPLATES[selected_template][0],
            "export_result_fields": EXPORT_TEMPLATES[selected_template][1],
            "export_options": EXPORT_TEMPLATES[selected_template][2],
        }
        form = ExportForm(initial=initial_fields)
        template_form = TemplateForm(initial={"select_template": selected_template})
        return render(
            request,
            "csv-export.html",
            context={"exp_block": obj, "form": form, "template_form": template_form},
        )

    export_csv.short_description = "Export CSV"

    def image_preview(self, obj):
        if obj.image and obj.image.file:
            img_src = obj.image.file.url
            return format_html(f'<img src="{img_src}" style="max-height: 50px;"/>')
        return ""

    def block_name_link(self, obj):
        """Generate a link to the block's admin change page."""
        url = reverse("admin:experiment_block_change", args=[obj.pk])
        name = obj.name or obj.slug or "No name"
        return format_html('<a href="{}">{}</a>', url, name)

    def block_slug_link(self, obj):
        dev_mode = settings.DEBUG is True
        url = f"http://localhost:3000/block/{obj.slug}" if dev_mode else f"/block/{obj.slug}"

        return format_html(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" title="Open {obj.slug} block in new tab" >{obj.slug}&nbsp;<small>&#8599;</small></a>'
        )

    # Name the columns
    image_preview.short_description = "Image"
    block_name_link.short_description = "Name"
    block_slug_link.short_description = "Slug"


admin.site.register(Block, BlockAdmin)


class BlockInline(NestedStackedInline):
    model = Block
    sortable_field_name = "index"

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class PhaseInline(NestedTabularInline):
    model = Phase
    sortable_field_name = "index"
    inlines = [BlockInline]

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class SocialMediaConfigInline(NestedStackedInline):
    form = SocialMediaConfigForm
    model = SocialMediaConfig

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class ExperimentAdmin(InlineActionsModelAdminMixin, NestedModelAdmin):
    list_display = (
        "name",
        "slug_link",
        "description_excerpt",
        "remarks",
        "dashboard",
        "phases",
        "active",
    )
    fields = [
        "slug",
        "active",
        "theme_config",
        "dashboard",
    ]
    inline_actions = ["dashboard"]
    form = ExperimentForm
    inlines = [
        ExperimentTranslatedContentInline,
        PhaseInline,
        SocialMediaConfigInline,
    ]

    class Media:
        css = {"all": ("experiment_admin.css",)}

    def name(self, obj):
        content = obj.get_fallback_content()
        return content.name if content else "No name"

    def slug_link(self, obj):
        dev_mode = settings.DEBUG is True
        url = f"http://localhost:3000/{obj.slug}" if dev_mode else f"/{obj.slug}"

        return format_html(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" title="Open {obj.slug} experiment group in new tab" >{obj.slug}&nbsp;<small>&#8599;</small></a>'
        )

    def description_excerpt(self, obj):
        fallback_content = obj.get_fallback_content()
        description = (
            fallback_content.description if fallback_content and fallback_content.description else "No description"
        )
        if len(description) < 50:
            return description

        return description[:50] + "..."

    def phases(self, obj):
        phases = Phase.objects.filter(series=obj)
        return format_html(
            ", ".join([f'<a href="/admin/experiment/phase/{phase.id}/change/">{phase.name}</a>' for phase in phases])
        )

    slug_link.short_description = "Slug"

    def dashboard(self, request, obj, parent_obj=None):
        """Open researchers dashboard for an experiment"""
        all_blocks = obj.associated_blocks()
        all_participants = obj.current_participants()
        all_sessions = obj.export_sessions()
        collect_data = {
            "participant_count": len(all_participants),
            "session_count": len(all_sessions),
        }

        blocks = [
            {
                "id": block.id,
                "name": block.name,
                "started": len(all_sessions.filter(block=block)),
                "finished": len(
                    all_sessions.filter(
                        block=block,
                        finished_at__isnull=False,
                    )
                ),
                "participant_count": len(block.current_participants()),
                "participants": block.current_participants(),
            }
            for block in all_blocks
        ]

        return render(
            request,
            "experiment-dashboard.html",
            context={
                "experiment": obj,
                "blocks": blocks,
                "sessions": all_sessions,
                "participants": all_participants,
                "collect_data": collect_data,
            },
        )

    def remarks(self, obj):
        remarks_array = []

        # Check if there is any translated content
        content = obj.translated_content.first()

        if not content:
            remarks_array.append(
                {
                    "level": "warning",
                    "message": "📝 No content",
                    "title": "Please add at least one translated content to this experiment.",
                }
            )

        has_consent = obj.translated_content.filter(consent__isnull=False).exclude(consent="").first()

        if not has_consent:
            remarks_array.append(
                {
                    "level": "info",
                    "message": "📋 No consent form",
                    "title": "Please add at least one consent form to this experiment.",
                }
            )

        if not remarks_array:
            remarks_array.append({"level": "success", "message": "✅ All good", "title": "No issues found."})

        supported_languages = obj.translated_content.values_list("language", flat=True).distinct()

        # TODO: Check if all blocks support the same languages as the experiment
        # Implement this when the blocks have been updated to support multiple languages

        # TODO: Check if all theme configs support the same languages as the experiment
        # Implement this when the theme configs have been updated to support multiple languages

        # TODO: Check if all social media configs support the same languages as the experiment
        # Implement this when the social media configs have been updated to support multiple languages

        return format_html(
            "\n".join(
                [
                    f'<span class="badge badge-{remark["level"]} whitespace-nowrap text-xs mt-1" title="{remark.get("title") if remark.get("title") else remark["message"]}">{remark["message"]}</span>'
                    for remark in remarks_array
                ]
            )
        )


admin.site.register(Experiment, ExperimentAdmin)


class PhaseAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "name_link",
        "related_experiment",
        "index",
        "dashboard",
        "randomize",
        "blocks",
    )
    fields = ["name", "series", "index", "dashboard", "randomize"]
    inlines = [BlockInline]

    def name_link(self, obj):
        obj_name = obj.__str__()
        url = reverse("admin:experiment_phase_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj_name)

    def related_experiment(self, obj):
        url = reverse("admin:experiment_experiment_change", args=[obj.series.pk])
        content = obj.series.get_fallback_content()
        experiment_name = content.name if content else "No name"
        return format_html('<a href="{}">{}</a>', url, experiment_name)

    def blocks(self, obj):
        blocks = Block.objects.filter(phase=obj)

        if not blocks:
            return "No blocks"

        return format_html(
            ", ".join([f'<a href="/admin/experiment/block/{block.id}/change/">{block.name}</a>' for block in blocks])
        )


admin.site.register(Phase, PhaseAdmin)
