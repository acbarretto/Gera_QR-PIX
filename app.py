import streamlit as st
import runpy

st.set_page_config(layout=  "wide",
                   page_title='Executor da Folha do 1RIFsa', page_icon="🖋️")

### Título da página
col1, col2 = st.columns([5, 1])
with col1:
    st.title('Executor de Folha para o 1º RI de Feira de Santana')
with col2:
    fig_Logo = st.image("1rifsa.jpeg", width=100)

def home():
    st.title("Bem-vindo!! Aqui iniciamos o processo...")   #Bem-vindo ao PagaFolha")
    st.write("Esta aplicação irá processar os dados da folha de pagamento. Cliuqe no botão Avançar abaixo para iniciar.")
    if st.button("Avançar"):
        st.session_state.page = "extracao"
        st.rerun()

def extracao():
    st.title("Extração dos Dados")
    st.write("Esse processo irá executar a extração dos dados da Folha através do arquivo enviado pela Contas.")
    
    # Executa o script import_folha_GUI.py
    # runpy.run_path("import_folha_GUI.py")

    # if st.button("Continuar para Execução da Folha"):
    #     st.session_state.page = "executa_folha"
    #     st.rerun()
    if "extracao_concluida" not in st.session_state:
        st.session_state.extracao_concluida = False

    runpy.run_path("import_folha_GUI.py")

   # with st.spinner("Processando... Aguarde!"):
    if not st.session_state.extracao_concluida:
        
        st.session_state.extracao_concluida = True
        #st.rerun()
    else:
        st.success("O processo de importação e extração dos dados foi concluído com sucesso!!! Agora clique no botão abaixo para continuar.")
        if st.button("Continuar para Execução da Folha"):
            st.session_state.page = "executa_folha"
            st.rerun()
    

def executa_folha():
    #st.title("Execução da Folha")
    #st.write("Executando processamento principal da folha de pagamento...")
    
    # Executa o script main.py
    runpy.run_path("main.py")
    
    #st.success("Processo concluído com sucesso!")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "extracao":
        extracao()
    elif st.session_state.page == "executa_folha":
        executa_folha()

if __name__ == "__main__":
    main()
