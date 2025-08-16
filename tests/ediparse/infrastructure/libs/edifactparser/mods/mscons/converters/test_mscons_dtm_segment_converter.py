import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.converters.dtm_segment_converter import \
    MSCONSDTMSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentDTM


class TestMSCONSDTMSegmentConverter(unittest.TestCase):
    """Test case for the MSCONSDTMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = MSCONSDTMSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = MSCONSDTMSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_7_qualifier_sg10(self):
        """Test the _get_identifier_name method with 7 qualifier code in SG10."""
        # Arrange
        qualifier_code = "7"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Nutzungszeitpunkt")

    def test_get_identifier_name_with_9_qualifier_sg10(self):
        """Test the _get_identifier_name method with 9 qualifier code in SG10."""
        # Arrange
        qualifier_code = "9"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ablesedatum")
        
    def test_get_identifier_name_with_60_qualifier_sg10(self):
        """Test the _get_identifier_name method with 60 qualifier code in SG10."""
        # Arrange
        qualifier_code = "60"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ausführungs- / Änderungszeitpunkt")

    def test_get_identifier_name_with_137_qualifier(self):
        """Test the _get_identifier_name method with 137 qualifier code."""
        # Arrange
        qualifier_code = "137"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Nachrichtendatum")

    def test_get_identifier_name_with_157_qualifier_sg6(self):
        """Test the _get_identifier_name method with 157 qualifier code in SG6."""
        # Arrange
        qualifier_code = "157"
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Gültigkeit, Beginndatum Profilschar")

    def test_get_identifier_name_with_163_qualifier_sg6(self):
        """Test the _get_identifier_name method with 163 qualifier code in SG6."""
        # Arrange
        qualifier_code = "163"
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Beginn Messperiode Übertragungszeitraum")

    def test_get_identifier_name_with_163_qualifier_sg10(self):
        """Test the _get_identifier_name method with 163 qualifier code in SG10."""
        # Arrange
        qualifier_code = "163"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Beginn Messperiode")

    def test_get_identifier_name_with_164_qualifier_sg6(self):
        """Test the _get_identifier_name method with 164 qualifier code in SG6."""
        # Arrange
        qualifier_code = "164"
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ende Messperiode Übertragungszeitraum")

    def test_get_identifier_name_with_164_qualifier_sg10(self):
        """Test the _get_identifier_name method with 164 qualifier code in SG10."""
        # Arrange
        qualifier_code = "164"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ende Messperiode")

    def test_get_identifier_name_with_293_qualifier_sg1(self):
        """Test the _get_identifier_name method with 293 qualifier code in SG1."""
        # Arrange
        qualifier_code = "293"
        current_segment_group = SegmentGroup.SG1

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Versionsangabe marktlokationsscharfe Allokationsliste Gas (MMMA)")

    def test_get_identifier_name_with_293_qualifier_sg6(self):
        """Test the _get_identifier_name method with 293 qualifier code in SG6."""
        # Arrange
        qualifier_code = "293"
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Versionsangabe")

    def test_get_identifier_name_with_306_qualifier_sg10(self):
        """Test the _get_identifier_name method with 306 qualifier code in SG10."""
        # Arrange
        qualifier_code = "306"
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Leistungsperiode")

    def test_get_identifier_name_with_492_qualifier_sg6(self):
        """Test the _get_identifier_name method with 492 qualifier code in SG6."""
        # Arrange
        qualifier_code = "492"
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Bilanzierungsmonat")

    def test_get_identifier_name_with_unknown_qualifier(self):
        """Test the _get_identifier_name method with an unknown qualifier code."""
        # Arrange
        qualifier_code = "999"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        # For unknown qualifiers, the result should be None or whatever the parent class returns
        self.assertIsNone(result)

    def test_convert_internal_with_137_qualifier(self):
        """Test the _convert_internal method with 137 qualifier code."""
        # Arrange
        element_components = ["DTM", "137:202106011315+00:303"]
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
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Nachrichtendatum")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_163_qualifier_sg10(self):
        """Test the _convert_internal method with 163 qualifier code in SG10."""
        # Arrange
        element_components = ["DTM", "163:202106011315+00:303"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Beginn Messperiode")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "163")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")
        
    def test_convert_internal_with_60_qualifier_sg10(self):
        """Test the _convert_internal method with 60 qualifier code in SG10."""
        # Arrange
        element_components = ["DTM", "60:202107011415+00:303"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Ausführungs- / Änderungszeitpunkt")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "60")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202107011415+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["DTM"]  # Missing required components
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