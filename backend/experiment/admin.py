from itertools import chain

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from inline_actions.admin import InlineActionsModelAdminMixin
from modeltranslation.admin import TabbedTranslationAdmin

from experiment.models import (
    Block,
    Experiment,
    Feedback,
    Phase,
    SocialMediaConfig,
)
from experiment.forms import (
    BlockForm,
    SocialMediaConfigForm,
)
from experiment.widgets import MarkdownPreviewTextInput
from question.admin import QuestionListInline
from question.models import QuestionList, QuestionInList
from .utils import get_block_json_export_as_repsonse


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback

    list_display = ("block", "text")
    list_filter = [
        ('block', admin.RelatedOnlyFieldListFilter),
    ]

    def has_module_permission(self, request):
        '''Prevents the admin from being shown in the sidebar.'''
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False


class BlockAdmin(TabbedTranslationAdmin):
    model = Block
    inlines = [QuestionListInline]
    autocomplete_fields = ["playlists"]
    form = BlockForm

    def has_module_permission(self, request):
        ''' Prevents the admin from being shown in the sidebar.'''
        return False

    def save_model(self, request, obj, form, changed):
        if request.GET.get('phase_id'):
            phase_id = int(request.GET.get('phase_id'))
            phase = Phase.objects.get(pk=phase_id)
            obj.phase = phase
        super().save_model(request, obj, form, changed)

    def response_change(self, request, obj):
        return self._close_popup()

    def response_add(self, request, obj, post_url_continue=None):
        return self._close_popup()

    def response_delete(self, request, obj_display, obj_id):
        return self._close_popup()

    def _close_popup(self):
        return HttpResponse(
            '<script type="text/javascript">window.close(); window.opener.location.reload();</script>'
        )


class PhaseInline(admin.StackedInline):
    model = Phase
    sortable_field_name = "index"
    template = "admin/phase_inline.html"
    show_change_link = True
    extra = 0

    class Media:
        js = ["add_phase_handler.js"]
        css = {"all": ("phase_inline.css",)}


