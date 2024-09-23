import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import datetime
import Funcoes_API_Teleporte 
import streamlit.components.v1 as components

def display_gif(file_path, tempo_execucao, width):
    # Adiciona um cache-bypass ao nome do arquivo
    current_time = datetime.now().strftime("%H%M%S")
    gif_path = file_path
    st.image(gif_path, width=width)
    time.sleep(tempo_execucao)  

class TeleporteQuanticoStreamlit:
    def __init__(self):
        # Inicializa os estados necessários para o circuito e medições
        self.initialize_session_state()

    def initialize_session_state(self):
        states = ['qc', 'input_Alice', 'bloch_mostrada', 'montar_circuito', 'qubits_medidos',
                  'q0', 'q1', 'correcoes', 'mensagem_enviada', 'matriz_resultante', 
                  'gif_exibido', 'mensagem_lida', 'q2', 'q2_ket', 'qubit_bob_medido']
        for state in states:
            if state not in st.session_state:
                st.session_state[state] = None

    ########## Etapa de Inicialização ##########
    
    def iniciar(self):
        st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)  # Linha Separadora
        st.title('API: Teleporte Quântico Interativo')
        st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)  # Linha Separadora

        st.markdown("### Quer enviar uma informação de Qubit de Alice para Bob?")
        st.markdown(" - Para começar, escolha um valor de Qubit entre 0 ou 1 e " +
                    "aperte o botão de Teleporte que lhe enviaremos para o computador quântico de Alice.")

        ########## Botão "Iniciar Teleporte" ##########
        if not st.session_state.bloch_mostrada:
            st.session_state.input_Alice = st.selectbox('Selecione o estado de Qubit para enviar [0 ou 1]:', [0, 1])

            if st.button('Iniciar Teleporte'):
                st.markdown('## Parte da Alice 👧')
                st.markdown('#### Passo 1 de Alice: Preparando o qubit q_2')

                # Use o valor de st.session_state.input_Alice, não input_Alice
                st.latex(r'| q_{{\text{{2}}}} \rangle = ' + (r'|1 \rangle' if st.session_state.input_Alice == 1 else r'|0 \rangle'))

                # Chamando a função plot_esfera_de_bloch que agora está no arquivo Funcoes_API_Teleporte
                bloch_fig = Funcoes_API_Teleporte.plot_esfera_de_bloch(st.session_state.input_Alice)
                st.pyplot(bloch_fig)
                st.session_state.bloch_mostrada = True

###

        ########## Estado Inicial de Alice ##########
        if st.session_state.bloch_mostrada:
            st.markdown('### Estado Inicial de Alice')  
            st.write(f'Qubit enviado por Alice:')
            st.latex(r'| q_{{\text{{2}}}} \rangle = ' + r'|' + str(st.session_state.input_Alice) + r' \rangle ')
            st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
            st.markdown("""<div style="margin-top: 50px;"></div>""", unsafe_allow_html=True) # Adiciona Espaço em branco
            
        ########## Botão "Montar Circuito" ##########
       
        if st.session_state.bloch_mostrada and not st.session_state.montar_circuito:
            if st.button('Montar Circuito'):
                st.session_state.montar_circuito = True
                st.markdown('### Preparando Circuito...') 
                display_gif("martelando_ibere.gif", 3, 300)

        if st.session_state.montar_circuito:
            st.session_state.qc = Funcoes_API_Teleporte.passo1_Alice_monta_circuito(st.session_state.input_Alice)
            st.success('Circuito montado!')
            st.markdown("""<div style="margin-top: 50px;"></div>""", unsafe_allow_html=True)  # Adiciona Espaço em branco


###

        ########## Botão "Medir Qubits de Alice" ##########
        if st.session_state.montar_circuito and not st.session_state.qubits_medidos:
            if st.button('Medir Qubits de Alice'):
                st.session_state.qubits_medidos = True
                st.markdown('### Medindo os Qubits...')
#                st.image('alice_medindo_qubit.png', width=300)
#                display_gif("alice_medindo_qubit.gif", 3, 300) 
                st.video("alice_medindo_qubit.mp4", format="video/mp4", start_time=0)

        if st.session_state.qubits_medidos:
            st.session_state.qc, st.session_state.q0, st.session_state.q1 = Funcoes_API_Teleporte.passo2_Alice_mede_qubits(st.session_state.qc)
            st.markdown('### Acabamos tendo como Resultados da medição:')
            st.latex(r'| q_{{\text{{0}}}} \rangle = ' + r'|' + str(st.session_state.q0) + r' \rangle ' + r'\quad | \quad' +
                     r'| q_{{\text{{1}}}} \rangle = ' + r'|' + str(st.session_state.q1) + r' \rangle ')                    
            st.markdown('##### Estado de Bell:')
            st.latex(r'| q_{{0}} q_{{1}} \rangle = |' + str(st.session_state.q0) + str(st.session_state.q1) + r' \rangle')
            st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
            st.success('Qubits de Alice medidos!')
            st.markdown("""<div style="margin-top: 50px;"></div>""", unsafe_allow_html=True) #Adiciona Espaço em branco

