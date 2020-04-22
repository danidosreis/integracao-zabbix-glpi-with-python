from funcoesZabbix import getAlerts, getProxy, ackAlerts
from funcoesGLPI import ticketSearch, ticketCreate, ticketUpdateGroup
from funcaoSendmail import send_email
from listaEntidade import listaEntidade
from datetime import datetime
import time

lista_alertas = getAlerts()
lista_entidade = listaEntidade()
datenow = int(datetime.now().timestamp())


count = 0
for i in lista_alertas:
    if count < len(lista_alertas):
        triggerid = lista_alertas[count]['triggerid']
        trigger_name = lista_alertas[count]['description']
        eventid = lista_alertas[count]['lastEvent']['eventid']
        hours_event = lista_alertas[count]['lastchange']
        hours_event = int(hours_event)
        hours_event_form = time.localtime(hours_event)
        hours_event_form = time.asctime(hours_event_form)
        count2 = 0
        len_groups = len(lista_alertas[count]['groups'])
        while count2 < len_groups:
            grupo = lista_alertas[count]['groups'][count2]['name']
            if 'Tecnologia' in grupo:
                group_tec = lista_alertas[count]['groups'][count2]['name']
                break
            else:
                count2 = count2 + 1
        else:
            group_tec = 'Não identificado'
        count3 = 0
        while count3 < len_groups:
            grupo = lista_alertas[count]['groups'][count3]['name']
            if 'Cliente' in grupo:
                group_cliente = lista_alertas[count]['groups'][count3]['name']
                break
            else:
                count3 = count3 + 1
        else:
            group_cliente = 'Não identificado'
        entidade = [y for x, y in lista_entidade if x.lower() == group_cliente.lower()]
        host_name = lista_alertas[count]['hosts'][0]['name']
        proxyid = lista_alertas[count]['hosts'][0]['proxy_hostid']
        proxyget = getProxy(proxyid)
        if proxyget == []:
            proxy_name = 'Zabbix Server'
        else:
            proxy_name = proxyget[0]['host']
        itemid = lista_alertas[count]['items'][0]['itemid']
        lastvalue = lista_alertas[count]['items'][0]['lastvalue']
        count = count + 1

        # Título do chamado no GLPI
        titulo = f'ALERTA: {group_cliente[8:]} | {trigger_name}'

        # Descrição do chamado no GLPI
        descricao = f'CLIENTE: {group_cliente} \n' \
                   f'ALERTA: {trigger_name} \n' \
                   f'HOSTNAME/IP: {host_name} \n' \
                   f'TECNOLOGIA: {group_tec} \n' \
                   f'HORA DO EVENTO: {hours_event_form} \n' \
                   f'TRIGGERID: {triggerid} \n' \
                   f'ITEMID: {itemid} \n' \
                   f'EVENTID: {eventid} \n' \
                   f'ÚLTIMO VALOR COLETADO: {lastvalue} \n' \
                   f'MONITORADO POR: {proxy_name}'

        # Entidade em que será aberto o chamado no GLPI
        entidade = int(entidade[0])

        # Verificando se existe chamado aberto
        searchchamado = ticketSearch(triggerid)

        if searchchamado is not None:
            ackAlerts(eventid, searchchamado)
            print('Já existe um chamado aberto para essa trigger')
        else:
            id_chamado = ticketCreate(titulo, descricao, entidade)
            ticketUpdateGroup(id_chamado)
            print(f'Chamado {id_chamado} aberto com sucesso')
            ackAlerts(eventid, id_chamado)
            print('Realizado ack no alerta')
            send_email(id_chamado, group_cliente[8:], trigger_name, host_name)
            print('E-mail enviado')


