# Módulo de Utilitários de Banco de Dados (SQLite)

"""
Este módulo gerencia a interação com o banco de dados SQLite,
armazenando informações dos pacientes e os resultados da triagem.
"""

import sqlite3
import os
from datetime import datetime

DB_NAME = "posto_saude.db"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", DB_NAME)

class BancoDadosUtils:
    def __init__(self, db_path=DB_PATH):
        """Inicializa a conexão com o banco de dados e cria as tabelas se não existirem."""
        # Garante que o diretório data exista
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._criar_tabelas()

    def _conectar(self):
        """Retorna uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)

    def _criar_tabelas(self):
        """Cria as tabelas 'pacientes' e 'triagens' se elas não existirem."""
        conn = self._conectar()
        cursor = conn.cursor()

        # Tabela de Pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                data_nascimento TEXT NOT NULL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de Triagens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS triagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                sintomas TEXT NOT NULL,
                prioridade TEXT NOT NULL, -- Emergência, Urgência, Prioridade, Comum
                justificativa_triagem TEXT,
                data_triagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
            )
        """)

        conn.commit()
        conn.close()

    def adicionar_paciente(self, nome_completo: str, cpf: str, data_nascimento: str) -> int | None:
        """Adiciona um novo paciente ao banco de dados. Retorna o ID do paciente ou None em caso de erro."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pacientes (nome_completo, cpf, data_nascimento)
                VALUES (?, ?, ?)
            """, (nome_completo, cpf, data_nascimento))
            conn.commit()
            paciente_id = cursor.lastrowid
            print(f"Paciente {nome_completo} (CPF: {cpf}) adicionado com ID: {paciente_id}")
            return paciente_id
        except sqlite3.IntegrityError:
            print(f"Erro: CPF {cpf} já cadastrado.")
            # Recuperar ID do paciente existente
            cursor.execute("SELECT id FROM pacientes WHERE cpf = ?", (cpf,))
            paciente_existente = cursor.fetchone()
            return paciente_existente[0] if paciente_existente else None
        except Exception as e:
            print(f"Erro ao adicionar paciente: {e}")
            return None
        finally:
            conn.close()

    def adicionar_triagem(self, paciente_id: int, sintomas: str, prioridade: str, justificativa: str) -> int | None:
        """Adiciona um novo registro de triagem para um paciente. Retorna o ID da triagem ou None."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO triagens (paciente_id, sintomas, prioridade, justificativa_triagem)
                VALUES (?, ?, ?, ?)
            """, (paciente_id, sintomas, prioridade, justificativa))
            conn.commit()
            triagem_id = cursor.lastrowid
            print(f"Triagem para paciente ID {paciente_id} adicionada com ID: {triagem_id} (Prioridade: {prioridade})")
            return triagem_id
        except Exception as e:
            print(f"Erro ao adicionar triagem: {e}")
            return None
        finally:
            conn.close()

    def buscar_paciente_por_cpf(self, cpf: str) -> dict | None:
        """Busca um paciente pelo CPF. Retorna um dicionário com os dados ou None."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome_completo, cpf, data_nascimento, data_registro FROM pacientes WHERE cpf = ?", (cpf,))
            paciente = cursor.fetchone()
            if paciente:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, paciente))
            return None
        except Exception as e:
            print(f"Erro ao buscar paciente por CPF: {e}")
            return None
        finally:
            conn.close()

    def buscar_triagens_paciente(self, paciente_id: int) -> list[dict]:
        """Busca todos os registros de triagem de um paciente. Retorna uma lista de dicionários."""
        conn = self._conectar()
        cursor = conn.cursor()
        triagens_lista = []
        try:
            cursor.execute("""
                SELECT id, paciente_id, sintomas, prioridade, justificativa_triagem, data_triagem 
                FROM triagens WHERE paciente_id = ? ORDER BY data_triagem DESC
            """, (paciente_id,))
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            for linha in resultados:
                triagens_lista.append(dict(zip(colunas, linha)))
            return triagens_lista
        except Exception as e:
            print(f"Erro ao buscar triagens do paciente: {e}")
            return []
        finally:
            conn.close()

if __name__ == '__main__':
    print("Iniciando teste do módulo de Banco de Dados...")
    # Ajustar o path para execução direta do script para teste
    # O DB será criado em ../../data/posto_saude.db relativo a este script
    # Se src/banco_dados/banco_dados_utils.py, então ../../data/
    db_utils = BancoDadosUtils()

    # Teste Adicionar Paciente
    paciente_id1 = db_utils.adicionar_paciente("João da Silva", "11122233344", "01/01/1980")
    paciente_id2 = db_utils.adicionar_paciente("Maria Oliveira", "55566677788", "15/05/1992")
    paciente_id_repetido = db_utils.adicionar_paciente("João da Silva", "11122233344", "01/01/1980") # Teste de CPF duplicado

    if paciente_id1:
        # Teste Adicionar Triagem
        db_utils.adicionar_triagem(paciente_id1, "Dor de cabeça forte e febre", "Prioridade", "Paciente relata dor de cabeça intensa e febre há 2 dias.")
        db_utils.adicionar_triagem(paciente_id1, "Tosse leve", "Comum", "Paciente com tosse seca há 1 dia.")

    if paciente_id2:
        db_utils.adicionar_triagem(paciente_id2, "Falta de ar intensa e dor no peito", "Emergência", "Sintomas clássicos de emergência cardíaca.")

    # Teste Buscar Paciente
    print("\nBuscando paciente CPF 11122233344:")
    paciente_encontrado = db_utils.buscar_paciente_por_cpf("11122233344")
    if paciente_encontrado:
        print(paciente_encontrado)
        # Teste Buscar Triagens do Paciente
        print(f"\nBuscando triagens do paciente ID {paciente_encontrado['id']}:")
        triagens = db_utils.buscar_triagens_paciente(paciente_encontrado['id'])
        for triagem in triagens:
            print(triagem)
    else:
        print("Paciente não encontrado.")

    print("\nBuscando paciente CPF 99999999999 (inexistente):")
    paciente_nao_encontrado = db_utils.buscar_paciente_por_cpf("99999999999")
    if not paciente_nao_encontrado:
        print("Paciente não encontrado, como esperado.")

    print("\nTeste do módulo de Banco de Dados concluído.")

