from json import JSONDecodeError
import json
from pathlib import Path
from datetime import datetime, timedelta

from src import g_a_requests as requests

TTL = 1 #horas
# fredidiaz17
def get_github_api(username, cache_file, url, func):

    ahora = datetime.now().replace(microsecond=0)
    path = Path(cache_file) # Convertimos la ruta en un objeto path
    # Consultar o no nuevamente la Api
    if path.exists(): # ¿Existe el archivo de la cache?
        try:
            with open(cache_file, "r", encoding="utf-8") as f: #El archivo debe tener mismo encoding en lectura y escritura
                cache = json.load(f)
                # ¿Usuario está en cache y/o han pasado menos de 1 hora?
                dt = datetime.fromisoformat(cache['timestamp'])
                if cache['user'] == username and (dt - ahora < timedelta(hours=TTL)):
                    print("----Usando data en cache----")
                    return cache['data']
        except JSONDecodeError:
            print('El archivo parece corrupto, generando uno nuevo...') # Se petatió esa vaina

    # No hay caché, expiró, está dañado o no existe archivo. Toca consultar

    print("----Consultando la API----")
    response = requests.get(url)

    # Creamos la ruta en caso de no existir
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    # Consiguiendo Repos
    cache = {'data': {}} # supondremos que no hay datos hasta que la consulta sea exitosa.

    if response.status_code == 200:
        data = response.json()

        # En la caché se guardarán tanto el usuario como el timestamp para saber si es necesario consultar de nuevo la API
        # Igualmente, se guardará la data conseguida de la api ya procesada, pudiendo ser los eventos o los repos del usuario dado.
        with open(cache_file, "w", encoding="utf-8") as f: # Es necesario el utf-8 para no petatear por ciertos caracteres
            cache = {
                'user': username,
                'timestamp': str(ahora),
                'data': func(data),
            }
            json.dump(cache, f, indent= 4, ensure_ascii=False)


    elif response.status_code == 404:
        print("Usuario no encontrado")

    else:
        print("Ha ocurrido un Error: ", response.status_code)

    return cache['data']


def repos_classifier(repos):
    repos_classified = {
        "notforked": {},"forked": {}
    }
    for repo in repos:
        r = {
            repo['name']: {
                'description': repo['description'],
                'language': repo['language'],
                'star_count': repo['stargazers_count'],
                'forks_count': repo['forks_count'],
                'updated_at': repo['updated_at'],
                'html_url': repo['html_url'],
            }
        }
        if not repo['fork']: # Es original del usuario
            repos_classified['notforked'].update(r)
        else: # Copia de otro repo
            repos_classified['forked'].update(r)

    return repos_classified

def message_generator(events):
    mssg_object = {}

    for event in events:
        message = ""
        tipo = event['type']
        repo = event['repo']['name']
        payload = event['payload']
        try:
            match tipo:
                case "CommitCommentEvent":
                    message = f"-Commented in a commit in {repo}"

                case "CreateEvent":
                    # ref_type puede ser repository, tag o branch, la estructura de repository es diferente al de los otros 2 mensajes
                    if payload['ref_type'] != 'repository':
                        message = f"-Created {payload['ref_type']} {payload['ref']} in {repo}"
                    else:
                        message = f"-Created repository {repo}"

                case "DeleteEvent":
                    message = f"-Deleted {payload['ref_type']} {payload['ref']} from {repo}"

                case "DiscussionEvent":
                    message = f"-{payload['action']} discussion {payload['discussion']['title']}"

                case "ForkEvent":
                    message = f"-Forked {repo} to {payload["forkee"]["full_name"]}"

                case "GollumEvent":
                    for page in payload['pages']:
                        message += f' - {page["action"]} wiki page "{page['title']}" in {repo}"'

                case "IssueCommentEvent":
                    issue = payload['issue']
                    if 'pull_requet' in issue:
                        message = f"-Commented on pull request {issue['title']}"
                    else:
                        message = f"-Commented on issue {issue['title']}"

                case "IssuesEvent":
                    message = f"-{payload['action']} issue '{payload['issue']['title']}'"

                case "MemberEvent":
                    message = f"-{payload['action']} '{payload['member']['login']} to/from {repo}'"

                case "PublicEvent":
                    message = f"-Made {repo} public"

                case "PullRequestEvent":
                    pr = payload['pull_request']
                    action = payload['action']
                    head = pr['head']['ref']
                    base = pr['base']['ref']
                    if action == 'opened':
                        message = f'-Opened pull request from "{head}" to "{base}" in "{repo}"'
                    if action == "closed" and not pr['merged']:
                        message = f'-Closed pull request from "{head}" to "{base}" in "{repo}"'
                    if action == 'closed' and pr['merged']:
                        message = f'-Merged pull request from "{head}" to "{base}" in "{repo}"'
                    if action == 'reopened':
                        message = f'-Reopened pull request from "{head}" to "{base}" in "{repo}"'
                    if action == 'ready_for_review':
                        message = f'-Marked pull request from "{head}" to "{base}" in "{repo}" ready for review'
                    if action == 'review_requested':
                        message = f'-Requested review on pull request from "{head}" to "{base}" in "{repo}"'

                case "PullRequestReviewEvent":
                    estado = payload['review']['state']
                    title = payload['pull_request']['title']

                    if estado == "approved":
                        message = f'-Approved pull request "{title}"'
                    if estado == "changes_requested":
                        message = f'-Requested changes on "{title}"'
                    if estado == "commented":
                        message = f'-Reviewed pull request "{title}"'

                case "PullRequestReviewCommentEvent":
                    # Este evento parece que solo tiene una acción (created), y por ende, un solo mensaje
                    message = f"-Commented on pull request {payload['pull_request']['title']}"

                case "PushEvent":
                    # se supone que aqui hay Size, pero ni la doc oficial ni la respuesta de la Api tienen esto, asi que...
                    message = f"-Pushed commit(s) to {payload['ref']} in {repo}"

                case "ReleaseEvent":
                    action = payload['action']
                    tag = payload['release']['tag_name']
                    if action == 'published':
                        message = f'-Published release "{tag}"'
                    else: # is created
                        message = f'-Created release "{tag}"'

                case "WatchEvent":
                    message = f"-Starred {repo}"

                case _:
                    pass
        except KeyError:
            message = f'\nEvent type "{tipo}" took place in "{repo}"'

        if tipo not in mssg_object:
            mssg_object[tipo] = []

        mssg_object[tipo].append(message)

    return mssg_object