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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Receitas", "Cobranças", "Inadimplências", "Encargos de cobranças", "Correio", "Notas Fiscais"])
    with st.sidebar:
        st.subheader("Version - 27/02/25")
        pdf_docs = st.file_uploader("Carregue seus arquivos em formato PDF", accept_multiple_files=True)
    with tab1:
        st.image("./imgs/exemplo1.png")
        mascaraAcres = st.text_input("Mask Acrés./Desc (Ex: 08/24 A)", "")
        st.image("./imgs/exemplo2.png")
        mascaraManual = st.text_input("Mask Manual (Ex: 08/24 M)", "")
        st.image("./imgs/exemplo3.png")
        naoAcrescenta = st.text_input("Mask Prova Real (Ex: 109/ (ITAU)) (Ex: 25/ (SICREDI))", "")
        st.warning("Caso não puxe alguma informação alguma máscara pode estar errada!")
        if st.button("Puxar receitas"):

            # st.write(naoAcrescenta)

            SIGLASITAU = [
                '(ABA)',
                '(CAP)',
                '(CEN)',
                '(GLS)',
                '(GAS)',
                '(GRE)',
                '(GRY)',
                '(GTU)',
                '(GBA)',
                '(GUA)',
                '(HTO)',
                '(LHA)',
                '(IVO)',
                '(JAN)',
                '(JDS)',
                '(MEL)',
                '(MCA)',
                '(MAR)',
                '(ODE)',
                '(PDP)',
                '(PDS)',
                '(PRA)',
                '(PDE)',
                '(RAV)',
                '(RAY)',
                '(SBA)',
                '(SOL)',
                '(TAR)',
                '(TER)',
                '(UBI)',
                '(UNI)',
                '(VIR)',
                '(VFE)',
                '(ABA) (NG)',
                '(CAP) (NG)',
                '(CEN) (NG)',
                '(GLS) (NG)',
                '(GAS) (NG)',
                '(GRE) (NG)',
                '(GRY) (NG)',
                '(GTU) (NG)',
                '(GBA) (NG)',
                '(GUA) (NG)',
                '(HTO) (NG)',
                '(LHA) (NG)',
                '(IVO) (NG)',
                '(JAN) (NG)',
                '(JDS) (NG)',
                '(77) (NG)',
                '(MCA) (NG)',
                '(MAR) (NG)',
                '(ODE) (NG)',
                '(PDP) (NG)',
                '(PDS) (NG)',
                '(PRA) (NG)',
                '(PDE) (NG)',
                '(RAV) (NG)',
                '(RAY) (NG)',
                '(SBA) (NG)',
                '(SOL) (NG)',
                '(TAR) (NG)',
                '(TER) (NG)',
                '(UBI) (NG)',
                '(UNI) (NG)',
                '(VIR) (NG)',
                '(VFE) (NG)',
            ]

            SIGLASSICREDI = [
                '(PSV)',
                '(REI)',
                '(ACO)',
                '(PAN)',
                '(LEO)',
                '(MTO)',
                '(MAD)',
                '(EMI)',
                '(PSV) (NG)',
                '(REI) (NG)',
                '(ACO) (NG)',
                '(PAN) (NG)',
                '(LEO) (NG)',
                '(MTO) (NG)',
                '(MAD) (NG)',
                '(EMI) (NG)',
            ]
                        
            totalAcres = 0
            totalAcresConc = ""
            ng = False
            array = puxarTextoReceitas(pdf_docs, mascaraAcres, mascaraManual, naoAcrescenta)

            for i in range(len(array)):

                if array[i] == "Receitas":

                    sigla = array[i - 1]

                    if array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    for j in range(20):
                        if array[i - j] == "NG" or array[i - j] == "2NG":
                            ng = True
                            break
                    
                    # st.write("-----------------------------------------")

                    if ng:
                        sigla = sigla + " (NG)"
                    
                    ng = False

                if array[i] == "mascaraManual":
                    if naoAcrescenta == "109/" and sigla in SIGLASSICREDI:
                        continue
                    if naoAcrescenta == "25/" and sigla in SIGLASITAU:
                        continue
                    with tab1:
                        original_title = '<p style="color:red; font-weight: bold;">' + ' Manual: ' + array[i + 2] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                if array[i] == "mascaraAcres":
                    if naoAcrescenta == "109/" and sigla in SIGLASSICREDI:
                        continue
                    if naoAcrescenta == "25/" and sigla in SIGLASITAU:
                        continue
                    numero = array[i + 3]
                    if array[i + 4] != "naoAcrescenta":
                        totalAcres = totalAcres + float(numero.replace('.','').replace(',','.'))
                        if totalAcresConc == "":
                            totalAcresConc = numero
                        else:
                            totalAcresConc += "+" + numero
                        
                if array[i] == "Total:":
                    if naoAcrescenta == "109/" and sigla in SIGLASSICREDI:
                        continue
                    if naoAcrescenta == "25/" and sigla in SIGLASITAU:
                        continue
                    with tab1:
                        if totalAcres != 0:
                            totalAcres = round(totalAcres, 2)
                            totalAcres = str(totalAcres).replace('.',',')
                            st.code(sigla + ";;" + ";=" + array[i + 1] + "-" + totalAcres + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                        if totalAcres == 0:
                            st.code(sigla + ";;" + ";=" + array[i + 1] + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                        if totalAcresConc != "":
                            st.code(sigla + ";;" + ";=" + totalAcresConc + ";Encargos s/ atrasos Recebimento de Cobrança - Boleto Bancário", language="python")
                            totalAcresConc = ""
                        totalAcres = 0
    with tab2:
        if st.button("Puxar Cobranças G"):

            siglasGarantidasCobrancas = [
                '(ABA)',
                '(ACO)',
                '(CAP)',
                '(CEN)',
                '(GLS)',
                '(GAS)',
                '(GRE)',
                '(GRY)',
                '(GTU)',
                '(GBA)',
                '(GUA)',
                '(HTO)',
                '(LHA)',
                '(IVO)',
                '(JAN',
                '(JDS)',
                '(LEO)',
                '(MEL)',
                '(MAD)',
                '(MCA)',
                '(MAR)',
                '(MTO)',
                '(ODE)',
                '(PAN)',
                '(PDP)',
                'PSV',
                '(PDS)',
                '(PRA)',
                '(PDE)',
                '(RAV)',
                '(RAY)',
                '(REI)',
                '(SBA)',
                '(EMI)',
                '(SOL)',
                '(TAR)',
                '(TER)',
                '(UBI)',
                '(UNI)',
                '(VIR)',
                '(VFE)',
            ]
            
            cobrancas = {}
            st.write("------------------------------- G -------------------------------")
            array = puxarTexto(pdf_docs)

            for i in range(len(array)):
                if array[i] == "Composição":
                    
                    sigla = array[i - 1]

                    if array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    cobrancas |= {sigla: 0}

                if array[i] == "Total":
                    cobrancas |= {sigla: array[i + 1]}

            for i in range(len(siglasGarantidasCobrancas)):
                if siglasGarantidasCobrancas[i] in cobrancas:
                    st.code(cobrancas[siglasGarantidasCobrancas[i]])

        if st.button("Puxar Cobranças NG"):
                    
            siglasNaoGarantidasCobrancas = [
                '(ABA)',
                '(ACO)',
                '(CAP)',
                '(CEN)',
                '(GLS)',
                '(GAS)',
                '(GRE)',
                '(GRY)',
                '(GTU)',
                '(IVO)',
                '(JAN)',
                '(MEL)',
                '(MTO)',
                '(ODE)',
                '(PDP)',
                '(PSV)',
                '(PDS)',
                '(PDE)',
                '(RAY)',
                '(SOL)',
                '(UBI)',
                '(UNI)',
                '(VFE)'
            ]

            array = puxarTexto(pdf_docs)
            cobrancas = {}
            st.write("------------------------------- NG -------------------------------")

            for i in range(len(array)):
                if array[i] == "Composição":
                    
                    sigla = array[i - 1]

                    if array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    cobrancas |= {sigla: 0}
                
                if array[i] == "Total":
                    cobrancas |= {sigla: array[i + 1]}

            for i in range(len(siglasNaoGarantidasCobrancas)):
                if siglasNaoGarantidasCobrancas[i] in cobrancas:
                    st.code(cobrancas[siglasNaoGarantidasCobrancas[i]])

    with tab3:
        if st.button("Puxar Inadimplências"):
            
            siglasGarantidasInads = [
                '(ABA)',
                '(ACO)',
                '(CAP)',
                '(CEN)',
                '(GLS)',
                '(GAS)',
                '(GRE)',
                '(GRY)',
                '(GTU)',
                '(GBA)',
                '(GUA)',
                '(HTO)',
                '(LHA)',
                '(IVO)',
                '(JAN)',
                '(JDS)',
                '(LEO)',
                '(MEL)',
                '(MAD)',
                '(MCA)',
                '(MAR)',
                '(MTO)',
                '(ODE)',
                '(PAN)',
                '(PDP)',
                '(PSV)',
                '(PDS)',
                '(PRA)',
                '(PDE)',
                '(RAV)',
                '(RAY)',
                '(REI)',
                '(SBA)',
                '(EMI)',
                '(SOL)',
                '(TAR)',
                '(TER)',
                '(UBI)',
                '(UNI)',
                '(VIR)',
                '(VFE)',
            ]

            siglasNaoGarantidasInads = [
                '(ABA) (NG)',
                '(ACO) (NG)',
                '(CAP) (NG)',
                '(CEN) (NG)',
                '(GLS) (NG)',
                '(GAS) (NG)',
                '(GRE) (NG)',
                '(GRY) (NG)',
                '(GTU) (NG)',
                '(IVO) (NG)',
                '(JAN) (NG)',
                '(77) (NG)',
                '(MTO) (NG)',
                '(ODE) (NG)',
                '(PDP) (NG)',
                '(PSV) (NG)',
                '(PDS) (NG)',
                '(PDE) (NG)',
                '(RAY) (NG)',
                '(SOL) (NG)',
                '(UBI) (NG)',
                '(UNI) (NG)',
                '(VFE) (NG)'
            ]
            
            inads = {}
            ng = False
            array = puxarTexto(pdf_docs)

            for i in range(len(array)):

                if array[i] == "Inadimplência":
                        
                    sigla = array[i - 1]

                    if array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    for j in range(20):
                        if array[i - j] == "NG" or array[i - j] == "2NG":
                            ng = True
                            break

                    if ng:
                        sigla = sigla + " (NG)"
                    
                if array[i] == "inadimplentes" or array[i] == "inadimplente" or array[i] == "(0,00%)":
                    if array[i + 2] == "W002B" or array[i + 2] == "CONDOMÍNIO":
                        inads |= {sigla: 0}
                    else:
                        inads |= {sigla: array[i + 2]}

                    ng = False

            st.write("------------------------------- G -------------------------------")

            for i in range(len(siglasGarantidasInads)):
                if siglasGarantidasInads[i] in inads:
                    st.code(inads[siglasGarantidasInads[i]])
            
            st.write("------------------------------- NG -------------------------------")

            for i in range(len(siglasNaoGarantidasInads)):
                if siglasNaoGarantidasInads[i] in inads:
                    st.code(inads[siglasNaoGarantidasInads[i]])


    with tab4:
        if st.button("Puxar Encargos"):

            array = puxarTextoEncargos(pdf_docs)

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

                    st.write("-----------------------------------------")
                    st.write(sigla)
                    st.write("Encargos:")


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

    with tab5:
        if st.button("Puxar correio"):

            ng = False
            array = puxarTexto(pdf_docs)

            for i in range(len(array)):

                if array[i] == "Contatos":

                    sigla = array[i - 1]

                    if array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    for j in range(20):
                        if array[i - j] == "NG" or array[i - j] == "2NG":
                            ng = True
                            break
                    if ng:
                        st.write(sigla + " (NG)")
                    else:
                        st.write(sigla)
                    
                    ng = False

                if array[i] == "Contatos:":
                    with tab5:
                        st.code(array[i + 1], language="python")

    with tab6:
        mesValor = st.text_input("Mês", "")
        anoValor = st.text_input("Ano", "")
        if st.button("Puxar notas"):

            array = puxarTexto(pdf_docs)


            siglas = [
                "ABA",
                "ACO",
                "CAP",
                "CEN",
                "GLS",
                "GAS",
                "GRE",
                "GRY",
                "GTU",
                "GBA",
                "GUA",
                "HTO",
                "LHA",
                "IVO",
                "JAN",
                "JDS",
                "LEO",
                "MEL",
                "LUA",
                "MAD",
                "MCA",
                "MAR",
                "MTO",
                "ODE",
                "PAN",
                "PDP",
                "PSV",
                "PDS",
                "PRA",
                "PDE",
                "RAV",
                "RAY",
                "REI",
                "SBA",
                "EMI",
                "SOL",
                "TAR",
                "TER",
                "UBI",
                "UNI",
                "VIR",
                "VFE",
            ]


            for i in range(len(array)):
                if array[i] in siglas:
                    original_title = '<p style="color:red; font-weight: bold;">' + '---------------------------------------------------------------' + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    st.code("COND: " + array[i])
                    st.code(array[i + 1])
                    st.code("Total: " + array[i + 4])
                    st.code("SERVIÇOS DE COBRANÇA PRESTADOS EM " + mesValor + " " + anoValor + ":")
                    st.code("ENCARGOS DE COBRANÇA ...................... " + array[i + 3])
                    st.code("TX. OPERACIONAL ........................... " + array[i + 2])
                    


if __name__ == "__main__":
    main()
