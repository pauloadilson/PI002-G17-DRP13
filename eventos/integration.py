import webbrowser
from msal import ConfidentialClientApplication, PublicClientApplication
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import requests
from .ms_graph import generate_access_token, GRAPH_API_ENDPOINT
from rich import console
from django.conf import settings
#client = ConfidentialClientApplication(client_id=client_id, client_credential=client_secret)
#authorization_url = client.get_authorization_request_url(scope)
#print(authorization_url)

def obter_token_acesso_public(client_id, scope):
    app = PublicClientApplication(client_id=client_id)
    flow = app.initiate_device_flow(scopes=scope)
    print(flow['message'])
    webbrowser.open(flow['verification_uri'], new=2)

    token_result =  app.acquire_token_by_device_flow(flow)
    print(token_result['access_token'])

    if 'access_token' in token_result:
        return token_result['access_token']
    else:
        raise Exception("Erro ao obter o token de acesso.")

def obter_token_acesso_confidential(app_id, client_secret, scope, authority):
    authority = f'https://login.microsoftonline.com/{authority}'
    scope = ['https://graph.microsoft.com/.default']  # Permissão padrão para acessar o calendário

    app = ConfidentialClientApplication(client_id=app_id, authority=authority, client_credential=client_secret)
    token_result = app.acquire_token_for_client(scopes=scope)
    if 'access_token' in token_result:
        return token_result['access_token']
    else:
        raise Exception("Erro ao obter o token de acesso.")
    
      
def criar_evento_no_microsoft_graph(evento):
    print('Entrando em criar evento')
    client_id = settings.MICROSOFT_CLIENT_ID
    client_secret = settings.MICROSOFT_CLIENT_SECRET
    authority = settings.MICROSOFT_AUTHORITY
    scope = ['Calendars.ReadWrite','User.Read']
    access_token = obter_token_acesso_public(client_id, scope)
    url = f"{GRAPH_API_ENDPOINT}/me/events"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    evento_data = {
        "subject": evento.titulo,
        "body": {
            "contentType": "HTML",
            "content": evento.descricao,
        },
        "start": {
            "dateTime": evento.data_inicio.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": evento.data_fim.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
        "location": {
            "displayName": evento.local,
        },
    }

    response = requests.post(url, json=evento_data, headers=headers)

    if response.status_code == 201:
        return response.json()  # Evento criado com sucesso
    else:
        raise Exception(f"Erro ao criar evento: {response.content}")
