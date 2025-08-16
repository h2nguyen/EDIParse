import logging
import unittest

from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.unh_segment_handler import APERAKUNHSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import EdifactAperakMessage
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import EdifactInterchange
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message import SegmentUNH, NachrichtenKennung


class TestAPERAKUNHSegmentHandler(unittest.TestCase):
    """Test case for the APERAKUNHSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKUNHSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()
        # Set up interchange for testing

        self.context.interchange = EdifactInterchange()
        self.context.interchange.unh_unt_nachrichten = []

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKUNHSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_aperak_message_type(self):
        """Test the _update_context method with APERAK message type."""
        # Arrange
        message_identification = NachrichtenKennung(
            nachrichtentyp_kennung="APERAK",
            versionsnummer_des_nachrichtentyps="D",
            freigabenummer_des_nachrichtentyps="07B",
            verwaltende_organisation="UN",
            anwendungscode_der_zustaendigen_organisation="EAN007"
        )

        segment = SegmentUNH(
            nachrichten_referenznummer="12345",
            nachrichten_kennung=message_identification
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(self.context.current_message, EdifactAperakMessage)
        self.assertEqual(self.context.message_type, EdifactMessageType.APERAK)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment, segment)
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)

    def test_update_context_with_non_aperak_message_type(self):
        """Test the _update_context method with a message type other than APERAK."""
        # Arrange
        message_identification = NachrichtenKennung(
            nachrichtentyp_kennung="MSCONS",
            versionsnummer_des_nachrichtentyps="D",
            freigabenummer_des_nachrichtentyps="04B",
            verwaltende_organisation="UN",
            anwendungscode_der_zustaendigen_organisation="EAN007"
        )

        segment = SegmentUNH(
            nachrichten_referenznummer="12345",
            nachrichten_kennung=message_identification
        )
        current_segment_group = None

        # Capture log messages
        with self.assertLogs(logger='ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.unh_segment_handler', level=logging.WARNING) as log:
            # Act
            self.handler._update_context(
                segment=segment,
                current_segment_group=current_segment_group,
                context=self.context
            )

            # Assert
            self.assertTrue(any(f"Expected APERAK message type, but got: {segment.nachrichten_kennung}" in message for message in log.output))
            self.assertTrue(any(f"Fallback to message type: '{EdifactMessageType.APERAK}'" in message for message in log.output))

        self.assertIsInstance(self.context.current_message, EdifactAperakMessage)
        self.assertEqual(self.context.message_type, EdifactMessageType.APERAK)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment, segment)
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)

    def test_update_context_with_none_message_identification(self):
        """Test the _update_context method with None message identification."""
        # Arrange
        segment = SegmentUNH(
            nachrichten_referenznummer="12345",
            nachrichten_kennung=None
        )
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(EdifactParserException) as context:
            self.handler._update_context(
                segment=segment,
                current_segment_group=current_segment_group,
                context=self.context
            )

        self.assertEqual(str(context.exception), "nachrichten_kennung should not be None.")

    def test_handle_with_aperak_message_type(self):
        """Test the handle method with APERAK message type."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "12345", "APERAK:D:07B:UN:EAN007"]
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
        self.assertIsInstance(self.context.current_message, EdifactAperakMessage)
        self.assertEqual(self.context.message_type, EdifactMessageType.APERAK)
        unh_segment = self.context.current_message.unh_nachrichtenkopfsegment
        self.assertEqual(unh_segment.nachrichten_referenznummer, "12345")
        self.assertEqual(unh_segment.nachrichten_kennung.nachrichtentyp_kennung, "APERAK")
        self.assertEqual(unh_segment.nachrichten_kennung.versionsnummer_des_nachrichtentyps, "D")
        self.assertEqual(unh_segment.nachrichten_kennung.freigabenummer_des_nachrichtentyps, "07B")
        self.assertEqual(unh_segment.nachrichten_kennung.verwaltende_organisation, "UN")
        self.assertEqual(unh_segment.nachrichten_kennung.anwendungscode_der_zustaendigen_organisation, "EAN007")
        self.assertEqual(len(self.context.interchange.unh_unt_nachrichten), 1)
        self.assertEqual(self.context.interchange.unh_unt_nachrichten[0], self.context.current_message)


if __name__ == '__main__':
    unittest.main()
