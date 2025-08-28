from django.utils.translation import gettext_lazy as _

BOOLEAN = {
    "yes": _("Yes"),
    "no": _("No")
}

BOOLEAN_NEGATIVE_FIRST = {
    "no": _("No"),
    "yes": _("Yes"),
}

LIKERT_AGREE_5 = {
    1: _("Strongly Disagree"),
    2: _("Disagree"),
    3: _("Neither Agree nor Disagree"),  # Undecided
    4: _("Agree"),
    5: _("Strongly Agree"),
}

LIKERT_AGREE_7 = {
    1: _("Completely Disagree"),
    2: _("Strongly Disagree"),
    3: _("Disagree"),
    4: _("Neither Agree nor Disagree"),  # Undecided
    5: _("Agree"),
    6: _("Strongly Agree"),
    7: _("Completely Agree"),
}

LIKERT_PREFERENCE_7 = {
    1: _("Dislike Strongly"),
    2: _("Dislike Moderately"),
    3: _("Dislike a Little"),
    4: _("Neither Like nor Dislike"),
    5: _("Like a Little"),
    6: _("Like Moderately"),
    7: _("Like Strongly")
}

LIKERT_ICONS_7 = {
    1: "fa-face-grin-hearts",
    2: "fa-face-grin",
    3: "fa-face-smile",
    4: "fa-face-meh",  # Undecided
    5: "fa-face-frown",
    6: "fa-face-frown-open",
    7: "fa-face-angry",
}