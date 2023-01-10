from .models import Result

def get_result(session, data):
    result_id = data.get('result_id')
    try:
        result = Result.objects.get(pk=result_id, session=session)
    except Result.DoesNotExist:
        # Create new result
        result = Result(session=session)
    return result

def handle_results(session, data):
    """ 
    if the given_result is an array of results, retrieve and save results for all of them
    else, handle results at top level
    """
    try:
        form = data.pop('form')
    except KeyError:
        # no form, handle results at top level
        result = score_result(session, data)
        return result
    for form_element in form:
        result = score_result(session, form_element)
        # save any relevant data (except for the popped form)
        result.merge_json_data(data)
        result.save()
    return result

def prepare_result(session, key, section=None, expected_response=None, comment='', scoring_rule='', is_profile=False):
    ''' Create a Result object, and provide its id to be serialized
    - session: the session on which the Result is going to be registered
    - section: optionally, provide a section to which the Result is going to be tied
    - expected_response: optionally, provide the correct answer, used for scoring  
    - comment: optionally, provide a comment to be saved in the database, e.g. "training phase"
    - scoring_rule: optionally, provide a scoring rule
    - is_profile: optionally, flag that the Result is a profile type question
    '''     
    result = Result(
        session=session,
        section=section,
        question_key=key,
        expected_response=expected_response,
        scoring_rule=scoring_rule,
        comment=comment,
        is_profile=is_profile
    )
    result.save()
    return result.id 

def score_result(session, data):
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
    result.given_response = data.get('value')
    # Calculate score: by default, apply a scoring rule
    # Can be overridden by defining calculate_score in the rules file    
    score = session.experiment_rules().calculate_score(result, data)
    if not score:
        score = 0
    # Populate and save the result
    result.score = score
    result.save_json_data(data)
    result.save()
    return result
    