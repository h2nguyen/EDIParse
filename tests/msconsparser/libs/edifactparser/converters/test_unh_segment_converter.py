import unittest

from ediparse.libs.edifactparser.converters import UNHSegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentUNH


class TestUNHSegmentConverter(unittest.TestCase):
    """Test case for the UNHSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = MSCONSParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = UNHSegmentConverter(syntax_parser=self.syntax_parser)

    def test_convert_internal_with_basic_components(self):
        """Test the _convert_internal method with basic components."""
        # Arrange
        element_components = ["UNH", "4", "MSCONS:D:04B:UN:2.4c"]
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
        self.assertIsInstance(result, SegmentUNH)
        self.assertEqual(result.nachrichten_referenznummer, "4")
        self.assertEqual(result.nachrichten_kennung.nachrichtentyp_kennung, "MSCONS")
        self.assertEqual(result.nachrichten_kennung.versionsnummer_des_nachrichtentyps, "D")
        self.assertEqual(result.nachrichten_kennung.freigabenummer_des_nachrichtentyps, "04B")
        self.assertEqual(result.nachrichten_kennung.verwaltende_organisation, "UN")
        self.assertEqual(result.nachrichten_kennung.anwendungscode_der_zustaendigen_organisation, "2.4c")
        self.assertIsNone(result.allgemeine_zuordnungsreferenz)
        self.assertIsNone(result.status_der_uebermittlung)

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["UNH", "1", "MSCONS:D:04B:UN:2.4c", "UNB_DE0020_nr_1", "1:C"]
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
        self.assertIsInstance(result, SegmentUNH)
        self.assertEqual(result.nachrichten_referenznummer, "1")
        self.assertEqual(result.nachrichten_kennung.nachrichtentyp_kennung, "MSCONS")
        self.assertEqual(result.nachrichten_kennung.versionsnummer_des_nachrichtentyps, "D")
        self.assertEqual(result.nachrichten_kennung.freigabenummer_des_nachrichtentyps, "04B")
        self.assertEqual(result.nachrichten_kennung.verwaltende_organisation, "UN")
        self.assertEqual(result.nachrichten_kennung.anwendungscode_der_zustaendigen_organisation, "2.4c")
        self.assertEqual(result.allgemeine_zuordnungsreferenz, "UNB_DE0020_nr_1")
        self.assertEqual(result.status_der_uebermittlung.uebermittlungsfolgenummer, "1")
        self.assertEqual(result.status_der_uebermittlung.erste_und_letzte_uebermittlung, "C")

    def test_convert_internal_with_zuordnungsreferenz_only(self):
        """Test the _convert_internal method with zuordnungsreferenz only."""
        # Arrange
        element_components = ["UNH", "4", "MSCONS:D:04B:UN:2.4c", "UNB_DE0020_nr_1"]
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
        self.assertIsInstance(result, SegmentUNH)
        self.assertEqual(result.nachrichten_referenznummer, "4")
        self.assertEqual(result.nachrichten_kennung.nachrichtentyp_kennung, "MSCONS")
        self.assertEqual(result.allgemeine_zuordnungsreferenz, "UNB_DE0020_nr_1")
        self.assertIsNone(result.status_der_uebermittlung)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "4"]  # Missing required components
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
