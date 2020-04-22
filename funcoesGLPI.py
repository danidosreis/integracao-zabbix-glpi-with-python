import requests

url = 'http://10.0.0.0/apirest.php'
usertoken = 'usertoken'
apptoken = 'apptoken'

def login():
    url_full = url + '/initSession'
    headers = {'Content-Type': 'application/json', 'Authorization': f'user_token {usertoken}', 'App-Token': apptoken}
    r = requests.get(url_full, headers=headers)
    session = r.json()['session_token']
    return session

def logout(session):
    url_full = url + '/killSession'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    r = requests.get(url_full, headers=headers)
    return r

def ticketSearch(triggerid):
    session = login()
    url_full = url + '/Ticket/?range=0-20&order=DESC'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    r = requests.get(url_full, headers=headers)
    result = r.json()
    for i in result:
        chamado = i['id']
        titulo = i['name']
        descricao = i['content']
        if triggerid in descricao and 'ALERTA' in titulo:
            return chamado
    logout(session)

def ticketCreate(titulo, desc, id_ent):
    session = login()
    url_full = url + '/Ticket/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                 {'name': titulo,
                       'content': desc,
                       '_users_id_requester': 1264, # Requerente
                       'itilcategories_id': 1560, # Categoria/Serviço
                       'requesttypes_id': 8, # Origem
                       'urgency': 3,
                       'impact': 3,
                       'priority': 3,
                       'entities_id': id_ent # Entidade
                 }
             }
    r = requests.post(url_full, headers=headers, json=payload)
    result = r.json()['id']
    logout(session)
    return result

def ticketUpdateGroup(id_chamado):
    session = login()
    url_full = url + f'/Ticket/{id_chamado}/Group_ticket/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                   {'tickets_id': id_chamado,
                    'groups_id': 20, # N1
                    'type': 2 # 1: requester; 2: assigned; 3: observer
                    }
               }
    r = requests.post(url_full, headers=headers, json=payload)
    logout(session)
    return r

def ticketUpdateUser(id_chamado):
    session = login()
    url_full = url + f'/Ticket/{id_chamado}/Ticket_User/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                   {'tickets_id': id_chamado,
                    'users_id': 1350, # Ususario grafana
                    'type': 2 # 1:requester; 2:assigned; 3:observer
                    }
               }
    r = requests.post(url_full, headers=headers, json=payload)
    logout(session)
    return r

def ticketAcompanhamento(id_chamado):
    session = login()
    url_full = url + f'/Ticket/{id_chamado}/TicketFollowup/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                   {'tickets_id': id_chamado,
                    'requesttypes_id': 8, # Origem
                    'content': "Teste lançamento acompanhamento API",
                    '_close': 0,
                    'add_close': 0
                   }
               }
    r = requests.post(url_full, headers=headers, json=payload)
    logout(session)
    return r

def ticketTask(id_chamado):
    session = login()
    url_full = url + f'/Ticket/{id_chamado}/TicketTask/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                   {'tickets_id': id_chamado,
                    'requesttypes_id': 8, # Origem
                    'content': "Teste lançamento task via API",
                    'taskcategories_id': 43,  # Serviço
                    'is_private': 0,  # Não privado
                    'actiontime': 60,  # Duração da tarefa em seg.
                    'state': 2  # Status 
                    }
               }
    r = requests.post(url_full, headers=headers, json=payload)
    logout(session)
    return r


def ticketClose(id_chamado):
    session = login()
    url_full = url + f'/Ticket/{id_chamado}/'
    headers = {'Content-Type': 'application/json', 'Session-Token': session, 'App-Token': apptoken}
    payload = {'input':
                   {'tickets_id': id_chamado,
                    'solutiontypes_id': 1, # Tipo da solução
                    'solution': 'Solution api' # Descrição da solução
                    }
               }
    r = requests.put(url_full, headers=headers, json=payload)
    logout(session)
    return r
