import random
from typing import Optional

from django.db.models import QuerySet

from result.models import Result
from session.models import Session

class StaircasingMixin(object):
    """ The Staircasing mixin can be used to determine whether difficulty should increase or decrease, 
    and to register turnpoints if the difficulty change reverses.

    Attributes:
        max_turnpoints (int): after how many changes to difficulty increase / decrease the block should finish
        block_size (int): in case staircasing is registered in blocks, how many trials go into each block
        increase_diffulty_multiplier (float): if difficulty increases, by which number to multiply it to get the next difficulty
        decrease_difficulty_multiplier (float): if difficulty decreases, by which number to multiply it to get the next difficulty
        first_condition (str): label of the first condition (cf. also PracticeMixin), used to check correctness
        second_condition (str): label of the second condition (cf. also PracticeMixin), used to check correctness
    
    """
    max_turnpoints = 8
    block_size = 5
    increase_difficulty_multiplier = .5
    decrease_difficulty_multiplier = 1.5
    first_condition = "longer"
    second_condition = "shorter"

    def get_next_trial(self, session: Session):
        raise NotImplementedError

    def get_fallback_result(self, session: Session) -> Optional[Result]:
        """
        Description: Retrieve a fallback result if no turnpoints are found.

        Args:
            session (Session): The current session.

        Returns:
            (Result | None): The fallback result.
        """
        if session.result_set.count() == 0:
            # stopping right after practice rounds
            return None

        # TODO: Check if this is the correct way to get the last result as Python says .order_by returns a "Unknown" type
        result = session.result_set.order_by("-created_at")[0]
        return result

    def get_last_n_turnpoints(self, session: Session, num_turnpoints: int) -> QuerySet[Result]:
        """
        Description: Return the specified number of most recent turnpoint results from the session.

        Args:
            session (Session): The current session.
            num_turnpoints (int): How many latest turnpoint results to retrieve.

        Returns:
            (QuerySet[Result]): The latest turnpoint results.
        """
        all_results = (
            session.result_set.filter(comment__iendswith="turnpoint")
            .order_by("-created_at")
            .all()
        )
        cutoff = min(all_results.count(), num_turnpoints)
        return all_results[:cutoff]

    def get_trial_condition(self, session: Session) -> str:
        """make a list of the {block_size} conditions, of which one is a catch condition
        store updates in the session.json_data field
        """
        current_trials = session.json_data.get("current_trials")
        if not current_trials:
            current_trials = [self.first_condition] * (self.block_size - 1) + [
                self.second_condition
            ]
            random.shuffle(current_trials)
        condition = current_trials.pop()
        session.save_json_data({"current_trials": current_trials})
        session.save()
        return condition

    def last_non_catch_correct(self, previous_results: list[Result]) -> bool:
        """ check if previous responses (before the current one, which is correct)
        have been catch or non-catch, and if non-catch, if they were correct
        """
        n_results = len(previous_results)
        # get the previous scores and conditions, from most to least recent
        results = [previous_results[r] for r in range(1, n_results)]
        answer = False
        while results:
            result = results.pop(0)
            if result.score == 1:
                if result.comment:
                    # a comment on the second-to-last result indicates that difficulty changed there;
                    # we need to wait for another correct response before changing again
                    break
                else:
                    answer = True
                    break
            elif result.expected_response == self.second_condition:
                continue
            else:
                break
        return answer

    def register_turnpoint(self, session: Session, last_result: Result):
        """ register turnpoint:
            - set comment on previous result to indicate turnpoint
            - increase final_score (used as counter for turnpoints) """
        last_result.comment += ': turnpoint'
        last_result.save()
        session.final_score += 1
        session.save()
    
    def staircasing(self, session: Session):
        previous_results = session.result_set.order_by('-created_at')
        last_result = previous_results.first()
        if not last_result:
            # first trial
            action = self.get_next_trial(session)
        elif last_result.score == 0:
            # the previous response was incorrect
            direction = session.json_data.get('direction')
            last_result.save_json_data({"difficulty": "decrease"})
            last_result.save()
            if direction == 'increase':
                self.register_turnpoint(session, last_result)
            # register decreasing difficulty
            session.save_json_data({"direction": "decrease"})
            action = self.get_next_trial(session)
        else:
            if previous_results.count() == 1:
                # this is the second trial, so the level is still 1
                action = self.get_next_trial(session)
            elif previous_results.all()[1].score == 1 and not previous_results.all()[1].comment:
                # the previous two responses were correct
                direction = session.json_data.get("direction")
                last_result.save_json_data({"difficulty": "increase"})
                if direction == 'decrease':
                    # mark the turnpoint
                    self.register_turnpoint(session, last_result)
                # register increasing difficulty
                session.save_json_data({"direction": "increase"})
                action = self.get_next_trial(session)
            else:
                # previous answer was correct
                # but we didn't yet get two correct in a row
                action = self.get_next_trial(session)
        if not action:
            # action is None if the audio file doesn't exist
            return None
        return action


    def staircasing_blocks(self, session):
        """Calculate staircasing procedure in blocks of 5 trials with one catch trial

        Args:
            session: the session

        Returns:
            a Trial object
        """
        previous_results = session.result_set.order_by("-created_at")
        if not previous_results.count():
            # first trial
            return self.get_next_trial(session)
        previous_condition = previous_results.first().expected_response
        if previous_condition == self.second_condition:
            # last trial was catch trial, don't calculate turnpoints
            # don't manipulate duration
            action = self.get_next_trial(session)
        else:
            if previous_results.first().score == 0:
                # the previous response was incorrect
                direction = session.json_data.get("direction")
                last_result = previous_results.first()
                last_result.save_json_data(
                    {"multiplier": self.decrease_difficulty_multiplier}
                )
                if direction == 'increase':
                    # register turnpoint
                    self.register_turnpoint(session, last_result)
                if session.final_score == self.max_turnpoints + 1:
                    # experiment is finished, None will be replaced by final view
                    return None
                else:
                    # register decreasing difficulty
                    session.save_json_data({"direction": "decrease"})
                    # decrease difficulty
                    action = self.get_next_trial(session)
            else:
                # the previous response was correct - check if previous non-catch trial was 1
                if previous_results.count() > 1 and self.last_non_catch_correct(previous_results.all()):
                    # the previous two responses were correct
                    direction = session.json_data.get("direction")
                    last_correct_result = previous_results.first()
                    last_correct_result.save_json_data(
                        {"multiplier": self.increase_difficulty_multiplier}
                    )
                    if direction == 'decrease':
                        # register turnpoint
                        self.register_turnpoint(session, last_correct_result)
                    if session.final_score == self.max_turnpoints + 1:
                        # experiment is finished, None will be replaced by final view
                        action = None
                    else:
                        # register increasing difficulty
                        session.save_json_data({"direction": "increase"})
                        # increase difficulty
                        action = self.get_next_trial(session)
                else:
                    action = self.get_next_trial(session)
        if not action:
            # action is None if the audio file doesn't exist
            return self.get_final_view(session)
        return action