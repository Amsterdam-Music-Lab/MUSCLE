from os.path import join
import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.db.models.query import QuerySet

from experiment.actions import Final
from session.models import Session, Result

EXPERIMENT_KEY = "experiment"


def get_current_experiment_url(session: Session) -> str | None:
    """
    Description: Retrieve the URL for the current experiment.

    Args:
        session (Session): The current user experiment session.

    Returns:
        (str | None): The URL for the current experiment.

    Example:
        ```python
        url = get_current_experiment_url(session)
        ```

    Note:
        Returns None if there is no experiment slug.
    """
    experiment_slug = session.json_data.get(EXPERIMENT_KEY)
    if not experiment_slug:
        return None

    if session.participant.participant_id_url:
        participant_id_url = session.participant.participant_id_url
        return f"/{experiment_slug}?participant_id={participant_id_url}"
    else:
        return f"/{experiment_slug}"


def final_action_with_optional_button(session, final_text="", title=_("End"), button_text=_("Continue")) -> Final:
    """
    Description: Create a final action with an optional button to proceed to the next block, if available.

    Args:
        session (Session): The current session.
        final_text (str): The text to display in the final action.
        title (str): The title for the final action screen.
        button_text (str): The text displayed on the continuation button.

    Returns:
        (Final): The final action with an optional button.

    Example:
        ```python
        action = final_action_with_optional_button(my_session, final_text="Complete!")
        ```
    """
    redirect_url = get_current_experiment_url(session)

    if redirect_url:
        return Final(
            title=title, session=session, final_text=final_text, button={"text": button_text, "link": redirect_url}
        )
    else:
        return Final(
            title=title,
            session=session,
            final_text=final_text,
        )


def render_feedback_trivia(feedback, trivia) -> str:
    """
    Description: Render feedback and trivia into the final template.

    Args:
        feedback (str): The feedback text.
        trivia (str): The trivia text.

    Returns:
        (str): The rendered HTML.

    Example:
        ```python
        rendered = render_feedback_trivia("Good job!", "Did you know ...?")
        ```

    Note: Can be used as the `final_text` parameter in the `Final` action or the `final_action_with_optional_button` function.
    """
    context = {"feedback": feedback, "trivia": trivia}
    return render_to_string(join("final", "feedback_trivia.html"), context)


def get_average_difference(session, num_turnpoints, initial_value) -> float:
    """
    Description: Calculate and return the average difference in milliseconds participants could hear (from the last `num_turnpoints` records).

    Args:
        session (Session): The current session.
        num_turnpoints (int): The number of last turnpoints to consider.
        initial_value (float): A fallback initial value.

    Returns:
        (float): The average difference in milliseconds.

    Example:
        ```python
        avg_diff = get_average_difference(my_session, 3, 20.0)
        ```
    """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        last_result = get_fallback_result(session)
        if last_result:
            return float(last_result.section.song.name)
        else:
            # this cannot happen in DurationDiscrimination style blocks
            # for future compatibility, still catch the condition that there may be no results
            return initial_value
    return sum([int(result.section.song.name) for result in last_turnpoints]) / last_turnpoints.count()


def get_average_difference_level_based(session, num_turnpoints, initial_value) -> float:
    """
    Description: Calculate the difference level based on exponential decay.

    Args:
        session (Session): The current session.
        num_turnpoints (int): The number of last turnpoints to consider.
        initial_value (float): The starting reference value.

    Returns:
        (float): The average difference in milliseconds.

    Example:
        ```python
        level_diff = get_average_difference_level_based(my_session, 5, 20.0)
        ```
    """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        # outliers
        last_result = get_fallback_result(session)
        if last_result:
            return initial_value / (2 ** (int(last_result.section.song.name.split("_")[-1]) - 1))
        else:
            # participant didn't pay attention,
            # no results right after the practice rounds
            return initial_value
    # Difference by level starts at initial value (which is level 1, so 20/(2^0)) and then halves for every next level
    return (
        sum([initial_value / (2 ** (int(result.section.song.name.split("_")[-1]) - 1)) for result in last_turnpoints])
        / last_turnpoints.count()
    )


def get_fallback_result(session) -> Result | None:
    """
    Description: Retrieve a fallback result if no turnpoints are found.

    Args:
        session (Session): The current session.

    Returns:
        (Result | None): The fallback result.

    Example:
        ```python
        fallback = get_fallback_result(my_session)
        ```
    """
    if session.result_set.count() == 0:
        # stopping right after practice rounds
        return None

    # TODO: Check if this is the correct way to get the last result as Python says .order_by returns a "Unknown" type
    result = session.result_set.order_by("-created_at")[0]
    return result


def get_last_n_turnpoints(session, num_turnpoints) -> QuerySet[Result]:
    """
    Description: Return the specified number of most recent turnpoint results from the session.

    Args:
        session (Session): The current session.
        num_turnpoints (int): How many latest turnpoint results to retrieve.

    Returns:
        (QuerySet[Result]): The latest turnpoint results.

    Example:
        ```python
        turnpoints = get_last_n_turnpoints(my_session, 3)
        ```
    """
    all_results = session.result_set.filter(comment__iendswith="turnpoint").order_by("-created_at").all()
    cutoff = min(all_results.count(), num_turnpoints)
    return all_results[:cutoff]


def randomize_playhead(min_jitter, max_jitter, continuation_correctness) -> float:
    """
    Description: Randomly create a playhead offset if correctness is not yet established.

    Args:
        min_jitter (float): Minimum offset.
        max_jitter (float): Maximum offset.
        continuation_correctness (bool): Whether the user is already correct.

    Returns:
        (float): The random offset.

    Example:
        ```python
        offset = randomize_playhead(0.5, 1.5, False)
        ```
    """
    return random.uniform(min_jitter, max_jitter) if not continuation_correctness else 0
