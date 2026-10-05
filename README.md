# Daily NJ/NYC Dance Classes

Little tool I made for fun that scrapes nearby studios for their dance class schedules daily, similar to how community artistry was ran. Refreshes every hour (or whenever the github actions likes to run).

Does not display whether or not a class is fully cancelled, mainly used to show all classes in one place! Find the teacher's/studio's instagram for more info!

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

be in root, have docker installed

```bash
make up
make rebuild-no-cache service=backend -> only if you make changes to the docker file
docker logs -f backend
```