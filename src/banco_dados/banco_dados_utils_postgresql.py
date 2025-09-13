# Módulo de Utilitários de Banco de Dados (PostgreSQL - Azure)

"""
Este módulo gerencia a interação com o banco de dados PostgreSQL no Azure,
armazenando informações dos pacientes e os resultados da triagem.
"""

import psycopg2
import psycopg2.extras
import os
from datetime import datetime
from typing import Optional, Dict, List

class BancoDadosUtils:
    def __init__(self):
        """Inicializa a conexão com o banco de dados PostgreSQL no Azure."""
        from .config import DatabaseConfig
        
        # Carregar configurações
        self.config = DatabaseConfig.get_connection_string()
        self.host = self.config['host']
        self.database = self.config['database']
        self.user = self.config['user']
        self.password = self.config['password']
        self.port = self.config['port']
        self.sslmode = self.config['sslmode']
        
        self._criar_tabelas()

    def _conectar(self):
        """Retorna uma conexão com o banco de dados PostgreSQL."""
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode=self.sslmode
            )
            return conn
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def _criar_tabelas(self):
        """Cria as tabelas 'pacientes' e 'triagens' se elas não existirem."""
        conn = self._conectar()
        cursor = conn.cursor()
        
        try:
            # Tabela de Pacientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id SERIAL PRIMARY KEY,
                    nome_completo VARCHAR(255) NOT NULL,
                    cpf VARCHAR(11) NOT NULL UNIQUE,
                    data_nascimento DATE NOT NULL,
                    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de Triagens
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS triagens (
                    id SERIAL PRIMARY KEY,
                    paciente_id INTEGER NOT NULL,
                    sintomas TEXT NOT NULL,
                    prioridade VARCHAR(50) NOT NULL CHECK (prioridade IN ('Emergência', 'Urgência', 'Prioridade', 'Comum')),
                    justificativa_triagem TEXT,
                    data_triagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
                )
            """)

            # Criar índices para melhor performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pacientes_cpf ON pacientes(cpf)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_triagens_paciente_id ON triagens(paciente_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_triagens_data ON triagens(data_triagem)")

            conn.commit()
            print("Tabelas criadas/verificadas com sucesso no PostgreSQL.")
            
        except psycopg2.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def adicionar_paciente(self, nome_completo: str, cpf: str, data_nascimento: str) -> Optional[int]:
        """
        Adiciona um novo paciente ao banco de dados. 
        Retorna o ID do paciente ou None em caso de erro.
        
        Args:
            nome_completo: Nome completo do paciente
            cpf: CPF do paciente (apenas números)
            data_nascimento: Data de nascimento no formato DD/MM/AAAA
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        try:
            # Converter data do formato brasileiro para formato PostgreSQL
            data_nascimento_formatada = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
            
            cursor.execute("""
                INSERT INTO pacientes (nome_completo, cpf, data_nascimento)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (nome_completo, cpf, data_nascimento_formatada))
            
            paciente_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Paciente {nome_completo} (CPF: {cpf}) adicionado com ID: {paciente_id}")
            return paciente_id
            
        except psycopg2.IntegrityError:
            print(f"Erro: CPF {cpf} já cadastrado.")
            conn.rollback()
            # Recuperar ID do paciente existente
            cursor.execute("SELECT id FROM pacientes WHERE cpf = %s", (cpf,))
            paciente_existente = cursor.fetchone()
            return paciente_existente[0] if paciente_existente else None
            
        except Exception as e:
            print(f"Erro ao adicionar paciente: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def adicionar_triagem(self, paciente_id: int, sintomas: str, prioridade: str, justificativa: str) -> Optional[int]:
        """
        Adiciona um novo registro de triagem para um paciente. 
        Retorna o ID da triagem ou None.
        
        Args:
            paciente_id: ID do paciente
            sintomas: Descrição dos sintomas
            prioridade: Nível de prioridade (Emergência, Urgência, Prioridade, Comum)
            justificativa: Justificativa da triagem
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO triagens (paciente_id, sintomas, prioridade, justificativa_triagem)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (paciente_id, sintomas, prioridade, justificativa))
            
            triagem_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Triagem para paciente ID {paciente_id} adicionada com ID: {triagem_id} (Prioridade: {prioridade})")
            return triagem_id
            
        except Exception as e:
            print(f"Erro ao adicionar triagem: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def buscar_paciente_por_cpf(self, cpf: str) -> Optional[Dict]:
        """
        Busca um paciente pelo CPF. 
        Retorna um dicionário com os dados ou None.
        
        Args:
            cpf: CPF do paciente
        """
        conn = self._conectar()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT id, nome_completo, cpf, data_nascimento, data_registro 
                FROM pacientes WHERE cpf = %s
            """, (cpf,))
            
            paciente = cursor.fetchone()
            if paciente:
                # Converter data_nascimento para formato brasileiro
                paciente_dict = dict(paciente)
                if paciente_dict['data_nascimento']:
                    paciente_dict['data_nascimento'] = paciente_dict['data_nascimento'].strftime("%d/%m/%Y")
                return paciente_dict
            return None
            
        except Exception as e:
            print(f"Erro ao buscar paciente por CPF: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def buscar_triagens_paciente(self, paciente_id: int) -> List[Dict]:
        """
        Busca todos os registros de triagem de um paciente. 
        Retorna uma lista de dicionários.
        
        Args:
            paciente_id: ID do paciente
        """
        conn = self._conectar()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT id, paciente_id, sintomas, prioridade, justificativa_triagem, data_triagem 
                FROM triagens 
                WHERE paciente_id = %s 
                ORDER BY data_triagem DESC
            """, (paciente_id,))
            
            triagens = cursor.fetchall()
            return [dict(triagem) for triagem in triagens]
            
        except Exception as e:
            print(f"Erro ao buscar triagens do paciente: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def listar_pacientes_por_prioridade(self, prioridade: str = None) -> List[Dict]:
        """
        Lista pacientes com suas últimas triagens, opcionalmente filtrados por prioridade.
        
        Args:
            prioridade: Filtro de prioridade (opcional)
        """
        conn = self._conectar()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        try:
            if prioridade:
                cursor.execute("""
                    SELECT DISTINCT p.id, p.nome_completo, p.cpf, t.prioridade, t.data_triagem
                    FROM pacientes p
                    JOIN triagens t ON p.id = t.paciente_id
                    WHERE t.prioridade = %s
                    AND t.data_triagem = (
                        SELECT MAX(t2.data_triagem) 
                        FROM triagens t2 
                        WHERE t2.paciente_id = p.id
                    )
                    ORDER BY t.data_triagem DESC
                """, (prioridade,))
            else:
                cursor.execute("""
                    SELECT DISTINCT p.id, p.nome_completo, p.cpf, t.prioridade, t.data_triagem
                    FROM pacientes p
                    JOIN triagens t ON p.id = t.paciente_id
                    WHERE t.data_triagem = (
                        SELECT MAX(t2.data_triagem) 
                        FROM triagens t2 
                        WHERE t2.paciente_id = p.id
                    )
                    ORDER BY 
                        CASE t.prioridade 
                            WHEN 'Emergência' THEN 1
                            WHEN 'Urgência' THEN 2
                            WHEN 'Prioridade' THEN 3
                            WHEN 'Comum' THEN 4
                        END,
                        t.data_triagem DESC
                """)
            
            pacientes = cursor.fetchall()
            return [dict(paciente) for paciente in pacientes]
            
        except Exception as e:
            print(f"Erro ao listar pacientes: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def testar_conexao(self) -> bool:
        """Testa a conexão com o banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            print("Conexão com PostgreSQL estabelecida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao conectar com PostgreSQL: {e}")
            return False


if __name__ == '__main__':
    print("Iniciando teste do módulo de Banco de Dados PostgreSQL...")
    
    # Para teste, você precisa definir as variáveis de ambiente ou passar os parâmetros
    # Exemplo de uso com variáveis de ambiente:
    # export AZURE_POSTGRES_HOST="meuservidor.postgres.database.azure.com"
    # export AZURE_POSTGRES_DATABASE="posto_saude"
    # export AZURE_POSTGRES_USER="meuusuario@meuservidor"
    # export AZURE_POSTGRES_PASSWORD="minhasenha"
    
    try:
        db_utils = BancoDadosUtils()
        
        # Testar conexão
        if not db_utils.testar_conexao():
            print("Falha na conexão. Verifique as configurações.")
            exit(1)

        # Teste Adicionar Paciente
        paciente_id1 = db_utils.adicionar_paciente("João da Silva", "11122233344", "01/01/1980")
        paciente_id2 = db_utils.adicionar_paciente("Maria Oliveira", "55566677788", "15/05/1992")
        
        if paciente_id1:
            # Teste Adicionar Triagem
            db_utils.adicionar_triagem(paciente_id1, "Dor de cabeça forte e febre", "Prioridade", 
                                     "Paciente relata dor de cabeça intensa e febre há 2 dias.")
            db_utils.adicionar_triagem(paciente_id1, "Tosse leve", "Comum", 
                                     "Paciente com tosse seca há 1 dia.")

        if paciente_id2:
            db_utils.adicionar_triagem(paciente_id2, "Falta de ar intensa e dor no peito", "Emergência", 
                                     "Sintomas clássicos de emergência cardíaca.")

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

        # Teste Listar Pacientes por Prioridade
        print("\nListando pacientes com prioridade 'Emergência':")
        pacientes_emergencia = db_utils.listar_pacientes_por_prioridade("Emergência")
        for paciente in pacientes_emergencia:
            print(paciente)

        print("\nTeste do módulo de Banco de Dados PostgreSQL concluído.")
        
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        print("\nPara usar este módulo, defina as seguintes variáveis de ambiente:")
        print("AZURE_POSTGRES_HOST=seu-servidor.postgres.database.azure.com")
        print("AZURE_POSTGRES_DATABASE=nome_do_banco")
        print("AZURE_POSTGRES_USER=usuario@servidor")
        print("AZURE_POSTGRES_PASSWORD=sua_senha")
    except Exception as e:
        print(f"Erro durante o teste: {e}")

