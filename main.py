import streamlit as st
import re
from utlis import text

def allFilesText(docs):
    all_files_text = text.process_files(docs)
    all_files_text = re.sub("Total: 0,00", "", all_files_text)
    all_files_text = re.sub("08/24 A", " mascaraAcres", all_files_text)
    all_files_text = re.sub("08/24 M", " mascaraManual", all_files_text)
    return all_files_text.split()

def main():
    st.set_page_config(page_title="ESR - Auxílio", page_icon=":crown:")
    tab1, tab2, tab3 = st.tabs(["Receitas", "Cobranças", "Inadimplências"])
    
    with st.sidebar:
        st.subheader("PDFs")
        pdf_docs = st.file_uploader("Carregue seus arquivos em formato PDF", accept_multiple_files=True)

    with tab1:
        if st.button("Puxar receitas"):
            array = allFilesText(pdf_docs)
            
            for i in range(len(array)):
                if array[i] == "Receitas":

                    sigla = ""
                    if array[i - 1] == "(2NG)":
                        sigla += array[i - 2] + " NG"
                    elif array[i - 1] == ")":
                        sigla += array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla += array[i - 2] + " NG"
                    else:
                        sigla += array[i - 1]

                if array[i] == "mascaraManual":
                    with tab1:
                        st.write(sigla + " Manual: " + array[i + 2])
                
                if array[i] == "mascaraAcres":
                    numero = 0
                    numero = array[i + 3]
                    numero = float(numero.replace('.','').replace(',','.'))
                    if numero < 100:
                        with tab1:
                            st.write(sigla + " Acrés./Desc: " + str(numero).replace('.',','))

                if array[i] == "Total:":
                    with tab1:
                        st.write(sigla + " " + array[i] + " " + array[i + 1])
                        st.write("-----------------------------------------")

    with tab2:
        if st.button("Puxar Cobranças"):
            array = allFilesText(pdf_docs)
            
            for i in range(len(array)):
                if array[i] == "Composição":
                    
                    sigla = ""
                    if array[i - 1] == "(2NG)":
                        sigla += array[i - 2] + " NG"
                    elif array[i - 1] == ")":
                        sigla += array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla += array[i - 2] + " NG"
                    else:
                        sigla += array[i - 1]

                if array[i] == "unidades" and array[i + 2] != "Outros":
                    with tab2:
                        st.write(sigla + " Pendentes: " + array[i + 2])
                        st.write("-----------------------------------------")

    with tab3:
        if st.button("Puxar Inadimplências"):
            siglasRepetidas = []
            print(siglasRepetidas)
            array = allFilesText(pdf_docs)
            
            for i in range(len(array)):
                if array[i] == "Inadimplência":

                    sigla = ""
                    if array[i - 1] == "(2NG)":
                        sigla += array[i - 2] + " NG"
                    elif array[i - 1] == ")":
                        sigla += array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla += array[i - 2] + " NG"
                    else:
                        sigla += array[i - 1]

                    if siglasRepetidas != [] and siglasRepetidas[0] == sigla:
                        sigla = sigla + " (NG)"
                        siglasRepetidas.pop()

                    if siglasRepetidas != [] and siglasRepetidas[0] != sigla:
                        siglasRepetidas.pop()

                if array[i] == "inadimplentes":
                    with tab3:
                        if siglasRepetidas == []:
                            siglasRepetidas.append(sigla)
                            
                        st.write(sigla + " Inadimplência: " + array[i + 2])
                        st.write("-----------------------------------------")

if __name__ == "__main__":
    main()