def combine_actions(*argv):
    """Combine actions, make them next_round of each predecessor"""
    last = None
    for action in reversed(argv):
        # Skip empty actions
        if not action:
            continue
        if last:
            action['next_round'] = last
        last = action

    # Action stored in last is actually the first action
    return last
