import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from pixqrcodegen import Payload
import qrcode
from time import sleep

#  streamlit run /Users/Andre/PagaFolha/main.py

st.set_page_config(layout=  "wide")

df_folha = pd.read_csv("folha.csv", sep=";")

#st.title("Contador em Tempo Real")

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'total' not in st.session_state:
   st.session_state.total = 0.0
#total = 0.0

increment = st.button("Próximo")

if increment:
    st.session_state.count += 1

#st.write("Contagem:", st.session_state.count)

# if st.button("xxx"):
#     incrementar_contador()
#     st.write(cont)

#edited_df = st.data_editor(df_folha)
#st.table(df_folha)

# cliar a columa SELECIONADO na tabela
# st.data_editor(
#     df_folha,
#     column_config={
#         "realizado": st.column_config.CheckboxColumn(
#             "Realizado",
#             help="Marque após concluir o pagamento",
#             default=False,
#         )
#     },
#     disabled=["widgets"],
#     hide_index=True,
# )

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

valor = colab_valor
valor = valor.replace(".","")
valor = valor.replace(",",".")
st.session_state.total += float(valor)

#### Gera a Linha PIX e o QR Code
payload = Payload(nome, chave, valor, "FSA", "1RIFsa")
payload.gerarPayload()

col1, col2 = st.columns([1.3, 1])
with col1:
    st.dataframe(df_folha, width=900, height=410)
    total = f"Total pago: R$ {st.session_state.total:,.2f}"
    total = total.replace(".","_")
    total = total.replace(",",".")
    total = total.replace("_",",")
    st.title(total)
    if st.session_state.count <= 0:
        st.subheader(f"De {st.session_state.count + 1} colaborador")
    else:
        st.subheader(f"De {st.session_state.count + 1} colaboradores")

with col2:
    fig_QR = st.image("pixqrcodegen.png")
    st.subheader(f">>> {nome} {sobrenome} - R$ {colab_valor}")

    

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