import logging
import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.dtm_segment_handler import APERAKDTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup2
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentDTM


class TestAPERAKDTMSegmentHandler(unittest.TestCase):
    """Test case for the APERAKDTMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKDTMSegmentHandler(syntax_parser=self.syntax_parser)
        self.context = APERAKParsingContext()
        # Add dtm_nachrichtendatum list to the current_message if it doesn't exist
        if not hasattr(self.context.current_message, 'dtm_nachrichtendatum'):
            self.context.current_message.dtm_nachrichtendatum = []

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKDTMSegmentHandler(syntax_parser=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_no_segment_group(self):
        """Test the _update_context method with no segment group."""
        # Arrange
        segment = SegmentDTM(
            bezeichner="Dokumenten-/Nachrichtendatum/-zeit",
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202106011315+00",
            datums_oder_uhrzeit_oder_zeitspannen_format_code="303"
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_message.dtm_nachrichtendatum), 1)
        self.assertEqual(self.context.current_message.dtm_nachrichtendatum[0], segment)

    def test_update_context_with_sg2(self):
        """Test the _update_context method with segment group SG2."""
        # Arrange
        segment = SegmentDTM(
            bezeichner="Referenzdatum/-zeit",
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="171",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202106011315+00",
            datums_oder_uhrzeit_oder_zeitspannen_format_code="303"
        )
        current_segment_group = SegmentGroup.SG2

        self.context.current_sg2 = SegmentGroup2()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg2.dtm_referenzdatum), 1)
        self.assertEqual(self.context.current_sg2.dtm_referenzdatum[0], segment)

    def test_update_context_with_unknown_segment_group(self):
        """Test the _update_context method with an unknown segment group."""
        # Arrange
        segment = SegmentDTM(
            bezeichner="Dokumenten-/Nachrichtendatum/-zeit",
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202106011315+00",
            datums_oder_uhrzeit_oder_zeitspannen_format_code="303"
        )
        current_segment_group = SegmentGroup.SG3  # Not handled by the handler
        
        # Capture log messages
        with self.assertLogs(logger='ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.dtm_segment_handler', level=logging.DEBUG) as log:
            # Act
            self.handler._update_context(
                segment=segment,
                current_segment_group=current_segment_group,
                context=self.context
            )
            
            # Assert
            self.assertTrue(any(f"No handling defined for DTM-Segment '{segment}'" in message for message in log.output))

    def test_handle_with_no_segment_group(self):
        """Test the handle method with no segment group."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "137:202106011315+00:303"]
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
        self.assertEqual(len(self.context.current_message.dtm_nachrichtendatum), 1)
        dtm_segment = self.context.current_message.dtm_nachrichtendatum[0]
        self.assertEqual(dtm_segment.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertEqual(dtm_segment.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(dtm_segment.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_handle_with_sg2(self):
        """Test the handle method with segment group SG2."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "171:202106011315+00:303"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG2
        
        # We need to set up the SG2 context first
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup2
        self.context.current_sg2 = SegmentGroup2()

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg2.dtm_referenzdatum), 1)
        dtm_segment = self.context.current_sg2.dtm_referenzdatum[0]
        self.assertEqual(dtm_segment.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "171")
        self.assertEqual(dtm_segment.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(dtm_segment.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")


if __name__ == '__main__':
    unittest.main()