from experiment.actions.question import TextRangeQuestion
from question.choice_sets.general import LIKERT_AGREE_7


def tipi_question(key: str, trait: str, scoring_rule: str) -> TextRangeQuestion:
    """Define a standard STOMP question for a genre"""
    return TextRangeQuestion(
        key=key,
        text="I see myself as %s." % trait,
        choices=LIKERT_AGREE_7,
        scoring_rule=scoring_rule,
    )


TIPI = [
    tipi_question('tipi_op', 'open to new experiences and complex', 'LIKERT'),
    tipi_question('tipi_on', 'conventional and uncreative', 'REVERSE_LIKERT'),
    tipi_question('tipi_cp', 'dependable and self-disciplined', 'LIKERT'),
    tipi_question('tipi_cn', 'disorganised and careless', 'REVERSE_LIKERT'),
    tipi_question('tipi_ep', 'extraverted and enthusiastic', 'LIKERT'),
    tipi_question('tipi_en', 'reserved and quiet', 'REVERSE_LIKERT'),
    tipi_question('tipi_ap', 'sympathetic and warm', 'LIKERT'),
    tipi_question('tipi_an', 'critical and quarrelsome', 'REVERSE_LIKERT'),
    tipi_question('tipi_np', 'anxious and easily upset', 'LIKERT'),
    tipi_question('tipi_nn', 'calm and emotionally stable', 'REVERSE_LIKERT'),
]
