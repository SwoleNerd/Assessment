## Funcionalidades

- Busca artigos de notícias do TecMundo usando a News API
- Gera resumos automáticos usando Google Gemini AI
- Suporta filtros por palavra-chave
- Salva resultados em formato JSON
- Interface via linha de comando

## Pré-requisitos

- Python 3.8+
- Chave de API do News API (https://newsapi.org/)
- Chave de API do Google Gemini (https://aistudio.google.com/)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/news-article-analyzer.git
cd news-article-analyzer
bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Copie o arquivo `.env_template` para `.env`
- Adicione suas chaves de API no arquivo `.env`:

    NEWS_API_KEY=sua_chave_news_api
    GEMINI_API_KEY=sua_chave_gemini

```bash
python main.py -q "inteligencia artificial"
```

### Parâmetros disponíveis:
- `-q` ou `--query`: Palavra-chave para busca (padrão: "tech")

## Estrutura do Projeto

news-article-analyzer/

├── main.py # Script principal

├── article.py # Classe Article para gerenciar artigos

├── news_manager.py # Classe NewsManager para gerenciar requisições

├── requirements.txt # Dependências do projeto

├── .env_template # Modelo para variáveis de ambiente

└── .gitignore # Arquivos ignorados pelo git


## Exemplo de Saída

O programa irá:
1. Buscar artigos baseados na palavra-chave (com certos critérios*)
2. Gerar resumos usando IA
3. Salvar os resultados em `articles.json`

## Configurações*

- Tamanho da busca: 5 artigos por busca
- Idioma: Português
- Domínio: tecmundo.com.br
- Período: Janeiro de 2025