import unittest
from unittest import mock

from ediparse.infrastructure.libs.edifactparser.handlers.bgm_segment_handler import BGMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.segment_handler_factory import SegmentHandlerFactory
from ediparse.infrastructure.libs.edifactparser.handlers.una_segment_handler import UNASegmentHandler
# Import standard segment handlers
from ediparse.infrastructure.libs.edifactparser.handlers.unb_segment_handler import UNBSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unt_segment_handler import UNTSegmentHandler
from ediparse.infrastructure.libs.edifactparser.handlers.unz_segment_handler import UNZSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.com_segment_handler import APERAKCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.cta_segment_handler import APERAKCTASegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.dtm_segment_handler import APERAKDTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.erc_segment_handler import APERAKERCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.ftx_segment_handler import APERAKFTXSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.nad_segment_handler import APERAKNADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.rff_segment_handler import APERAKRFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.unh_segment_handler import APERAKUNHSegmentHandler
# Import message-type-specific segment handlers
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.com_segment_handler import MSCONSCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.cta_segment_handler import MSCONSCTASegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.dtm_segment_handler import MSCONSDTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.nad_segment_handler import MSCONSNADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.rff_segment_handler import MSCONSRFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.unh_segment_handler import MSCONSUNHSegmentHandler
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
        # For segment types that require a message-type-specific context
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
        from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType

        # Create contexts with message types
        mscons_context = MSCONSParsingContext()
        mscons_context.message_type = EdifactMessageType.MSCONS
        mscons_context.current_message = mock.MagicMock()

        aperak_context = APERAKParsingContext()
        aperak_context.message_type = EdifactMessageType.APERAK
        aperak_context.current_message = mock.MagicMock()

        # Test standard segment handlers (no message type required)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNA), UNASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNB), UNBSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.BGM), BGMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNT), UNTSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNZ), UNZSegmentHandler)

        # Test message-type-specific segment handlers for MSCONS
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM, mscons_context), MSCONSCOMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA, mscons_context), MSCONSCTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.DTM, mscons_context), MSCONSDTMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.NAD, mscons_context), MSCONSNADSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.RFF, mscons_context), MSCONSRFFSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNH, mscons_context), MSCONSUNHSegmentHandler)

        # Test message-type-specific segment handlers for APERAK
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM, aperak_context), APERAKCOMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA, aperak_context), APERAKCTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.DTM, aperak_context), APERAKDTMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.ERC, aperak_context), APERAKERCSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.FTX, aperak_context), APERAKFTXSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.NAD, aperak_context), APERAKNADSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.RFF, aperak_context), APERAKRFFSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNH, aperak_context), APERAKUNHSegmentHandler)

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

        # Create contexts with message types for testing message-type-specific handlers
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
        from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
        from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange

        # MSCONS context
        mscons_context = MSCONSParsingContext()
        mscons_context.message_type = EdifactMessageType.MSCONS
        mscons_context.current_message = mock.MagicMock()
        mscons_context.interchange = mock.MagicMock(spec=EdifactInterchange)

        # APERAK context
        aperak_context = APERAKParsingContext()
        aperak_context.message_type = EdifactMessageType.APERAK
        aperak_context.current_message = mock.MagicMock()
        aperak_context.interchange = mock.MagicMock(spec=EdifactInterchange)

        # Standard segment types (no message type required)
        standard_segments = {
            SegmentType.UNA, SegmentType.UNB, SegmentType.BGM, 
            SegmentType.UNT, SegmentType.UNZ
        }

        # Message-type-specific segment types for MSCONS
        mscons_specific_segments = {
            SegmentType.COM, SegmentType.CTA, SegmentType.DTM, SegmentType.NAD, 
            SegmentType.RFF, SegmentType.UNH, SegmentType.UNS, SegmentType.LOC, 
            SegmentType.CCI, SegmentType.LIN, SegmentType.PIA, SegmentType.QTY, 
            SegmentType.STS
        }

        # Message-type-specific segment types for APERAK
        aperak_specific_segments = {
            SegmentType.COM, SegmentType.CTA, SegmentType.DTM, SegmentType.ERC, SegmentType.FTX, 
            SegmentType.NAD, SegmentType.RFF, SegmentType.UNH
        }

        # Verify that all registered handlers are detected
        for segment_type in SegmentType:
            # Act
            if segment_type in standard_segments:
                # For standard segment types, no context is needed
                handler = factory.get_handler(segment_type)
                # Assert
                self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
                self.assertEqual(handler.__class__.__name__, f"{segment_type}SegmentHandler", 
                                f"Handler class name should be {segment_type}SegmentHandler")
            elif segment_type in mscons_specific_segments:
                # For MSCONS-specific segments, we need to provide a MSCONS context
                handler = factory.get_handler(segment_type, mscons_context)
                # Assert
                self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
                self.assertEqual(handler.__class__.__name__, f"MSCONS{segment_type}SegmentHandler", 
                                f"Handler class name should be MSCONS{segment_type}SegmentHandler")
            elif segment_type in aperak_specific_segments and segment_type not in mscons_specific_segments:
                # For APERAK-only segments, we need to provide an APERAK context
                handler = factory.get_handler(segment_type, aperak_context)
                # Assert
                self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
                self.assertEqual(handler.__class__.__name__, f"APERAK{segment_type}SegmentHandler", 
                                f"Handler class name should be APERAK{segment_type}SegmentHandler")

    def test_all_message_types_have_message_specific_segment_handlers(self):
        """Test that all message types defined in EdifactMessageType have corresponding message-specific segment handlers."""
        # Arrange
        from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
        from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext
        from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange

        # Create a new factory instance
        factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

        # Common message-type-specific segment types (implemented for all message types)
        common_message_type_specific_segments = [
            SegmentType.COM, SegmentType.CTA, SegmentType.DTM, 
            SegmentType.NAD, SegmentType.RFF, SegmentType.UNH
        ]

        # MSCONS-specific segment types
        mscons_specific_segments = [
            SegmentType.UNS, SegmentType.LOC, SegmentType.CCI, 
            SegmentType.LIN, SegmentType.PIA, SegmentType.QTY, 
            SegmentType.STS
        ]

        # APERAK-specific segment types
        aperak_specific_segments = [SegmentType.FTX, SegmentType.ERC]

        # For each message type, create a context and check if all message-specific segment handlers exist
        for message_type in EdifactMessageType:
            # Create a mock context with the message type
            context = mock.MagicMock(spec=ParsingContext)
            context.message_type = message_type
            context.current_message = mock.MagicMock()
            context.interchange = mock.MagicMock(spec=EdifactInterchange)

            # Test common message-type-specific segments
            for segment_type in common_message_type_specific_segments:
                # Act
                handler = factory.get_handler(segment_type, context)

                # Assert
                self.assertIsNotNone(handler, f"No {segment_type} segment handler found for message type {message_type}")
                self.assertEqual(handler.__class__.__name__, f"{message_type}{segment_type}SegmentHandler", 
                                f"Handler class name should be {message_type}{segment_type}SegmentHandler")

            # Test MSCONS-specific segments
            if message_type == EdifactMessageType.MSCONS:
                for segment_type in mscons_specific_segments:
                    # Act
                    handler = factory.get_handler(segment_type, context)

                    # Assert
                    self.assertIsNotNone(handler, f"No {segment_type} segment handler found for message type {message_type}")
                    self.assertEqual(handler.__class__.__name__, f"{message_type}{segment_type}SegmentHandler", 
                                    f"Handler class name should be {message_type}{segment_type}SegmentHandler")

            # Test APERAK-specific segments
            if message_type == EdifactMessageType.APERAK:
                for segment_type in aperak_specific_segments:
                    # Act
                    handler = factory.get_handler(segment_type, context)

                    # Assert
                    self.assertIsNotNone(handler, f"No {segment_type} segment handler found for message type {message_type}")
                    self.assertEqual(handler.__class__.__name__, f"{message_type}{segment_type}SegmentHandler", 
                                    f"Handler class name should be {message_type}{segment_type}SegmentHandler")


if __name__ == '__main__':
    unittest.main()
