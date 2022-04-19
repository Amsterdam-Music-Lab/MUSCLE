def get_average_difference(session, num_turnpoints, initial_value):
    """ 
    return the average difference in milliseconds participants could hear
    """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        last_result = get_fallback_result(session)
        if last_result:
            return float(last_result.section.name)
        else:
            # this cannot happen in DurationDiscrimination style experiments
            # for future compatibility, still catch the condition that there may be no results                 
            return initial_value
    return (sum([int(result.section.name) for result in last_turnpoints]) / last_turnpoints.count())

def get_average_difference_level_based(session, num_turnpoints, initial_value):
    """ calculate the difference based on exponential decay,
    starting from an initial_value """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        # outliers
        last_result = get_fallback_result(session)
        if last_result:
            return initial_value / (2 ** (int(last_result.section.name.split('_')[-1]) - 1))
        else:
            # participant didn't pay attention,
            # no results right after the practice rounds
            return initial_value
    # Difference by level starts at initial value (which is level 1, so 20/(2^0)) and then halves for every next level
    return sum([initial_value / (2 ** (int(result.section.name.split('_')[-1]) - 1)) for result in last_turnpoints]) / last_turnpoints.count() 

def get_fallback_result(session):
    """ if there were no turnpoints (outliers):
    return the last result, or if there are no results, return None
    """
    if session.result_set.count() == 0:
        # stopping right after practice rounds
        return None
    return session.result_set.order_by('-created_at')[0]

def get_last_n_turnpoints(session, num_turnpoints):
    """
    select all results associated with turnpoints in the result set
    return the last num_turnpoints results, or all turnpoint results if fewer than num_turnpoints
    """
    all_results = session.result_set.filter(comment__iendswith='turnpoint').order_by('-created_at').all()
    cutoff = min(all_results.count(), num_turnpoints)
    return all_results[:cutoff]
