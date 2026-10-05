# Daily NJ/NYC Dance Classes

Little tool I made for fun that scrapes nearby studios for their dance class schedules daily, similar to how community artistry was ran.

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

be in root, have docker installed

```bash
make up
make rebuild-no-cache service=backend -> only if you make changes to the docker file
docker logs -f backend
```