def get_average_difference(session, num_turnpoints):
    """ 
    return the average difference in milliseconds participants could hear
    """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    return (sum([int(result.section.name) for result in last_turnpoints]) / last_turnpoints.count()) - 600

def get_average_difference_level_based(session, num_turnpoints):
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    return sum([20 / int(result.section.name.split('_')[-1]) for result in last_turnpoints]) / last_turnpoints.count()

def get_last_n_turnpoints(session, num_turnpoints):
    """
    select all results associated with turnpoints in the result set
    return the last num_turnpoints results, or all turnpoint results if fewer than num_turnpoints
    """
    all_results = session.result_set.filter(score=4).order_by('-created_at').all()
    cutoff = min(all_results.count(), num_turnpoints)
    return all_results[:cutoff]
