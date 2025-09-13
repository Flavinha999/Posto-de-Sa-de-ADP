# Sistema de Recepção Inteligente para Posto de Saúde

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?style=for-the-badge&logo=postgresql)
![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?style=for-the-badge&logo=microsoftazure)

## 📚 Sobre o Projeto

Este projeto visa desenvolver um sistema inteligente de primeira recepção para um posto de saúde público, utilizando Python e Streamlit. O objetivo principal é agilizar o atendimento inicial e priorizar pacientes com base nos sintomas relatados através de uma interface gráfica intuitiva. A versão atual foi modificada para operar exclusivamente via interface gráfica, removendo funcionalidades de áudio, e migrada para utilizar **PostgreSQL no Azure** como banco de dados, garantindo escalabilidade, segurança e acessibilidade em nuvem.

## ✨ Funcionalidades

- **Recepção Automatizada:** Coleta de informações básicas do paciente (nome, CPF, data de nascimento, sintomas) via interface gráfica.
- **Triagem Automatizada por IA:** Classificação do nível de prioridade do atendimento (Emergência, Urgência, Prioridade, Comum) com base nos sintomas, utilizando regras médicas simples.
- **Interface Gráfica Intuitiva:** Desenvolvida com Streamlit, oferece feedback visual claro e é acessível para diferentes níveis de familiaridade com tecnologia.
- **Integração com Banco de Dados:** Registro persistente de informações de pacientes e resultados de triagem no PostgreSQL no Azure.
- **Modularidade:** Arquitetura que facilita a manutenção, evolução e adição de novos módulos.
- **Segurança e Privacidade:** Conformidade com a LGPD, controle de acesso, criptografia de dados sensíveis e registros de auditoria.

## 🚀 Como Começar

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

Certifique-se de ter instalado:

- [Python 3.10 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- Uma conta Azure com permissões para criar recursos de PostgreSQL.

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Configurar Banco de Dados PostgreSQL no Azure

1.  **Acesse o Portal do Azure:** Vá para [https://portal.azure.com](https://portal.azure.com).
2.  **Crie um Recurso de "Azure Database for PostgreSQL - Flexible Server"**.
    *   **Nome do servidor:** Escolha um nome único (ex: `posto-saude-db-server`).
    *   **Versão:** PostgreSQL 13 ou superior.
    *   **Localização:** Escolha a região mais próxima.
    *   **Método de autenticação:** Autenticação do PostgreSQL.
    *   **Nome de usuário admin:** `seu_usuario` (anote este nome, será `AZURE_POSTGRES_USER`).
    *   **Senha:** Crie uma senha segura (anote, será `AZURE_POSTGRES_PASSWORD`).
3.  **Configure o Firewall:** No seu servidor PostgreSQL no Azure, vá em "Segurança" → "Rede" e adicione regras para permitir o acesso do seu IP local e/ou de serviços do Azure.
4.  **Crie o Banco de Dados:** Em "Bancos de dados", adicione um novo banco com o nome `posto_saude` (será `AZURE_POSTGRES_DATABASE`).

### 3. Configuração do Ambiente Local

1.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure as Variáveis de Ambiente:**
    *   Copie o arquivo de exemplo: `cp .env.example .env`
    *   Edite o arquivo `.env` com as credenciais do seu banco de dados Azure PostgreSQL:
        ```env
        AZURE_POSTGRES_HOST=seu-servidor.postgres.database.azure.com
        AZURE_POSTGRES_DATABASE=posto_saude
        AZURE_POSTGRES_USER=seu_usuario@seu-servidor
        AZURE_POSTGRES_PASSWORD=sua_senha_segura
        AZURE_POSTGRES_PORT=5432
        AZURE_POSTGRES_SSLMODE=require
        ```

### 4. Testar Conexão com o Banco de Dados

```bash
python src/banco_dados/banco_dados_utils.py
```

Se a mensagem "Conexão com PostgreSQL estabelecida com sucesso!" aparecer, a configuração está correta.

### 5. Migração de Dados (Opcional)

Se você possuía dados em uma versão anterior do projeto com SQLite e deseja migrá-los para o PostgreSQL:

```bash
python migrar_dados_sqlite_para_postgresql.py
```

### 6. Executar a Aplicação

```bash
streamlit run src/interface/main_app.py
```

A aplicação estará disponível em `http://localhost:8501`.

## 📁 Estrutura do Projeto

```
.env.example
.env
README.md
requirements.txt
migrar_dados_sqlite_para_postgresql.py
src/
├── banco_dados/
│   ├── banco_dados_utils.py
│   ├── banco_dados_utils_postgresql.py
│   └── config.py
├── interface/
│   └── main_app.py
├── recepcao/
│   └── recepcao_automatizada.py
└── triagem/
    └── triagem_ia.py
```

## 🛠️ Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Streamlit:** Para a construção da interface gráfica web.
- **PostgreSQL:** Sistema de gerenciamento de banco de dados relacional.
- **Azure Database for PostgreSQL:** Serviço de banco de dados em nuvem.
- **`python-dotenv`:** Para gerenciamento de variáveis de ambiente.
- **`psycopg2-binary`:** Driver Python para PostgreSQL.

## ⚠️ Solução de Problemas Comuns

### Erro de Conexão com o Banco de Dados

Se você receber um erro como `connection failed` ou `FATAL: password authentication failed`:

- Verifique se as credenciais no seu arquivo `.env` estão corretas.
- Certifique-se de que o firewall do Azure permite o acesso do seu IP.
- Confirme que o servidor PostgreSQL no Azure está ativo.
- Para o usuário, use o formato `seu_usuario@seu-servidor`.

### Erro de Instalação do `psycopg2-binary` (no Windows)

Se você encontrar erros de compilação (`Microsoft Visual C++ 14.0 or greater is required` ou `fatal error LNK1120`):

- Instale as [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) e selecione "Desenvolvimento para desktop com C++".
- **Recomendado:** Use uma versão do Python como 3.10, 3.11 ou 3.12, pois o `psycopg2-binary` tem binários pré-compilados mais estáveis para essas versões no Windows.

##  Imagens 


<img width="1861" height="875" alt="Captura de tela 2025-09-13 015118" src="https://github.com/user-attachments/assets/873bf179-d31e-43fe-949e-f551ec915a3d" />
<img width="1887" height="874" alt="Captura de tela 2025-09-13 015002" src="https://github.com/user-attachments/assets/fa7a6234-b63e-46e9-b281-f296f4c748b9" />

## Video 



https://github.com/user-attachments/assets/727fd14c-05ef-4afa-b3f5-876422fb1c9c



## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Se aplicável, crie um arquivo LICENSE no seu repositório).

---
