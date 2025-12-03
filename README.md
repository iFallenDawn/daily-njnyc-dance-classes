# Daily NJ/NYC Dance Classes
Little tool I made for fun that scrapes nearby studios for their dance class schedules daily, similar to how community artistry was ran.

## General Notes
need to sort somehow

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

## how to run
be in root, have docker installed
```bash
make up
make rebuild-no-cache service=backend -> only if you make changes to the docker file
docker logs -f backend
```

## ILD Notes

```html
<div class="bw-widget__sessions bw-widget__sessions--hide-empty-days" data-start_date="2025-12-01"> -> overall div with all ays
    <div class="bw-widget__day"> -> each day
        <div class="bw-session"> -> each class
            ...
            <time class="hc_starttime" datetime="2025-12-01T18:00"> -> start time
            <time class="hc_endtime" datetime="2025-12-01T19:20"> -> end time
            ...
            <div class="bw-session__name"> -> take text for class name
            <div class="bw-session__staff"> -> take text for teacher
            <div class="bw-session__description"> -> take text for location
        <div class="bw-session">
        ...
    <div class="bw-widget__day">
    ...
</div>
```

## Modega Notes
[url](https://sutrapro.com/modega)

```html
<div class="card-list__card-group"> -> each of these is a day
    <div class="class-list__day border-bottom"> -> take text for day
    <div class="class-list__card"> -> each of these is a class
        <p class="dateTimeText"> -> take text for time
        <div class="card-title"> -> take text for class title
        <div class="d-flex flex-row justify-content-between align-items-center"> -> have to narrow this down for more class info
            <p class="m-0 p-0 font-weight-bold card-text"> -> first p tag has instructor name
            <p class="m-0 p-0 mb-2 card-text"> -> second p tag has location but we don't really need that
            <div class="ml-2"> -> if text is cancelled class is cancelled
</div>

<button type="button" class="m-auto primaryColor btn btn-link">Show More</button> -> paginates 10 at a time. probably click this 5 times
```

`dateTimeText` need to parse start and end time, ex `05:00 PM EST • (85 min)`


## bdc
[link to scrape](https://clients.mindbodyonline.com/classic/ws?studioid=28329&stype=-103&sView=week&sLoc=0)

```html
<div class="view-content">
    ...
</div>
```