class SocialMediaConfigInline(admin.StackedInline):
    form = SocialMediaConfigForm
    model = SocialMediaConfig

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class ExperimentAdmin(InlineActionsModelAdminMixin, TabbedTranslationAdmin):
    list_display = (
        "experiment_name",
        "slug_link",
        "remarks",
        "active",
    )
    inline_actions = ["experimenter_dashboard", "duplicate"]

    inlines = [
        PhaseInline,
        SocialMediaConfigInline,
    ]

    save_on_top = True

    def get_formsets_with_inlines(self, request, obj=None):
        """only show inlines if the experiment has already been saved"""
        if obj:
            for inline in self.get_inline_instances(request, obj):
                yield inline.get_formset(request, obj), inline

    formfield_overrides = {
        models.TextField: {"widget": MarkdownPreviewTextInput},
    }

    def experiment_name(self, obj):
        return obj.name or "<Unnamed>"

    experiment_name.short_description = "Name"

    def save_model(self, request, obj, form, changed):
        """delete all phases which don't have associated blocks when saving"""
        if obj.pk:
            phases = obj.phases
            for phase in phases.all():
                if not phase.blocks.count():
                    phase.delete()
        super().save_model(request, obj, form, changed)

    def redirect_to_overview(self):
        return redirect(reverse("admin:experiment_experiment_changelist"))

    def slug_link(self, obj):
        dev_mode = settings.DEBUG is True
        url = f"http://localhost:3000/{obj.slug}" if dev_mode else f"/{obj.slug}"

        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="Open {} experiment group in new tab" >{}</a>',
            url,
            obj.slug,
            obj.slug,
        )

    slug_link.short_description = "Slug"

    def duplicate(self, request, obj, parent_obj=None):
        """Duplicate an experiment"""

        if "_duplicate" in request.POST:
            # Get slug from the form
            extension = request.POST.get("slug-extension")
            if extension == "":
                extension = "copy"

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
            if Experiment.objects.filter(slug=f"{obj.slug}-{extension}").exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"An experiment with slug: {obj.slug}-{extension} already exists. Please choose a different slug extension.",
                )
            extended_blog_slugs = [
                f"{block.slug}-{extension}" for block in obj.associated_blocks()
            ]
            if Block.objects.filter(slug__in=extended_blog_slugs).exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"A block with slug: {block.slug}-{extension} already exists. Please choose a different slug extension.",
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
            exp_copy.slug = f"{obj.slug}-{extension}"
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
                    question_lists = QuestionList.objects.filter(block=block)

                    block_copy = block
                    block_copy.pk = None
                    block_copy._state.adding = True
                    block_copy.slug = f"{block.slug}-{extension}"
                    block_copy.phase = phase_copy
                    block_copy.save()
                    block_copy.playlists.set(these_playlists)

                    # Duplicate the Block QuestionList
                    for ql in question_lists:
                        all_in_question_list = QuestionInList.objects.filter(
                            questionlist=ql
                        )
                        these_questions = ql.questions.all()
                        ql_copy = ql
                        ql_copy.pk = None
                        ql_copy._state.adding = True
                        ql_copy.block = block_copy
                        ql_copy.index = block.index
                        ql_copy.save()

                        # Duplicate the QuestionList QuestionInList
                        for in_ql in all_in_question_list:
                            in_ql_copy = in_ql
                            in_ql_copy.pk = None
                            in_ql_copy._state.adding = True
                            in_ql_copy.questionlist = ql
                            in_ql_copy.save()
                        ql_copy.questions.set(these_questions)

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
            block_slug = request.POST.get("export-block")
            return get_block_json_export_as_repsonse(block_slug)

        annotated_blocks = self._annotate_blocks(obj.associated_blocks())
        stats = self._generate_stats(annotated_blocks)

        blocks = annotated_blocks.values(
            "id",
            "slug",
            "name",
            "participants",
            "n_feedback",
            "n_sessions",
            "n_sessions_finished",
            "n_participants",
        )

        return render(
            request,
            "experiment-dashboard.html",
            context={
                "experiment": obj,
                "blocks": blocks,
                "stats": stats,
            },
        )

    def _annotate_blocks(self, blocks: QuerySet[Block]) -> QuerySet[Block]:
        """add annotations to QuerySet of experiment blocks indicating the number of sessions and feedback per block

        Args:
            blocks: QuerySet of blocks

        Returns:
            Queryset of blocks with annotations of `n_feedback`, `n_sessions`, `n_sessions_finished`, `n_participants`
        """
        all_blocks = blocks.annotate(
            participants=ArrayAgg(
                "sessions__participant__id",
                distinct=True,
            ),
            n_feedback=models.Count("feedback", distinct=True),
            n_sessions=models.Count("sessions"),
            n_sessions_finished=models.Count(
                "sessions", filter=models.Q(sessions__finished_at__isnull=False)
            ),
            n_participants=models.Count("sessions__participant", distinct=True),
        )
        return all_blocks

    def _generate_stats(self, annotated_blocks: QuerySet[Block]) -> dict:
        """Calculate the total number of participants, feedback and sessionsfor the experiment"""
        participant_count = len(
            set(
                chain.from_iterable(
                    [
                        stat.get('participants')
                        for stat in annotated_blocks.values('participants')
                    ]
                )
            )
        )
        return {
            "participant_count": participant_count,
            "session_count": annotated_blocks.aggregate(models.Sum('n_sessions')).get(
                'n_sessions__sum'
            ),
            "feedback_count": annotated_blocks.aggregate(models.Sum('n_feedback')).get(
                'n_feedback__sum'
            ),
        }

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

        return format_html_join(
            '\n',
            '<span class="badge badge-{} whitespace-nowrap text-xs mt-1" title="{}" >{}</span><br>',
            (
                (
                    remark["level"],
                    remark["title"],
                    remark["message"],
                )
                for remark in remarks_array
            ),
        )

admin.site.register(Block, BlockAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
