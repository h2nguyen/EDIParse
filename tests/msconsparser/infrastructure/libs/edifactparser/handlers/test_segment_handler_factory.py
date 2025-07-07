import unittest
from unittest import mock

from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.com_segment_handler import MSCONSCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.com_segment_handler import APERAKCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.cta_segment_handler import MSCONSCTASegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.cta_segment_handler import APERAKCTASegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.erc_segment_handler import ERCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.ftx_segment_handler import FTXSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unb_segment_handler import UNBSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.bgm_segment_handler import BGMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.cci_segment_handler import CCISegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.dtm_segment_handler import DTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.lin_segment_handler import LINSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.loc_segment_handler import LOCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.nad_segment_handler import NADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.pia_segment_handler import PIASegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.qty_segment_handler import QTYSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.rff_segment_handler import RFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.sts_segment_handler import STSSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.una_segment_handler import UNASegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unh_segment_handler import UNHSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.uns_segment_handler import UNSSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unt_segment_handler import UNTSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unz_segment_handler import UNZSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.segment_handler_factory import SegmentHandlerFactory
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentType


class TestSegmentHandlerFactory(unittest.TestCase):
    """Test case for the SegmentHandlerFactory class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

    def test_get_handler_returns_correct_handler_for_each_segment_type(self):
        """Test that get_handler returns the correct handler for each segment type."""
        # Test for each segment type
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNA), UNASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNB), UNBSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNH), UNHSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.BGM), BGMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.DTM), DTMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.ERC), ERCSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.FTX), FTXSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.RFF), RFFSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.NAD), NADSegmentHandler)
        # For CTA and COM segments, we need to provide a context with a message type
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
        from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType

        # Create contexts with message types
        mscons_context = MSCONSParsingContext()
        mscons_context.message_type = EdifactMessageType.MSCONS
        aperak_context = APERAKParsingContext()
        aperak_context.message_type = EdifactMessageType.APERAK

        # Test that the factory returns the correct handler for each message type
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM, mscons_context), MSCONSCOMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM, aperak_context), APERAKCOMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA, mscons_context), MSCONSCTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA, aperak_context), APERAKCTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNS), UNSSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.LOC), LOCSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CCI), CCISegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.LIN), LINSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.PIA), PIASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.QTY), QTYSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.STS), STSSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNT), UNTSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNZ), UNZSegmentHandler)

    def test_get_handler_returns_none_for_unknown_segment_type(self):
        """Test that get_handler returns None for an unknown segment type."""
        # Arrange
        unknown_segment_type = "UNKNOWN"

        # Act
        with self.assertLogs(level='WARNING') as cm:
            result = self.factory.get_handler(unknown_segment_type)

        # Assert
        self.assertIsNone(result)
        self.assertIn(f"No handler found for segment type '{unknown_segment_type}'.", cm.output[0])

    def test_new_registered_handler_is_detected(self):
        """Test that a newly registered handler is properly detected."""
        # Arrange
        # Create a new factory instance
        factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

        # Create contexts with message types for testing COM segment handler
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
        from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
        mscons_context = MSCONSParsingContext()
        mscons_context.message_type = EdifactMessageType.MSCONS

        # Verify that all registered handlers are detected
        for segment_type in SegmentType:
            # Act
            # For COM and CTA segments, we need to provide a context with a message type
            if segment_type == SegmentType.COM or segment_type == SegmentType.CTA:
                handler = factory.get_handler(segment_type, mscons_context)
                # Assert
                self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
                self.assertEqual(handler.__class__.__name__, f"MSCONS{segment_type}SegmentHandler", 
                                f"Handler class name should be MSCONS{segment_type}SegmentHandler")
            else:
                handler = factory.get_handler(segment_type)
                # Assert
                self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
                self.assertEqual(handler.__class__.__name__, f"{segment_type}SegmentHandler", 
                                f"Handler class name should be {segment_type}SegmentHandler")

    def test_all_message_types_have_com_segment_handlers(self):
        """Test that all message types defined in EdifactMessageType have a corresponding COM segment handler."""
        # Arrange
        from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
        from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext

        # Create a new factory instance
        factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

        # For each message type, create a context and check if a COM segment handler exists
        for message_type in EdifactMessageType:
            # Create a mock context with the message type
            context = mock.MagicMock(spec=ParsingContext)
            context.message_type = message_type
            context.current_message = mock.MagicMock()

            # Act
            handler = factory.get_handler(SegmentType.COM, context)

            # Assert
            self.assertIsNotNone(handler, f"No COM segment handler found for message type {message_type}")
            self.assertEqual(handler.__class__.__name__, f"{message_type}COMSegmentHandler", 
                            f"Handler class name should be {message_type}COMSegmentHandler")

    def test_all_message_types_have_cta_segment_handlers(self):
        """Test that all message types defined in EdifactMessageType have a corresponding CTA segment handler."""
        # Arrange
        from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
        from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext

        # Create a new factory instance
        factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

        # For each message type, create a context and check if a CTA segment handler exists
        for message_type in EdifactMessageType:
            # Create a mock context with the message type
            context = mock.MagicMock(spec=ParsingContext)
            context.message_type = message_type
            context.current_message = mock.MagicMock()

            # Act
            handler = factory.get_handler(SegmentType.CTA, context)

            # Assert
            self.assertIsNotNone(handler, f"No CTA segment handler found for message type {message_type}")
            self.assertEqual(handler.__class__.__name__, f"{message_type}CTASegmentHandler", 
                            f"Handler class name should be {message_type}CTASegmentHandler")


if __name__ == '__main__':
    unittest.main()
