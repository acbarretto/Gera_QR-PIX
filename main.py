import streamlit as st
import pandas as pd
from pixqrcodegen import Payload


#  streamlit run /Users/Andre/PagaFolha/main.py


# st.set_page_config(layout=  "wide",
#                    page_title='Executor da Folha do 1RIFsa', page_icon="🖋️")


### Título da página
col1, col2 = st.columns([5, 1])
with col1:
    st.title('Executor de Folha para o 1º RI de Feira de Santana')
with col2:
    fig_Logo = st.image("1rifsa.jpeg", width=100)

df_folha = pd.read_csv("folha.csv", sep=";")

max_index = df_folha.index.max() # Pego o indice do ultimo registro da tabela



# Inicializar o índice de exibição no session_state
if 'row_index' not in st.session_state:
    st.session_state.row_index = 0

# Definir o número de linhas visíveis por vez
linhas_por_pagina = 6

# Atualizar o índice para rolagem automática
def forcarScrollDown():
    st.session_state.row_index += linhas_por_pagina # = min(st.session_state.row_index + linhas_por_pagina, len(df) - linhas_por_pagina) #
    st.rerun()



#AQUI
### Crio um contador para percorrer o dataframe
if 'count' not in st.session_state:
    st.session_state.count = 0

# somente para contar quantos cliques já foi dado até o scroll
if 'count_scroll' not in st.session_state:
    st.session_state.count_scroll = 0

increment = st.button("Próximo")

if increment and st.session_state.count <= max_index:
    st.session_state.count += 1
    if st.session_state.count_scroll >= 6:
        st.session_state.count_scroll = 1
        forcarScrollDown()
    else:
        st.session_state.count_scroll += 1

### Crio uma variavel para o Total do que foi pago - Exibir no final da pagina
if 'total' not in st.session_state:
   st.session_state.total = 0.0


### Só executo se o indice (count) for menor/igual ao qtde maximo de itens da lista
if st.session_state.count <= max_index:
    for i in range(0, st.session_state.count): # preciso preencher todos os anteriores que já foram marcados
        df_folha.iat[i, 4] = True # iat[linha, coluna] - marco Realizado como True - st.session_state.count

    nomes = df_folha["Nome"].unique()
    nome = nomes[st.session_state.count] 

    df_nome = df_folha[df_folha["Nome"] == nome]

    colab_cpf = df_nome["CPF"].iloc[0]
    colab_nome = df_nome["Nome"].iloc[0]
    colab_valor = df_nome["PAGO"].iloc[0]

    chave = colab_cpf
    chave = chave.replace(".", "")
    chave = chave.replace("-", "")

    nome = colab_nome
    nome = nome.split()[0]
    sobrenome = colab_nome
    sobrenome = sobrenome.split()[-1]

    valor = f"{colab_valor}"  # Garante que valor seja uma string
    valor_formatado = float(valor) #.replace(".", "").replace(",", "."))  # Converte corretamente para float

    st.session_state.total += valor_formatado  # Soma o valor numérico ao total

    #### Gera a Linha PIX e o QR Code
    payload = Payload(nome, chave, valor, "FSA", "1RIFsa")
    payload.gerarPayload()

    col1, col2 = st.columns([2.5, 1])
    with col1:
        # Formato o dataframe para a coluna PAGO aparecer no formato brasileiro #.###,##
        df_folha["PAGO"] = df_folha["PAGO"].apply(lambda x: f"{x:,.2f}".replace(",", "_").replace(".", ",").replace("_", "."))
 
        st.dataframe(df_folha.iloc[st.session_state.row_index:st.session_state.row_index + max_index+1], width=900, height=270)

        total = f"{st.session_state.total:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        st.title(f"Total pago: R$ :red[{total}]")
        if st.session_state.count <= 0:
            st.subheader(f"De {st.session_state.count + 1} colaborador")
        else:
            st.subheader(f"De {st.session_state.count + 1} colaboradores")

    with col2:
        fig_QR = st.image("pixqrcodegen.png", width=300)
        st.subheader(f"==> {nome} {sobrenome}  -  R$ {colab_valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", "."))
else:
    st.header('FIM DO PROCESSO !!')
    total = f"{st.session_state.total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.title(f"Foi processado um Total de : R$ :red[{total}]")
    st.title(f"pagos a {st.session_state.count} colaboradores")