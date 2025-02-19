from typing import Optional

from .styles import FrontendStyle


class BaseAction(object):
    """Base class for all experiment actions in the MUSCLE framework.

    This class serves as the foundation for various action types that configure
    frontend components. All action classes (e.g., Score, Playback, Form, etc.)
    inherit from this base class to ensure consistent behavior and structure.

    Key Features:
    - Provides a standardized way to serialize action data for frontend components
    - Handles frontend styling configuration
    - Ensures each action has a unique identifier through the ID class variable
    - Implements a common interface for action serialization via the action() method

    Example:
        ```python
        class CustomAction(BaseAction):
            view = "CUSTOM"

            def __init__(self, custom_data, style=None):
                super().__init__(style=style)
                self.custom_data = custom_data
        ```

    Note:
        When creating a new action type: \n
        1. Inherit from `BaseAction` \n
        2. Define a unique `view` class variable \n
        3. Initialize with required parameters \n
        4. Override `action()` method if custom serialization is needed
    """

    view = "BASE"

    def __init__(self, style: Optional[list[str]] = None):
        """Initialize the base action with optional styling.

        Args:
            style: list of class arguments to set in the frontend
        """
        self.style = self._apply_style(style)

    def _apply_style(self, style: list[str]) -> Optional[FrontendStyle]:
        if style:
            return FrontendStyle(style)

    def action(self) -> dict:
        """Serialize the action configuration for frontend consumption.

        This method creates a standardized dictionary format that frontend
        components expect. All instance variables are included, and the
        action's ID is added to identify the correct frontend component.

        Returns:
            dict: A dictionary containing:
                - All instance variables from __dict__
                - 'view': The action's ID for frontend component mapping
                - 'style': Serialized style configuration if present
        """
        action_dict = self.__dict__
        action_dict['view'] = self.view
        if getattr(self, 'style', None):
            action_dict['style'] = self.style.to_dict()
        return action_dict
