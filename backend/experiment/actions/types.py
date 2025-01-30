from typing import TypedDict


class FeedbackInfo(TypedDict):
    header: str
    button: str
    contact_body: str
    thank_you: str
    show_float_button: bool
