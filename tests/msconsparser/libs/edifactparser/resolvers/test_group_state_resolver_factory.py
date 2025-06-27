import unittest

from ediparse.libs.edifactparser.resolvers.group_state_resolver_factory import GroupStateResolverFactory
from ediparse.libs.edifactparser.mods.mscons.group_state_resolver import MsconsGroupStateResolver
from ediparse.libs.edifactparser.mods.aperak.group_state_resolver import AperakGroupStateResolver
from ediparse.libs.edifactparser.wrappers.constants import EdifactMessageType


class TestGroupStateResolverFactory(unittest.TestCase):
    """Test case for the GroupStateResolverFactory class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.factory = GroupStateResolverFactory()

    def test_get_resolver_for_mscons(self):
        """Test getting a resolver for MSCONS message type."""
        # Act
        resolver = self.factory.get_resolver(EdifactMessageType.MSCONS)

        # Assert
        self.assertIsNotNone(resolver)
        self.assertIsInstance(resolver, MsconsGroupStateResolver)

    def test_get_resolver_for_aperak(self):
        """Test getting a resolver for APERAK message type."""
        # Act
        resolver = self.factory.get_resolver(EdifactMessageType.APERAK)

        # Assert
        self.assertIsNotNone(resolver)
        self.assertIsInstance(resolver, AperakGroupStateResolver)

    def test_get_resolver_for_unknown_message_type(self):
        """Test getting a resolver for an unknown message type."""
        # Act
        resolver = self.factory.get_resolver("UNKNOWN")

        # Assert
        self.assertIsNone(resolver)


if __name__ == '__main__':
    unittest.main()