###

        if st.session_state.qubits_medidos and not st.session_state.mensagem_enviada:
            if st.button('Enviar Mensagem'):
                st.session_state.mensagem_enviada = True
                st.markdown('### Mandando um Email ...') 
                display_gif("mandando_mensagem.gif", 3, 300)

        if st.session_state.mensagem_enviada:
            st.session_state.correcoes, st.session_state.matriz_resultante = Funcoes_API_Teleporte.passo3_Alice_manda_mensagem_para_Bob(
                                                                             st.session_state.qc, st.session_state.q0, st.session_state.q1)
            st.success('Mensagem enviada para Bob!')

###

        ########## Botão "Trocar para Bob" ##########
        if st.session_state.mensagem_enviada and not st.session_state.gif_exibido:
            st.write('## Aqui acaba a parte da Alice. ##')
            
            if st.button('Trocar para Bob'):
                gif_path = 'teleporte_botao_trocar_para_bob.gif'               
                st.image(gif_path, use_column_width=True)  # Centraliza o GIF usando o argumento 'use_column_width' do st.image                
                time.sleep(3)
                st.session_state.gif_exibido = True

###

        ########## Parte de Bob ##########
        if st.session_state.gif_exibido and not st.session_state.mensagem_lida:
            st.markdown("""
                <div style="background-color: #0004ff; padding: 10px; border-radius: 10px; text-align: center;">
                     <h3 style="color: white;">Estamos no PC Quântico de Bob</h3>
                </div>
                <br><br> <!-- Adiciona espaço vertical --> """, unsafe_allow_html=True
            )
            st.write('Como primeiro passo de Bob, precisamos: Ler as informações que Alice enviou.')
                
            if st.button('Ler Mensagens'):   
                st.session_state.mensagem_lida = True
                st.markdown('### Lendo a mensagem de Alice...') 
#                display_gif("lendo_mensagens_de_alice.gif", 3, 300)
            giphy_html = """
            <iframe src="https://giphy.com/embed/n1dFDLwXu4Qkwy7OJ0" width="480" height="480" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
            <p><a href="https://giphy.com/gifs/zero21surf-www-gppark-greenplacepark-n1dFDLwXu4Qkwy7OJ0">via GIPHY</a></p>
            """
            components.html(giphy_html, height=500)
         
        if st.session_state.mensagem_lida:
            Funcoes_API_Teleporte.passo4_Bob_verifica_portas_logicas_de_Alice_parte1(
                st.session_state.input_Alice, st.session_state.qc, st.session_state.q0, 
                st.session_state.q1, st.session_state.correcoes, st.session_state.matriz_resultante
            )
            st.session_state.q2, st.session_state.q2_ket = Funcoes_API_Teleporte.passo4_Bob_verifica_portas_logicas_de_Alice_parte2(
                st.session_state.input_Alice, st.session_state.qc, st.session_state.q0, 
                st.session_state.q1, st.session_state.correcoes, st.session_state.matriz_resultante
            )
            st.success('Mensagens de Alice lidas com sucesso!')

        ########## Botão "Medir Qubit de Bob" ##########
        if st.session_state.mensagem_lida and not st.session_state.qubit_bob_medido:
            if st.button('Medir Qubit de Bob'):
                st.session_state.qubit_bob_medido = True
                st.markdown('### Medindo o qubit ...') 
                display_gif("medindo_qubit_de_bob.gif", 3, 300)

        if st.session_state.qubit_bob_medido:
            st.session_state.qc = Funcoes_API_Teleporte.passo5_Bob_mede_qubit_enviado_por_Alice(
                st.session_state.input_Alice, st.session_state.qc, st.session_state.q0, 
                st.session_state.q1, st.session_state.q2, st.session_state.q2_ket, st.session_state.correcoes
            )           
            st.success('Qubit de Bob medido com sucesso!')

###

        ########## Botão "Calcular Qubit de Bob" ##########
        if st.session_state.qubit_bob_medido:
            if st.button('Calcular Qubit de Bob'):
                Funcoes_API_Teleporte.passo6_Bob_aplica_correcoes_obtem_resultado(
                    st.session_state.input_Alice, st.session_state.qc, st.session_state.q0, 
                    st.session_state.q1, st.session_state.q2, st.session_state.q2_ket, st.session_state.matriz_resultante
                )
                st.success('Correções aplicadas e resultado final obtido com sucesso!')


########################################################################################################
#  C H A M A D A   D A   F U N C A O    " M A I N "
########################################################################################################

if __name__ == "__main__":
    teleporte = TeleporteQuanticoStreamlit()
    teleporte.iniciar()
