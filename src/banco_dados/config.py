# Configuração do Banco de Dados

"""
Este módulo carrega as configurações do banco de dados PostgreSQL
a partir de variáveis de ambiente ou arquivo .env
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env se existir
load_dotenv()

class DatabaseConfig:
    """Configurações do banco de dados PostgreSQL no Azure"""
    
    HOST = os.getenv('AZURE_POSTGRES_HOST')
    DATABASE = os.getenv('AZURE_POSTGRES_DATABASE', 'posto_saude')
    USER = os.getenv('AZURE_POSTGRES_USER')
    PASSWORD = os.getenv('AZURE_POSTGRES_PASSWORD')
    PORT = int(os.getenv('AZURE_POSTGRES_PORT', '5432'))
    SSLMODE = os.getenv('AZURE_POSTGRES_SSLMODE', 'require')
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        required_vars = ['HOST', 'DATABASE', 'USER', 'PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(f'AZURE_POSTGRES_{var}')
        
        if missing_vars:
            raise ValueError(
                f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}\n"
                f"Crie um arquivo .env baseado no .env.example ou defina essas variáveis no sistema."
            )
        
        return True
    
    @classmethod
    def get_connection_string(cls):
        """Retorna a string de conexão para o PostgreSQL"""
        cls.validate()
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'port': cls.PORT,
            'sslmode': cls.SSLMODE
        }

