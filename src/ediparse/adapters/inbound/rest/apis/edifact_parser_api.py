# coding: utf-8
"""
API routes for the EDIFACT parser.

This module defines the FastAPI router and endpoints for the EDIFACT parser API.
It provides routes for parsing EDIFACT messages (e.g., APERAK, MSCONS) from both
file uploads and string inputs, with options to download the parsed results or
return them directly in the response.

The API supports various EDIFACT message types used in the energy sector (DE/AT/CH)
and includes example request bodies to demonstrate the expected format.
"""

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from fastapi.openapi.models import Example

from ediparse.adapters.inbound.rest.apis.edifact_parser_api_base import BaseEDIFACTParserApi
import ediparse.adapters.inbound.rest.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from ediparse.adapters.inbound.rest.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictBool, StrictBytes, StrictStr
from typing import Any, Dict, Tuple, Union
from typing_extensions import Annotated


router = APIRouter()

ns_pkg = ediparse.adapters.inbound.rest.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/download-parsed-file",
    responses={
        201: {"model": object, "description": "Created"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["EDIFACT Parser"],
    summary="Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) from a file and download the result as a JSON file.",
    response_model_by_alias=True,
)
async def download_parsed_file(
    body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.")] = Body(None, description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.", media_type="application/octet-stream"),
) -> object:
    if not BaseEDIFACTParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEDIFACTParserApi.subclasses[0]().download_parsed_file(body)


