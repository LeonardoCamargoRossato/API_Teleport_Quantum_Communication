import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d

# Definindo as matrizes das portas X e Z
porta_X = np.array([[0, 1], [1, 0]])
porta_Z = np.array([[1, 0], [0, -1]])

# Função para converter inteiro 0 ou 1 para um vetor coluna |0> ou |1>
def converte_inteiro_0_ou_1_em_bra_ket(num_inteiro):
    if num_inteiro == 0:
        return np.array([[1], [0]])
    elif num_inteiro == 1:
        return np.array([[0], [1]])

# Função para converter matriz para formato LaTeX
def matriz_para_latex(matriz):
    latex_str = r'\begin{bmatrix}'
    if matriz.ndim == 1:  # Se a matriz for um vetor
        matriz = matriz.reshape(-1, 1)  # Transforma o vetor em matriz de coluna
    rows, cols = matriz.shape
    for i in range(rows):
        for j in range(cols):
            latex_str += str(matriz[i, j])
            if j != cols - 1:
                latex_str += '&'
        if i != rows - 1:
            latex_str += r'\\'
    latex_str += r'\end{bmatrix}'
    return latex_str

# Função que determina o estado de q2 com base em q0, q1 e no estado preparado por Alice (input_Alice)
def tabela_verdade_protocoloBB84(input_Alice, q0, q1):
    if input_Alice == 0:
        if q0 == 0 and q1 == 0:
            return 0
        elif q0 == 0 and q1 == 1:
            return 1
        elif q0 == 1 and q1 == 0:
            return 0
        elif q0 == 1 and q1 == 1:
            return 1
    elif input_Alice == 1:
        if q0 == 0 and q1 == 0:
            return 1
        elif q0 == 0 and q1 == 1:
            return 0
        elif q0 == 1 and q1 == 0:
            return 1
        elif q0 == 1 and q1 == 1:
            return 0

# Função para determinar as correções que Bob deve aplicar
def correcoes_que_Bob_deve_aplicar(q0, q1):
    correcoes = []
    matriz_final = np.eye(2)
    if q0 == 1:
        correcoes.append('Porta Z no qubit 2')
        matriz_final = np.dot(porta_Z, matriz_final)
    if q1 == 1:
        correcoes.append('Porta X no qubit 2')
        matriz_final = np.dot(porta_X, matriz_final)
    return correcoes, matriz_final

# Função para plotar a Esfera de Bloch
def plot_esfera_de_bloch(input_Alice):
    def vetor_para_matriz_densidade(vetor):
        return np.outer(vetor, np.conj(vetor))

    def plot_estado_quantico(input_Alice):
        fig_size = (8, 6)  # Define o tamanho da figura
        vetor_estado = converte_inteiro_0_ou_1_em_bra_ket(input_Alice)
        matriz_densidade = vetor_para_matriz_densidade(vetor_estado)

        # Usar plot_bloch_multivector sem o ax
        bloch_fig = plot_bloch_multivector(matriz_densidade, figsize=fig_size)
        return bloch_fig

    return plot_estado_quantico(input_Alice)


#########################################################################################################
#    F  U  N  Ç  Õ  E  S       P  A  S  S  O  S      #
#########################################################################################################

# Função para o passo 1 de Alice (montar circuito)
def passo1_Alice_monta_circuito(input_Alice):
    qc = QuantumCircuit(3, 3)
    if input_Alice == 1:
        qc.x(2)
    qc.h(0)
    qc.cx(0, 2)
    qc.cx(1, 0)
    qc.h(1)

    st.write(qc.draw(output='mpl'))
    return qc

# Função para o passo 2 de Alice (medir qubits)
def passo2_Alice_mede_qubits(qc):
    q0 = random.randint(0, 1)
    q1 = random.randint(0, 1)
    qc.measure(0, 0)  # Medir qubit 0
    qc.measure(1, 1)  # Medir qubit 1

    st.markdown('### Passo 2 de Alice: Medição dos Qubits de Alice')
    st.write(qc.draw(output='mpl'))
    return qc, q0, q1

# Função para o passo 3 de Alice (enviar mensagem para Bob)
def passo3_Alice_manda_mensagem_para_Bob(qc, q0, q1):
    st.markdown('### Passo 3 de Alice: Comunicação clássica para Bob')
    correcoes, matriz_resultante = correcoes_que_Bob_deve_aplicar(q0, q1)
    st.write('Correções que Bob deve aplicar:')
    st.write(correcoes)
    return correcoes, matriz_resultante

# Função para o passo 4 de Bob (parte 1)
def passo4_Bob_verifica_portas_logicas_de_Alice_parte1(input_Alice, qc, q0, q1, correcoes, matriz_resultante):
    st.markdown('## Parte do Bob 👦')
    st.latex(r'| q_{{0}} \rangle = ' + str(q0) + r' \quad | \quad | q_{{1}} \rangle = ' + str(q1))

    st.write('Correções recebidas de Alice:')
    st.write(correcoes)

    # Exibe a matriz resultante
    st.write('Matriz resultante enviada por Alice:')
    st.latex(matriz_para_latex(matriz_resultante))

# Função para o passo 4 de Bob (parte 2)
def passo4_Bob_verifica_portas_logicas_de_Alice_parte2(input_Alice, qc, q0, q1, correcoes, matriz_resultante):
    st.write('Bob agora sabe as informações de Alice.')
    st.write('Correções aplicadas por Bob:')
    for correcao in correcoes:
        st.write(correcao)
    
    q2 = tabela_verdade_protocoloBB84(input_Alice, q0, q1)
    q2_ket = converte_inteiro_0_ou_1_em_bra_ket(q2)
    return q2, q2_ket

# Função para o passo 5 de Bob (medir qubit de Bob)
def passo5_Bob_mede_qubit_enviado_por_Alice(input_Alice, qc, q0, q1, q2, q2_ket, correcoes):
    st.markdown('### Passo 2 de Bob: Medição do qubit')
    
    # Aplica as correções (Z e X) no qubit 2
    for correcao in correcoes:
        if 'Z' in correcao:
            qc.z(2)
        elif 'X' in correcao:
            qc.x(2)
    
    qc.measure(2, 2)  # Mede o qubit 2
    st.write(qc.draw(output='mpl'))
    st.latex(r'| q_{{\text{{Bob}}}} \rangle = | q_{{\text{{2}}}} \rangle = ' + str(q2))
    return qc

# Função para o passo 6 de Bob (calcular resultado final)
def passo6_Bob_aplica_correcoes_obtem_resultado(input_Alice, qc, q0, q1, q2, q2_ket, matriz_resultante):
    st.markdown("### Passo 3 de Bob: Aplicação de correções")
    
    # Calcula o resultado final
    resultado_final = np.dot(matriz_resultante, q2_ket)
    st.latex(r'| U_{{\text{{Bob}}}} \rangle \times | q_{{\text{{2}}}} \rangle = ' +
             f'{matriz_para_latex(matriz_resultante)} \\times {matriz_para_latex(q2_ket)} = {matriz_para_latex(resultado_final)}')

    st.pyplot(plot_esfera_de_bloch(input_Alice))  
    st.write(qc.draw(output='mpl'))

    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    st.markdown("### Resultado Final Medido por Bob:")
    st.latex(r'| q_{{\text{{Bob}}}} \rangle = ' + str(q2))
    return qc

