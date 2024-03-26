import streamlit as st
from datetime import datetime

@st.cache(allow_output_mutation=True)
def get_tasks():
    return []

def add_task(task_list, new_task, label, description, deadline):
    if new_task.strip() != "":
        task_list.append({"task": new_task, "label": label, "description": description, "deadline": deadline, "done": False})
        st.success("Tarefa adicionada com sucesso!")
    else:
        st.warning("Por favor, insira uma tarefa válida.")

def delete_task(task_list, index):
    del task_list[index]
    st.success("Tarefa excluída com sucesso!")

def edit_task(task_list, index, updated_task, updated_label, updated_description, updated_deadline):
    task_list[index]["task"] = updated_task
    task_list[index]["label"] = updated_label
    task_list[index]["description"] = updated_description
    task_list[index]["deadline"] = updated_deadline
    st.success("Tarefa atualizada com sucesso!")

def toggle_task_status(task_list, index):
    task_list[index]["done"] = not task_list[index]["done"]
    if task_list[index]["done"]:
        st.success("Tarefa marcada como concluída!")
    else:
        st.info("Tarefa marcada como não concluída.")

def main():
    st.title("Gerenciador de Atividades")

    # Inicializar a lista de tarefas
    tasks = get_tasks()
    col1, col2 = st.columns([1, 1])
    with col1:
        # Expander para adicionar nova tarefa
        with st.expander("Adicionar Tarefa", expanded=False):
            col1, col2 = st.columns([1, 1])
            with col1:
                new_task = st.text_input("Atividade")
            with col2:
                deadline = st.date_input("Prazo:", format="DD/MM/YYYY")
    
            description = st.text_area("Descrição:")
            label = st.text_input("🔗 Link da atividade:")
            if st.button("`Adicionar`"):
                add_task(tasks, new_task, label, description, deadline)
    
    # Ordenar a lista de tarefas por data de prazo (em ordem decrescente)
    sorted_tasks = sorted(tasks, key=lambda x: x["deadline"], reverse=True)
    with col2:
        # Criar um expander para cada tarefa
        for idx, item in enumerate(sorted_tasks):
            task = item["task"]
            done = item["done"]
            label = item["label"]
            description = item["description"]
            deadline = item["deadline"]
            expander_title = f"Tarefa: {task} (Prazo: {deadline.strftime('%d/%m/%Y')})"
            with st.expander(expander_title, expanded=False):
                checkbox = st.checkbox(f"Concluído", key=idx, value=done)
                if checkbox:
                    toggle_task_status(sorted_tasks, idx)
    
                # Exibir informações da tarefa dentro do expander
                st.write(f"Link da atividade: {label}")
                st.write(f"Descrição: {description}")
    
                # Adicionar funcionalidade para editar e excluir tarefa
                col1, col2, col3, col4 = st.columns([0.15, 0.5, 0.15, 0.2])
                with col1:
                    if st.button("✏️", key=f"edit_{idx}"):
                        sorted_tasks[idx]["editing"] = True
                        sorted_tasks[idx]["edited_task"] = sorted_tasks[idx]["task"]
                        sorted_tasks[idx]["edited_label"] = sorted_tasks[idx]["label"]
                        sorted_tasks[idx]["edited_description"] = sorted_tasks[idx]["description"]
                        sorted_tasks[idx]["edited_deadline"] = sorted_tasks[idx]["deadline"]
                if "editing" in sorted_tasks[idx] and sorted_tasks[idx]["editing"]:
                    with col2:
                        edited_task = st.text_input("Editar Tarefa:", value=sorted_tasks[idx]["edited_task"])
                        edited_label = st.text_input("Editar Link da atividade:", value=sorted_tasks[idx]["edited_label"])
                        edited_description = st.text_area("Editar Descrição:", value=sorted_tasks[idx]["edited_description"])
                        edited_deadline = st.date_input("Editar Prazo:", value=datetime.strptime(str(sorted_tasks[idx]["edited_deadline"]), '%Y-%m-%d'), format="DD/MM/YYYY")
                    with col3:
                        if st.button("Salvar", key=f"save_{idx}"):
                            edit_task(sorted_tasks, idx, edited_task, edited_label, edited_description, edited_deadline)
                            sorted_tasks[idx]["editing"] = False
                else:
                    with col2:
                        pass  # Apenas para ajustar o layout
                with col4:
                    if st.button("❌", key=f"delete_{idx}"):
                        delete_task(tasks, idx)  # Remover a tarefa original
    
if __name__ == "__main__":
    main()
