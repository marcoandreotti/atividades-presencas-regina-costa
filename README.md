# Registro de Atividades e Presenças do Núcleo de Convivência Regina Costa

Aplicação web acadêmica para organizar atividades e registrar a situação de presença dos participantes nos encontros do Núcleo de Convivência Regina Costa.

## Objetivo do MVP

O MVP será desenvolvido como aplicação web responsiva para apoiar a equipe na organização de atividades e no registro de chamadas. A implementação seguirá os requisitos definidos nas experiências práticas anteriores:

- cadastrar atividades com título e data obrigatórios, e horário e descrição opcionais;
- consultar e selecionar uma atividade;
- registrar presença ou ausência de participantes fictícios;
- evitar mais de um registro para o mesmo participante na mesma atividade;
- permitir correção de uma chamada como evolução do fluxo inicial.

## Arquitetura e tecnologias

O sistema será um monólito organizado em camadas, desenvolvido em Python com Flask. As páginas serão renderizadas no servidor com Jinja, as entidades relacionais serão mapeadas com SQLAlchemy e o banco local do protótipo será SQLite.

```text
app/
├── models/       # Entidades e mapeamento relacional
├── repositories/ # Consultas e gravações no banco
├── routes/       # Rotas HTTP e integração com a interface
├── services/     # Casos de uso e regras de negócio
├── static/       # CSS e demais arquivos estáticos
└── templates/    # Páginas Jinja
instance/         # Banco SQLite local (ignorado pelo Git)
run.py            # Inicialização local da aplicação
```

## Situação atual

A estrutura inicial do projeto e os modelos das entidades Atividade, Participante e Presença estão preparados. As rotas e os casos de uso serão desenvolvidos gradativamente, com commits semânticos e revisão do próprio código por Pull Request.

Use apenas dados fictícios nas demonstrações. Este protótipo acadêmico não deve receber dados pessoais de participantes reais nem ser usado em produção.

## Licença

Nenhuma licença foi definida para este projeto. Sem uma licença explícita, não há concessão de permissão para reutilização ou redistribuição do código.

## Instalação e execução

### Softwares necessários

- **Git**, para obter o código e acompanhar as versões;
- **Python 3.12**, para executar a aplicação;
- um navegador web atualizado;
- um terminal (PowerShell no Windows, Terminal no macOS ou shell no Linux).

O SQLite é utilizado por meio do módulo incluído no Python; não é necessário instalar ou iniciar um servidor de banco de dados separado.

### Preparar o ambiente

Na pasta raiz do projeto, crie e ative um ambiente virtual:

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS ou Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Iniciar a aplicação

```bash
python run.py
```

Abra <http://127.0.0.1:5000> no navegador. O banco de desenvolvimento será criado em `instance/atividades.db` na primeira execução. Encerre o servidor com `Ctrl+C` no terminal.

## Histórico de desenvolvimento

O desenvolvimento será incremental. Para cada mudança, crie uma branch curta a partir de `main`, faça commits pequenos com mensagens no padrão `tipo: descrição` e abra um Pull Request para revisar a alteração antes de integrá-la.

Tipos de commit recomendados: `feat` para funcionalidade, `fix` para correção, `docs` para documentação, `refactor` para reorganização sem mudança de comportamento e `chore` para manutenção.

Exemplos:

```text
feat: adiciona cadastro de atividades
fix: impede presença duplicada na mesma atividade
docs: explica a execução local do projeto
```

Antes de concluir cada Pull Request, confira se a mudança atende ao requisito correspondente, revise os arquivos alterados e descreva o que foi feito e como foi verificado.

