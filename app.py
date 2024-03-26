import streamlit as st
from datetime import datetime, timedelta

def get_tasks():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    return st.session_state.tasks

st.set_page_config(
    page_title="Hagliberto", 
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "`Página inicial:`🌍 https://hagliberto.streamlit.app/"}  
)

# Definindo o estilo CSS para o rodapé
footer_style = """
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #f0f0f0;
color: #333;
text-align: center;
padding: 10px 0;
"""

# Adicionando o rodapé com o texto "Hagliberto Alves de Oliveira"
st.markdown(
    """
    <div style='"""+ footer_style +"""'>
        👨🏻‍💻 Hagliberto Alves de Oliveira ®️
    </div>
    """,
    unsafe_allow_html=True
)


def get_tasks():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    return st.session_state.tasks

def add_task(new_task, label, description, deadline):
    tasks = get_tasks()
    if new_task.strip() != "":
        tasks.append({"task": new_task, "label": label, "description": description, "deadline": deadline, "done": False})
        st.session_state.tasks = tasks
        st.success("Tarefa adicionada com sucesso!")
        st.rerun()  # Recarrega a página após adicionar a tarefa
    else:
        st.warning("Por favor, insira uma tarefa válida.")

def delete_task(index):
    tasks = get_tasks()
    del tasks[index]
    st.session_state.tasks = tasks
    st.success("Tarefa excluída com sucesso!")
    st.rerun()  # Recarrega a página após excluir a tarefa

def edit_task(index, updated_task, updated_label, updated_description, updated_deadline):
    tasks = get_tasks()
    tasks[index]["task"] = updated_task
    tasks[index]["label"] = updated_label
    tasks[index]["description"] = updated_description
    tasks[index]["deadline"] = updated_deadline
    st.session_state.tasks = tasks
    st.success("Tarefa atualizada com sucesso!")
    st.rerun()  # Recarrega a página após editar a tarefa

def toggle_task_status(index):
    tasks = get_tasks()
    tasks[index]["done"] = not tasks[index]["done"]
    st.session_state.tasks = tasks
    if tasks[index]["done"]:
        st.success("Tarefa marcada como concluída!")
    else:
        st.info("Tarefa marcada como não concluída.")
    st.rerun()  # Recarrega a página após alterar o status da tarefa

def main():
    # Adicionar funcionalidade para editar e excluir tarefa
    col1, col2= st.columns([1, 1])
                  
    with col1:
        st.success("Crie tarefas")
        # Expander para adicionar nova tarefa
        with st.expander("Adicionar Tarefa", expanded=False):
            col3, col4= st.columns([1, 2])
            with col3: 
                new_task = st.text_input("Atividade", key="new_task")
                deadline = st.date_input("Prazo:", format="DD/MM/YYYY", key="new_deadline")

            with col4: 
                description = st.text_area("Descrição:", key="new_description")
            label = st.text_input("🔗 Link da atividade:", key="new_label")
            if st.button("`Adicionar`"):
                add_task(new_task, label, description, deadline)
        
    with col2:    
        st.info("Realize operações com as tarefas criadas")
        # Ordenar a lista de tarefas por data de prazo (em ordem decrescente)
        sorted_tasks = sorted(get_tasks(), key=lambda x: x["deadline"], reverse=True)
        
    
        # Criar um expander para cada tarefa
        for idx, item in enumerate(sorted_tasks):
            task = item["task"]
            done = item["done"]
            label = item["label"]
            description = item["description"]
            deadline = item["deadline"]
            expander_title = f"Tarefa: {task} (Prazo para realizar: {deadline.strftime('%d/%m/%Y')})"
            with st.expander(expander_title, expanded=False
):
                checkbox = st.checkbox(f"`Concluído` {task}", value=done, key=f"checkbox_{idx}")
                if checkbox:
                    toggle_task_status(idx)
    
                # Exibir informações da tarefa dentro do expander
                st.write(f"`Link da atividade`: {label}")
                st.write(f"🔜 `Descrição`: {description}")
    
                # Adicionar funcionalidade para editar e excluir tarefa
                col1, col2, col3, col4 = st.columns([0.5, 0.15, 0.15, 0.15])
                  
                with col2:
                    if st.button("✏️ `Editar`", key=f"edit_{idx}_{task}"):  # Alterada a chave aqui
                        item["editing"] = True
                        item["edited_task"] = task
                        item["edited_label"] = label
                        item["edited_description"] = description
                        item["edited_deadline"] = deadline
                if "editing" in item and item["editing"]:
                    with col1:
                        edited_task = st.text_input("Editar Tarefa:", value=item["edited_task"], key=f"edited_task_{idx}")
                        edited_label = st.text_input("Editar Link da atividade:", value=item["edited_label"], key=f"edited_label_{idx}")
                        edited_description = st.text_area("Editar Descrição:", value=item["edited_description"], key=f"edited_description_{idx}")
                        edited_deadline = st.date_input("Editar Prazo:", value=item["edited_deadline"], format="DD/MM/YYYY", key=f"edited_deadline_{idx}")
                    with col3:
                        if st.button("🆙 `Salvar`", key=f"save_{idx}"):
                            edit_task(idx, edited_task, edited_label, edited_description, edited_deadline)
                            if "editing" in item:
                                del item["editing"]  # Remover chave "editing" após salvar
                        st.rerun()

                else:
                    with col2:
                        pass  # Apenas para ajustar o layout
                with col4:
                    if st.button("❌ `Excluir`", key=f"delete_{idx}"):
                        delete_task(idx)  # Remover a tarefa original

if __name__ == "__main__":
    main()
