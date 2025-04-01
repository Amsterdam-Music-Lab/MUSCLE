from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import render, redirect

from inline_actions.admin import InlineActionsModelAdminMixin
from django.urls import reverse
from django.utils.html import format_html

from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from experiment.models import (
    Block,
    Experiment,
    Phase,
    SocialMediaConfig,
)
from experiment.forms import (
    BlockForm,
    ExperimentForm,
    SocialMediaConfigForm,
)
from question.admin import QuestionSeriesInline
from question.models import QuestionSeries, QuestionInSeries
from .utils import export_json_results


class BlockInline(NestedStackedInline):
    model = Block
    inlines = [QuestionSeriesInline]
    form = BlockForm
    autocomplete_fields = ["playlists"]
    classes = ["wide"]

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
        "experiment_name",
        "slug_link",
        "remarks",
        "active",
    )
    inline_actions = ["experimenter_dashboard", "duplicate"]
    form = ExperimentForm
    inlines = [
        PhaseInline,
        SocialMediaConfigInline,
    ]

    class Media:
        css = {"all": ("experiment_admin.css",)}

    def experiment_name(self, obj):
        return obj.name or "No name"

    experiment_name.short_description = "Name"

    def redirect_to_overview(self):
        return redirect(reverse("admin:experiment_experiment_changelist"))

    def slug_link(self, obj):
        dev_mode = settings.DEBUG is True
        url = f"http://localhost:3000/{obj.slug}" if dev_mode else f"/{obj.slug}"

        return format_html(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" title="Open {obj.slug} experiment group in new tab" >{obj.slug}&nbsp;<small>&#8599;</small></a>'
        )

    slug_link.short_description = "Slug"

    def duplicate(self, request, obj, parent_obj=None):
        """Duplicate an experiment"""

        if "_duplicate" in request.POST:
            # Get slug from the form
            extension = request.POST.get("slug-extension")
            if extension == "":
                extension = "copy"
            slug_extension = f"-{extension}"

            # Validate slug
            if not extension.isalnum():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{extension} is nog a valid slug extension. Only alphanumeric characters are allowed.",
                )
            if extension.lower() != extension:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"{extension} is nog a valid slug extension. Only lowercase characters are allowed.",
                )
            # Check for duplicate slugs
            for exp in Experiment.objects.all():
                if exp.slug == f"{obj.slug}{slug_extension}":
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"An experiment with slug: {obj.slug}{slug_extension} already exists. Please choose a different slug extension.",
                    )
            for as_block in obj.associated_blocks():
                for block in Block.objects.all():
                    if f"{as_block.slug}{slug_extension}" == block.slug:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            f"A block with slug: {block.slug}{slug_extension} already exists. Please choose a different slug extension.",
                        )
            # Return to form with error messages
            if len(messages.get_messages(request)) != 0:
                return render(
                    request,
                    "duplicate-experiment.html",
                    context={"exp": obj},
                )

            # order_by is inserted here to prevent a query error
            exp_phases = obj.phases.order_by("index").all()

            # Duplicate Experiment object
            exp_copy = obj
            exp_copy.pk = None
            exp_copy._state.adding = True
            exp_copy.slug = f"{obj.slug}{slug_extension}"
            exp_copy.save()

            # Duplicate phases
            for phase in exp_phases:
                these_blocks = Block.objects.filter(phase=phase)

                phase_copy = phase
                phase_copy.pk = None
                phase_copy._state.adding = True
                phase_copy.save()

                # Duplicate blocks in this phase
                for block in these_blocks:
                    # order_by is inserted here to prevent a query error
                    these_playlists = block.playlists.all()
                    question_series = QuestionSeries.objects.filter(block=block)

                    block_copy = block
                    block_copy.pk = None
                    block_copy._state.adding = True
                    block_copy.slug = f"{block.slug}{slug_extension}"
                    block_copy.phase = phase_copy
                    block_copy.save()
                    block_copy.playlists.set(these_playlists)

                    # Duplicate the Block QuestionSeries
                    for series in question_series:
                        all_in_series = QuestionInSeries.objects.filter(
                            question_series=series
                        )
                        these_questions = series.questions.all()
                        series_copy = series
                        series_copy.pk = None
                        series_copy._state.adding = True
                        series_copy.block = block_copy
                        series_copy.index = block.index
                        series_copy.save()

                        # Duplicate the QuestionSeries QuestionInSeries
                        for in_series in all_in_series:
                            in_series_copy = in_series
                            in_series_copy.pk = None
                            in_series_copy._state.adding = True
                            in_series_copy.question_series = series
                            in_series_copy.save()
                        series_copy.questions.set(these_questions)

            return self.redirect_to_overview()

        # Go back to experiment overview
        if "_back" in request.POST:
            return self.redirect_to_overview()

        # Show experiment duplicate form
        return render(
            request,
            "duplicate-experiment.html",
            context={"exp": obj},
        )

    def experimenter_dashboard(self, request, obj, parent_obj=None):
        """Open researchers dashboard for an experiment"""

        if "_export" in request.POST:
            blockId = request.POST.get("export-block")
            return export_json_results(blockId)

        all_blocks = obj.associated_blocks()
        all_participants = obj.current_participants()
        all_sessions = obj.export_sessions()
        all_feedback = obj.export_feedback()
        collect_data = {
            "participant_count": len(all_participants),
            "session_count": len(all_sessions),
            "feedback_count": len(all_feedback),
        }

        blocks = [
            {
                "id": block.id,
                "slug": block.slug,
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
                "feedback": all_feedback,
                "collect_data": collect_data,
            },
        )

    def remarks(self, obj):
        remarks_array = []

        if not obj.name:
            remarks_array.append(
                {
                    "level": "warning",
                    "message": "📝 No content",
                    "title": "Add content in at least one language to this experiment.",
                }
            )

        if not obj.consent:
            remarks_array.append(
                {
                    "level": "info",
                    "message": "📋 No consent form",
                    "title": "You may want to add a consent form (approved by an ethical board) to this experiment.",
                }
            )

        if not remarks_array:
            remarks_array.append(
                {
                    "level": "success",
                    "message": "✅ All good",
                    "title": "No issues found.",
                }
            )

        return format_html(
            "\n".join(
                [
                    f'<span class="badge badge-{remark["level"]} whitespace-nowrap text-xs mt-1" title="{remark.get("title") if remark.get("title") else remark["message"]}">{remark["message"]}</span><br>'
                    for remark in remarks_array
                ]
            )
        )


class PhaseAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "name_link",
        "related_experiment",
        "index",
        "dashboard",
        "randomize",
        "blocks",
    )
    fields = ["name", "experiment", "index", "dashboard", "randomize"]
    inlines = [BlockInline]

    def name_link(self, obj):
        obj_name = obj.__str__()
        url = reverse("admin:experiment_phase_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj_name)

    def related_experiment(self, obj):
        url = reverse("admin:experiment_experiment_change", args=[obj.experiment.pk])
        experiment_name = obj.experiment.name or "No name"
        return format_html('<a href="{}">{}</a>', url, experiment_name)

    def blocks(self, obj):
        blocks = Block.objects.filter(phase=obj)

        if not blocks:
            return "No blocks"

        return format_html(", ".join([block.slug for block in blocks]))


admin.site.register(Experiment, ExperimentAdmin)
