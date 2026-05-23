import streamlit as st
import sqlite3
import pandas as pd


# BANCO DE DADOS

conn = sqlite3.connect('tarefas.db', check_same_thread = False)
c =  conn.cursor()

c.execute('''
          
        CREATE TABLE IF NOT EXISTS tarefas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente'
          
          )
''')

conn.commit()


st.title('GERENCIADOR DE TAREFAS')
st.subheader('streamlit + SQLITE')

st.markdown(' 🦑 NOVA TAREFA ')
nova_tarefa =  st.text_input('O que você precisa fazer? ')

if st.button('Add tarefa'):
    if nova_tarefa == '':
        st.warning('Digite algo...') 

    else:
        c.execute('INSERT INTO tarefas (nome, status) values(?,?)',(nova_tarefa, 'Pendente'))
        conn.commit()
        st.success('Tarefa adicionada com sucesso')
        
    
           

st.write('---')

st.markdown('SUAS TAREFAS')

c.execute('SELECT id, nome, status from tarefas')

dados  =  c.fetchall()

if dados:
    df = pd.DataFrame(dados, columns = ['ID', 'TAREFA', 'STATUS'])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('GERENCIAR')
    col1, col2 = st.columns(2)

    with col1: 
        tarefa_selecionada = st.selectbox('ESCOLHA PELO ID', df['ID'])
    with col2:
        acao = st.radio('Ação', ['CONCLUIR', 'EXCLUIR']) 

    if st.button('Confirmar...'):
        if acao  == 'CONCLUIR':
            c.execute("UPDATE tarefas SET status = 'CONCLUIDA' where id = ?  ", (tarefa_selecionada,))
            st.success('TAREFA CONCLUIDA')
        elif acao == 'EXCLUIR':
            c.execute("UPDATE tarefas SET status = 'EXCLUIDA' where id = ?  ", (tarefa_selecionada,))
            st.success('TAREFA  excluida')       
        conn.commit()
        st.rerun()

else:
    st.info('DIGITE ALGUMA TAREFA')
