from django.utils.translation import gettext_lazy as _

class Question:  # pylint: disable=too-few-public-methods
    """
    Provide data for a question view, with different question types

    Relates to client component: Question.js
    """

    ID_RESULT_QUESTION = 'RESULT_QUESTION'
    ID_PROFILE_QUESTION = 'PROFILE_QUESTION'

    @staticmethod
    def action(question, title="", view=ID_PROFILE_QUESTION, button_label=_('Continue'), skip_label=_('Skip')):
        """Get data for question view"""
        return {
            'view': view,
            'question': question,
            'title': title,
            'button_label': button_label,
            'skip_label': skip_label
        }

    @staticmethod
    def profile_action(question, title=""):
        """Get data for profile question view"""
        return Question.action(question, title, Question.ID_PROFILE_QUESTION)

    @staticmethod
    def result_action(question, title=""):
        """Get data for a result question view"""
        return Question.action(question, title, Question.ID_RESULT_QUESTION)

    @staticmethod
    def button_array(key, question, choices, explainer="", is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip"), result_pk=None):
        """Create a button array question action"""
        return Question.action(
            question={
                'view': 'BUTTON_ARRAY',
                'key': key,
                'question': question,
                'explainer': explainer,
                'choices': choices,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label,
            result_pk=result_pk
        )

    @staticmethod
    def dropdown(key, question, choices, explainer="", is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a dropdown question action"""
        return Question.action(
            question={
                'view': 'DROPDOWN',
                'key': key,
                'question': question,
                'explainer': explainer,
                'choices': choices,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label)

    @staticmethod
    def checkboxes(key, question, choices, explainer="", is_skippable=False,  title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a checkboxes question action"""
        return Question.action(
            question={
                'view': 'CHECKBOXES',
                'key': key,
                'question': question,
                'explainer': explainer,
                'choices': choices,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )

    @staticmethod
    def range(key, question, min_value, max_value, explainer="", is_skippable=False, title="",  view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a range question action"""
        return Question.action(
            question={
                'view': 'RANGE',
                'key': key,
                'explainer': explainer,
                'question': question,
                'min_value': min_value,
                'max_value': max_value,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label)

    @staticmethod
    def text_range(key, question, choices, explainer="", is_skippable=False, title="",  view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a text_range question action"""
        return Question.action(
            question={
                'view': 'TEXT_RANGE',
                'key': key,
                'explainer': explainer,
                'question': question,
                'choices': choices,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label)

    @staticmethod
    def radios(key, question, choices, explainer="", is_skippable=False, title="",  view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a radios question action"""
        return Question.action(
            question={
                'view': 'RADIOS',
                'key': key,
                'question': question,
                'explainer': explainer,
                'choices': choices,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )

    @staticmethod
    def likert(key, question, explainer=_("How much do you agree or disagree?"), is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a likert question action"""
        return Question.text_range(
            key=key,
            question=question,
            choices=[
                _("Completely Disagree"),
                _("Strongly Disagree"),
                _("Disagree"),
                _("Neither Agree nor Disagree"),  # Undecided
                _("Agree"),
                _("Strongly Agree"),
                _("Completely Agree"),
            ],
            explainer=explainer,
            is_skippable=is_skippable,
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )

    @staticmethod
    def likert_radios(key, question, explainer=_("How much do you agree?"), is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a likert question action with radio buttons"""
        return Question.radios(
            key=key,
            question=question,
            choices={
                '1': _("Completely Disagree"),
                '2': _("Strongly Disagree"),
                '3': _("Disagree"),
                '4': _("Neither Agree nor Disagree"),  # Undecided
                '5': _("Agree"),
                '6': _("Strongly Agree"),
                '7': _("Completely Agree"),
            },
            explainer=explainer,
            is_skippable=is_skippable,
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )

    @staticmethod
    def string(key, question, max_length=140, is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a string question action"""
        return Question.action(
            question={
                'view': 'STRING',
                'key': key,
                'question': question,
                'max_length': max_length,
                'is_skippable': is_skippable,
            },
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )

    @staticmethod
    def certainty_radios(key, question=_("How certain are you of this answer?"), explainer="", is_skippable=False, title="", view=ID_PROFILE_QUESTION, button_label=_("Continue"), skip_label=_("Skip")):
        """Create a certainty question action with radio buttons"""
        return Question.radios(
            key=key,
            question=question,
            choices={
                '1': _("I guessed"),
                '2': _("I think I know"),
                '3': _("I am sure I know"),
            },
            explainer=explainer,
            is_skippable=is_skippable,
            title=title,
            view=view,
            button_label=button_label,
            skip_label=skip_label
        )
