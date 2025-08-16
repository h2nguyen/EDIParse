import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.group_state_resolver import (
    AperakGroupStateResolver,
)
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import (
    EdifactMessageType,
)
from ediparse.infrastructure.libs.edifactparser.mods.mscons.group_state_resolver import (
    MsconsGroupStateResolver,
)
from ediparse.infrastructure.libs.edifactparser.resolvers.group_state_resolver import (
    GroupStateResolver,
)
from ediparse.infrastructure.libs.edifactparser.resolvers.group_state_resolver_factory import (
    GroupStateResolverFactory,
)


class TestGroupStateResolverFactory(unittest.TestCase):
    """Tests for the GroupStateResolverFactory class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.factory = GroupStateResolverFactory()

    def test_get_resolver_returns_mscons_group_resolver(self):
        # Arrange
        message_type = EdifactMessageType.MSCONS

        # Act
        resolver = self.factory.get_resolver(message_type)

        # Verify
        self.assertIsNotNone(resolver, "Resolver for MSCONS should not be None")
        self.assertIsInstance(resolver, MsconsGroupStateResolver)
        self.assertTrue(isinstance(resolver, GroupStateResolver))

    def test_get_resolver_returns_aperak_group_resolver(self):
        # Arrange
        message_type = EdifactMessageType.APERAK

        # Act
        resolver = self.factory.get_resolver(message_type)

        # Verify
        self.assertIsNotNone(resolver, "Resolver for APERAK should not be None")
        self.assertIsInstance(resolver, AperakGroupStateResolver)
        self.assertTrue(isinstance(resolver, GroupStateResolver))

    def test_get_resolver_logs_warning_and_returns_none_when_missing(self):
        # Arrange
        # Simulate missing resolver registry for negative path
        # (fresh factory instance per test ensures isolation)
        self.factory._GroupStateResolverFactory__handlers = {}
        logger_name = (
            "ediparse.infrastructure.libs.edifactparser.resolvers."
            "group_state_resolver_factory"
        )

        # Act
        with self.assertLogs(logger_name, level="WARNING") as cm:
            resolver = self.factory.get_resolver(EdifactMessageType.MSCONS)

        # Verify
        self.assertIsNone(resolver)
        # Check that a warning about missing resolver has been logged
        self.assertTrue(
            any("No resolver found" in msg for msg in cm.output),
            f"Expected warning about missing resolver, got: {cm.output}",
        )


if __name__ == "__main__":
    unittest.main()
