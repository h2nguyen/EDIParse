import unittest
from unittest.mock import Mock

from ediparse.infrastructure.libs.edifactparser.resolvers.group_state_resolver import (
    GroupStateResolver,
)
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import (
    SegmentGroup,
)
from ediparse.infrastructure.libs.edifactparser.wrappers.context import (
    ParsingContext,
)


class TestGroupStateResolver(unittest.TestCase):
    """Tests for the base GroupStateResolver class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.context = Mock(spec=ParsingContext)

    def test_base_resolve_and_get_segment_group_returns_none(self):
        # Arrange
        current_segment_type = "ANY"
        current_segment_group = SegmentGroup.SG1

        # Act
        result = GroupStateResolver.resolve_and_get_segment_group(
            current_segment_type=current_segment_type,
            current_segment_group=current_segment_group,
            context=self.context,
        )

        # Verify
        self.assertIsNone(
            result,
            "Base GroupStateResolver should return None by default (no implementation).",
        )

    def test_subclass_can_override_and_be_called_statically(self):
        # Arrange
        class DummyResolver(GroupStateResolver):
            @staticmethod
            def resolve_and_get_segment_group(current_segment_type, current_segment_group, context):
                # Minimal example override: return SG2 when type is 'X', else keep current
                if current_segment_type == "X":
                    return SegmentGroup.SG2
                return current_segment_group

        current_segment_group = SegmentGroup.SG1

        # Act
        result_when_x = DummyResolver.resolve_and_get_segment_group(
            current_segment_type="X",
            current_segment_group=current_segment_group,
            context=self.context,
        )
        result_when_other = DummyResolver.resolve_and_get_segment_group(
            current_segment_type="OTHER",
            current_segment_group=current_segment_group,
            context=self.context,
        )

        # Verify
        self.assertEqual(result_when_x, SegmentGroup.SG2)
        self.assertEqual(result_when_other, SegmentGroup.SG1)


if __name__ == "__main__":
    unittest.main()
