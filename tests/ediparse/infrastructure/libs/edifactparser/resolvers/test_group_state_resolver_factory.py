import unittest
from unittest import mock

from ediparse.infrastructure.libs.edifactparser.mods.aperak.group_state_resolver import AperakGroupStateResolver
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.mods.mscons.group_state_resolver import MsconsGroupStateResolver
from ediparse.infrastructure.libs.edifactparser.resolvers.group_state_resolver import GroupStateResolver
from ediparse.infrastructure.libs.edifactparser.resolvers.group_state_resolver_factory import GroupStateResolverFactory


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
        with self.assertLogs(level='WARNING') as cm:
            resolver = self.factory.get_resolver("UNKNOWN")

        # Assert
        self.assertIsNone(resolver)
        self.assertIn("No resolver found for EdifactMessageType 'UNKNOWN'.", cm.output[0])

    def test_all_message_types_have_resolvers(self):
        """Test that all message types defined in EdifactMessageType have corresponding resolvers."""
        # Arrange
        factory = GroupStateResolverFactory()

        # Act & Assert
        for message_type in EdifactMessageType:
            resolver = factory.get_resolver(message_type)
            self.assertIsNotNone(resolver, f"No resolver found for message type {message_type}")
            self.assertIsInstance(resolver, GroupStateResolver)
            # Check that the resolver class name follows the expected pattern
            # The class name uses title case for the message type (e.g., "MsconsGroupStateResolver")
            expected_class_name = f"{message_type.title()}GroupStateResolver"
            self.assertEqual(resolver.__class__.__name__, expected_class_name,
                            f"Resolver class name should be {expected_class_name}")

    def test_dynamic_discovery_extracts_message_type_correctly(self):
        """Test that the dynamic discovery mechanism correctly extracts message types from class names."""
        # This test verifies that the factory correctly extracts message types from class names
        # by checking that the resolvers for MSCONS and APERAK are correctly registered

        # Arrange
        factory = GroupStateResolverFactory()

        # Act & Assert
        # Check MSCONS resolver
        mscons_resolver = factory.get_resolver(EdifactMessageType.MSCONS)
        self.assertIsNotNone(mscons_resolver)
        self.assertEqual(mscons_resolver.__class__.__name__, "MsconsGroupStateResolver")

        # Check APERAK resolver
        aperak_resolver = factory.get_resolver(EdifactMessageType.APERAK)
        self.assertIsNotNone(aperak_resolver)
        self.assertEqual(aperak_resolver.__class__.__name__, "AperakGroupStateResolver")

    def test_handles_import_errors_gracefully(self):
        """Test that the factory handles import errors gracefully during discovery."""
        # This test verifies that the factory correctly handles import errors during discovery
        # by mocking the importlib.import_module function to raise an ImportError

        # Arrange
        # Mock the importlib.import_module function to raise an ImportError
        with mock.patch('importlib.import_module', side_effect=ImportError("Mocked import error")):
            # Act
            with self.assertLogs(level='WARNING') as cm:
                factory = GroupStateResolverFactory()

            # Assert
            # Check that the warning was logged
            self.assertTrue(any("Error importing group state resolver" in log for log in cm.output),
                           "Warning about import error should be logged")

            # Check that the factory was created but has no resolvers
            self.assertEqual(len(factory._GroupStateResolverFactory__handlers), 0,
                           "Factory should have no resolvers when import fails")


if __name__ == '__main__':
    unittest.main()
