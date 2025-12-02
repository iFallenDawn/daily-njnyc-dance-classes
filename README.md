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

take the div that matches `data-start_date="YYYY-MM-DD"`
from that div, take the list of divs with `class="bw-widget__day"`
from the div above, take the list of `bw-session` and extract data
from each `bw-session` 

```python
for each bw-widget__day:
    for each bw-session in bw-widget__day
        <time class="hc_starttime" datetime="2025-12-01T18:00"> -> start time
        <time class="hc_endtime" datetime="2025-12-01T19:20"> -> end time
        <div class="bw-session__name"> -> take text for class name
        <div class="bw-session__staff"> -> take text for teacher
        <div class="bw-session__description"> -> take text for location
```

## bdc
[link to scrape](https://clients.mindbodyonline.com/classic/ws?studioid=28329&stype=-103&sView=week&sLoc=0)

```html
<div class="view-content">
    ...
</div>
```

## modega
sutrapro
make api call to [this](https://sutrapro.com/api/widget/data?widgetName=modega&type=classes&start_time=1764478800)

