import unittest
from unittest.mock import patch, MagicMock

from ediparse.libs.edifactparser.exceptions import EdifactParserException
from ediparse.libs.edifactparser.parser import EdifactParser
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.wrappers.constants import SegmentType, SegmentGroup
from ediparse.libs.edifactparser.wrappers.segments import EdifactInterchange

# Import these directly to avoid circular imports
from ediparse.libs.edifactparser.mods.mscons.group_state_resolver import MsconsGroupStateResolver
from ediparse.libs.edifactparser.mods.aperak.group_state_resolver import AperakGroupStateResolver


class TestEdifactParser(unittest.TestCase):
    """Test case for the EdifactParser class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = EdifactParser()

    def test_init(self):
        """Test that the parser initializes correctly."""
        self.assertIsNotNone(self.parser._EdifactParser__handler_factory)
        self.assertIsNotNone(self.parser._EdifactParser__resolver_factory)
        # Context is private, so we don't test it directly

    def test_init_with_custom_factories(self):
        """Test that the parser initializes correctly with custom factories."""
        # Arrange
        mock_handler_factory = MagicMock()
        mock_resolver_factory = MagicMock()

        # Act
        parser = EdifactParser(
            handler_factory=mock_handler_factory,
            resolver_factory=mock_resolver_factory
        )

        # Assert
        self.assertEqual(mock_handler_factory, parser._EdifactParser__handler_factory)
        self.assertEqual(mock_resolver_factory, parser._EdifactParser__resolver_factory)

    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        # Act & Assert
        with self.assertRaises(EdifactParserException):
            self.parser.parse("")

    @patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_segments')
    @patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_elements')
    @patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_components')
    def test_parse_with_mocked_utils(self, mock_split_components, mock_split_elements, mock_split_segments):
        """Test parsing with mocked utility methods."""
        # Arrange
        mock_split_segments.return_value = ["UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345"]
        mock_split_elements.return_value = ["UNB", "UNOC:3", "SENDER:ZZ", "RECIPIENT:ZZ", "230101:1200", "12345"]
        # The first call to split_components is for the segment type
        mock_split_components.side_effect = [["UNB"]]

        # Mock the handler factory and handler
        self.parser._EdifactParser__handler_factory = MagicMock()
        mock_handler = MagicMock()
        self.parser._EdifactParser__handler_factory.get_handler.return_value = mock_handler

        # Act & Assert
        with self.assertRaises(EdifactParserException):
            self.parser.parse("test_data")

    @patch('ediparse.libs.edifactparser.utils.context_factory.ParsingContextFactory.identify_and_create_context')
    def test_parse_uses_parsing_context_factory(self, mock_identify_and_create_context):
        """Test that the parser uses the ParsingContextFactory to identify and create contexts."""
        # Arrange
        # We need to mock the return value to avoid TypeError with split_segments
        # Use the existing context from the parser instead of creating a new one
        mock_identify_and_create_context.return_value = self.parser._EdifactParser__context

        # We need to patch split_segments to avoid the MSCONSParserException
        with patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_segments') as mock_split_segments:
            # Return enough segments to pass the minimum segment count check
            mock_split_segments.return_value = ["UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345", 
                                              "UNH+12345+MSCONS:D:96A:UN:EAN005",
                                              "BGM+7+MSI5422+9",
                                              "DTM+137:202106011315?+00:303",
                                              "UNT+4+12345",
                                              "UNZ+1+12345"]

            # Act
            try:
                self.parser.parse("test_data")
            except Exception:
                # We don't care about other exceptions in this test
                pass

            # Assert
            mock_identify_and_create_context.assert_called_once()

    @patch('ediparse.libs.edifactparser.resolvers.group_state_resolver_factory.GroupStateResolverFactory.get_resolver')
    def test_parse_uses_resolver_factory(self, mock_get_resolver):
        """Test that the parser uses the GroupStateResolverFactory to get resolvers."""
        # Arrange
        mock_resolver = MagicMock()
        mock_get_resolver.return_value = mock_resolver

        # We need to patch identify_and_create_context to set the message_type
        with patch('ediparse.libs.edifactparser.utils.context_factory.ParsingContextFactory.identify_and_create_context') as mock_identify_and_create_context:
            # Create a context with a message type
            from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
            mock_context = MSCONSParsingContext()
            mock_identify_and_create_context.return_value = mock_context

            # We need to patch split_segments to avoid the MSCONSParserException
            with patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_segments') as mock_split_segments:
                # Return enough segments to pass the minimum segment count check
                mock_split_segments.return_value = ["UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345", 
                                                  "UNH+12345+MSCONS:D:96A:UN:EAN005",
                                                  "BGM+7+MSI5422+9",
                                                  "DTM+137:202106011315?+00:303",
                                                  "UNT+4+12345",
                                                  "UNZ+1+12345"]

                # We need to patch split_elements and split_components to avoid errors
                with patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_elements') as mock_split_elements:
                    with patch('ediparse.libs.edifactparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_components') as mock_split_components:
                        # Set up the mocks to return values that will allow the code to proceed
                        mock_split_elements.return_value = ["UNB", "UNOC:3", "SENDER:ZZ", "RECIPIENT:ZZ", "230101:1200", "12345"]
                        mock_split_components.return_value = ["UNB"]

                        # Act
                        try:
                            self.parser.parse("test_data")
                        except Exception:
                            # We don't care about other exceptions in this test
                            pass

                        # Assert
                        mock_get_resolver.assert_called_once()

    def test_parse_with_mscons_sample_data(self):
        """Test parsing with a simple MSCONS sample data string."""
        # Arrange
        sample_data = """UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345'
