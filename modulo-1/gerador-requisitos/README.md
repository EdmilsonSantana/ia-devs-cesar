# Gerador e Validador de Documentação de Requisitos com IA

Esta aplicação de linha de comando gera documentação de requisitos usando IA, valida esses requisitos através de iterações automáticas até que todos os critérios sejam aceitáveis, e produz um documento PDF final simplificado.

## ✨ Características Principais

- **Geração automática** de documentação de requisitos usando IA
- **Validação iterativa** que refina automaticamente os requisitos até eliminar critérios "Inaceitáveis"
- **Processo inteligente** que para quando todos os critérios são aceitáveis ou após máximo de 3 iterações
- **PDF final simplificado** contendo apenas o documento refinado
- **Interface clara** com feedback visual do progresso

## 📋 Requisitos

- Python 3.12+
- Bibliotecas Python (veja `requirements.txt`):
  - openai >= 1.0.0
  - fpdf >= 1.7.2
  - rich >= 12.0.0
  - python-dotenv >= 1.0.0

## 🚀 Instalação

### Opção 1: pip tradicional
```bash
pip install -r requirements.txt
```

### Opção 2: uv (recomendado para Python 3.12+)
```bash
uv sync
```

## ⚙️ Configuração

### Configuração da API OpenAI

Configure sua chave de API da OpenAI criando um arquivo `.env`:

```bash
# Crie o arquivo .env na raiz do projeto
OPENAI_API_KEY=sua_chave_api_aqui
```

**Alternativa - Variável de ambiente:**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sua_chave_api_aqui"

# Linux/MacOS
export OPENAI_API_KEY="sua_chave_api_aqui"
```

## 🎯 Uso

Execute o script com os argumentos necessários:

```bash
python gerar_validar_docs.py --titulo "Nome da Aplicação" --conceito "Descrição detalhada" --publico "Público-alvo" --foco "Foco principal"
```

Exemplo:

```bash
uv run gerar_validar_docs.py --titulo "Sistema de Gerenciamento Inteligente de Energia" --conceito "Um sistema IoT e IA que monitora e controla o consumo de energia (iluminação, HVAC, equipamentos) em grandes edifícios comerciais. Ele aprende os padrões de uso, considera tarifas de energia variáveis, previsão do tempo e ocupação do edifício para otimizar o consumo, reduzir custos e minimizar o impacto ambiental, permitindo também o controle manual e relatórios detalhados para os gestores do edifício." --publico "Gestores de Facilities, Engenheiros de Manutenção, Diretores Financeiros de empresas proprietárias de edifícios comerciais." --foco "Lógica de otimização de consumo baseada em IA e a interface de controle e relatórios para os gestores."
```
### Parâmetros Obrigatórios

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `--titulo` | Título da aplicação | "App de Gestão de Tarefas" |
| `--conceito` | Descrição detalhada do conceito | "Aplicativo para gerenciar tarefas com sync" |
| `--publico` | Público-alvo principal | "Profissionais ocupados" |
| `--foco` | Foco dos requisitos | "Eficiência e produtividade" |

### Parâmetros Opcionais

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--modelo` | Modelo de IA a usar | "gpt-4o" |

## 📝 Exemplo Prático

```bash
python gerar_validar_docs.py \
  --titulo "EcoTask" \
  --conceito "Aplicativo de gestão de tarefas com gamificação e impacto ambiental" \
  --publico "Jovens profissionais conscientes ambientalmente" \
  --foco "Engajamento através de gamificação sustentável"
```

## 🔄 Fluxo de Funcionamento (Novo - Iterativo)

O processo foi otimizado para garantir qualidade através de iterações automáticas:

### 1. **Geração Inicial**
- Executa o prompt em `prompt_gerar_docs.md` com os parâmetros fornecidos
- Gera documentação inicial com critérios de aceitação

### 2. **Processo Iterativo de Validação** (⭐ Nova Funcionalidade)
- **Validação**: Analisa a documentação usando `prompt_validar_docs.md`
- **Verificação**: Identifica critérios com avaliação "Inaceitável"
- **Refinamento**: Se encontrados problemas, refina automaticamente a documentação
- **Repetição**: Repete até não haver critérios inaceitáveis (máximo 3 iterações)

