import pandas as pd
import streamlit as st
import os

def extrair_dados_excel(arquivo):
    # Carregar a planilha
    xls = pd.ExcelFile(arquivo)
    sheet_name = xls.sheet_names[0]  # Assumindo que os dados estão na primeira aba
    df = pd.read_excel(xls, sheet_name, dtype=str, header=None)
    
    # Exibir os nomes das colunas para depuração
    print("Colunas encontradas:", df.columns.tolist())
    
    # Renomear colunas para garantir acesso correto
    df.columns = [str(i) for i in range(len(df.columns))]
    
    # Inicializar lista de dados
    empregados = []
    
    # Percorrer a planilha linha por linha
    cpf, nome, cargo, pago, realizado = None, None, None, None, None
    for index, row in df.iterrows():
        if row["0"] == "Empr.:":
            cpf = row["45"]  # Coluna "AT" no índice correspondente
            nome = row["9"]   # Coluna "J" no índice correspondente
        elif row["0"] == "Cargo:" and cpf:
            cargo = row["9"]
        elif row["0"] == "ND:" and cpf:
            pago = row["68"]  # Coluna "BQ" no índice correspondente
            try:
                pago = float(pago.replace(',', '.'))  # Converter para float, tratando vírgulas
            except ValueError:
                pago = None  # Se não puder ser convertido, definir como None
            realizado = False # coloco o valor default de realizado com False
            if pago is not None and pago > 0:
                empregados.append({"CPF": cpf, "Nome": nome, "Cargo": cargo, "PAGO": pago, "Realizado": realizado})
            cpf, nome, cargo, pago, realizado = None, None, None, None, None  # Resetar os valores
    
    return pd.DataFrame(empregados)


# Upload do arquivo
arquivo = st.file_uploader("Para iniciar, clique abaixo para selecionar o arquivo Excel, referente a Folha do mês, que foi enviado pela Contas", type=["xlsx"])

if arquivo is not None:
    #output_path = f"{os.path.splitext(arquivo.name)[0]}.csv"
    output_path = "folha.csv"
    tabela = extrair_dados_excel(arquivo)
    tabela.to_csv(output_path, index=False, sep=';')
    #st.success(f"Os dados da Folha foram extraídos e salvos em: {output_path}")
    #st.download_button("Baixar Arquivo Extraído", data=tabela.to_csv(index=False, sep=';'), file_name=os.path.basename(output_path), mime="text/csv")