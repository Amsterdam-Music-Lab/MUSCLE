from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import render, redirect

from inline_actions.admin import InlineActionsModelAdminMixin
from django.urls import reverse
from django.utils.html import format_html

from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from experiment.models import (
    Block,
    BlockText,
    Experiment,
    ExperimentText,
    Phase,
    SocialMediaConfig,
)
from experiment.forms import (
    BlockForm,
    BlockTranslatedContentForm,
    ExperimentForm,
    ExperimentTranslatedContentForm,
    SocialMediaConfigForm,
)
from question.admin import QuestionSeriesInline
from question.models import QuestionSeries, QuestionInSeries
from .utils import export_json_results


class BlockTextInline(NestedTabularInline):
    model = BlockText
    form = BlockTranslatedContentForm
    extra = 0
    fields = [
        "name",
        "description",
    ]
    can_delete = False
    verbose_name = 'Block Text'

    def has_add_permission(self, request, obj):
        return False


class ExperimentTextInline(NestedStackedInline):
    model = ExperimentText
    form = ExperimentTranslatedContentForm
    extra = 1


class BlockInline(NestedStackedInline):
    model = Block
    inlines = [BlockTextInline, QuestionSeriesInline]
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
        "name",
        "slug_link",
        "remarks",
        "active",
    )
    fields = [
        "slug",
        "active",
        "theme_config",
    ]
    inline_actions = ["experimenter_dashboard", "duplicate"]
    form = ExperimentForm
    inlines = [
        ExperimentTextInline,
        PhaseInline,
        SocialMediaConfigInline,
    ]

    class Media:
        css = {"all": ("experiment_admin.css",)}

    def name(self, obj):
        return obj.name or "No name"

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
            exp_contents = obj.text.order_by("name").all()
            # order_by is inserted here to prevent a query error
            exp_phases = obj.phases.order_by("index").all()

            # Duplicate Experiment object
            exp_copy = obj
            exp_copy.pk = None
            exp_copy._state.adding = True
            exp_copy.slug = f"{obj.slug}{slug_extension}"
            exp_copy.save()

            # Duplicate experiment translated content objects
            for content in exp_contents:
                exp_content_copy = content
                exp_content_copy.pk = None
                exp_content_copy._state.adding = True
                exp_content_copy.experiment = exp_copy
                exp_content_copy.save()

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
                    block_contents = blocktext.order_by('name').all()
                    these_playlists = block.playlists.all()
                    question_series = QuestionSeries.objects.filter(block=block)

                    block_copy = block
                    block_copy.pk = None
                    block_copy._state.adding = True
                    block_copy.slug = f"{block.slug}{slug_extension}"
                    block_copy.phase = phase_copy
                    block_copy.save()
                    block_copy.playlists.set(these_playlists)

                    # Duplicate Block translated content objects
                    for content in block_contents:
                        block_content_copy = content
                        block_content_copy.pk = None
                        block_content_copy._state.adding = True
                        block_content_copy.block = block_copy
                        block_content_copy.save()

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
                "name": block,
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

        if not obj.text.name:
            remarks_array.append(
                {
                    "level": "warning",
                    "message": "📝 No content",
                    "title": "Add content in at least one language to this experiment.",
                }
            )

        if not obj.text.consent:
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

        # TODO: Check if all theme configs support the same languages as the experiment
        # Implement this when the theme configs have been updated to support multiple languages

        # TODO: Check if all social media configs support the same languages as the experiment
        # Implement this when the social media configs have been updated to support multiple languages

        return format_html(
            "\n".join(
                [
                    f'<span class="badge badge-{remark["level"]} whitespace-nowrap text-xs mt-1" title="{remark.get("title") if remark.get("title") else remark["message"]}">{remark["message"]}</span><br>'
                    for remark in remarks_array
                ]
            )
        )

    def save_model(self, request, obj, form, change):
        # Save the model
        super().save_model(request, obj, form, change)

        # Check for missing translations after saving
        missing_content_blocks = get_missing_content_blocks(obj)

        if missing_content_blocks:
            for block, missing_languages in missing_content_blocks:
                missing_language_flags = [
                    get_flag_emoji(language) for language in missing_languages
                ]
                self.message_user(
                    request,
                    f"Block {block.slug} does not have content in {', '.join(missing_language_flags)}",
                    level=messages.WARNING,
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


class BlockTranslatedContentAdmin(admin.ModelAdmin):
    list_display = ["name", "block", "language"]
    list_filter = ["language"]
    search_fields = [
        "name",
        "block__name",
    ]

    def blocks(self, obj):
        # Block is manytomany, so we need to find it through the related name
        blocks = Block.objects.filter(texts=obj)

        if not blocks:
            return "No block"

        return format_html(
            ", ".join(
                [
                    f'<a href="/admin/experiment/block/{block.id}/change/">{block.name}</a>'
                    for block in blocks
                ]
            )
        )

admin.site.register(Experiment, ExperimentAdmin)
