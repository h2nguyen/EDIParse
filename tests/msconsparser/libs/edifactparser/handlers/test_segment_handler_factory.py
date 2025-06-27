import unittest

from ediparse.libs.edifactparser.handlers import COMSegmentHandler, ERCSegmentHandler, FTXSegmentHandler
from ediparse.libs.edifactparser.handlers import CTASegmentHandler
from ediparse.libs.edifactparser.handlers import UNBSegmentHandler
from ediparse.libs.edifactparser.handlers import BGMSegmentHandler
from ediparse.libs.edifactparser.handlers import CCISegmentHandler
from ediparse.libs.edifactparser.handlers import DTMSegmentHandler
from ediparse.libs.edifactparser.handlers import LINSegmentHandler
from ediparse.libs.edifactparser.handlers import LOCSegmentHandler
from ediparse.libs.edifactparser.handlers import NADSegmentHandler
from ediparse.libs.edifactparser.handlers import PIASegmentHandler
from ediparse.libs.edifactparser.handlers import QTYSegmentHandler
from ediparse.libs.edifactparser.handlers import RFFSegmentHandler
from ediparse.libs.edifactparser.handlers import STSSegmentHandler
from ediparse.libs.edifactparser.handlers import UNASegmentHandler
from ediparse.libs.edifactparser.handlers import UNHSegmentHandler
from ediparse.libs.edifactparser.handlers import UNSSegmentHandler
from ediparse.libs.edifactparser.handlers import UNTSegmentHandler
from ediparse.libs.edifactparser.handlers import UNZSegmentHandler
from ediparse.libs.edifactparser.handlers import SegmentHandlerFactory
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.wrappers.constants import SegmentType


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
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA), CTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM), COMSegmentHandler)
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
        self.assertIn(f"Kein Handler für Segmenttyp '{unknown_segment_type}' definiert.", cm.output[0])

    def test_new_registered_handler_is_detected(self):
        """Test that a newly registered handler is properly detected."""
        # Arrange
        # Create a new factory instance
        factory = SegmentHandlerFactory(syntax_parser=self.syntax_parser)

        # Verify that all registered handlers are detected
        for segment_type in SegmentType:
            # Act
            handler = factory.get_handler(segment_type)

            # Assert
            self.assertIsNotNone(handler, f"Handler for {segment_type} should not be None")
            self.assertEqual(handler.__class__.__name__, f"{segment_type}SegmentHandler", 
                            f"Handler class name should be {segment_type}SegmentHandler")


if __name__ == '__main__':
    unittest.main()
