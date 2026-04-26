"""
Output:
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened a new issue in kamranahmedse/developer-roadmap
- Starred kamranahmedse/developer-roadmap
- ...

Handle errors gracefully, such as invalid usernames or API failures.

If you are looking to build a more advanced version of this project,
you can consider adding features like filtering the activity by event type,
displaying the activity in a more structured format, or caching the fetched data to improve performance.
You can also explore other endpoints of the GitHub API to fetch additional information about the user or their repositories.
"""
from src import g_a_repos as repos, g_a_events as events
import argparse

parser = argparse.ArgumentParser()

# argumento posicional
parser.add_argument(
    "username",
    help="Username used to fetch info from GitHub API"
)

# --- grupo modo (solo uno) ---
mode_group = parser.add_mutually_exclusive_group()

mode_group.add_argument(
    "--event", "-e",
    help="Show Events",
    action="store_true"
)

mode_group.add_argument(
    "--repos", "-r",
    help="Show Repositories",
    action="store_true"
)

# --- filtros (NO exclusivos entre sí) ---
parser.add_argument(
    "--filter", "-f",
    help="Filter events by type"
)

parser.add_argument(
    "--language", "-l",
    help="Filter repositories by language"
)

parser.add_argument(
    "--contains", "-c",
    help="Filter repositories by name"
)

args = parser.parse_args()

if __name__ == "__main__":
    if args.username is not None:

        if args.event: # Listar eventos

            if args.filter: # Hay filtro de eventos
                events.user_events(args.username, args.filter)
            else: # No hay
                events.user_events(args.username)

        elif args.repos: # Listar repositorios

            if args.contains:
                repos.user_repos(args.username, repo_name= args.contains)
            elif args.language:
                repos.user_repos(args.username, repo_language= args.language)
            else:
                repos.user_repos(args.username)
        else: # Vacios los dos
            print("Debe elegir evento o repositorio. \n Use -e o --event para eventos, -r o --repos para repositorios")

    else:
        print("Debe digitar usuario para proceder")