# Protótipo experimental

Este diretório contém o protótipo inicial utilizado para comparar as arquiteturas de agente único e multiagente.

## Estrutura esperada

```text
prototipos/
├── base-conhecimento/base-comum-piloto.md
├── cenarios/cenario-piloto-001.json
├── prompts/
├── src/
├── resultados/
├── .env.example
└── requirements.txt
```

## Preparação

```bash
cd prototipos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Teste sem API

```bash
python src/executar_piloto.py --mode mock --architecture both
```

Esse comando executa o mesmo cenário nas duas arquiteturas e grava os registros em `resultados/`.

## Teste com modelo real

Preencha `OPENAI_API_KEY` e `TCC_OPENAI_MODEL` no arquivo `.env`. Depois execute:

```bash
python src/executar_piloto.py --mode openai --architecture both
```

Não registre o arquivo `.env` no Git.
