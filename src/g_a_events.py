from src.github_activity_functions import get_github_api, message_generator


FILTER = {
    "pushes": 'PushEvent',
    "pr": 'PullRequestEvent',
    "review": 'PullRequestReviewEvent',
    "pr-comments": 'PullRequestReviewCommentEvent',
    "issues": 'IssuesEvent',
    "comments": 'IssueCommentEvent',
    "commits-comments": 'CommitCommentEvent',
    "branches": ['CreateEvent','branch'],
    "tags": ['CreateEvent','tag'],
    "deletions": 'DeleteEvent',
    "forks": 'ForkEvent',
    "stars": 'WatchEvent',
    "releases": 'ReleaseEvent',
    "discussions": 'DiscussionEvent',
    "wiki": 'GollumEvent',
    "collaborators": 'MemberEvent',
    "visibility": 'PublicEvent'
}

CACHE_FILE = "cache/events.json"

def user_events(username, filt = None):

    url = f"https://api.github.com/users/{username}/events"
    events = get_github_api(username, CACHE_FILE, url, message_generator)
    if events:

        if not filt:

            print(f"""---------------------------------------------------------------
            Eventos realizados por el usuario "{username}" en los ultimos 30 dias:\n""")
            for event in events.keys():
                print(f"TIPO EVENTO: {event}")
                for message in events[event]:
                    print(f"    {message}")
            print("---------------------------------------------------------------""")

        else: # Hay filtro, pero si es el correcto?

            if filt in FILTER: # Si, es el correcto :v
                mssg_filt = []
                f = FILTER[filt] # ¿Es una lista?
                if isinstance(f, str):
                    mssg_filt = events.get(f)

                else: # Es una lista, toca iterar
                    if f[0] in events:
                        for mssg in events[f[0]]:
                            if filt in mssg:
                                mssg_filt.append(mssg)

                if not mssg_filt:
                    mssg_filt = [f'\nNinguno. No hay eventos que coincidan con "{filt}" realizados por el usuario "{username}" en los ultimos 30 dias.']

                print(f"""---------------------------------------------------------------
                Eventos que coinciden con '{filt}' realizados por el usuario "{username}" en los ultimos 30 dias:\n""")
                for message in mssg_filt:
                    print(f"    {message}")
                print("---------------------------------------------------------------""")

            else:
                print("Filtro equivocado, prueba con alguna de las siguientes palabras para filtrar por evento:\n"
                      "pushes - pr - pr-comments - review - issues - comments - commits-comments - branches\n"
                      " - tags - deletions - forks - stars - releases - discussions - wiki - collaborators\n"
                      " - visibility")

    else:
        print(f" El usuario {username} no ha estado activo en los ultimos 30 dias o no existe. Por favor, pruebe con otro")


