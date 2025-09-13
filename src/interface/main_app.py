# Interface Gráfica Principal com Streamlit (Sem Áudio)

"""
Este arquivo contém a interface gráfica principal do sistema de recepção inteligente,
utilizando Streamlit para interagir com os módulos de recepção, triagem e banco de dados.
As funcionalidades de áudio foram removidas/desabilitadas.
"""

import streamlit as st
import os
import sys
# from datetime import datetime # Não parece ser usado diretamente, pode ser removido se não houver uso futuro

# Adicionar o diretório src ao sys.path para permitir importações dos módulos
SRC_DIR = os.path.join(os.path.dirname(__file__), "..") # Vai para src/
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# Tentar importar os módulos. Se falhar, pode ser o primeiro acesso ou erro de path.
try:
    # from recepcao.recepcao_automatizada import Recepcao # Recepcao não é instanciada ou usada
    from triagem.triagem_ia import TriagemIA
    #from audio.audio_utils import AudioUtils # Mantido, mas a classe foi esvaziada de funcionalidade de áudio
    from banco_dados.banco_dados_utils import BancoDadosUtils # DB_PATH não é mais importado diretamente aqui
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}. Verifique a estrutura de pastas e o PYTHONPATH.")
    st.stop() # Impede a execução do restante do app se os módulos não puderem ser carregados

# --- Inicialização dos Módulos ---
st.set_page_config(layout="wide", page_title="Recepção Inteligente - Posto de Saúde")

@st.cache_resource # Cache para evitar recriar em cada interação
def inicializar_modulos():
    # audio_util = AudioUtils(idioma="pt-BR") # AudioUtils agora não faz nada com áudio
    # Inicializar banco de dados PostgreSQL (configurações vêm do .env)
    try:
        db_util = BancoDadosUtils()
    except ValueError as e:
        st.error(f"Erro de configuração do banco de dados: {e}")
        st.info("Verifique se o arquivo .env está configurado corretamente com as credenciais do Azure PostgreSQL.")
        st.stop()
    
    triagem_ia = TriagemIA()
    # Retornar um objeto AudioUtils "dummy" para evitar mais alterações no código que o chama
    # A classe AudioUtils foi modificada para ter métodos vazios ou que apenas printam.
    #return AudioUtils(idioma="pt-BR"), db_util, triagem_ia

db, triagem = inicializar_modulos()

# --- Estado da Sessão Streamlit ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "paciente_id" not in st.session_state:
    st.session_state.paciente_id = None
if "dados_paciente" not in st.session_state:
    st.session_state.dados_paciente = {}
# if "sintomas_falados" not in st.session_state: # Não é mais necessário com a remoção da funcionalidade de voz
#     st.session_state.sintomas_falados = ""

# --- Funções Auxiliares da Interface ---
def mostrar_info(texto):
    # audio.falar(texto) # Chamada de áudio removida
    st.info(texto)

def ir_para_pagina(nome_pagina):
    st.session_state.pagina = nome_pagina
    st.rerun()

# --- Layout da Aplicação ---
st.title("Sistema de Recepção Inteligente do Posto de Saúde")

