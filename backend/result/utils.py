from .models import Result

from .score import SCORING_RULES

def get_result(session, data):
    result_id = data.get('result_id')
    try:
        result = Result.objects.get(pk=result_id, session=session)
    except Result.DoesNotExist:
        # check if a profile type result exists
        try:
            result = Result.objects.get(pk=result_id, participant=session.participant)
        except Result.DoesNotExist:
            raise
    return result

def handle_results(data, session):
    """ 
    if the given_result is an array of results, retrieve and save results for all of them
    else, handle results at top level
    """
    try:
        form = data.pop('form')
    except KeyError:
        # no form, handle results at top level
        result = score_result(data, session)
        return result
    for form_element in form:
        result = score_result(form_element, session)
        # save any relevant data (except for the popped form)
        result.merge_json_data(data)
        result.save()
    return result

def prepare_result(session, is_profile=False, **kwargs):
    ''' Create a Result object, and provide its id to be serialized
    - session: the session on which the Result is going to be registered
    - is_profile: optionally, flag that the Result is a profile type question
    possible kwargs: 
        - section: optionally, provide a section to which the Result is going to be tied
        - expected_response: optionally, provide the correct answer, used for scoring  
        - comment: optionally, provide a comment to be saved in the database, e.g. "training phase"
        - scoring_rule: optionally, provide a scoring rule
    '''
    if not is_profile:
        result = Result(
            session=session,
            **kwargs
        )
    else:
        participant = session.participant
        result = Result(
            participant=participant,
            **kwargs
        )
    result.save()
    return result.id 

def score_result(data, session):
    """
    Create a result for given session, based on the result data 
    (form element or top level data)
    parameters:
    session: a Session object
    data: a dictionary, containing an optional result_id, and optional other params:
    {
        result_id: int [optional]
        params: ...
    }
    """
    result = get_result(session, data)
    result.question_key = data.get('key')
    result.given_response = data.get('value')
    # Calculate score: by default, apply a scoring rule
    # Can be overridden by defining calculate_score in the rules file    
    if result.session:
        score = session.experiment_rules().calculate_score(result, data)
    else:
        # this is a profile type result, i.e., it doesn't have a session:
        score = apply_scoring_rule(result, data)
    # Populate and save the result
    # result can also be None
    result.score = score
    result.save_json_data(data)
    result.save()
    return result

def apply_scoring_rule(result, data):
    scoring_rule = SCORING_RULES.get(result.scoring_rule)
    if scoring_rule:
        return scoring_rule(result, data)
    return None