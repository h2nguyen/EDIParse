import unittest
from unittest.mock import Mock, patch

from ediparse.infrastructure.libs.edifactparser.mods.aperak.group_state_resolver import AperakGroupStateResolver
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup, SegmentType
from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext


class TestAperakGroupStateResolver(unittest.TestCase):
    """Test case for the AperakGroupStateResolver class."""

    def setUp(self):
        """Set up the test case."""
        self.context = Mock(spec=ParsingContext)

    def test_empty_segment_type(self):
        """Test resolve_and_get_segment_group with empty segment type."""
        # Arrange
        current_segment_type = ""
        current_segment_group = None

        # Act
        with patch('ediparse.infrastructure.libs.edifactparser.mods.aperak.group_state_resolver.logger') as mock_logger:
            result = AperakGroupStateResolver.resolve_and_get_segment_group(
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
        current_segment_group = SegmentGroup.SG2

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
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
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG2)

    def test_rff_segment_type_with_sg2_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG2 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG2

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG2)

    def test_rff_segment_type_with_sg4_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG4 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG4

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG5)

    def test_rff_segment_type_with_sg5_group(self):
        """Test resolve_and_get_segment_group with RFF segment type and SG5 group."""
        # Arrange
        current_segment_type = SegmentType.RFF
        current_segment_group = SegmentGroup.SG5

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG5)

    def test_nad_segment_type(self):
        """Test resolve_and_get_segment_group with NAD segment type."""
        # Arrange
        current_segment_type = SegmentType.NAD
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG3)

    def test_cta_segment_type(self):
        """Test resolve_and_get_segment_group with CTA segment type."""
        # Arrange
        current_segment_type = SegmentType.CTA
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG3)

    def test_com_segment_type(self):
        """Test resolve_and_get_segment_group with COM segment type."""
        # Arrange
        current_segment_type = SegmentType.COM
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG3)

    def test_erc_segment_type(self):
        """Test resolve_and_get_segment_group with ERC segment type."""
        # Arrange
        current_segment_type = SegmentType.ERC
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG4)

    def test_ftx_segment_type_with_none_group(self):
        """Test resolve_and_get_segment_group with FTX segment type and None group."""
        # Arrange
        current_segment_type = SegmentType.FTX
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG4)

    def test_ftx_segment_type_with_sg4_group(self):
        """Test resolve_and_get_segment_group with FTX segment type and SG4 group."""
        # Arrange
        current_segment_type = SegmentType.FTX
        current_segment_group = SegmentGroup.SG4

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG4)

    def test_ftx_segment_type_with_sg5_group(self):
        """Test resolve_and_get_segment_group with FTX segment type and SG5 group."""
        # Arrange
        current_segment_type = SegmentType.FTX
        current_segment_group = SegmentGroup.SG5

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, SegmentGroup.SG5)

    def test_unknown_segment_type(self):
        """Test resolve_and_get_segment_group with unknown segment type."""
        # Arrange
        current_segment_type = "UNKNOWN"
        current_segment_group = None

        # Act
        result = AperakGroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()