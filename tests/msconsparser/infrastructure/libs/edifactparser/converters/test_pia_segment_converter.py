import unittest

from ediparse.infrastructure.libs.edifactparser.converters.pia_segment_converter import PIASegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentPIA


class TestPIASegmentConverter(unittest.TestCase):
    """Test case for the PIASegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = PIASegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_obis_code(self):
        """Test the _convert_internal method with OBIS code."""
        # Arrange
        element_components = ["PIA", "5", "1-1?:1.29.1:SRW"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentPIA)
        self.assertEqual(result.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(result.waren_leistungsnummer_identifikation)
        self.assertEqual(result.waren_leistungsnummer_identifikation.produkt_leistungsnummer, "1-1:1.29.1")
        self.assertEqual(result.waren_leistungsnummer_identifikation.art_der_produkt_leistungsnummer_code, "SRW")

    def test_convert_internal_with_medium(self):
        """Test the _convert_internal method with medium."""
        # Arrange
        element_components = ["PIA", "5", "AUA:Z08"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentPIA)
        self.assertEqual(result.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(result.waren_leistungsnummer_identifikation)
        self.assertEqual(result.waren_leistungsnummer_identifikation.produkt_leistungsnummer, "AUA")
        self.assertEqual(result.waren_leistungsnummer_identifikation.art_der_produkt_leistungsnummer_code, "Z08")

    def test_convert_internal_without_art_der_produkt_leistungsnummer_code(self):
        """Test the _convert_internal method without art_der_produkt_leistungsnummer_code."""
        # Arrange
        element_components = ["PIA", "5", "1-1:1.29.1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentPIA)
        self.assertEqual(result.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(result.waren_leistungsnummer_identifikation)
        # According to the requirements, we should split at the last colon
        self.assertEqual(result.waren_leistungsnummer_identifikation.produkt_leistungsnummer, "1-1")
        self.assertEqual(result.waren_leistungsnummer_identifikation.art_der_produkt_leistungsnummer_code, "1.29.1")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["PIA", "5", "test:code"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentPIA)
        self.assertEqual(result.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(result.waren_leistungsnummer_identifikation)
        self.assertEqual(result.waren_leistungsnummer_identifikation.produkt_leistungsnummer, "test")
        self.assertEqual(result.waren_leistungsnummer_identifikation.art_der_produkt_leistungsnummer_code, "code")

    def test_convert_internal_with_escaped_colon(self):
        """Test the _convert_internal method with escaped colon."""
        # Arrange
        element_components = ["PIA", "5", "1-1?:1.29.1:SRW"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentPIA)
        self.assertEqual(result.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(result.waren_leistungsnummer_identifikation)
        # The escaped colon should be treated as part of the product number
        self.assertEqual(result.waren_leistungsnummer_identifikation.produkt_leistungsnummer, "1-1:1.29.1")
        self.assertEqual(result.waren_leistungsnummer_identifikation.art_der_produkt_leistungsnummer_code, "SRW")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["PIA"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(
                line_number=line_number,
                element_components=element_components,
                last_segment_type=last_segment_type,
                current_segment_group=current_segment_group,
                context=self.context
            )


if __name__ == '__main__':
    unittest.main()
