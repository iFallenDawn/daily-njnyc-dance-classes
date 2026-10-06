# Daily NJ/NYC Dance Classes

Little tool I made for fun that scrapes nearby studios for their dance class schedules daily, similar to how community artistry was ran. Refreshes every hour (or whenever the github actions likes to run).

Does not display whether or not a class is fully cancelled, mainly used to show all classes in one place! Find the teacher's/studio's instagram for more info!

> **Note:** class data is compiled every hour and may not reflect cancellations. Check the teacher's Instagram and the studio's booking website to confirm a class before you go.

Live at https://daily-njnyc-dance-classes.fastapicloud.dev

## Features

- Every class from the supported studios in one table, sorted by start time
- Search by class name
- Filter by studio and instructor (lists are built from whatever classes are currently scraped, so new studios show up automatically)
- Filter by date range
- Filter by time of day, e.g. 6pm - 9pm shows any class that overlaps that window
- Shows difficulty when the studio lists it (Peridance, PMT, Modega)
- Works on mobile, classes show as cards on small screens

## How it works

- `backend/scrapers` has a scraper per studio. Most studios embed a Mindbody or Arketa booking widget, and those widgets load their schedules from public endpoints, so the scrapers request those directly instead of driving a browser
- A GitHub Action (`.github/workflows/studioscraper.yaml`) runs `python -m scrapers.scrape_all` every hour, which clears the Supabase table and inserts the fresh classes
- The FastAPI backend serves the class API under `/api` and the built React frontend at `/`
- Pushing to `main` builds the frontend and deploys everything to FastAPI Cloud (`.github/workflows/deploy.yml`)

## API

`GET /api/classes` returns a page of classes. All query params are optional:

| Param | Example | Notes |
| --- | --- | --- |
| `title` | `choreography` | partial match on class name |
| `studios` | `studios=Modega&studios=Peridance` | can repeat, partial match on studio name |
| `instructors` | `instructors=Youran Lee` | can repeat, partial match on instructor name |
| `start_time` / `end_time` | `2026-10-06T00:00:00` | date range |
| `start_time_of_day` / `end_time_of_day` | `18:00` / `21:00` | time of day window |
| `page` / `limit` | `1` / `10` | limit max is 50 |

Interactive docs are at `/docs`.

## Studios Currently Supported

- ILoveDance - Manhattan, Queens, and Fort Lee
- Modega
- Phresh
- Peridance
- PJM
- PMT
- XSpace
- Any class hosted on dnce.club

## General Notes

data structure? some form of fuzzy matching for difficulty

```json
classname:
instructor:
studio:
location:
style: blank for now, semantic search
starttime:
endtime:
difficulty: semantic search but easier
```

community artistry sorts by this

```json
studio
time
class
instructor
```

who uses mindbody

- ild
- peridance
- bdc
- pmt
etc

## how to run

in `docker/env` create `user.env`
```

# User Info
_UID=1000
_ADJUSTED_UID=1000
USER=NAMEHERE

# Docker Info
COMPOSE_PROJECT_NAME=

# API Keys
SUPABASE_URL=[FILLTHISOUT]
SUPABASE_KEY=[FILLTHISOUT]

# Service Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000

```

for a new Supabase project, run `backend/migrations/001_create_danceclasses.sql` once in the SQL editor to create the table

be in root, have docker installed

```bash
make up
make rebuild-no-cache service=backend -> only if you make changes to the docker file
docker logs -f backend
```