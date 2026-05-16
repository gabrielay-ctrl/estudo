
from unittest.mock import patch
from requests.exceptions import RequestException

from src.api_client import get_motivational_advice

def test_get_motivational_advice_success():
    """Teste de integração com mock: sucesso na requisição da API."""
    mock_response_data = {"slip": {"advice": "Mocked motivational advice!"}}
    
    with patch('src.api_client.requests.get') as mock_get:
        # Configura o mock para simular uma resposta de sucesso
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data
        
        advice = get_motivational_advice()
        
        # Verifica se o endpoint correto foi chamado e o retorno esperado
        mock_get.assert_called_once_with("https://api.adviceslip.com/advice", timeout=5)
        assert advice == "Mocked motivational advice!"

def test_get_motivational_advice_failure():
    """Teste de integração com mock: falha na requisição (timeout/offline)."""
    with patch('src.api_client.requests.get') as mock_get:
        # Simula uma exceção de conexão
        mock_get.side_effect = RequestException("Timeout")
        
        advice = get_motivational_advice()
        
        # Garante que o fallback silencioso (mensagem padrão) seja ativado
        assert advice == "Lembre-se: avance 1% de cada vez. Beba água!"
