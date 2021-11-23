def get_average_difference(session, num_turnpoints):
    """ given num_turnpoints (or all turnpoints so far), 
    return the average difference in milliseconds participants could hear
    """
    all_results = session.result_set
    cutoff = min(all_results.count(), num_turnpoints)
    last_turnpoints = all_results.filter(score=4).order_by('-created_at').all()[:cutoff]
    return (sum([int(result.section.name) for result in last_turnpoints]) / cutoff) - 600

def get_average_difference_level_based(session, num_turnpoints):
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    return sum([20 / int(result.section.name.split('_')[-1]) for result in last_turnpoints]) / num_turnpoints

def get_last_n_turnpoints(session, num_turnpoints):
    all_results = session.result_set
    return all_results.filter(score=4).order_by('-created_at').all()[:num_turnpoints]
