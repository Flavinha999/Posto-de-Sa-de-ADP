# Módulo de Triagem Inteligente por IA

"""
Este módulo é responsável por realizar uma triagem inteligente com base nos
sintomas relatados pelo paciente, classificando o nível de prioridade do atendimento.
Utiliza uma base de regras médicas simples.
"""

class TriagemIA:
    def __init__(self):
        # Definição de palavras-chave para cada nível de prioridade
        # Esta é uma simplificação e deve ser expandida/validada por profissionais de saúde
        self.regras_triagem = {
            "emergencia": [
                "dor no peito intensa", "dor forte no peito", "aperto no peito",
                "falta de ar grave", "dificuldade respiratória severa",
                "sangramento intenso", "hemorragia",
                "perda de consciência", "desmaio",
                "convulsão",
                "parada cardíaca", "parada respiratória",
                "sintomas de avc", "dormência súbita", "fraqueza facial"
            ],
            "urgencia": [
                "febre alta persistente", "febre acima de 39",
                "fratura exposta", "osso quebrado visível",
                "dor abdominal forte", "dor abdominal intensa",
                "vômito persistente com sangue", "diarreia com sangue",
                "queimadura grave",
                "reação alérgica grave", "inchaço na garganta"
            ],
            "prioridade": [
                "dor de cabeça forte", "dor de cabeça persistente",
                "tontura frequente", "vertigem",
                "vômitos repetidos", "náusea intensa",
                "dor moderada", "ferimento que precisa de sutura",
                "sintomas gripais intensos", "piora de condição crônica"
            ],
            "comum": [
                "resfriado leve", "coriza", "espirros",
                "dor de garganta leve",
                "tosse leve", "mal-estar geral",
                "dor muscular leve", "consulta de rotina", "retorno"
            ]
        }

    def classificar_prioridade(self, sintomas_texto: str) -> tuple[str, str]:
        """
        Classifica a prioridade com base nos sintomas fornecidos.

        Args:
            sintomas_texto (str): Descrição dos sintomas pelo paciente.

        Returns:
            tuple[str, str]: (Nível de prioridade, Justificativa simplificada)
        """
        sintomas_lower = sintomas_texto.lower()

        for palavra_chave in self.regras_triagem["emergencia"]:
            if palavra_chave in sintomas_lower:
                return "Emergência", f"Sintoma indicativo de emergência detectado: '{palavra_chave}'."

        for palavra_chave in self.regras_triagem["urgencia"]:
            if palavra_chave in sintomas_lower:
                return "Urgência", f"Sintoma indicativo de urgência detectado: '{palavra_chave}'."

        for palavra_chave in self.regras_triagem["prioridade"]:
            if palavra_chave in sintomas_lower:
                return "Prioridade", f"Sintoma indicativo de atendimento prioritário detectado: '{palavra_chave}'."
        
        # Se nenhuma palavra-chave de maior prioridade for encontrada, verifica para comum
        # ou classifica como comum por padrão se nenhuma regra específica for atendida.
        for palavra_chave in self.regras_triagem["comum"]:
            if palavra_chave in sintomas_lower:
                return "Comum", f"Sintoma indicativo de atendimento comum detectado: '{palavra_chave}'."

        return "Comum", "Nenhum sintoma de alta prioridade identificado explicitamente. Classificado como comum para avaliação médica."

if __name__ == '__main__':
    print("Iniciando simulação do módulo de Triagem IA...")
    triagem_ia = TriagemIA()

    # Casos de teste
    sintomas_paciente1 = "Estou com uma dor no peito intensa e falta de ar grave."
    prioridade1, justificativa1 = triagem_ia.classificar_prioridade(sintomas_paciente1)
    print(f"Paciente 1 - Sintomas: {sintomas_paciente1}")
    print(f"Prioridade: {prioridade1} - Justificativa: {justificativa1}\n")

    sintomas_paciente2 = "Tenho tido febre alta persistente nos últimos dois dias."
    prioridade2, justificativa2 = triagem_ia.classificar_prioridade(sintomas_paciente2)
    print(f"Paciente 2 - Sintomas: {sintomas_paciente2}")
    print(f"Prioridade: {prioridade2} - Justificativa: {justificativa2}\n")

    sintomas_paciente3 = "Minha dor de cabeça está muito forte e não passa."
    prioridade3, justificativa3 = triagem_ia.classificar_prioridade(sintomas_paciente3)
    print(f"Paciente 3 - Sintomas: {sintomas_paciente3}")
    print(f"Prioridade: {prioridade3} - Justificativa: {justificativa3}\n")

    sintomas_paciente4 = "Acho que peguei um resfriado leve, só coriza."
    prioridade4, justificativa4 = triagem_ia.classificar_prioridade(sintomas_paciente4)
    print(f"Paciente 4 - Sintomas: {sintomas_paciente4}")
    print(f"Prioridade: {prioridade4} - Justificativa: {justificativa4}\n")

    sintomas_paciente5 = "Me sinto um pouco enjoado."
    prioridade5, justificativa5 = triagem_ia.classificar_prioridade(sintomas_paciente5)
    print(f"Paciente 5 - Sintomas: {sintomas_paciente5}")
    print(f"Prioridade: {prioridade5} - Justificativa: {justificativa5}\n")
    
    print("Simulação do módulo de Triagem IA concluída.")

