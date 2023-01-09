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
    