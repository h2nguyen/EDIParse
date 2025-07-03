# coding: utf-8
"""
Package for EDIFACT segment handlers.

This package contains handler classes that process EDIFACT segments during parsing.
Each handler is specialized for a specific segment type (e.g., DTM, BGM, NAD) and is
responsible for updating the parsing context with the information extracted from
that segment.

The handlers follow a common pattern defined by the SegmentHandler base class,
which provides a consistent interface for all segment types. The SegmentHandlerFactory
is used to create and manage the appropriate handler for each segment type.
"""

from .segment_handler import SegmentHandler
from .segment_handler_factory import SegmentHandlerFactory
from .bgm_segment_handler import BGMSegmentHandler
from .cci_segment_handler import CCISegmentHandler
from .com_segment_handler import COMSegmentHandler
from .cta_segment_handler import CTASegmentHandler
from .dtm_segment_handler import DTMSegmentHandler
from .erc_segment_handler import ERCSegmentHandler
from .ftx_segment_handler import FTXSegmentHandler
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
