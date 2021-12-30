from typing import Any, Dict, Optional


class MultiSerializerViewSetMixin:
    """Mixin for choosing an appropriate serializer from `serializer_action_classes`."""

    serializer_action_classes: Optional[Dict[str, Any]] = None

    def get_serializer_class(self):
        """Get an appropriate serializer based on `action`."""
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super().get_serializer_class()
