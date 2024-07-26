
## Instalação bibliotecas
Instale o selenium

```bash
  pip install selenium
```
Instale o BeautifulSoup4
```bash
  pip install BeautifulSoup4
```
Instale o pandas
```bash
  pip install pandas
```
## Para rodar no edge
### Baixe o Webdriver Edge
Para baixar o webdriver acesse: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH

Extraia o arquivo e execulte:
```bash
  msedgedriver.exe
```
isso fara com que abra seu pront de comando, deixem aberto e nao finalizem a tarefa para que o script funcione.
## Para rodar no chrome
Necessita de apens ter o chrome instalado na sua maquina. O chrme quando chamado ele criará um ambiente de navegação  automatizado.

## USO
### Passo 1
Apos instalar todas as bibliotecas mude as o valor das varivaies:
```bash
  usuario = "NOME DO SEU USUARIO"
```
para o seu nome de usuario
```bash
  senha = "SUA SENHA"
```
para a sua senha

Lembrando que e o usuario e senha de acesso ao sigaa

### Passo 2
Entre no diretorio do seu navegador e digite no console

```bash
  python scriptForChrome.py
```
para o chrome

```bash
  python scriptForEdge.py
```
para o edge

### Passo 3
No diretorio Results, devera conter o json com todos os dados.

# Bom uso :)
