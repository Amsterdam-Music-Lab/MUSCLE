def get_average_difference(session, num_turnpoints):
    all_results = session.result_set
    last_turnpoints = all_results.filter(score=4).order_by('-created_at').all()[:num_turnpoints]
    return sum([int(result.section.name) for result in last_turnpoints])/num_turnpoints - 600