# coding: utf-8

import logging
from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentQTY

logger = logging.getLogger(__name__)


class QTYSegmentConverter(SegmentConverter[SegmentQTY]):
    """
    Converter for QTY (Quantity) segments.

    This __converter transforms QTY segment data from EDIFACT format into a structured
    SegmentQTY object. The QTY segment is used to specify quantities for the current 
    item position, including the quantity value and unit of measurement.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the QTY segment __converter with the syntax parser.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper=syntax_helper)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentQTY:
        """
        Converts QTY (Quantities) segment components to a SegmentQTY object.

        The QTY segment is used to specify quantities for the current item position.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentQTY object with quantity qualifier, the quantity and unit measurement code

        Examples:
        QTY+220:4250.465:D54'
        QTY+220:4250,465:D54' - When UNA overwritten by decimal separator with ','
        QTY+67:4250.465' - Example of a quantity and status specification as a substitute value with 3 decimal places without a unit of measurement
        QTY+220:4.123:D54' - Example of a quantity and status specification as a true value with 3 decimal places and the unit of measurement watts per square meter
        QTY+79:-4.987:KWH' - Example of a quantity and status specification as a summed energy quantity (total value, balance sheet total) as a negative value with 3 decimal places and the unit of measurement kilowatt hours
        """
        details = self._syntax_parser.split_components(
            string_content=element_components[1],
            context=context,
            include_escape_symbol=False
        )
        menge_qualifier = details[0]
        menge = self._convert_decimal(details[1], context) if len(details) > 1 else None
        masseinheit_code = details[2] if len(details) > 2 else None

        return SegmentQTY(
            menge_qualifier=menge_qualifier,
            menge=menge,
            masseinheit_code=masseinheit_code
        )