UNH+12345+MSCONS:D:96A:UN:EAN005'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
UNT+4+12345'
UNZ+1+12345'"""

        # Act
        result = self.parser.parse(sample_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, EdifactInterchange)
        # Additional assertions would depend on the expected structure of the result

    def test_parse_with_aperak_sample_data(self):
        """Test parsing with a simple APERAK sample data string."""
        # Arrange
        sample_data = """UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345'
UNH+12345+APERAK:D:07B:UN:2.1i'
BGM+313+AFBM5422'
DTM+137:202104081015?+00:303'
RFF+ACE:TG9523'
UNT+5+12345'
UNZ+1+12345'"""

        # Act
        result = self.parser.parse(sample_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, EdifactInterchange)
        # Additional assertions would depend on the expected structure of the result

    def test_resolve_and_get_segment_group_with_empty_segment_type(self):
        """Test resolve_and_get_segment_group with an empty segment type."""
        # Arrange
        resolver = MsconsGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group("", None, None)

        # Assert
        self.assertIsNone(result)

    def test_resolve_and_get_segment_group_with_dtm(self):
        """Test resolve_and_get_segment_group with DTM segment type."""
        # Arrange
        resolver = MsconsGroupStateResolver()
        current_group = None

        # Act
        result = resolver.resolve_and_get_segment_group(SegmentType.DTM, current_group, None)

        # Assert
        self.assertEqual(current_group, result)

    def test_resolve_and_get_segment_group_with_rff(self):
        """Test resolve_and_get_segment_group with RFF segment type in different contexts."""
        # Arrange
        resolver = MsconsGroupStateResolver()

        # Test RFF in No group
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, None, None)
        self.assertEqual(SegmentGroup.SG1, result)

        # Test RFF in SG1
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG1, None)
        self.assertEqual(SegmentGroup.SG1, result)

        # Test RFF in SG6
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG6, None)
        self.assertEqual(SegmentGroup.SG7, result)

        # Test RFF in SG7
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG7, None)
        self.assertEqual(SegmentGroup.SG7, result)

    def test_resolve_and_get_segment_group_with_nad(self):
        """Test resolve_and_get_segment_group with NAD segment type in different contexts."""
        # Arrange
        resolver = MsconsGroupStateResolver()

        # Test NAD in SG1
        result = resolver.resolve_and_get_segment_group(SegmentType.NAD, SegmentGroup.SG1, None)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test NAD in SG4
        result = resolver.resolve_and_get_segment_group(SegmentType.NAD, SegmentGroup.SG4, None)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test NAD in no group
        result = resolver.resolve_and_get_segment_group(SegmentType.NAD, None, None)
        self.assertEqual(SegmentGroup.SG5, result)

    def test_resolve_and_get_segment_group_with_other_types(self):
        """Test resolve_and_get_segment_group with other segment types."""
        # Arrange
        resolver = MsconsGroupStateResolver()

        # Test CTA
        result = resolver.resolve_and_get_segment_group(SegmentType.CTA, None, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test COM
        result = resolver.resolve_and_get_segment_group(SegmentType.COM, None, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test LOC
        result = resolver.resolve_and_get_segment_group(SegmentType.LOC, None, None)
        self.assertEqual(SegmentGroup.SG6, result)

        # Test CCI
        result = resolver.resolve_and_get_segment_group(SegmentType.CCI, None, None)
        self.assertEqual(SegmentGroup.SG8, result)

        # Test LIN
        result = resolver.resolve_and_get_segment_group(SegmentType.LIN, None, None)
        self.assertEqual(SegmentGroup.SG9, result)

        # Test PIA
        result = resolver.resolve_and_get_segment_group(SegmentType.PIA, None, None)
        self.assertEqual(SegmentGroup.SG9, result)

        # Test QTY
        result = resolver.resolve_and_get_segment_group(SegmentType.QTY, None, None)
        self.assertEqual(SegmentGroup.SG10, result)

        # Test STS
        result = resolver.resolve_and_get_segment_group(SegmentType.STS, None, None)
        self.assertEqual(SegmentGroup.SG10, result)

    def test_resolve_and_get_segment_group_with_unknown_type(self):
        """Test resolve_and_get_segment_group with an unknown segment type."""
        # Arrange
        resolver = MsconsGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group("UNKNOWN", None, None)

        # Assert
        self.assertEqual(None, result)

    # Tests for AperakGroupStateResolver

    def test_aperak_resolve_and_get_segment_group_with_empty_segment_type(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with an empty segment type."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group("", None, None)

        # Assert
        self.assertIsNone(result)

    def test_aperak_resolve_and_get_segment_group_with_dtm(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with DTM segment type."""
        # Arrange
        resolver = AperakGroupStateResolver()
        current_group = None

        # Act
        result = resolver.resolve_and_get_segment_group(SegmentType.DTM, current_group, None)

        # Assert
        self.assertEqual(current_group, result)

    def test_aperak_resolve_and_get_segment_group_with_rff(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with RFF segment type in different contexts."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Test RFF in No group
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, None, None)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test RFF in SG2
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG2, None)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test RFF in SG4
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG4, None)
        self.assertEqual(SegmentGroup.SG5, result)

        # Test RFF in SG5
        result = resolver.resolve_and_get_segment_group(SegmentType.RFF, SegmentGroup.SG5, None)
        self.assertEqual(SegmentGroup.SG5, result)

    def test_aperak_resolve_and_get_segment_group_with_nad(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with NAD segment type."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group(SegmentType.NAD, None, None)

        # Assert
        self.assertEqual(SegmentGroup.SG3, result)

    def test_aperak_resolve_and_get_segment_group_with_cta_com(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with CTA and COM segment types."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Test CTA
        result = resolver.resolve_and_get_segment_group(SegmentType.CTA, None, None)
        self.assertEqual(SegmentGroup.SG3, result)

        # Test COM
        result = resolver.resolve_and_get_segment_group(SegmentType.COM, None, None)
        self.assertEqual(SegmentGroup.SG3, result)

    def test_aperak_resolve_and_get_segment_group_with_erc(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with ERC segment type."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group(SegmentType.ERC, None, None)

        # Assert
        self.assertEqual(SegmentGroup.SG4, result)

    def test_aperak_resolve_and_get_segment_group_with_ftx(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with FTX segment type in different contexts."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Test FTX in No group
        result = resolver.resolve_and_get_segment_group(SegmentType.FTX, None, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test FTX in SG4
        result = resolver.resolve_and_get_segment_group(SegmentType.FTX, SegmentGroup.SG4, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test FTX in SG5
        result = resolver.resolve_and_get_segment_group(SegmentType.FTX, SegmentGroup.SG5, None)
        self.assertEqual(SegmentGroup.SG5, result)

    def test_aperak_resolve_and_get_segment_group_with_unknown_type(self):
        """Test AperakGroupStateResolver.resolve_and_get_segment_group with an unknown segment type."""
        # Arrange
        resolver = AperakGroupStateResolver()

        # Act
        result = resolver.resolve_and_get_segment_group("UNKNOWN", None, None)

        # Assert
        self.assertEqual(None, result)

    def test_parse_with_una_segment(self):
        """Test parsing with a UNA segment at the beginning of the file."""
        # Arrange
        sample_data = "UNA;*%? '"

        # We need to patch the __find_una_segment method to return the UNA segment
        with patch('ediparse.libs.edifactparser.parser.EdifactParser._EdifactParser__find_una_segment') as mock_find_una_segment:
            # Return the UNA segment
            mock_find_una_segment.return_value = "UNA;*%? '"

            # Act
            # We're not actually parsing the whole message, just initializing the UNA segment
            self.parser._EdifactParser__initialize_una_segment_logic_return_if_has_una_segment(sample_data)

            # Assert
            # Verify that the UNA segment was found and initialized
            context = self.parser._EdifactParser__context
            self.assertIsNotNone(context.interchange.una_service_string_advice)
            self.assertEqual(";", context.interchange.una_service_string_advice.component_separator)
            self.assertEqual("*", context.interchange.una_service_string_advice.element_separator)
            self.assertEqual("%", context.interchange.una_service_string_advice.decimal_mark)
            self.assertEqual("?", context.interchange.una_service_string_advice.release_character)
            self.assertEqual(" ", context.interchange.una_service_string_advice.reserved)
            self.assertEqual("'", context.interchange.una_service_string_advice.segment_terminator)

            # Verify that EdifactSyntaxHelper methods return the correct values from the context
            self.assertEqual(";", EdifactSyntaxHelper.get_component_separator(context))
            self.assertEqual("*", EdifactSyntaxHelper.get_element_separator(context))
            self.assertEqual("%", EdifactSyntaxHelper.get_decimal_mark(context))
            self.assertEqual("?", EdifactSyntaxHelper.get_release_indicator(context))
            self.assertEqual(" ", EdifactSyntaxHelper.get_reserved_indicator(context))
            self.assertEqual("'", EdifactSyntaxHelper.get_segment_terminator(context))


if __name__ == '__main__':
    unittest.main()
