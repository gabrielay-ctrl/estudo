import requests

ADVICE_API_URL = "https://api.adviceslip.com/advice"

def get_motivational_advice() -> str:
    """
    Busca um conselho motivacional na Advice Slip API pública.
    Em caso de falha de conexão ou erro, retorna uma mensagem padrão
    para não quebrar a aplicação principal.
    """
    try:
        response = requests.get(ADVICE_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("slip", {}).get("advice", "Continue avançando um passo de cada vez!")
    except (requests.RequestException, ValueError):
        # Fallback silencioso para não interromper a UX do usuário
        return "Lembre-se: avance 1% de cada vez. Beba água!"
