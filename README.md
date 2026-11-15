# Saúde em Dia

Sistema web desenvolvido como MVP acadêmico para apoiar o trabalho de
Agentes Comunitários de Saúde (ACS) no cadastro de pacientes e no
acompanhamento de visitas domiciliares.

O projeto foi desenvolvido no contexto do curso de Análise e
Desenvolvimento de Sistemas, com foco em uma solução simples para
organizar informações e facilitar a consulta dos registros da microárea.

## Objetivo

O Saúde em Dia busca reunir, em um único ambiente, informações básicas
dos pacientes e registros de visitas domiciliares. A proposta é reduzir
a dependência de controles manuais dispersos e facilitar a localização
de cadastros, o acompanhamento das visitas e a consulta do histórico.

O projeto está relacionado ao **ODS 3 --- Saúde e Bem-Estar**,
especialmente à Meta 3.8, por apoiar indiretamente a organização e o
acompanhamento dos serviços de saúde.

## Funcionalidades

-   **Autenticação:** acesso ao sistema por usuário e senha, com
    verificação de senha armazenada em formato hash e opção de sair da
    sessão.
-   **Cadastro de pacientes:** inclusão de informações como nome, data
    de nascimento, endereço, telefone e número de cadastro.
-   **Consulta de pacientes:** listagem dos registros e pesquisa pelo
    nome.
-   **Edição de pacientes:** atualização das informações cadastradas.
-   **Agendamento de visitas:** registro de visitas domiciliares
    vinculadas a pacientes.
-   **Acompanhamento de visitas:** consulta do histórico e atualização
    do status da visita para agendada, concluída ou cancelada.
-   **Última visita concluída:** visualização da informação da visita
    concluída mais recente.
-   **Acessibilidade:** controle para aumentar ou restaurar o tamanho
    dos textos da interface, com preferência mantida no navegador.
-   **Testes automatizados:** testes das principais rotas relacionadas à
    autenticação e ao controle de acesso.
-   **Integração contínua:** execução automatizada dos testes pelo
    GitHub Actions em atualizações do repositório e em pull requests
    direcionados à branch principal.

## Tecnologias utilizadas

-   Python 3.13
-   Flask 3.1.3
-   SQLite
-   HTML5
-   CSS3
-   JavaScript
-   Git e GitHub
-   pytest e pytest-cov
-   GitHub Actions

## Estrutura do projeto

``` text
Saúde em Dia/
├── .github/
│   └── workflows/
│       └── testes.yml
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── acessibilidade.js
├── templates/
│   ├── login.html
│   ├── pacientes.html
│   └── visitas.html
├── tests/
│   └── test_app.py
├── app.py
├── database.py
├── criar_usuario.py
├── requirements.txt
├── README.md
└── .gitignore
```

O banco de dados SQLite é criado localmente pelo sistema e não deve ser
enviado ao repositório. A pasta do ambiente virtual (`venv`) e arquivos
temporários também são ignorados pelo Git.

## Como executar localmente

### 1. Pré-requisitos

-   Python 3.13 instalado.
-   Git (opcional, para clonar o repositório).

### 2. Obter o projeto

``` bash
git clone https://github.com/gabrielrochag30/saude-em-dia.git
cd saude-em-dia
```

### 3. Criar e ativar o ambiente virtual

No Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

``` powershell
python -m pip install -r requirements.txt
```

### 5. Configurar a chave de sessão

No PowerShell, gere uma chave secreta:

``` powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o valor gerado e configure a variável de ambiente no terminal:

``` powershell
$env:SECRET_KEY = "COLE_AQUI_A_CHAVE_GERADA"
```

A variável precisa estar configurada no terminal utilizado para iniciar
a aplicação. Não compartilhe a chave nem a inclua no repositório.

### 6. Criar um usuário de acesso

Execute o script de criação de usuário:

``` powershell
python criar_usuario.py
```

Siga as instruções apresentadas pelo script para cadastrar as
credenciais de acesso.

### 7. Iniciar a aplicação

``` powershell
python app.py
```

Acesse pelo navegador:

``` text
http://127.0.0.1:5000
```

## Executar os testes

Com o ambiente virtual ativado, instale as ferramentas de teste:

``` powershell
python -m pip install pytest pytest-cov
```

Execute:

``` powershell
python -m pytest --cov=app --cov=database --cov-report=term
```

Os testes utilizam um banco temporário, evitando que os dados locais da
aplicação sejam utilizados durante a execução.

## Integração contínua

O repositório possui um workflow do GitHub Actions em
`.github/workflows/testes.yml`. O pipeline configura o Python, instala
as dependências e executa os testes automatizados. A configuração é
acionada em atualizações de branches e em pull requests direcionados à
branch `main`.

## Observações e limitações

-   Este projeto é um **MVP acadêmico**, desenvolvido para demonstrar
    funcionalidades essenciais de cadastro e acompanhamento de visitas.
-   A aplicação foi projetada para execução local e demonstração. Não
    deve ser considerada um sistema pronto para uso com dados reais de
    saúde.
-   Utilize somente dados fictícios nos testes e nas demonstrações.
-   Antes de qualquer implantação real, seriam necessárias avaliações
    adicionais de segurança, privacidade, controle de acesso,
    infraestrutura, backups e conformidade com a legislação aplicável,
    incluindo a LGPD.
-   A chave secreta deve ser configurada por variável de ambiente e
    nunca armazenada no código-fonte.

## Repositório

[GitHub --- Saúde em
Dia](https://github.com/gabrielrochag30/saude-em-dia)

------------------------------------------------------------------------

Projeto acadêmico desenvolvido por Gabriel Rocha.
