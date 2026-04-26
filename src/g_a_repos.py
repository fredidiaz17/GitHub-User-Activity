from src.github_activity_functions import get_github_api, repos_classifier

CACHE_FILE = 'cache/repos.json'
def user_repos(username, repo_name = None, repo_language = None):
    url = f"https://api.github.com/users/{username}/repos"
    repos = get_github_api(username, CACHE_FILE, url, repos_classifier) # Ya retorna la data

    if repos['forked'] or repos['notforked']: # Hay tan siquiera algún repo?
        if not repo_name and not repo_language:
            print("---------------------------------------------------------------""")
            if repos['notforked']:
                print("\n Repositorios propios del usuario (no derivan de otros repositorios):")
                print_repos(repos['notforked'])
            else:
                print("El usuario no ha creado repositorios propios")
            print("---------------------------------------------------------------""")

            print("---------------------------------------------------------------""")
            if repos['forked']:
                print("\n Repositorios que derivan de otro repositorio (forked):")
                print_repos(repos['forked'])
            else:
                print("El usuario no cuenta con repositorios derivados de otros (forked)")
            print("---------------------------------------------------------------""")

        else: # Se buscan algunos que contengan un string en el nombre o un lenguage especifico, ¿estarán?
            repos_coincidence = {}

            if repo_name:
                target = repo_name.lower()
            else:
                target = repo_language.lower()


            for obj_type in repos.values(): #Accedo al dict contenido por forked o notforked
                for nombre, repo in obj_type.items():
                   if (repo_name and target in nombre.lower()) or (repo_language and target == repo['language'].lower()):
                       repos_coincidence.update({nombre:repo})

            if repos_coincidence:
                print("---------------------------------------------------------------""")
                if repo_name:
                    print(f'Repositorios del usuario "{username}" que tienen el nombre "{repo_name}" en su nombre: ')
                else:
                    print(f'Repositorios del usuario "{username}" que tienen el lenguaje "{repo_language}": ')
                print_repos(repos_coincidence)
                print("---------------------------------------------------------------""")
            else:
                if repo_name:
                    print(f'Ninguno de los repositorios del usuario "{username}" contiene el nombre "{repo_name}"')
                else:
                    print(f'Ninguno de los repositorios del usuario "{username}" contiene el lenguaje "{repo_language}"')

    else:
        print(f"El usuario {username} no cuenta con repositorios, ni propios ni derivados de otros. Prueba con otro usuario")


def print_repos(repos):

    for repo_name,repo in repos.items():  #
        print(repo_name)
        print("Caraterísticas del repositorio: ")
        print(f"Descripción: {repo['description']} \n Lenguaje(s): {repo['language']}")
        print(f"⭐ {repo['star_count']}    |   Forks: {repo['forks_count']}")
        print(f"Ultima vez actualizado: {repo['updated_at']}\n{repo['html_url']}")
        print("----------------- \n\n")
