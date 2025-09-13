# Módulo de Recepção Automatizada

"""
Este módulo é responsável pelo atendimento inicial dos pacientes,
coletando informações básicas como nome, CPF, data de nascimento e sintomas.
Ele será integrado com os módulos de áudio (STT/TTS) e interface gráfica.
"""

class Recepcao:
    def __init__(self):
        self.paciente_atual = {}

    def iniciar_atendimento(self):
        """Inicia o processo de atendimento e coleta de dados."""
        print("Bem-vindo ao nosso sistema de atendimento automatizado.")
        # Futuramente, aqui chamaremos as funções de TTS para falar
        # e STT/GUI para obter as respostas.
        self.coletar_nome()
        self.coletar_cpf()
        self.coletar_data_nascimento()
        self.coletar_sintomas()
        
        print("\nDados coletados:")
        for chave, valor in self.paciente_atual.items():
            print(f"{chave.replace('_', ' ').capitalize()}: {valor}")
        
        # Aqui, os dados seriam enviados para o módulo de triagem
        # e para o banco de dados.
        return self.paciente_atual

    def coletar_nome(self):
        """Coleta o nome do paciente."""
        # Simulação de entrada - será substituído por STT/GUI
        nome = input("Por favor, diga ou digite seu nome completo: ")
        self.paciente_atual["nome_completo"] = nome
        print(f"Nome registrado: {nome}")

    def coletar_cpf(self):
        """Coleta o CPF do paciente e realiza uma validação simples de formato."""
        while True:
            # Simulação de entrada - será substituído por STT/GUI
            cpf = input("Por favor, informe seu CPF (apenas números): ")
            if cpf.isdigit() and len(cpf) == 11:
                self.paciente_atual["cpf"] = cpf
                print(f"CPF registrado: {cpf}")
                break
            else:
                print("CPF inválido. Por favor, insira 11 dígitos numéricos.")
                # Futuramente, TTS para informar o erro.

    def coletar_data_nascimento(self):
        """Coleta a data de nascimento do paciente (formato DD/MM/AAAA)."""
        while True:
            # Simulação de entrada - será substituído por STT/GUI
            data_nasc = input("Qual sua data de nascimento (DD/MM/AAAA)? ")
            # Validação simples de formato (pode ser melhorada com regex ou datetime)
            if len(data_nasc) == 10 and data_nasc[2] == '/' and data_nasc[5] == '/' and data_nasc[:2].isdigit() and data_nasc[3:5].isdigit() and data_nasc[6:].isdigit():
                self.paciente_atual["data_nascimento"] = data_nasc
                print(f"Data de nascimento registrada: {data_nasc}")
                break
            else:
                print("Formato de data inválido. Use DD/MM/AAAA.")
                # Futuramente, TTS para informar o erro.

    def coletar_sintomas(self):
        """Coleta os sintomas relatados pelo paciente."""
        # Simulação de entrada - será substituído por STT/GUI
        sintomas = input("Por favor, descreva seus sintomas: ")
        self.paciente_atual["sintomas"] = sintomas
        print(f"Sintomas registrados: {sintomas}")

if __name__ == '__main__':
    print("Iniciando simulação do módulo de recepção...")
    recepcao = Recepcao()
    dados_paciente = recepcao.iniciar_atendimento()
    print("\nSimulação do módulo de recepção concluída.")
    print("Dados finais do paciente:", dados_paciente)

