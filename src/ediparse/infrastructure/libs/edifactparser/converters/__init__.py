# coding: utf-8
"""
Package for EDIFACT segment converters.

This package contains __converter classes that transform raw EDIFACT segment data
into structured domain model objects. Each __converter is specialized for a specific
segment type (e.g., DTM, BGM, NAD) and handles the parsing and conversion of that
segment's components according to the EDIFACT standard.

The converters follow a common pattern defined by the SegmentConverter base class,
which provides exception handling and a consistent interface for all segment types.
"""

from .segment_converter import SegmentConverter
from .bgm_segment_converter import BGMSegmentConverter
from .cci_segment_converter import CCISegmentConverter
from .com_segment_converter import COMSegmentConverter
from .cta_segment_converter import CTASegmentConverter
from .dtm_segment_converter import DTMSegmentConverter
from .erc_segment_converter import ERCSegmentConverter
from .ftx_segment_converter import FTXSegmentConverter
from .lin_segment_converter import LINSegmentConverter
from .loc_segment_converter import LOCSegmentConverter
from .nad_segment_converter import NADSegmentConverter
from .pia_segment_converter import PIASegmentConverter
from .qty_segment_converter import QTYSegmentConverter
from .rff_segment_converter import RFFSegmentConverter
from .sts_segment_converter import STSSegmentConverter
from .una_segment_converter import UNASegmentConverter
from .unb_segment_converter import UNBSegmentConverter
from .unh_segment_converter import UNHSegmentConverter
from .uns_segment_converter import UNSSegmentConverter
from .unt_segment_converter import UNTSegmentConverter
from .unz_segment_converter import UNZSegmentConverter
