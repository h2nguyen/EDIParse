import unittest
from unittest.mock import Mock, patch

from ediparse.infrastructure.libs.edifactparser.mods.mscons.group_state_resolver import MsconsGroupStateResolver
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup, SegmentType
from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext


class TestMsconsGroupStateResolver(unittest.TestCase):
    """Test case for the MsconsGroupStateResolver class."""

    def setUp(self):
        """Set up the test case."""
        self.context = Mock(spec=ParsingContext)

    def test_empty_segment_type(self):
        """Test resolve_and_get_segment_group with empty segment type."""
        # Arrange
        current_segment_type = ""
        current_segment_group = None

        # Act
        with patch('ediparse.infrastructure.libs.edifactparser.mods.mscons.group_state_resolver.logger') as mock_logger:
            result = MsconsGroupStateResolver.resolve_and_get_segment_group(
                current_segment_type=current_segment_type,
                current_segment_group=current_segment_group,
                context=self.context
            )

        # Assert
        self.assertIsNone(result)
        mock_logger.error.assert_called_once()

    def test_dtm_segment_type(self):
        """Test resolve_and_get_segment_group with DTM segment type."""
        # Arrange
        current_segment_type = SegmentType.DTM
        current_segment_group = SegmentGroup.SG1

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, current_segment_group)

    def test_rff_segment_type_with_none_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and None group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG1)

    def test_rff_segment_type_with_sg1_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG1 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG1

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG1)

    def test_rff_segment_type_with_sg6_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG6 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG6

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG7)

    def test_rff_segment_type_with_sg7_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG7 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG7

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG7)

    def test_nad_segment_type_with_none_group(self):
        """Test resolve_and_get_segment_group with NAD segment type and None group."""
        # Arrange
        current_segment_type = SegmentType.NAD
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG5)

    def test_nad_segment_type_with_sg1_group(self):
        """Test resolve_and_get_segment_group with NAD segment type and SG1 group."""
        # Arrange
        current_segment_type = SegmentType.NAD
        current_segment_group = SegmentGroup.SG1

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG2)

    def test_nad_segment_type_with_sg4_group(self):
        """Test resolve_and_get_segment_group with NAD segment type and SG4 group."""
        # Arrange
        current_segment_type = SegmentType.NAD
        current_segment_group = SegmentGroup.SG4

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG2)

    def test_cta_segment_type(self):
        """Test resolve_and_get_segment_group with CTA segment type."""
        # Arrange
        current_segment_type = SegmentType.CTA
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG4)

    def test_com_segment_type(self):
        """Test resolve_and_get_segment_group with COM segment type."""
        # Arrange
        current_segment_type = SegmentType.COM
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG4)

    def test_loc_segment_type(self):
        """Test resolve_and_get_segment_group with LOC segment type."""
        # Arrange
        current_segment_type = SegmentType.LOC
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG6)

    def test_cci_segment_type(self):
        """Test resolve_and_get_segment_group with CCI segment type."""
        # Arrange
        current_segment_type = SegmentType.CCI
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG8)

    def test_lin_segment_type(self):
        """Test resolve_and_get_segment_group with LIN segment type."""
        # Arrange
        current_segment_type = SegmentType.LIN
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG9)

    def test_pia_segment_type(self):
        """Test resolve_and_get_segment_group with PIA segment type."""
        # Arrange
        current_segment_type = SegmentType.PIA
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG9)

    def test_qty_segment_type(self):
        """Test resolve_and_get_segment_group with QTY segment type."""
        # Arrange
        current_segment_type = SegmentType.QTY
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG10)

    def test_sts_segment_type(self):
        """Test resolve_and_get_segment_group with STS segment type."""
        # Arrange
        current_segment_type = SegmentType.STS
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG10)

    def test_unknown_segment_type(self):
        """Test resolve_and_get_segment_group with unknown segment type."""
        # Arrange
        current_segment_type = "UNKNOWN"
        current_segment_group = None

        # Act
        result = MsconsGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()