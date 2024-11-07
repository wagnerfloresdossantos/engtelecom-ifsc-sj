# Aula 1 de POO

- Gian
- Beatriz Abreu
- Wagner Santos
- Bruno Hamon Porto


## Comandos Git

### status

Lista todos os arquivos novos ou modificados para serem commitados

```bash
git status
```
#### add

Faz o snapshot de um arquivo na preparação para versionamento

```bash
git add [arquivo]
```

### push

Pega os commits presentes feitos no seu computador e leva eles pro repositório no Github, ao fazer isso, é pedido a identificação do usuário atravéz do username e do Token de acesso

``` bash

git push

```

### pull

Pega o repositório do Github e trás a condição atual dele para o seu computador

```bash

git pull

```

### commit

Os commits são as unidades estruturais de um cronograma de projeto Git. Podem ser considerados instantâneos ou marcos ao longo do cronograma de um projeto Git. São criados com o comando git commit para capturar o estado de um projeto naquele momento.
Fonte: Atlassian

```bash
commit -m "Nome do commit"
```

### clone

O comando git clone copia um repositório do Git existente. É parecido com o checkout do SVN, com a diferença de que a "cópia de trabalho" é um repositório completo do Git — que tem seu próprio histórico, gerencia seus próprios arquivos e é um ambiente isolado como um todo do repositório original.
Fonte: Atlassian

```bash
git clone
```

### log
Lista o histórico de versões para o branch atual.

### GitHub PAT
Você pode usar um token de acesso pessoal no lugar de uma senha ao autenticar no GitHub na linha de comando ou com a API.
