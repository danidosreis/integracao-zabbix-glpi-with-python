# Integração Zabbix e GLPI

Esse projeto é uma integração entre o Zabbix e o GLPI utilizada para abertura automática de chamados através da detecção de alertas ativos no Zabbix.

### O que ela faz?
  - Detecta alertas ativos no Zabbix com severidades "Alta" e "Desastre".
  - Verifica se já existe um chamado aberto para o alerta consultando o GLPI.
  - Abre um novo chamado no GLPI com as informações do alerta.
  - Reconhece automaticamente o alerta no Zabbix com o número do chamado aberto ou encontrado.
  - Encaminha um template de e-mail com as informações do alerta/chamado.

### O que foi utilizado?
* Zabbix 3.2.11 - Ferramenta de monitoração
* GLPI 9.1 - Ferramenta ITSM
* Zabbix API - Documentação API do Zabbix
* GLPI API - Documentação API do GLPI
* Python3.8 - Linguagem de programação
* zabbix_api - Biblioteca do Python para realizar consultas api no Zabbix
* smtplib - Biblioteca do Pyhon para envio de e-mail


### Scripts:
| Nome | Descrição |
| ------ | ------ |
| funcaoSendmail.py  | Função para realizar envio de e-mail |
| funcaoGLPI.py | Funções para realizar busca, criação, atualização de chamados |
| funcaoZabbix.py | Funções para realizar busca e ack nos alrertas |
| listaEntidade.py | Função para trazer o id_entidade de um cliente |
| template-notificacao.html | Template para envio de e-mail |
| abertura.py | Script que contém todas as funcionalidades para realizar a integração |
