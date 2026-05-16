# MindStep Tracker

Aplicacao web para auxiliar pessoas neurodivergentes a vencer a paralisia de tarefas,
quebrando atividades em micro-passos gerenciaveis.

**Deploy:** https://estudo-bkp5.vercel.app

## Tecnologias

- Python 3.12 / FastAPI / Uvicorn
- API publica: [AdviceSlip](https://api.adviceslip.com/)
- Testes: Pytest
- CI/CD: GitHub Actions + Ruff
- Deploy: Vercel

## Como executar localmente

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Acesse: http://localhost:8000

## Como rodar os testes

```bash
pytest tests/
```

## Estrutura

| Arquivo | Descricao |
|---|---|
| `app.py` | Aplicacao principal (FastAPI + HTML + logica de negocios) |
| `requirements.txt` | Dependencias Python |
| `vercel.json` | Configuracao de deploy na Vercel |
| `tests/test_api_client.py` | Testes de integracao da API AdviceSlip |
| `.github/workflows/ci.yml` | Pipeline CI automatizado |

## Autor

Gabriela Yasmin Conceicao Viana - RA 22505273
