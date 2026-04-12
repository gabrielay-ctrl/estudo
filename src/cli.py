import argparse
from src.microstep import MindStepManager

def show_tasks(manager: MindStepManager):
    tasks = manager.get_all_tasks()
    if not tasks:
        print("\n[!] Nenhuma tarefa cadastrada no MindStep ainda.\n")
        return

    print("\n=== Suas Tarefas Atuais ===")
    for t in tasks:
        status = "[CONCLUÍDO] " if t["completed"] else "[EM ANDAMENTO]"
        print(f"\nID: {t['id']} | {t['title']} {status}")
        for idx, step in enumerate(t["steps"]):
            step_status = "[x]" if step["completed"] else "[ ]"
            print(f"   {idx}. {step_status} {step['name']}")
    print("===========================\n")

def main():
    parser = argparse.ArgumentParser(description="MindStep Tracker - Fatie suas tarefas para evitar a paralisia.")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando: list
    subparsers.add_parser("list", help="Lista todas as suas tarefas e micro-passos.")

    # Comando: add
    parser_add = subparsers.add_parser("add", help="Adiciona uma nova tarefa.")
    parser_add.add_argument("title", type=str, help="Título da tarefa principal")
    parser_add.add_argument("-s", "--steps", nargs="+", required=True, help="Lista de micro-passos separados por espaço (min 3)")

    # Comando: complete
    parser_complete = subparsers.add_parser("complete", help="Conclui um micro-passo.")
    parser_complete.add_argument("task_id", type=int, help="ID da tarefa principal")
    parser_complete.add_argument("step_id", type=int, help="Índice do micro-passo (começa em 0)")

    args = parser.parse_args()
    manager = MindStepManager()

    if args.command == "list":
        show_tasks(manager)

    elif args.command == "add":
        try:
            manager.create_task(args.title, args.steps)
            print(f"\n[+] Tarefa '{args.title}' adicionada com sucesso com {len(args.steps)} micro-passos!")
            print("Lembre-se: avance 1% de cada vez. Beba água!\n")
        except ValueError as e:
            print(f"\n[ERRO] {e}\n")

    elif args.command == "complete":
        try:
            task = manager.complete_micro_step(args.task_id, args.step_id)
            print(f"\n[+] Muito bem! Micro-passo {args.step_id} da tarefa {args.task_id} concluído.")
            if task["completed"]:
                print("🎉 PARABÉNS! Você conseguiu terminar a tarefa inteira! 🎉")
            print("")
        except (KeyError, IndexError) as e:
            print(f"\n[ERRO] {e}\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
