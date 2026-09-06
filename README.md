\# 🏏 Cricbuzz LiveStats



A multi-page Streamlit dashboard combining live cricket data from the Cricbuzz API with a PostgreSQL database for analytics and CRUD operations.



\*\*Live app:\*\* \_\[https://cricbuzz-livestats-nqfwyfxwgmyhcmgzk4kahp.streamlit.app/]\_



\---



\## Features



\- \*\*Home\*\* — live summary metrics (teams, players, matches, series), quick player search, and navigation shortcuts

\- \*\*Live Matches\*\* — real-time match data from the Cricbuzz API, filterable by format, with on-demand scorecards

\- \*\*Top Player Stats\*\* — live ICC-style rankings (API) alongside database-driven leaderboards with bar-chart visualizations and player drill-down history

\- \*\*SQL Analytics\*\* — 14 of 25 analytics questions, selectable from a dropdown, with the SQL query shown alongside results and optional bar-chart visualization

\- \*\*CRUD Operations\*\* — full Create/Read/Update/Delete for Players and Teams, with search/filter, validation, and delete confirmation safeguards



\---



\## Tech Stack



\- \*\*Frontend:\*\* Streamlit

\- \*\*Database:\*\* PostgreSQL (hosted on \[Supabase](https://supabase.com) in production)

\- \*\*API:\*\* \[Cricbuzz Cricket API](https://rapidapi.com) via RapidAPI

\- \*\*Libraries:\*\* psycopg2, pandas, plotly, python-dotenv, requests

\- \*\*Deployment:\*\* Streamlit Community Cloud



\---



\## Folder Structure



```

cricbuzz-livestats/

├── main.py                  # Streamlit entry point / Home page

├── config.py                 # Loads secrets from .env or Streamlit Cloud

├── requirements.txt

├── .env.example               # Template for required environment variables

│

├── database/

│   └── db\_connection.py       # Centralized DB connection (context manager)

│

├── api/

│   └── cricbuzz\_client.py     # All Cricbuzz API calls, with retry/backoff

│

├── services/                  # Business logic — pages call these, never SQL/API directly

│   ├── live\_match\_service.py

│   ├── player\_stats\_service.py

│   ├── analytics\_service.py

│   ├── crud\_service.py

│   └── home\_service.py

│

├── pages/                     # One file per Streamlit page

│   ├── 2\_Live\_Matches.py

│   ├── 3\_Top\_Player\_Stats.py

│   ├── 4\_SQL\_Analytics.py

│   └── 5\_CRUD\_Operations.py

│

├── utils/

│   ├── validators.py           # Input validation before any DB write

│   └── error\_handlers.py       # Friendly error messages for common DB errors

│

├── sql/

│   ├── schema.sql              # CREATE TABLE statements (8 tables, 3NF)

│   └── seed\_data.sql           # Sample data (10 teams, 34 players, 12 matches)

│

├── data/                       # Debug/manual test scripts (not part of the app)

└── .streamlit/

&#x20;   └── config.toml             # Theme configuration

```



\---



\## Database Setup



The schema is a normalized (3NF) relational design with 8 tables: `teams`, `players`, `venues`, `series`, `matches`, and three performance tables (`batting\_performances`, `bowling\_performances`, `fielding\_performances`) — split apart since a player's batting, bowling, and fielding involvement in a match are independent facts.



\*\*To set up your own instance:\*\*

1\. Create a PostgreSQL database (locally, or a free instance on \[Supabase](https://supabase.com))

2\. Run `sql/schema.sql` against it to create all tables

3\. Run `sql/seed\_data.sql` to load sample data (10 teams, 34 players, 12 matches spanning Test/ODI/T20 formats)



\*\*Note on Supabase specifically:\*\* if connecting from a network without IPv6 support, use Supabase's \*\*connection pooler\*\* host (not the direct `db.xxx.supabase.co` host), or you'll hit a DNS resolution error.



\---



\## API Setup



1\. Create a free account at \[RapidAPI](https://rapidapi.com)

2\. Subscribe to the \*\*Cricbuzz Cricket\*\* API (BASIC/free tier is sufficient for development)

3\. Copy your API key from the \*\*Endpoints\*\* tab

4\. Note: the free tier has a limited monthly request quota — the app is built to fail gracefully (showing "unavailable" messages rather than crashing) if the quota is exhausted



\---



\## Installation \& Running Locally



```bash

git clone https://github.com/Chetana870/cricbuzz-livestats.git

cd cricbuzz-livestats

pip install -r requirements.txt

cp .env.example .env

\# Edit .env with your real RAPIDAPI\_KEY and database credentials

streamlit run main.py

```



Required environment variables (see `.env.example`):

```

RAPIDAPI\_KEY=

RAPIDAPI\_HOST=cricbuzz-cricket.p.rapidapi.com

DB\_HOST=

DB\_PORT=

DB\_NAME=

DB\_USER=

DB\_PASSWORD=

```



\---



\## Deployment



Deployed on \*\*Streamlit Community Cloud\*\*, connected to a \*\*Supabase\*\* PostgreSQL instance. Secrets (API key, DB credentials) are configured via Streamlit Cloud's built-in Secrets manager — never committed to the repository.



\---



\## Screenshots



\_\[Add screenshots of each page here before final submission]\_



\- Home dashboard

\- Live Matches with scorecard

\- Top Player Stats with charts

\- SQL Analytics

\- CRUD Operations



\---



\## Future Improvements



\- Complete SQL Analytics Questions 15–25 (window functions, CTEs, advanced ranking)

\- Add line charts and scatter plots once more historical match data is available

\- Add automated test suite (pytest) for services and validators

\- Add authentication if multi-user access control becomes a requirement

\- Expand seed data further for deeper partnership/format-versatility analytics



\---



\## Author



Built as a learning project covering Python, PostgreSQL, REST APIs, and Streamlit — developed phase-by-phase with an emphasis on understanding each concept before implementation.

