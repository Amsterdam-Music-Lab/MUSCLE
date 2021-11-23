def get_average_difference(session, num_turnpoints):
    """ given num_turnpoints (or all turnpoints so far), 
    return the average difference in milliseconds participants could hear
    """
    all_results = session.result_set
    cutoff = min(all_results.count(), num_turnpoints)
    last_turnpoints = all_results.filter(score=4).order_by('-created_at').all()[:cutoff]
    return (sum([int(result.section.name) for result in last_turnpoints]) / cutoff) - 600