### 3. **Finalização**
- ✅ **Sucesso**: Para quando todos os critérios são aceitáveis
- ⚠️ **Limite**: Para após 3 iterações mesmo com critérios pendentes
- 📄 **PDF Final**: Gera documento simplificado apenas com a versão final

### 🎯 Benefícios do Processo Iterativo
- **Qualidade garantida**: Elimina automaticamente critérios inadequados
- **Eficiência**: Para assim que atinge qualidade aceitável
- **Transparência**: Mostra progresso e problemas encontrados em cada iteração

## 📂 Estrutura de Arquivos

```
curso-ia/
├── gerar_validar_docs.py          # Script principal
├── prompt_gerar_docs.md           # Prompt para geração de requisitos
├── prompt_validar_docs.md         # Prompt para validação de requisitos
├── requirements.txt               # Dependências Python
├── pyproject.toml                # Configuração do projeto
├── .python-version               # Versão do Python (3.12)
├── uv.lock                       # Lock file para uv
└── README.md                     # Este arquivo
```

## 📋 Saída do Processo

### Durante a Execução
- **Feedback visual**: Progresso colorido no terminal
- **Detalhes das iterações**: Mostra critérios problemáticos encontrados
- **Status de cada etapa**: Geração → Validação → Refinamento

### Arquivo Final
- **Nome**: `requisitos_final_AAAAMMDD_HHMMSS.pdf`
- **Conteúdo**: Apenas o documento final refinado
- **Formato**: PDF simples e limpo, otimizado para POC

## 🔧 Dependências e Estrutura

### Arquivos Obrigatórios
- `prompt_gerar_docs.md`: Prompt para geração inicial
- `prompt_validar_docs.md`: Prompt para validação iterativa
- Arquivo `.env` com `OPENAI_API_KEY`

### Tecnologias Utilizadas
- **OpenAI GPT**: Para geração e validação de conteúdo
- **Rich**: Interface colorida no terminal
- **FPDF**: Geração de PDF simplificada
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

## 🚨 Solução de Problemas

### Problemas Comuns

#### Erro de API Key
```
ValueError: API key não encontrada
```
**Solução**: Verifique se o arquivo `.env` existe e contém `OPENAI_API_KEY=sua_chave`

#### Arquivo de Prompt Não Encontrado
```
FileNotFoundError: prompt_gerar_docs.md
```
**Solução**: Certifique-se de que os arquivos `prompt_gerar_docs.md` e `prompt_validar_docs.md` estão no mesmo diretório

#### Erro de Encoding no PDF
```
'latin-1' codec can't encode character
```
**Solução**: O código automaticamente trata caracteres Unicode problemáticos, convertendo para ASCII equivalentes

#### Dependências Não Instaladas
```
ModuleNotFoundError: No module named 'openai'
```
**Solução**: Execute `pip install -r requirements.txt` ou `uv sync`

### Logs e Debug

O sistema fornece feedback visual detalhado:
- 🔵 **Azul**: Comunicação com API
- 🟢 **Verde**: Sucesso/Conclusão
- 🟡 **Amarelo**: Avisos/Iterações em andamento
- 🔴 **Vermelho**: Erros/Problemas

## 🔄 Changelog

### v0.1.0 (Atual)
- ✅ **Novo**: Sistema iterativo de validação e refinamento
- ✅ **Novo**: Verificação automática de critérios inaceitáveis
- ✅ **Novo**: PDF final simplificado
- ✅ **Novo**: Feedback visual aprimorado
- ✅ **Novo**: Suporte para Python 3.12+
- ✅ **Melhoria**: Código simplificado para POC
- ✅ **Melhoria**: Tratamento robusto de erros

## 🤝 Contribuição

Este é um projeto de Prova de Conceito (POC). O foco está na funcionalidade core, não em formatação ou validações complexas.

## 📄 Licença

Este projeto é parte de um curso de IA e destina-se a fins educacionais.
