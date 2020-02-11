from mock import Mock, patch
from nose.tools import assert_equal
import geckoboard

API_KEY = 'ABC'
ERROR_MESSAGE = 'Whoops!'
TIMEOUT = 50


@patch('geckoboard.api.get')
def test_makes_api_call(mock_api_get):
    mock_api_get.return_value = Mock(status_code=200)
    client = geckoboard.client(API_KEY, timeout=TIMEOUT)

    client.ping()

    mock_api_get.assert_called_with('/', API_KEY, TIMEOUT)


@patch('geckoboard.api.get')
def test_returns_true_on_success(mock_api_get):
    mock_api_get.return_value = Mock(status_code=200)
    client = geckoboard.client(API_KEY)

    response = client.ping()

    assert_equal(response, True)


@patch('geckoboard.api.get')
@patch('geckoboard.response_handler.get_error_message')
def test_rethrows_api_error(mock_get_error_message, mock_api_get):
    mock_response = Mock(status_code=401)
    mock_api_get.return_value = mock_response
    mock_get_error_message.return_value = ERROR_MESSAGE
    client = geckoboard.client(API_KEY)

    try:
        client.ping()
    except Exception as err:
        mock_get_error_message.assert_called_with(mock_response)
        assert_equal(err.message, ERROR_MESSAGE)
