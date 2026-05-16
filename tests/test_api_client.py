from unittest.mock import patch
from requests.exceptions import RequestException

from app import get_motivational_advice


def test_get_motivational_advice_success():
    """Teste de integração com mock: sucesso na requisição da API."""
    mock_response_data = {"slip": {"advice": "Mocked motivational advice!"}}

    with patch("app.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        advice = get_motivational_advice()

        mock_get.assert_called_once_with(
            "https://api.adviceslip.com/advice", timeout=5
        )
        assert advice == "Mocked motivational advice!"


def test_get_motivational_advice_failure():
    """Teste de integração com mock: falha na requisição (timeout/offline)."""
    with patch("app.requests.get") as mock_get:
        mock_get.side_effect = RequestException("Timeout")

        advice = get_motivational_advice()

        assert advice == "Lembre-se: avance 1% de cada vez. Beba água!"
