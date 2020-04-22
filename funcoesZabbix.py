from zabbix_api import ZabbixAPI

url = 'https://url.com.br/zabbix/api_jsonrpc.php'
login = 'zabbix'
senha = 'zabbix'

def logginZabbix():
    zapi = ZabbixAPI(url, timeout=20)
    zapi.validate_certs = False
    zapi.login(login, senha)
    return zapi

def getAlerts():
    zapi = logginZabbix()
    result = zapi.trigger.get ({
        "output": ["description", "value", "status", "lastchange"],
        "filter": {
            "value": 1
        },
        "min_severity": 4,
        "expandComment": "true",
        "expandDescription": "true",
        "expandExpression": "true",
        "expandData": "true",
        "monitored": "true",
        "maintenance": "false", # valor padrao false
        "skipDependent": "true",
        "withLastEventUnacknowledged": "true", # valor padrao true
        "selectHosts": ["name", "host", "proxy_hostid"],
        "selectItems": ["lastvalue"],
        "selectLastEvent": ["eventid", "clock", "value"],
        "selectGroups": ["name"],
        "sortfield": "lastchange",
        "sortorder": "ASC"
    })
    zapi.logout()
    return result


def ackAlerts(eventid, chamado):
    zapi = logginZabbix()
    result = zapi.event.acknowledge ({
        "eventids": eventid,
        "message": f"Registro automático: Chamado {chamado}"
    })
    zapi.logout()
    return result

def getProxy(proxyid):
    zapi = logginZabbix()
    result = zapi.proxy.get ({
        "proxyids": proxyid,
        "output": ["host"]
    })
    zapi.logout()
    return result
