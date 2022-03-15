def register_turnpoint(session, last_result):
    """ register turnpoint:
        - set comment on previous result to indicate turnpoint
        - increase final_score (used as counter for turnpoints) """
    last_result.comment += ': turnpoint'
    last_result.save()
    session.final_score += 1
    session.save()