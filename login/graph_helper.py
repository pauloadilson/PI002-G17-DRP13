import requests
import json

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
    # Send GET to /me
    user = requests.get(f'{graph_url}/me',
    headers={'Authorization': f"Bearer {token}"},
    params={
'$select':'displayName,mail,mailboxSettings,userPrincipalName'})
    return user.json()