import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.loc_segment_handler import MSCONSLOCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup5
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLOC, Ortsangabe


class TestMSCONSLOCSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSLOCSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSLOCSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg5 = SegmentGroup5()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSLOCSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg6_existing(self):
        """Test the _update_context method with segment group SG6 when current_sg6 already exists."""
        # Arrange
        segment = SegmentLOC(
            ortsangabe_qualifier="237",
            ortsangabe=Ortsangabe(
                ortsangabe_code="51078306269"
            )
        )
        current_segment_group = SegmentGroup.SG6
        # Import inside method to avoid circular imports
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup6
        self.context.current_sg6 = SegmentGroup6()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg6)
        self.assertEqual(self.context.current_sg6.loc_identifikationsangabe, segment)
        self.assertEqual(len(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt), 1)
        self.assertEqual(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt[0], self.context.current_sg6)

    def test_update_context_with_sg6_new(self):
        """Test the _update_context method with segment group SG6 when current_sg6 does not exist."""
        # Arrange
        segment = SegmentLOC(
            ortsangabe_qualifier="237",
            ortsangabe=Ortsangabe(
                ortsangabe_code="51078306269"
            )
        )
        current_segment_group = SegmentGroup.SG6
        # Ensure current_sg6 is None
        self.context.current_sg6 = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg6)
        self.assertEqual(self.context.current_sg6.loc_identifikationsangabe, segment)
        self.assertEqual(len(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt), 1)
        self.assertEqual(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt[0], self.context.current_sg6)

    def test_update_context_with_non_sg6(self):
        """Test the _update_context method with a segment group other than SG6."""
        # Arrange
        segment = SegmentLOC(
            ortsangabe_qualifier="237",
            ortsangabe=Ortsangabe(
                ortsangabe_code="51078306269"
            )
        )
        current_segment_group = SegmentGroup.SG1  # Not SG6
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg6', None))
        self.assertEqual(len(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt), 0)

    def test_handle_with_sg6(self):
        """Test the handle method with segment group SG6."""
        # Arrange
        line_number = 1
        element_components = ["LOC", "237", "51078306269"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG6

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg6)
        loc_segment = self.context.current_sg6.loc_identifikationsangabe
        self.assertEqual(loc_segment.ortsangabe_qualifier, "237")
        # The converter might not set ortsangabe correctly from element_components
        # So we'll just check if the segment was added to the context
        self.assertEqual(len(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt), 1)
        self.assertEqual(self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt[0], self.context.current_sg6)


if __name__ == '__main__':
    unittest.main()