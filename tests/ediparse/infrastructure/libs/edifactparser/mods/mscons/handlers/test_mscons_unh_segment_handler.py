import unittest
from unittest.mock import patch

from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.unh_segment_handler import MSCONSUNHSegmentHandler
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message import SegmentUNH, NachrichtenKennung
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange


class TestMSCONSUNHSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSUNHSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSUNHSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up interchange needed for testing
        self.context.interchange = EdifactInterchange()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSUNHSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_valid_segment(self):
        """Test the _update_context method with a valid UNH segment."""
        # Arrange
        segment = SegmentUNH(
            nachrichten_referenznummer="1",
            nachrichten_kennung=NachrichtenKennung(
                nachrichtentyp_kennung="MSCONS",
                versionsnummer_des_nachrichtentyps="D",
                freigabenummer_des_nachrichtentyps="04B",
                verwaltende_organisation="UN",
                anwendungscode_der_zustaendigen_organisation="2.4c"
            )
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.message_type, EdifactMessageType.MSCONS)
        self.assertIsNotNone(self.context.current_message)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment, segment)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_kennung.nachrichtentyp_kennung, "MSCONS")
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_kennung.versionsnummer_des_nachrichtentyps, "D")
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_kennung.freigabenummer_des_nachrichtentyps, "04B")
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_kennung.verwaltende_organisation, "UN")
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_kennung.anwendungscode_der_zustaendigen_organisation, "2.4c")
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)

    def test_update_context_with_invalid_segment(self):
        """Test the _update_context method with an invalid UNH segment (nachrichten_kennung is None)."""
        # Arrange
        segment = SegmentUNH(
            nachrichten_referenznummer="1",
            nachrichten_kennung=None
        )
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(EdifactParserException):
            self.handler._update_context(
                segment=segment,
                current_segment_group=current_segment_group,
                context=self.context
            )

    @patch('logging.Logger.warning')
    def test_update_context_with_non_mscons_message_type(self, mock_warning):
        """Test the _update_context method with a non-MSCONS message type."""
        # Arrange
        segment = SegmentUNH(
            nachrichten_referenznummer="1",
            nachrichten_kennung=NachrichtenKennung(
                nachrichtentyp_kennung="APERAK",
                versionsnummer_des_nachrichtentyps="D",
                freigabenummer_des_nachrichtentyps="04B",
                verwaltende_organisation="UN",
                anwendungscode_der_zustaendigen_organisation="2.4c"
            )
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.message_type, EdifactMessageType.MSCONS)
        self.assertIsNotNone(self.context.current_message)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment, segment)
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)
        # Check that warning was logged
        # Use a more flexible approach to check the warning message
        # Check that at least one warning call contains the expected content
        warning_calls = [call[0][0] for call in mock_warning.call_args_list]
        self.assertTrue(any("Expected MSCONS message type" in call and "APERAK" in call for call in warning_calls),
                       f"No warning message found containing 'Expected MSCONS message type' and 'APERAK'. Actual calls: {warning_calls}")
        mock_warning.assert_any_call("Fallback to message type: 'MSCONS'.")

    def test_handle_with_valid_segment(self):
        """Test the handle method with a valid UNH segment."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "1", "MSCONS:D:04B:UN:EAN010"]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.message_type, EdifactMessageType.MSCONS)
        self.assertIsNotNone(self.context.current_message)
        self.assertIsNotNone(self.context.current_message.unh_nachrichtenkopfsegment)
        unh_segment = self.context.current_message.unh_nachrichtenkopfsegment
        self.assertEqual(unh_segment.nachrichten_referenznummer, "1")
        self.assertEqual(unh_segment.nachrichten_kennung.nachrichtentyp_kennung, "MSCONS")
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)


if __name__ == '__main__':
    unittest.main()