if st.session_state.pagina == "inicio":
    st.header("Bem-vindo(a)!")
    mostrar_info("Bem-vindo ao sistema de atendimento automatizado. Por favor, preencha seus dados para iniciar.")
    
    with st.form("cadastro_paciente_form"):
        st.subheader("Identificação do Paciente")
        nome = st.text_input("Nome Completo:", key="nome_input")
        cpf = st.text_input("CPF (apenas números):", max_chars=11, key="cpf_input")
        data_nascimento = st.text_input("Data de Nascimento (DD/MM/AAAA):", key="data_nasc_input")
        
        st.subheader("Relato dos Sintomas")
        # sintomas_texto = st.text_area("Descreva seus sintomas aqui:", key="sintomas_text_input", value=st.session_state.sintomas_falados)
        sintomas_texto = st.text_area("Descreva seus sintomas aqui:", key="sintomas_text_input")
        
        # Botão de gravar sintomas por voz removido
        # col1, col2 = st.columns(2)
        # with col1:
        #     if st.button("🎤 Gravar Sintomas por Voz", use_container_width=True):
        #         with st.spinner("Ouvindo seus sintomas..."):
        #             # audio.falar("Por favor, diga seus sintomas após o sinal.")
        #             st.info("Funcionalidade de gravação de voz desabilitada. Por favor, digite os sintomas.")
        #             # sintomas_ouvidos = audio.ouvir_comando(prompt_tts="Estou ouvindo seus sintomas agora.")
        #             # if sintomas_ouvidos:
        #             #     st.session_state.sintomas_falados = sintomas_ouvidos
        #             #     # audio.falar(f"Entendi que seus sintomas são: {sintomas_ouvidos}. Eles foram preenchidos no campo de texto.")
        #             #     st.info(f"Sintomas entendidos (simulado): {sintomas_ouvidos}. Eles foram preenchidos no campo de texto.")
        #             #     st.rerun() # Atualiza o text_area
        #             # else:
        #             #     # audio.falar("Não consegui entender seus sintomas. Por favor, tente novamente ou digite-os.")
        #             #     st.warning("Não consegui entender seus sintomas. Por favor, tente novamente ou digite-os.")
        
        # with col2: # O botão de submit agora ocupa a largura total ou é o único
        submit_button = st.form_submit_button("Iniciar Triagem", use_container_width=True)

        if submit_button:
            # Validações básicas
            # if not nome or not cpf or not data_nascimento or not (sintomas_texto or st.session_state.sintomas_falados):
            if not nome or not cpf or not data_nascimento or not sintomas_texto:
                st.error("Todos os campos (Nome, CPF, Data de Nascimento e Sintomas) são obrigatórios.")
                # audio.falar("Por favor, preencha todos os campos obrigatórios antes de continuar.") # Áudio removido
            elif not (cpf.isdigit() and len(cpf) == 11):
                st.error("CPF inválido. Deve conter 11 dígitos numéricos.")
                # audio.falar("O CPF informado parece inválido. Por favor, verifique.") # Áudio removido
            else:
                # sintomas_finais = sintomas_texto if sintomas_texto else st.session_state.sintomas_falados
                sintomas_finais = sintomas_texto
                st.session_state.dados_paciente = {
                    "nome_completo": nome,
                    "cpf": cpf,
                    "data_nascimento": data_nascimento,
                    "sintomas": sintomas_finais
                }
                mostrar_info("Obrigado pelas informações. Iniciando a triagem.")
                ir_para_pagina("triagem")

elif st.session_state.pagina == "triagem":
    st.header("Resultado da Triagem")
    dados = st.session_state.dados_paciente
    
    if not dados:
        st.warning("Nenhum dado de paciente encontrado para triagem. Retornando ao início.")
        ir_para_pagina("inicio")
    else:
        with st.spinner("Processando sua triagem..."):
            # Adicionar ou buscar paciente no BD
            paciente_id_bd = db.adicionar_paciente(dados["nome_completo"], dados["cpf"], dados["data_nascimento"])
            st.session_state.paciente_id = paciente_id_bd

            if not paciente_id_bd:
                st.error("Ocorreu um erro ao registrar suas informações no banco de dados. Por favor, tente novamente.")
                # audio.falar("Desculpe, tivemos um problema ao salvar seus dados. Tente novamente.") # Áudio removido
                if st.button("Voltar ao Início"):
                    ir_para_pagina("inicio")
            else:
                # Realizar a triagem
                prioridade, justificativa = triagem.classificar_prioridade(dados["sintomas"])
                
                # Salvar triagem no BD
                db.adicionar_triagem(paciente_id_bd, dados["sintomas"], prioridade, justificativa)
                
                st.subheader(f"Paciente: {dados['nome_completo']}")
                st.write(f"**Sintomas Relatados:** {dados['sintomas']}")
                st.metric(label="Nível de Prioridade", value=prioridade)
                st.info(f"**Justificativa da Classificação:** {justificativa}")
                
                mensagem_visual = f"Olá {dados['nome_completo'].split()[0]}. Com base nos seus sintomas, sua prioridade de atendimento foi classificada como {prioridade}. {justificativa} Por favor, aguarde as instruções dos nossos atendentes."
                # falar_e_mostrar(mensagem_tts) # Substituído por apenas mostrar
                st.info(mensagem_visual)
                
                st.success("Sua triagem foi concluída. Por favor, aguarde o chamado para atendimento.")
                # st.session_state.sintomas_falados = "" # Não é mais necessário

                if st.button("Registrar Novo Paciente", use_container_width=True):
                    ir_para_pagina("inicio")

# Rodapé (opcional)
st.markdown("---")
st.markdown("Projeto de Recepção Inteligente - Posto de Saúde (Versão sem áudio)")

# Para executar: streamlit run src/interface/main_app.py

