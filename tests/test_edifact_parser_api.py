# coding: utf-8
import os
import json

from pathlib import Path
from fastapi.testclient import TestClient
from pydantic import Field, StrictBool, StrictBytes, StrictStr  # noqa: F401
from typing import Any, Dict, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401

# Define paths for test files
SAMPLE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "tests" / "samples"
APERAK_SAMPLE_FILE_PATH_REQUEST = SAMPLE_DIR / "aperak-message-example-request.txt"
APERAK_SAMPLE_FILE_PATH_RESPONSE = SAMPLE_DIR / "aperak-message-example-response.json"
MSCONS_SAMPLE_FILE_PATH_REQUEST = SAMPLE_DIR / "mscons-message-example-request.txt"
MSCONS_SAMPLE_FILE_PATH_RESPONSE = SAMPLE_DIR / "mscons-message-example-response.json"

def test_parse_string_input_for_aperak(client: TestClient):
    """Test case for parse_string_input

    Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) given in string format.
    """
    # Read the request from the TXT file
    request_file_path = APERAK_SAMPLE_FILE_PATH_REQUEST
    with open(request_file_path, "r") as f:
        request_input = f.read()

    # Read the expected response from the JSON file
    response_file_path = APERAK_SAMPLE_FILE_PATH_RESPONSE
    with open(response_file_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with plain text
    response = client.post(
        "/parse-string",
        content=request_input,
        headers={"Content-Type": "text/plain"},
        params={"limit_mode": True}
    )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response matches the expected JSON
    assert response.json() == expected_response

def test_parse_string_input_for_mscons(client: TestClient):
    """Test case for parse_string_input

    Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) given in string format.
    """
    # Read the request from the TXT file
    request_file_path = MSCONS_SAMPLE_FILE_PATH_REQUEST
    with open(request_file_path, "r") as f:
        request_input = f.read()

    # Read the expected response from the JSON file
    response_file_path = MSCONS_SAMPLE_FILE_PATH_RESPONSE
    with open(response_file_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with plain text
    response = client.post(
        "/parse-string",
        content=request_input,
        headers={"Content-Type": "text/plain"},
        params={"limit_mode": True}
    )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response matches the expected JSON
    assert response.json() == expected_response

def test_parse_file(client: TestClient):
    """Test case for parse_file

    Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) from a file.
    """
    # Read the request from the TXT file
    request_file_path = APERAK_SAMPLE_FILE_PATH_REQUEST

    # Read the expected response from the JSON file
    response_file_path = APERAK_SAMPLE_FILE_PATH_RESPONSE
    with open(response_file_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with file upload
    with open(request_file_path, "rb") as f:
        files = {"file": ("aperak-message-example.txt", f, "application/octet-stream")}
        response = client.post(
            "/parse-file",
            files=files,
            params={"limit_mode": True}
        )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response matches the expected JSON
    assert response.json() == expected_response

def test_download_parsed_string_input(client: TestClient):
    """Test case for download_parsed_string_input

    Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) in string format and download the result as a JSON file.
    """
    # Read the request from the TXT file
    request_file_path = MSCONS_SAMPLE_FILE_PATH_REQUEST
    with open(request_file_path, "r") as f:
        request_input = f.read()

    # Read the expected response from the JSON file
    response_file_path = MSCONS_SAMPLE_FILE_PATH_RESPONSE
    with open(response_file_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with plain text
    response = client.post(
        "/download-parsed-string",
        content=request_input,
        headers={"Content-Type": "text/plain"}
    )

    # Check that the response status code is 201
    assert response.status_code == 201

    # Check that the response has the Content-Disposition header
    assert "Content-Disposition" in response.headers
    assert "attachment; filename=" in response.headers["Content-Disposition"]

    # Check that the response matches the expected JSON
    assert response.json() == expected_response


def test_download_parsed_file(client: TestClient):
    """Test case for download_parsed_file

    Trigger the process to parse the provided EDIFACT messages (e.g., APERAK, MSCONS, etc.) from a file and download the result as a JSON file.
    """
    # Read the request from the TXT file
    request_file_path = APERAK_SAMPLE_FILE_PATH_REQUEST

    # Read the expected response from the JSON file
    response_file_path = APERAK_SAMPLE_FILE_PATH_RESPONSE
    with open(response_file_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with file upload
    with open(request_file_path, "rb") as f:
        files = {"file": ("aperak-message-example.txt", f, "application/octet-stream")}
        response = client.post(
            "/download-parsed-file",
            files=files
        )

    # Check that the response status code is 201
    assert response.status_code == 201

    # Check that the response has the Content-Disposition header
    assert "Content-Disposition" in response.headers
    assert "attachment; filename=" in response.headers["Content-Disposition"]

    # Check that the response matches the expected JSON
    assert response.json() == expected_response
