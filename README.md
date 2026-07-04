[Previous Project (Project #1 - Task Tracker)](https://github.com/fredidiaz17/Task-Traker-CLI)

> 🌐 [Leer en Español](README.es.md)

# Project #2 - GitHub User Activity

GitHub User Activity is a project from [Roadmap.sh](https://roadmap.sh/projects/github-user-activity).

## What is it about?

This project uses the GitHub API to fetch the **events** performed by a given user over the last 30 days (the maximum period offered by the API) and display them in a readable format.

Additionally, it includes the ability to query a user's **repositories**, making use of another GitHub API endpoint.

The entire program runs from the command line (CLI) and uses **no external libraries** (libraries such as `requests` are therefore not used).

---

## Prerequisites

- Python **3.10** or higher (`match` statements are used)
- No external dependencies required

---

## Installation and usage

1. Clone the repository.
```bash
git clone https://github.com/fredidiaz17/github-user-activity.git
```

2. Navigate to the project folder.
```bash
cd github-user-activity
```

3. Run the program with the desired options. Example:
```bash
python github-activity.py <username> -e
```

---

## Arguments

The program requires a **GitHub username** as a mandatory positional argument, along with one of two available query modes: **events** or **repositories** (mutually exclusive).

### Username
Mandatory positional argument. Specifies the GitHub user to query.

---

### `-e` / `--event` — Events
Fetches the user's events from the last 30 days.

```bash
python github-activity.py fredidiaz17 -e
```

#### Optional parameters for Events

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--filter` | `-f` | Filters events by type. | `python github-activity.py fredidiaz17 -e -f pushes` |

---

### `-r` / `--repos` — Repositories
Fetches the user's public repositories.

```bash
python github-activity.py fredidiaz17 -r
```

#### Optional parameters for Repositories

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--contains` | `-c` | Shows repos whose name contains the given text. | `python github-activity.py fredidiaz17 -r -c task` |
| `--language` | `-l` | Filters repos by predominant language. | `python github-activity.py fredidiaz17 -r -l C` |

---

## Additional features

### Caching
Every API call stores its result in a local cache, avoiding redundant requests for the same user within a set time window. The program generates and uses two cache files: one for **events** and one for **repositories**.

- **Validity**: Both caches are valid for 1 hour. The API is queried again once that time has elapsed or when a different user is requested.
- **Name and location**: The **events** cache is stored as `events.json` and the **repositories** cache as `repos.json`. Both files are saved in the `cache/` folder.

### Argparse
Argument handling is done with `argparse`, a module from the Python standard library, providing a comfortable and consistent CLI experience without violating the no-external-libraries constraint.

---

## Project structure

```text
github-user-activity/
├── github-activity.py       # Program entry point
├── cache/                   # Auto-generated on first run
│   ├── events.json
│   └── repos.json
├── src/
│   ├── g_a_events.py
│   ├── g_a_repos.py
│   ├── g_a_requests.py
│   └── github_activity_functions.py
└── README.md
```

---

## Limitations

- The GitHub API limits event history to the **last 30 days**.
- Only **public** repositories and events are retrieved.
- The GitHub API enforces a rate limit of **60 requests per hour** for unauthenticated users.

---

## Development challenges

1. **Building event messages**: GitHub's official documentation does not specify what message to display for each event type; community forums and references were consulted instead.
2. **Payload diversity**: Each event type has its own payload structure, varying significantly across types. The official documentation provides limited detail, requiring additional exploration.

---

## License

This is a **personal project with no defined license**.

---

[Next Project (Project #3 - Expense-Tracker)](https://github.com/fredidiaz17/Expense-Tracker)