@router.post(
    "/download-parsed-string",
    responses={
        201: {"model": object, "description": "Created"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["EDIFACT Parser"],
    summary="Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) in string format and download the result as a JSON file.",
    response_model_by_alias=True,
)
async def download_parsed_string_input(
    body: Annotated[
        StrictStr,
        Field(description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.")] = Body(
        None,
        description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.",
        media_type="text/plain",
        openapi_examples={
            "insert_your_data": Example(
                summary="Insert your data ...",
                description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.",
                value=""
            ),
            "mscons_sample": Example(
                summary="Sample of an EDIFACT-MSCONS message",
                description="The raw EDIFACT-MSCONS message in plain text format.",
                value="""UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678902:15+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
NAD+MS+9920455302123::293'
CTA+IC+:P GETTY'
COM+no-reply@example.com:EM'
NAD+MR+4012345678901::9'
UNS+D'
NAD+DP'
LOC+237+11XUENBSOLS----X+11XVNBSOLS-----X'
DTM+163:202102012300?+00:303'
DTM+164:202102022300?+00:303'
LIN+1'
PIA+5+1-1?:1.29.1:SRW'
QTY+220:4250.465:D54'
DTM+163:202101012300?+00:303'
DTM+164:202101312315?+00:303'
QTY+220:4250.465:D54'
DTM+163:202101312315?+00:303'
DTM+164:202101312320?+00:303'
UNT+2+1'
UNZ+1+ABC4711'"""
            ),
            "aperak_sample": Example(
                summary="Sample of an EDIFACT-APERAK message",
                description="The raw EDIFACT-APERAK message in plain text format.",
                value="""UNB+UNOC:3+9900204000002:500+4012345000023:500+210408:1010+121234567ABC7D'
UNH+1234EF66EF3QAJ+APERAK:D:07B:UN:2.1i'
BGM+313+AFBM5422'
DTM+137:202104081015?+00:303'
RFF+ACE:TG9523'
DTM+171:202104081015?+00:303'
RFF+AGO:12312'
DTM+171:202104081016?+00:303'
DTM+173:202104081017?+00:303'
RFF+TN:1'
NAD+MS+9900204000002::293'
CTA+IC+:Example Energiedatenmanagement'
COM+info@example.com:EM'
NAD+MR+4012345000023::293'
ERC+Z10'
FTX+ABO+++DE00056266802AO6G56M11SN51G21M24S:201204181115?+00?:303'
RFF+ACW:9878u7987gh7'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
RFF+AGO:798790034532'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
ERC+Z10'
RFF+ACW:9211574a24fa'
RFF+AGO:9211574a24fa'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
ERC+Z18'
RFF+TN:200815'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
RFF+Z08:4399901957459'
ERC+Z10'
RFF+ACW:123ABD931EF'
RFF+AGO:123ABD931EF'
ERC+Z20'
RFF+ACW:93AF1274CDQ'
RFF+AGO:93AF1274CDQ'
UNT+8+1234EF66EF3QAJ'
UNZ+1+121234567ABC7D'"""
            ),
        }
    ),
) -> object:
    if not BaseEDIFACTParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEDIFACTParserApi.subclasses[0]().download_parsed_string_input(body)


@router.post(
    "/parse-file",
    responses={
        200: {"model": object, "description": "OK"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["EDIFACT Parser"],
    summary="Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) from a file.",
    response_model_by_alias=True,
)
async def parse_file(
    limit_mode: Annotated[StrictBool, Field(description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.")] = Query(True, description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.", alias="limit_mode"),
    body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.")] = Body(None, description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.", media_type="application/octet-stream"),
) -> object:
    if not BaseEDIFACTParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEDIFACTParserApi.subclasses[0]().parse_file(limit_mode, body)


@router.post(
    "/parse-string",
    responses={
        200: {"model": object, "description": "OK"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    tags=["EDIFACT Parser"],
    summary="Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) given in string format.",
    response_model_by_alias=True,
)
async def parse_string_input(
    limit_mode: Annotated[StrictBool, Field(description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.")] = Query(True, description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.", alias="limit_mode"),
    body: Annotated[
        StrictStr,
        Field(description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.")] = Body(
        None,
        description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.",
        media_type="text/plain",
        openapi_examples={
            "insert_your_data": Example(
                summary="Insert your data ...",
                description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.",
                value=""
            ),
            "mscons_sample": Example(
                summary="Sample of an EDIFACT-MSCONS message",
                description="The raw EDIFACT-MSCONS message in plain text format.",
                value="""UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678902:15+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
NAD+MS+9920455302123::293'
CTA+IC+:P GETTY'
COM+no-reply@example.com:EM'
NAD+MR+4012345678901::9'
UNS+D'
NAD+DP'
LOC+237+11XUENBSOLS----X+11XVNBSOLS-----X'
DTM+163:202102012300?+00:303'
DTM+164:202102022300?+00:303'
LIN+1'
PIA+5+1-1?:1.29.1:SRW'
QTY+220:4250.465:D54'
DTM+163:202101012300?+00:303'
DTM+164:202101312315?+00:303'
QTY+220:4250.465:D54'
DTM+163:202101312315?+00:303'
DTM+164:202101312320?+00:303'
UNT+2+1'
UNZ+1+ABC4711'"""
            ),
            "aperak_sample": Example(
                summary="Sample of an EDIFACT-APERAK message",
                description="The raw EDIFACT-APERAK message in plain text format.",
                value="""UNB+UNOC:3+9900204000002:500+4012345000023:500+210408:1010+121234567ABC7D'
UNH+1234EF66EF3QAJ+APERAK:D:07B:UN:2.1i'
BGM+313+AFBM5422'
DTM+137:202104081015?+00:303'
RFF+ACE:TG9523'
DTM+171:202104081015?+00:303'
RFF+AGO:12312'
DTM+171:202104081016?+00:303'
DTM+173:202104081017?+00:303'
RFF+TN:1'
NAD+MS+9900204000002::293'
CTA+IC+:Example Energiedatenmanagement'
COM+info@example.com:EM'
NAD+MR+4012345000023::293'
ERC+Z10'
FTX+ABO+++DE00056266802AO6G56M11SN51G21M24S:201204181115?+00?:303'
RFF+ACW:9878u7987gh7'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
RFF+AGO:798790034532'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
ERC+Z10'
RFF+ACW:9211574a24fa'
RFF+AGO:9211574a24fa'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
ERC+Z18'
RFF+TN:200815'
FTX+AAO+++Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text'
FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
RFF+Z08:4399901957459'
ERC+Z10'
RFF+ACW:123ABD931EF'
RFF+AGO:123ABD931EF'
ERC+Z20'
RFF+ACW:93AF1274CDQ'
RFF+AGO:93AF1274CDQ'
UNT+8+1234EF66EF3QAJ'
UNZ+1+121234567ABC7D'"""
            ),
        }
    ),
) -> object:
    if not BaseEDIFACTParserApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEDIFACTParserApi.subclasses[0]().parse_string_input(limit_mode, body)
