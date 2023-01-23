from experiment.actions import Question

def tipi_question(key, trait):
    """Define a standard STOMP question for a genre"""
    return Question.likert(
        key,
        question = "I see myself as %s." % trait
    )

TIPI = [
    tipi_question('tipi_op', 'open to new experiences and complex'),
    tipi_question('tipi_on', 'conventional and uncreative'),
    tipi_question('tipi_cp', 'dependable and self-disciplined'),
    tipi_question('tipi_cn', 'disorganised and careless'),
    tipi_question('tipi_ep', 'extraverted and enthusiastic'),
    tipi_question('tipi_en', 'reserved and quiet'),
    tipi_question('tipi_ap', 'sympathetic and warm'),
    tipi_question('tipi_an', 'critical and quarrelsome'),
    tipi_question('tipi_np', 'anxious and easily upset'),
    tipi_question('tipi_nn', 'calm and emotionally stable')
]
