# coding: utf-8

import logging
from typing import Dict, Optional

from ..utils.edifact_syntax_helper import EdifactSyntaxHelper
from ..wrappers.constants import SegmentType

from .segment_handler import SegmentHandler
from .bgm_segment_handler import BGMSegmentHandler
from .cci_segment_handler import CCISegmentHandler
from .com_segment_handler import COMSegmentHandler
from .cta_segment_handler import CTASegmentHandler
from .dtm_segment_handler import DTMSegmentHandler
from .lin_segment_handler import LINSegmentHandler
from .loc_segment_handler import LOCSegmentHandler
from .nad_segment_handler import NADSegmentHandler
from .pia_segment_handler import PIASegmentHandler
from .qty_segment_handler import QTYSegmentHandler
from .rff_segment_handler import RFFSegmentHandler
from .sts_segment_handler import STSSegmentHandler
from .una_segment_handler import UNASegmentHandler
from .unb_segment_handler import UNBSegmentHandler
from .unh_segment_handler import UNHSegmentHandler
from .uns_segment_handler import UNSSegmentHandler
from .unt_segment_handler import UNTSegmentHandler
from .unz_segment_handler import UNZSegmentHandler
from .erc_segment_handler import ERCSegmentHandler
from .ftx_segment_handler import FTXSegmentHandler

logger = logging.getLogger(__name__)


class SegmentHandlerFactory:
    """
    Factory class for creating segment handlers.

    This factory maintains a registry of segment handlers and provides a method to 
    retrieve the appropriate handler for a given segment type. It centralizes the 
    creation and management of segment handlers, ensuring that each segment type 
    is processed by its specialized handler.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the factory with a syntax parser and register all segment handlers.

        This constructor creates a dictionary mapping segment types to their respective
        handler instances, initializing each handler with the provided syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components,
                           which will be passed to each handler.
        """
        self.__handlers: Dict[str, SegmentHandler] = {}
        self.__register_handlers(syntax_parser)

    def __register_handlers(self, syntax_parser: EdifactSyntaxHelper) -> None:
        """
        Initialize and register the handlers dictionary with instances of all segment handlers.
        """
        # Initialize handlers for each segment type
        self.__handlers = {
            SegmentType.UNA: UNASegmentHandler(syntax_parser),
            SegmentType.UNB: UNBSegmentHandler(syntax_parser),
            SegmentType.UNH: UNHSegmentHandler(syntax_parser),
            SegmentType.BGM: BGMSegmentHandler(syntax_parser),
            SegmentType.DTM: DTMSegmentHandler(syntax_parser),
            SegmentType.RFF: RFFSegmentHandler(syntax_parser),
            SegmentType.NAD: NADSegmentHandler(syntax_parser),
            SegmentType.CTA: CTASegmentHandler(syntax_parser),
            SegmentType.COM: COMSegmentHandler(syntax_parser),
            SegmentType.UNS: UNSSegmentHandler(syntax_parser),
            SegmentType.LOC: LOCSegmentHandler(syntax_parser),
            SegmentType.CCI: CCISegmentHandler(syntax_parser),
            SegmentType.LIN: LINSegmentHandler(syntax_parser),
            SegmentType.PIA: PIASegmentHandler(syntax_parser),
            SegmentType.QTY: QTYSegmentHandler(syntax_parser),
            SegmentType.STS: STSSegmentHandler(syntax_parser),
            SegmentType.UNT: UNTSegmentHandler(syntax_parser),
            SegmentType.UNZ: UNZSegmentHandler(syntax_parser),
            SegmentType.ERC: ERCSegmentHandler(syntax_parser),
            SegmentType.FTX: FTXSegmentHandler(syntax_parser),
        }

    def get_handler(self, segment_type: str) -> Optional[SegmentHandler]:
        """
        Get the handler for the specified segment type.

        Args:
            segment_type: The segment type to get a handler for.

        Returns:
            The handler for the segment type, or None if no handler is found.
        """
        handler = self.__handlers.get(segment_type)
        if not handler:
            logger.warning(f"Kein Handler für Segmenttyp '{segment_type}' definiert.")
        return handler
