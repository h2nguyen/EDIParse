# coding: utf-8
"""
Implementation of the EDIFACT parser API endpoints.

This module provides the concrete implementation of the EDIFACT parser API
endpoints defined in the apis package. It handles parsing of EDIFACT-specific
messages (e.g., APERAK, MSCONS) from both file uploads and string inputs,
with options to download the parsed results or return them directly in the response.

The implementation uses the ParserService from the application layer to perform
the actual parsing, and handles error cases, file content extraction, and
response formatting.
"""

import logging
import time
import uuid
from typing import Union, Tuple

from starlette.concurrency import run_in_threadpool
from typing_extensions import Annotated

from fastapi import status
from pydantic import StrictStr, Field, StrictBool, StrictBytes
from starlette.responses import JSONResponse

from ediparse.adapters.inbound.rest.apis.edifact_parser_api_base import BaseEDIFACTParserApi
from ediparse.libs.edifactparser.exceptions import CONTRLException, EdifactParserException
from ediparse.application.services import ParserService

logger = logging.getLogger(__name__)

MAX_LINES_TO_PARSE = 2442
UNLIMITED_LINES_TO_PARSE_INDICATOR = -1


class ParseEdifactMessageRouter(BaseEDIFACTParserApi):
    """
    Router class for handling EDIFACT-specific message parsing requests.

    This class implements the API for parsing EDIFACT-specific messages,
    providing an HTTP interface to the parsing functionality. It supports
    parsing raw EDIFACT-specific messages as text or from uploaded files, with options
    to limit the number of lines parsed and to download the results as JSON files.
    """

    def __init__(
            self,
            parser_service: ParserService = None,
    ):
        """
        Initialize the ParseEdifactMessageRouter with a parser service.

        Args:
            parser_service (ParserService): The parser service to use.
                If None, a new ParserService instance will be created.
        """
        self.__parser_service = parser_service or ParserService()

    async def parse_string_input(
            self,
            limit_mode: Annotated[StrictBool, Field(
                description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.")],
            body: Annotated[StrictStr, Field(
                description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.")],
    ) -> JSONResponse:
        """
        Parse a raw EDIFACT-specific message and return the result as JSON.

        This endpoint accepts a raw EDIFACT-specific message string and returns
        the parsed data in a structured JSON format.

        Args:
            limit_mode (bool): If true, limits parsing to a maximum of 2442 lines;
                if false, parses the entire message regardless of size
            body (str): The raw EDIFACT-specific message to parse

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200 - Success)
                or an error message (status 400 - Bad request)
        """
        try:
            parsed_obj = await self.__get_parsed_result(body=body, limit_mode=limit_mode)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except EdifactParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_obj.model_dump())

    async def parse_file(
        self,
        limit_mode: Annotated[StrictBool, Field(
            description="If set to true, enables a parsing limit for the maximum number of lines. By default, the limit is 2442 lines.")],
        body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(
            description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.")],
    ) -> JSONResponse:
        """
        Parse a raw EDIFACT-specific message from a file and return the result as JSON.

        This endpoint accepts an uploaded file containing a raw EDIFACT-specific message
        and returns the parsed data in a structured JSON format. The method handles
        different file content formats and converts bytes to strings, attempting UTF-8
        decoding first and falling back to ISO-8859-1 if UTF-8 decoding fails.

        Args:
            limit_mode (bool): If true, limits parsing to a maximum of 2442 lines;
                if false, parses the entire message regardless of size
            body (str | dict[str, bytes]): The uploaded file containing the raw EDIFACT-specific message,
                which may be a tuple or direct file content in various formats

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200 - Success)
                or an error message (status 400 - Bad request)
        """
        if not body:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": "No file provided"})

        try:
            file_content = await self.__get_file_content(body)
            parsed_obj = await self.__get_parsed_result(body=file_content, limit_mode=limit_mode)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except EdifactParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_obj.model_dump())

    async def download_parsed_string_input(
        self,
        body: Annotated[StrictStr, Field(description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) in plain text format.")],
    ) -> JSONResponse:
        """
        Parse a raw EDIFACT-specific message and return the result as a downloadable JSON file.

        This endpoint accepts a raw EDIFACT-specific message string and returns
        the parsed data as a downloadable JSON file. Unlike `parse_string_input(...)`,
        this method always parses the entire message without line limits and sets
        appropriate headers for file download.

        Args:
            body (str): The raw EDIFACT-specific message to parse

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 201 - Created)
                or an error message (status 400 - Bad request), with headers set for file download
                including a timestamp in the filename
        """
        try:
            parsed_obj = await self.__get_parsed_result(body=body, limit_mode=False)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except EdifactParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=parsed_obj.model_dump(),
            headers={"Content-Disposition": f"attachment; filename=edifact_message_parsed_{timestamp}.json"}
        )

    async def download_parsed_file(
        self,
        body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(
            description="The raw EDIFACT-specific message (e.g., APERAK, MSCONS, etc.) provided as a file.")],
    ) -> JSONResponse:
        """
        Parse a raw EDIFACT-specific message from a file and return the result as a downloadable JSON file.

        This endpoint accepts an uploaded file containing a raw EDIFACT-specific message
        and returns the parsed data as a downloadable JSON file. The method handles
        different file content formats, converts bytes to strings (attempting UTF-8
        decoding first and falling back to ISO-8859-1 if UTF-8 decoding fails),
        and always parses the entire message without line limits.

        Args:
            body (str | dict[str, bytes]): The uploaded file containing the raw EDIFACT-specific message,
                which may be a tuple or direct file content in various formats

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 201 - Created)
                or an error message (status 400 - Bad request), with headers set for file download
                including a timestamp in the filename
        """
        if not body:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": "No file provided"})

        try:
            file_content = await self.__get_file_content(body)
            parsed_obj = await self.__get_parsed_result(body=file_content, limit_mode=False)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except EdifactParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=parsed_obj.model_dump(),
            headers={"Content-Disposition": f"attachment; filename=edifact_message_parsed_{timestamp}.json"}
        )

    async def __get_parsed_result(self, body: str, limit_mode: bool) -> object:
        max_lines_to_parse = MAX_LINES_TO_PARSE if limit_mode else UNLIMITED_LINES_TO_PARSE_INDICATOR
        job_id = uuid.uuid4()
        logger.info(f"Parsing process triggered for job ID: {job_id} ...")
        t1 = time.perf_counter()
        parsed_obj = await run_in_threadpool(
            self.__parser_service.parse_message,
            message_content=body,
            max_lines_to_parse=max_lines_to_parse
        )
        t2 = time.perf_counter()
        logger.info(f"SPEED-TEST: Parsing took {(t2 - t1):2.2f}s for job ID: {job_id} ...")
        return parsed_obj

    @staticmethod
    async def __get_file_content(body):
        # If body is None or empty, return empty string
        if not body:
            return ""

        # Handle FastAPI's UploadFile format
        if hasattr(body, "file"):
            return await body.read()

        # Handle case when body is a tuple (filename, file content) from FastAPI file upload
        if isinstance(body, tuple) and len(body) >= 2:
            # Extract the file content from the tuple
            file_content = body[1]
            if hasattr(file_content, "read"):
                # If it's a file-like object, read its content
                return file_content.read()
            return file_content

        # Handle case when body is a dictionary from FastAPI file upload
        if isinstance(body, dict) and "file" in body:
            file_content = body["file"]
            if isinstance(file_content, tuple) and len(file_content) >= 2:
                # If it's a tuple (filename, file content), extract the file content
                file_content = file_content[1]
            if hasattr(file_content, "read"):
                # If it's a file-like object, read its content
                return file_content.read()
            return file_content

        # If body is already a string, return it as is
        if isinstance(body, str):
            return body

        # If body is bytes, decode it
        if isinstance(body, bytes):
            try:
                return body.decode('utf-8')
            except UnicodeDecodeError:
                # Fall back to ISO-8859-1 (Latin-1) which is a common encoding for EDIFACT files
                # and can handle all byte values from 0x00 to 0xFF
                return body.decode('iso-8859-1')

        # If we get here, we don't know how to handle the body
        logger.warning(f"Unknown body type: {type(body)}")
        return str(body)
