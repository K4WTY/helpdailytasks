import streamlit as st
import re
from utlis import text

def puxarTextoReceitas(docs, maskAcres, maskManual):
    all_files_text = text.process_files(docs)
    all_files_text = re.sub("Total: 0,00", "", all_files_text)
    all_files_text = re.sub("CONDOMÍNIO", "naoAcrescenta", all_files_text)
    all_files_text = re.sub(maskAcres, " mascaraAcres", all_files_text)
    all_files_text = re.sub(maskManual, " mascaraManual", all_files_text)
    all_files_text = re.sub("109/", "naoAcrescenta ", all_files_text)
    #all_files_text = re.sub("25/", "naoAcrescenta ", all_files_text)
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
        #naoAcrescenta = st.text_input("Mask Prova Real (Ex: 109/ (ITAU)) (Ex: 25/ (SICREDI))", "")
        #st.warning("Caso não puxe alguma informação alguma máscara pode estar errada!")
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
                '(LUA)',
                '(ICO)',
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
                '(ICO) (NG)',
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

            testeAutomatizarResumo = {
                '(ACA)': '0',
                '(AFA)': '0',
                '(ARO)': '0',
                '(BLU)': '0',
                '(CMA)': '0',
                '(CAR)': '0',
                '(CAS)': '0',
                '(DEZ)': '0',
                '(FLS)': '0',
                '(GNI)': '0',
                '(ITA)': '0',
                '(NAT)': '0',
                '(NEU)': '0',
                '(PNG)': '0',
                '(RFA)': '0',
                '(SAN)': '0',
                '(TRI)': '0',
                '(DIP)': '0',
                '(JCK)': '0',
                '(VZN)': '0',
                '(JCK 2)': '0',
                '(ARO NG)': '0',
                '(CAR NG)': '0',
                '(DEZ NG)': '0',
                '(NEU NG)': '0',
                '(GAP)': '0',
                '(ABA)': '0',
                '(ACO)': '0',
                '(CAP)': '0',
                '(CEN)': '0',
                '(GLS)': '0',
                '(GAS)': '0',
                '(GRE)': '0',
                '(GRY)': '0',
                '(GTU)': '0',
                '(GBA)': '0',
                '(GUA)': '0',
                '(HTO)': '0',
                '(LHA)': '0',
                '(ICO)': '0',
                '(IVO)': '0',
                '(JAN)': '0',
                '(JDS)': '0',
                '(LEO)': '0',
                '(MEL)': '0',
                '(LUA)': '0',
                '(MAD)': '0',
                '(MCA)': '0',
                '(MAR)': '0',
                '(MTO)': '0',
                '(ODE)': '0',
                '(PAN)': '0',
                '(PDP)': '0',
                '(PSV)': '0',
                '(PDS)': '0',
                '(PRA)': '0',
                '(PDE)': '0',
                '(RAV)': '0',
                '(RAY)': '0',
                '(REI)': '0',
                '(SBA)': '0',
                '(EMI)': '0',
                '(SOL)': '0',
                '(TAR)': '0',
                '(TER)': '0',
                '(UBI)': '0',
                '(UNI)': '0',
                '(VIR)': '0',
                '(VFE)': '0',
                '(ABA) (NG)': '0',
                '(ACO) (NG)': '0',
                '(CAP) (NG)': '0',
                '(CEN) (NG)': '0',
                '(GLS) (NG)': '0',
                '(GAS) (NG)': '0',
                '(GRE) (NG)': '0',
                '(GRY) (NG)': '0',
                '(GTU) (NG)': '0',
                '(ICO) (NG)': '0',
                '(IVO) (NG)': '0',
                '(JAN) (NG)': '0',
                '(77) (NG)': '0',
                '(MTO) (NG)': '0',
                '(ODE) (NG)': '0',
                '(PDP) (NG)': '0',
                '(PSV) (NG)': '0',
                '(PDS) (NG)': '0',
                '(PDE) (NG)': '0',
                '(RAY) (NG)': '0',
                '(SOL) (NG)': '0',
                '(UBI) (NG)': '0',
                '(UNI) (NG)': '0',
                '(VFE) (NG)': '0'
            }

            testeAutomatizarResumoExtra = {
                '(ACA)': '0',
                '(AFA)': '0',
                '(ARO)': '0',
                '(BLU)': '0',
                '(CMA)': '0',
                '(CAR)': '0',
                '(CAS)': '0',
                '(DEZ)': '0',
                '(FLS)': '0',
                '(GNI)': '0',
                '(ITA)': '0',
                '(NAT)': '0',
                '(NEU)': '0',
                '(PNG)': '0',
                '(RFA)': '0',
                '(SAN)': '0',
                '(TRI)': '0',
                '(DIP)': '0',
                '(JCK)': '0',
                '(VZN)': '0',
                '(JCK 2)': '0',
                '(ARO) (NG)': '0',
                '(CAR) (NG)': '0',
                '(DEZ) (NG)': '0',
                '(NEU) (NG)': '0',
                '(ABA)': '0',
                '(ACO)': '0',
                '(CAP)': '0',
                '(CEN)': '0',
                '(GLS)': '0',
                '(GAS)': '0',
                '(GRE)': '0',
                '(GRY)': '0',
                '(GTU)': '0',
                '(GBA)': '0',
                '(GUA)': '0',
                '(HTO)': '0',
                '(LHA)': '0',
                '(ICO)': '0',
                '(IVO)': '0',
                '(JAN)': '0',
                '(JDS)': '0',
                '(LEO)': '0',
                '(MEL)': '0',
                '(LUA)': '0',
                '(MAD)': '0',
                '(MCA)': '0',
                '(MAR)': '0',
                '(MTO)': '0',
                '(ODE)': '0',
                '(PAN)': '0',
                '(PDP)': '0',
                '(PSV)': '0',
                '(PDS)': '0',
                '(PRA)': '0',
                '(PDE)': '0',
                '(RAV)': '0',
                '(RAY)': '0',
                '(REI)': '0',
                '(SBA)': '0',
                '(EMI)': '0',
                '(SOL)': '0',
                '(TAR)': '0',
                '(TER)': '0',
                '(UBI)': '0',
                '(UNI)': '0',
                '(VIR)': '0',
                '(VFE)': '0',
                '(ABA) (NG)': '0', # TA 
                '(ACO) (NG)': '0', # TA 
                '(CAP) (NG)': '0', # TA 
                '(CEN) (NG)': '0', # TA 
                '(GLS) (NG)': '0', # TA 
                '(GAS) (NG)': '0', # TA 
                '(GRE) (NG)': '0', # TA 
                '(GRY) (NG)': '0', # TA 
                '(GTU) (NG)': '0', # TA 
                '(ICO) (NG)': '0', # TA 
                '(IVO) (NG)': '0', # TA 
                '(JAN) (NG)': '0', # TA 
                '(77) (NG)': '0', # TA 
                '(MTO) (NG)': '0', # TA 
                '(ODE) (NG)': '0', # TA 
                '(PDP) (NG)': '0', # TA 
                '(PSV) (NG)': '0', # TA 
                '(PDS) (NG)': '0', # TA 
                '(PDE) (NG)': '0', # TA 
                '(RAY) (NG)': '0', # TA 
                '(SOL) (NG)': '0', # TA 
                '(UBI) (NG)': '0', # TA 
                '(UNI) (NG)': '0', # TA 
                '(VFE) (NG)': '0' # TA 
            }

            renomearSiglas = {
                '(ACA)': 'ACÁCIAS',
                '(AFA)': 'ANGELO FATTORI', 
                '(ARO)': 'ANTONIO ROHN', # TA
                '(BLU)': 'BRUNO DE LUCCA', # TA
                '(CMA)': 'CARIN A MATEUSE', # TA 
                '(CAR)': 'CAROLINA', # TA
                '(CAS)': 'CASTRO', # TA
                '(DEZ)': 'DEZZMAI', # TA
                '(FLS)': 'FLOR DA SÍRIA',
                '(GNI)': 'O GUARANI', # TA
                '(ITA)': 'ITAMAMBUCA', # TA
                '(NAT)': 'NATÁLIA', # TA 
                '(NEU)': 'NOVA EUROPA ', # TA 
                '(PNG)': 'PONGAÍ', # TA
                '(RFA)': 'ROBERTO FADEL', # TA
                '(SAN)': 'SANTO ANTONIO', # TA
                '(TRI)': 'TRIANON', # TA
                '(DIP)': 'VILLAGIO DI PARMA', # TA
                '(JCK)': 'VILLAGIO DO JOCKEY', # TA 
                '(VZN)': 'VENEZA',
                '(JCK 2)': 'VILLAGIO DO JOCKEY JURÍDICO', # TA
                '(ARO) (NG)': 'ANTONIO ROHN (NG)', # TA
                '(CAR) (NG)': 'CAROLINA (NG)', # TA 
                '(DEZ) (NG)': 'DEZZMAI (NG)', # TA
                '(NEU) (NG)': 'NOVA EUROPA (NG)', # TA 
                '(ABA)': 'ABAETE', # TA 
                '(ACO)': 'ACAPULCO', # TA 
                '(CAP)': 'CAPRI', # TA 
                '(CEN)': 'CENÁRIO',
                '(GLS)': 'GALASSI', # TA
                '(GAS)': 'GASPAR',
                '(GRE)': 'GRÉCIA', # TA 
                '(GRY)': 'GRYGOR', # TA 
                '(GTU)': 'GUARATUBA', # TA
                '(GBA)': 'GUARIBA', # TA 
                '(GUA)': 'GUARINI',
                '(HTO)': 'HORTO', # TA 
                '(LHA)': 'ITARUÇUCA', # TA 
                '(ICO)': 'ÍNDICO', # TA
                '(IVO)': 'IVONE', # TA 
                '(JAN)': 'JANAINA',
                '(JDS)': 'JOÃO DE SOUZA', # TA
                '(LEO)': 'LEON', # TA
                '(MEL)': 'LUA DE MEL', # TA
                '(LUA)': 'LUARA', # TA 
                '(MAD)': 'MADRI', # TA 
                '(MCA)': 'MANACA', # TA 
                '(MAR)': 'MARACANÃ', # TA 
                '(MTO)': 'MARALTO', # TA 
                '(ODE)': 'ODETE', # TA 
                '(PAN)': 'PANORAMA', # TA
                '(PDP)': 'PARQUE DA PRAIA', # TA 
                '(PSV)': 'PARQUE SÃO VICENTE', # TA
                '(PDS)': 'PORTAL DO SOL', # TA 
                '(PRA)': 'PRADO', # TA 
                '(PDE)': 'PUNTA DEL ESTE', # TA 
                '(RAV)': 'RAVENA', # TA
                '(RAY)': 'RAYRA', # TA 
                '(REI)': 'REI DAVID', # TA 
                '(SBA)': 'SANTA BÁRBARA', # TA
                '(EMI)': 'SANTO EMÍLIO', # TA 
                '(SOL)': 'SOL NASCENTE',
                '(TAR)': 'TARSILA', 
                '(TER)': 'TERRACE', # TA 
                '(UBI)': 'UBIRAJARA', # TA 
                '(UNI)': 'UNIQUE', # TA
                '(VIR)': 'VIRGINIA', # TA
                '(VFE)': 'VIVA FELIZ', # TA 
                '(ABA) (NG)': 'ABAETE (NG)',
                '(ACO) (NG)': 'ACAPULCO (NG)',
                '(CAP) (NG)': 'CAPRI (NG)',
                '(CEN) (NG)': 'CENÁRIO (NG)',
                '(GLS) (NG)': 'GALASSI (NG)',
                '(GAS) (NG)': 'GASPAR (NG)',
                '(GRE) (NG)': 'GRÉCIA (NG)',
                '(GRY) (NG)': 'GRYGOR (NG)',
                '(GTU) (NG)': 'GUARATUBA (NG)',
                '(GBA) (NG)': 'GUARIBA (NG)',
                '(GUA) (NG)': 'GUARINI (NG)',
                '(HTO) (NG)': 'HORTO (NG)',
                '(LHA) (NG)': 'ITARUÇUCA (NG)',
                '(ICO) (NG)': 'ÍNDICO (NG)',
                '(IVO) (NG)': 'IVONE (NG)',
                '(JAN) (NG)': 'JANAINA (NG)',
                '(JDS) (NG)': 'JOÃO DE SOUZA (NG)',
                '(LEO) (NG)': 'LEON (NG)',
                '(77) (NG)': 'LUA DE MEL (NG)',
                '(LUA) (NG)': 'LUARA (NG)',
                '(MAD) (NG)': 'MADRI (NG)',
                '(MCA) (NG)': 'MANACA (NG)',
                '(MAR) (NG)': 'MARACANÃ (NG)',
                '(MTO) (NG)': 'MARALTO (NG)',
                '(ODE) (NG)': 'ODETE (NG)',
                '(PAN) (NG)': 'PANORAMA (NG)',
                '(PDP) (NG)': 'PARQUE DA PRAIA (NG)',
                '(PSV) (NG)': 'PARQUE SÃO VICENTE (NG)',
                '(PDS) (NG)': 'PORTAL DO SOL (NG)',
                '(PRA) (NG)': 'PRADO (NG)',
                '(PDE) (NG)': 'PUNTA DEL ESTE (NG)',
                '(RAV) (NG)': 'RAVENA (NG)',
                '(RAY) (NG)': 'RAYRA (NG)',
                '(REI) (NG)': 'REI DAVID (NG)',
                '(SBA) (NG)': 'SANTA BÁRBARA (NG)',
                '(EMI) (NG)': 'SANTO EMÍLIO (NG)',
                '(SOL) (NG)': 'SOL NASCENTE (NG)',
                '(TAR) (NG)': 'TARSILA (NG)',
                '(TER) (NG)': 'TERRACE (NG)',
                '(UBI) (NG)': 'UBIRAJARA (NG)',
                '(UNI) (NG)': 'UNIQUE (NG)',
                '(VIR) (NG)': 'VIRGINIA (NG)',
                '(VFE) (NG)': 'VIVA FELIZ (NG)',
            }
            
            sicredCondominios = []

            totalAcres = 0
            valorManual = 0
            valorManuelConc = ""
            totalAcresConc = ""
            ng = False
            guardarCond = False
            array = puxarTextoReceitas(pdf_docs, mascaraAcres, mascaraManual)
            print(array)
            for i in range(len(array)):

                if array[i] == "Receitas":

                    sigla = array[i - 1]

                    
                    

                    if array[i - 1] == "2)" and array[i - 2] == "(JCK":
                        sigla = "(JCK 2)"
                    elif array[i - 1] == "(2NG)":
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
                    
                    #print(sigla)
                
                    ng = False

                if array[i] == "mascaraManual":
                    valorManual = "-" + array[i + 2].replace('.','')
                    if valorManuelConc == "":
                        valorManuelConc = valorManual
                    else:
                        valorManuelConc += valorManual
                        
                if array[i] == "mascaraAcres":
                    numero = array[i + 3]
                    if array[i + 4] != "naoAcrescenta":
                        totalAcres = totalAcres + float(numero.replace('.','').replace(',','.'))
                        if totalAcresConc == "":
                            totalAcresConc = numero
                        else:
                            totalAcresConc += "+" + numero
                        
                if array[i] == "Total:":
                    with tab1:
                        if totalAcres != 0:
                            totalAcres = round(totalAcres, 2)
                            totalAcres = str(totalAcres).replace('.',',')

                            if valorManual != 0:
                                testeAutomatizarResumo[sigla] = array[i + 1].replace('.','') + "-" + totalAcres + valorManuelConc
                            else:
                                testeAutomatizarResumo[sigla] = array[i + 1].replace('.','') + "-" + totalAcres

                        if totalAcres == 0:
                            if valorManual != 0:
                                testeAutomatizarResumo[sigla] = array[i + 1].replace('.','') + valorManuelConc
                            else:
                                testeAutomatizarResumo[sigla] = array[i + 1].replace('.','')
                        if totalAcresConc != "":
                            if valorManual != 0:
                                testeAutomatizarResumoExtra[sigla] =  totalAcresConc + valorManuelConc
                            else:
                                testeAutomatizarResumoExtra[sigla] =  totalAcresConc

                        if sigla in SIGLASSICREDI:
                            guardarCond = True

                        for key, value in renomearSiglas.items():
                            if sigla == key:
                                sigla = value
                                break

                        if guardarCond:
                            if totalAcres != 0:
                                if valorManual != 0:
                                    sicredCondominios.append(sigla + ";;" + ";=" + array[i + 1].replace('.','') + "-" + totalAcres + valorManuelConc + ";Recebimento de Cobrança - Boleto Bancário")
                                else:
                                    sicredCondominios.append(sigla + ";;" + ";=" + array[i + 1].replace('.','') + "-" + totalAcres + ";Recebimento de Cobrança - Boleto Bancário")
                                
                            if totalAcres == 0:
                                if valorManual != 0:
                                    sicredCondominios.append(sigla + ";;" + ";=" + array[i + 1].replace('.','') + valorManuelConc + ";Recebimento de Cobrança - Boleto Bancário")
                                else:
                                    sicredCondominios.append(sigla + ";;" + ";=" + array[i + 1].replace('.','') + ";Recebimento de Cobrança - Boleto Bancário")
                                
                            if totalAcresConc != "":
                                sicredCondominios.append(sigla + ";;" + ";=" + totalAcresConc + ";Encargos s/ atrasos Recebimento de Cobrança - Boleto Bancário")
                                totalAcresConc = ""
                            
                            guardarCond = False
                            totalAcres = 0
                            valorManual = 0
                            valorManuelConc = ""
                            continue

                        if totalAcres != 0:
                            if valorManual != 0:
                                st.code(sigla + ";;" + ";=" + array[i + 1].replace('.','') + "-" + totalAcres + valorManuelConc + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                            else:
                                st.code(sigla + ";;" + ";=" + array[i + 1].replace('.','') + "-" + totalAcres + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                            
                        if totalAcres == 0:
                            if valorManual != 0:
                                st.code(sigla + ";;" + ";=" + array[i + 1].replace('.','') + valorManuelConc + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                            else:
                                st.code(sigla + ";;" + ";=" + array[i + 1].replace('.','') + ";Recebimento de Cobrança - Boleto Bancário", language="python")
                            
                        if totalAcresConc != "":
                            st.code(sigla + ";;" + ";=" + totalAcresConc + ";Encargos s/ atrasos Recebimento de Cobrança - Boleto Bancário", language="python")
                            totalAcresConc = ""

                        totalAcres = 0
                        valorManual = 0
                        valorManuelConc = ""

            original_title = '<p style="color:red; font-weight: bold;">' + 'SICREDI Condomínios:' + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)

            for i in range(len(sicredCondominios)):
                st.code(sicredCondominios[i], language="python")
            
            st.write("---------------------------------------------------------------")
            st.write("Receitas para automatizar resumo principal:")
            for key, value in testeAutomatizarResumo.items():
                st.code("=" + value, language="python")

            st.write("---------------------------------------------------------------")
            st.write("Receitas para automatizar resumo juros:")
            for key, value in testeAutomatizarResumoExtra.items():
                st.code("=" + value, language="python")
    with tab2:
        if st.button("Puxar Cobranças G"):

            siglasGarantidasCobrancas = [
                '(ACA)',
                '(AFA)', 
                '(ARO)', # TA
                '(BLU)', # TA
                '(CMA)', # TA 
                '(CAR)', # TA
                '(CAS)', # TA
                '(DEZ)', # TA
                '(FLS)',
                '(GNI)', # TA
                '(ITA)', # TA
                '(NAT)', # TA 
                '(NEU)', # TA 
                '(PNG)', # TA
                '(RFA)', # TA
                '(SAN)', # TA
                '(TRI)', # TA
                '(DIP)', # TA
                '(JCK)', # TA 
                '(VNZ)',
                '(JCK 2)', # TA
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
                '(ICO)',
                '(IVO)',
                '(JAN',
                '(JDS)',
                '(LEO)',
                '(MEL)',
                '(LUA)',
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

                    if array[i - 1] == "2)" and array[i - 2] == "(JCK":
                        sigla = "(JCK 2)"
                    elif array[i - 1] == "(2NG)":
                        sigla = array[i - 2]
                    elif array[i - 1] == ")":
                        sigla = array[i - 2] + ")"
                    elif array[i - 1] == "2)":
                        sigla = array[i - 2] + ")"

                    if sigla in cobrancas:
                        sigla = "(JCK 2)"

                    cobrancas |= {sigla: 0}

                if array[i] == "Total":
                    cobrancas |= {sigla: array[i + 1]}

            for i in range(len(siglasGarantidasCobrancas)):
                if siglasGarantidasCobrancas[i] in cobrancas:
                    st.code(cobrancas[siglasGarantidasCobrancas[i]])

        if st.button("Puxar Cobranças NG"):
                    
            siglasNaoGarantidasCobrancas = [
                '(ARO)', # TA
                '(CAR)', # TA 
                '(DEZ)', # TA
                '(NEU)', # TA 
                '(ABA)',
                '(ACO)',
                '(CAP)',
                '(CEN)',
                '(GLS)',
                '(GAS)',
                '(GRE)',
                '(GRY)',
                '(GTU)',
                '(ICO)',
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
                '(ACA)',
                '(AFA)', 
                '(ARO)', # TA
                '(BLU)', # TA
                '(CMA)', # TA 
                '(CAR)', # TA
                '(CAS)', # TA
                '(DEZ)', # TA
                '(FLS)',
                '(GNI)', # TA
                '(ITA)', # TA
                '(NAT)', # TA 
                '(NEU)', # TA 
                '(PNG)', # TA
                '(RFA)', # TA
                '(SAN)', # TA
                '(TRI)', # TA
                '(DIP)', # TA
                '(JCK)', # TA 
                '(VZN)',
                '(JCK 2)', # TA
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
                '(ICO)',
                '(IVO)',
                '(JAN)',
                '(JDS)',
                '(LEO)',
                '(MEL)',
                '(LUA)',
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
                '(ARO) (NG)', # TA
                '(CAR) (NG)', # TA 
                '(DEZ) (NG)', # TA
                '(NEU) (NG)', # TA 
                '(ABA) (NG)',
                '(ACO) (NG)',
                '(CAP) (NG)',
                '(CEN) (NG)',
                '(GLS) (NG)',
                '(GAS) (NG)',
                '(GRE) (NG)',
                '(GRY) (NG)',
                '(GTU) (NG)',
                '(ICO) (NG)',
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

                    if array[i - 1] == "2)" and array[i - 2] == "(JCK":
                        sigla = "(JCK 2)"
                    elif array[i - 1] == "(2NG)":
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
                    if array[i + 2] == "W002B" or array[i + 2] == "CONDOMÍNIO" or array[i + 2] == "CONDOMINIO":
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
                "VFE",
                "VIR",
                "ICO"
                
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

