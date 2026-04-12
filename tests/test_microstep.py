import os
import pytest
from src.microstep import MindStepManager

# Arquivo JSON temporário para testes
TEST_FILE = "test_mindstep_data.json"

@pytest.fixture
def manager():
    # Setup
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    mgr = MindStepManager(data_file=TEST_FILE)
    yield mgr
    # Teardown
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_create_task_success(manager):
    """Teste de caminho feliz: cadastrar tarefa com 3 passos."""
    task = manager.create_task("Estudar Matemática", ["Ler capítulo 1", "Fazer 5 exercícios", "Beber água"])
    assert task["title"] == "Estudar Matemática"
    assert len(task["steps"]) == 3
    assert not task["completed"]
    assert len(manager.get_all_tasks()) == 1

def test_create_task_invalid_steps(manager):
    """Teste de caso inválido: tentar criar com menos de 3 passos."""
    with pytest.raises(ValueError, match="Paralisia de análise"):
        manager.create_task("Limpar o quarto", ["Tirar o lixo"])
        
def test_create_task_empty_title(manager):
    """Teste de caso inválido: tentar criar com título vazio."""
    with pytest.raises(ValueError, match="título"):
        manager.create_task("", ["Passo 1", "Passo 2", "Passo 3"])

def test_complete_micro_step_and_task(manager):
    """Teste de caso limite/sucesso: marcar passos e checar conclusão total."""
    manager.create_task("Lavar louça", ["Pegar esponja", "Lavar pratos", "Lamber os beiços (brincadeira)"])
    
    # Conclui primeiro passo
    t = manager.complete_micro_step(1, 0)
    assert t["steps"][0]["completed"] is True
    assert t["completed"] is False
    
    # Conclui os demais
    manager.complete_micro_step(1, 1)
    t_final = manager.complete_micro_step(1, 2)
    
    # Ao concluir o último, a tarefa principal deve ser dada como concluída
    assert t_final["completed"] is True

def test_complete_invalid_step(manager):
    """Teste de erro: marcar um passo que não existe."""
    manager.create_task("Estudar Matemática", ["Ler capítulo 1", "Fazer 5 exercícios", "Beber água"])
    with pytest.raises(IndexError, match="Micro-passo não enc"):
        manager.complete_micro_step(1, 99)
