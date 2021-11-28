from typing import Any, Dict, Optional


class MultiSerializerViewSetMixin:
    """Миксин для выбора нужного сериалайзера из `serializer_action_classes`."""

    serializer_action_classes: Optional[Dict[str, Any]] = None

    def get_serializer_class(self):
        """Возвращает нужный сериалайзер, исходя из `action`."""
        return self.serializer_action_classes.get(self.action, super().get_serializer_class())
