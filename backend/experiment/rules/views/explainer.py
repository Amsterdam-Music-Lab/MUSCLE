class Explainer:  # pylint: disable=too-few-public-methods
    """
    Provide data for a explainer that explains the experiment steps

    Relates to client component: Explainer.js    
    """

    ID = "EXPLAINER"

    @staticmethod
    def action(instruction, steps, button_label="Let's go!"):
        """Get data for explainer action"""
        return {
            'view': Explainer.ID,
            'instruction': instruction,
            'button_label': button_label,
            'steps': steps,
        }

    @staticmethod
    def step(description, number=None):
        """Create an explainer step, with description and optional number"""
        return {
            'number': number,
            'description': description
        }
