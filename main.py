import streamlit as st
import re
from utlis import text

def puxarTextoReceitas(docs, maskAcres, maskManual, maskProvaReal):
    all_files_text = text.process_files(docs)
    all_files_text = re.sub("Total: 0,00", "", all_files_text)
    all_files_text = re.sub("CONDOMÍNIO", "naoAcrescenta", all_files_text)
    all_files_text = re.sub(maskAcres, " mascaraAcres", all_files_text)
    all_files_text = re.sub(maskManual, " mascaraManual", all_files_text)
    all_files_text = re.sub(maskProvaReal, "naoAcrescenta ", all_files_text)
    return all_files_text.split()

def puxarTextoEncargos(docs):
    all_files_text = text.process_files(docs)
    all_files_text = re.sub("Encargos de Cobrança", "encargosCob", all_files_text)
    return all_files_text.split()

def puxarTexto(docs):
    all_files_text = text.process_files(docs)
    return all_files_text.split()

def main():
    st.set_page_config(page_title="ESR - Auxílio", page_icon=":crown:")
    tab1, tab2, tab3, tab4 = st.tabs(["Receitas", "Cobranças", "Inadimplências", "Encargos de cobranças"])
    with st.sidebar:
        st.subheader("Version - 12.08.2024 17:52")
        pdf_docs = st.file_uploader("Carregue seus arquivos em formato PDF", accept_multiple_files=True)
    with tab1:
        st.image("./imgs/exemplo1.png")
        mascaraAcres = st.text_input("Mask Acrés./Desc (Ex: 08/24 A)", "")
        st.image("./imgs/exemplo2.png")
        mascaraManual = st.text_input("Mask Manual (Ex: 08/24 M)", "")
        st.image("./imgs/exemplo3.png")
        naoAcrescenta = st.text_input("Mask Prova Real (Ex: 109/)", "")
        st.warning("Caso não puxe alguma informação alguma máscara pode estar errada!")
        if st.button("Puxar receitas"):
            totalAcres = 0
            totalAcresConc = ""
            array = puxarTextoReceitas(pdf_docs, mascaraAcres, mascaraManual, naoAcrescenta)
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
                        original_title = '<p style="color:red; font-weight: bold;">' + sigla + ' Manual: ' + array[i + 2] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                if array[i] == "mascaraAcres":
                    numero = array[i + 3]
                    if array[i + 4] != "naoAcrescenta":
                        totalAcres = totalAcres + float(numero.replace('.','').replace(',','.'))
                        if totalAcresConc == "":
                            totalAcresConc = numero
                        else:
                            totalAcresConc += "+" + numero
                        with tab1:
                            st.write(sigla + " Acrés./Desc: " + numero)
                if array[i] == "Total:":
                    with tab1:
                        if totalAcresConc != "":
                            st.code("=" + totalAcresConc, language="python")
                            totalAcresConc = ""
                        st.write(sigla + " " + array[i] + " " + array[i + 1])
                        if totalAcres != 0:
                            st.code("=" + array[i + 1] + "-" + str(totalAcres).replace('.',','), language="python")
                        st.write("-----------------------------------------")
                        totalAcres = 0
    with tab2:
        if st.button("Puxar Cobranças"):
            array = puxarTexto(pdf_docs)
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
                if array[i] == "Total":
                    with tab2:
                        st.write(sigla + " A vencer: " + array[i + 1])
                        st.write("-----------------------------------------")
    with tab3:
        if st.button("Puxar Inadimplências"):
            array = puxarTexto(pdf_docs)
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
                if array[i] == "inadimplentes":
                    with tab3:
                        st.write(sigla + " Inadimplência: " + array[i + 2])
                        st.write("-----------------------------------------")
    with tab4:
        if st.button("Puxar Encargos"):
            array = puxarTextoEncargos(pdf_docs)
            siglaBackup = ""
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
                    if sigla != siglaBackup:
                        st.write("-----------------------------------------")
                        st.write(sigla)
                        st.write("Encargos:")
                        siglaBackup = sigla
                if array[i] == "encargosCob":
                    with tab4:
                        if array[i + 4] == "Total":
                            st.write("Total: " + array[i + 5])
                            break
                        st.code(array[i + 5], language="python")
                if array[i] == "Total":
                    with tab4:
                        if array[i + 1] != "1.60.10":
                            st.write("Total: " + array[i + 1])
if __name__ == "__main__":
    main()
