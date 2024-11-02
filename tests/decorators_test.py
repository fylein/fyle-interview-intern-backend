import pytest
import json
from flask import Flask, request
from core.apis.decorators import authenticate_principal
from core.libs.exceptions import FyleError


@authenticate_principal
def mock_endpoint(principal):
    return "Authorized", 200


@pytest.mark.parametrize(
    "path, headers",
    [
        (
            "/invalid_path",
            {"X-Principal": json.dumps({"user_id": 1, "principal_id": 2})},
        ),
    ],
)
def test_authenticate_principal_no_such_api(mocker, path, headers):

    app = Flask(__name__)
    with app.test_request_context(path=path, headers=headers):
        mock_assert_found = mocker.patch(
            "core.libs.assertions.assert_found",
            side_effect=FyleError("No such api", 404),
        )  # Mocking the assert_found function called in authenticate_principal when no such api is found

        with pytest.raises(
            FyleError
        ):  # Handling the exception raised by the mock_assert_found function
            mock_endpoint()

        mock_assert_found.assert_called_once_with(None, "No such api")
