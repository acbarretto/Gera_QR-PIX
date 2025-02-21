import streamlit as st
import pandas as pd
from pixqrcodegen import Payload

import time
from streamlit_javascript import st_javascript

#  streamlit run /Users/Andre/PagaFolha/main.py


st.set_page_config(layout=  "wide",
                   page_title='Executor da Folha do 1RIFsa', page_icon="🖋️")


### Título da página
col1, col2 = st.columns([5, 1])
with col1:
    st.title('Executor de Folha para o 1º RI de Feira de Santana')
with col2:
    fig_Logo = st.image("1rifsa.jpeg", width=100)

df_folha = pd.read_csv("folha.csv", sep=";")

max_index = df_folha.index.max() # Pego o indice do ultimo registro da tabela

###############################
def scroll_down():
    st_javascript("""
        const container = parent.document.querySelector('.stDataFrame div[data-testid="stVerticalBlock"]');
        if (container) container.scrollTop = container.scrollHeight;
    """)

# # Exibir o DataFrame no Streamlit
# st.dataframe(df_folha, height=200)

# # Adicionar botão para rolar automaticamente
# if st.button("Forçar Scroll Down"):
#     scroll_down()

# Criando um DataFrame grande para exemplo
#data = {'Coluna A': range(1, 101), 'Coluna B': range(101, 201)}
df = df_folha

# Inicializar o índice de exibição no session_state
if 'row_index' not in st.session_state:
    st.session_state.row_index = 0

# Definir o número de linhas visíveis por vez
linhas_por_pagina = 6

# Atualizar o índice para rolagem automática
#if st.button("Forçar Scroll Down"):
def forcarScrollDown():
    #st.write(st.session_state.row_index)
    st.session_state.row_index += linhas_por_pagina # = min(st.session_state.row_index + linhas_por_pagina, len(df) - linhas_por_pagina) #
    time.sleep(0.5)
    st.rerun()

# Exibir apenas as linhas visíveis
#st.dataframe(df.iloc[st.session_state.row_index:st.session_state.row_index + linhas_por_pagina], height=250)
#st.dataframe(df.iloc[st.session_state.row_index:st.session_state.row_index + max_index+1], height=250)


###############################






#AQUI
### Crio um contador para percorrer o dataframe
if 'count' not in st.session_state:
    st.session_state.count = 0

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
    #nome = st.selectbox("Colaborador", nomes)

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

    valor = colab_valor
    valor = valor.replace(".","")
    valor = valor.replace(",",".")
    st.session_state.total += float(valor)

    #### Gera a Linha PIX e o QR Code
    payload = Payload(nome, chave, valor, "FSA", "1RIFsa")
    payload.gerarPayload()

    col1, col2 = st.columns([2.5, 1])
    with col1:
        #st.dataframe(df_folha, width=900, height=250)
        st.dataframe(df_folha.iloc[st.session_state.row_index:st.session_state.row_index + max_index+1], width=900, height=270)
        #df_folha.style.set_table_styles([{'selector': 'tr:hover', 'props': [('background-color', 'green'), ('color', 'black')]}])
        total = f" {st.session_state.total:,.2f}"
        total = total.replace(".","_")
        total = total.replace(",",".")
        total = total.replace("_",",")
        st.title(f"Total pago: R$ :red[{total}]")
        if st.session_state.count <= 0:
            st.subheader(f"De {st.session_state.count + 1} colaborador")
        else:
            st.subheader(f"De {st.session_state.count + 1} colaboradores")

    with col2:
        fig_QR = st.image("pixqrcodegen.png", width=300)
        #st.markdown(f" ==>  {nome} {sobrenome}  -  R$ {colab_valor}")
        st.subheader(f"==> {nome} {sobrenome}  -  R$ {colab_valor}")
else:
    st.header('FIM DO PROCESSO !!')
    total = f" {st.session_state.total:,.2f}"
    total = total.replace(".","_")
    total = total.replace(",",".")
    total = total.replace("_",",")
    st.title(f"Foi processado um Total de : R$ :red[{total}]")
    st.title(f"pagos a {st.session_state.count} colaboradores")


    






# if st.button("PAGAR"):
#     proxPgto(cont)
#     cont += 1
#     print(cont)

#df_folha = pd.read_csv("folha.csv", sep=";")

#df_folha.iterrows()
# btn = st.button("PAGAR")
# while btn == True:

#for index, row in df_folha.iterrows():
    # cont += 1
    # row = next(df_folha.iterrows())[cont]
    # #row
    # #print(row["CPF"])
    # btn
    # cpf = row['CPF']
    # cpf = cpf.replace(".", "")
    # cpf = cpf.replace("-", "")
    # cpf
    # sleep(1)

    # nome = row['Nome']
    # nome = nome.split(sep=" ")[0]
    # nome
    # sleep(1)

    # valor = row['PAGO']
    # valor
    # cont += 1
    # sleep(1)
    # btn = False


#price_max = df_top100_books["book price"].max()
#price_min = df_top100_books["book price"].min()

#max_price = st.sidebar.slider("Price Range", price_min, price_max, price_max)
#df_books = df_top100_books[df_top100_books["book price"] <= max_price]

#df_books

#fig = px.bar(df_books["year of publication"].value_counts())
#fig2 = px.histogram(df_books["book price"])

#col1, col2 = st.columns(2)
#col1.plotly_chart(fig)
#col2.plotly_chart(fig2)