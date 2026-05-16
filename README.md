# MindStep Tracker 

![Status do Build](https://github.com/gabrielay-ctrl/estudo/actions/workflows/ci.yml/badge.svg)

**MindStep Tracker** é uma aplicação em Linha de Comando (CLI) desenvolvida em Python para apoiar pessoas neurodivergentes e/ou que enfrentam Transtorno do Déficit de Atenção com Hiperatividade (TDAH) e Ansiedade.

 entrega-intermediaria
## 🚀 Aplicação Online (Deploy Público - Entrega Intermediária)
Acesse a aplicação web completa com interface interativa:
👉 **[Link Vercel]** (Em breve - Deploy via Vercel)

## O Problema Real
=======
##  O Problema Real
main
Imagine o seguinte cenário: **Júlia** é uma universitária com diagnóstico de TDAH e Transtorno de Ansiedade Generalizada. Durante as semanas de provas, ela frequentemente sofre crises de paralisia de tarefas. Diante do item "Estudar Física", tudo parece muito grande, complexo e inatingível. A ansiedade toma conta, e, devido ao estresse e esquecimento gerados pelas crises, ela frequentemente se esquece até do autocuidado primário, como beber água ou tomar seus medicamentos durante longos períodos de estudo.

A principal dor aqui é a **Paralisia por Análise e Sobrecarga Cognitiva**, onde grandes tarefas geram não apenas a procrastinação evasiva, mas danos paralelos ao esquecer hábitos fundamentais.

## A Proposta de Solução
O MindStep atua como um facilitador de foco e fatiamento de tarefas. Quando Júlia tenta cadastrar algo como "Estudar Física", o CLI **obriga** a quebra da tarefa em pelo menos 3 "micro-passos" (ex: "Ler o sumário", "Beber um copo d'água", "Fazer 2 exercícios"). 
Isso ameniza a paralisia, promove ancoragem atencional e recompensa passos muito curtos.

entrega-intermediaria
##  Público-Alvo
=======
## Público-Alvo
 main
- Estudantes neurodivergentes (ADHD/TDAH e Autistas).
- Pessoas sofrendo de crises agudas de ansiedade que atrapalhem as atividades do dia a dia.
- Qualquer usuário enfrentando episódios de "task paralysis" e esquecimento devido à sobrecarga.

## Funcionalidades Principais
1. **Quebra obrigatória:** Não é possível adicionar uma tarefa grande sem minimamente fatiá-la em 3 passos menores.
2. **Sistema de recompensas e API Externa:** Ajuda a nutrir a sensação de "1% de progresso". O sistema está integrado com a **Advice Slip API**, provendo conselhos motivacionais dinâmicos a cada passo concluído.
3. **Persistência leve de dados:** Tudo fica salvo localmente em `mindstep_data.json` - não requer internet nem login complexo.

##Tecnologias Utilizadas
- **Python 3.12+** (Linguagem pura / Base de Código)
- **Pytest** (Automático: Caminho feliz, Regras de quebra, Exceções)
- **Ruff** (Linting / Análise Estática de Código)
- **GitHub Actions** (Workflow de CI - Integração Contínua)
- **Versão Semântica** declarada no arquivo `VERSION` (1.0.0)

## Instruções de Instalação e Execução

### Pré-requisitos
- Ter o Python 3 instalado no computador (versão 3.8+ recomendada)
- Git para clonar o repositório

### Passo 1: Clone o Repositório
Abra o seu terminal e rode:
```bash
git clone https://github.com/gabrielay-ctrl/estudo.git
cd estudo
```

### Passo 2: Configure o Ambiente de Python (Opcional, mas recomendado)
Você pode rodar a aplicação pura apenas com Python, mas para instalar a suíte de testes e linting, defina seu ambiente:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Passo 3: Instale as Dependências Formais
```bash
pip install -r requirements.txt
```

### Passo 4: Como Executar a Interface Web (Nova Versão)
O projeto agora possui uma interface Web moderna utilizando **FastAPI**. Para iniciar o servidor local:

```bash
uvicorn app:app --reload
```
Acesse no seu navegador: `http://localhost:8000`

### Como usar o antigo CLI:
O núcleo CLI continua disponível em `src/cli.py`.
**1. Adicionando:** `python -m src.cli add "Estudar Quimica" -s "Passo 1" "Passo 2" "Passo 3"`
**2. Listando:** `python -m src.cli list`
**3. Concluindo:** `python -m src.cli complete 1 0`

---

## Testes Automatizados e Qualidade

O projeto conta com CI contínuo através da plataforma *GitHub Actions* configurada no arquivo `.github/workflows/ci.yml`.

### Como rodar os Testes Manualmente?
No terminal, digite:
```bash
pytest tests/
```
Isso validará o comportamento esperado: checará sucesso, tratará entradas vazias e certificará que as tarefas falham em ser salvas sem os 3 micro-passos.

### Como rodar o Linting localmente?
Utilizamos a análise estática mais rápida do Python atualmente (Ruff).
Para checar padrões, digite:
```bash
ruff check .
```

---

**Autor:** Gabriela
**Licença:** MIT
**Versão Atual:** Veja o arquivo `VERSION` (Atualmente: v1.0.0)
