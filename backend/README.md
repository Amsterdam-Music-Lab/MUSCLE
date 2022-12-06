# AML experiment server

The AML experiment server consists of:

- Django admin that can be used to manage all experiment/playlist/participant data
- Experiment rules and views that enable server-side construction and configuration of experiments
- API endpoints for AML experiment client


## Create a new experiment

- Login to Django admin: http://localhost:8000/admin
- Create a playlist with sections
- Manually upload your sections to the `src/upload` folder
- Create a new experiment with a unique slug and at least one playlist
- Use the experiment slug to link the client to your experiment

## Export data

### From Admin

- Login to Django admin: http://localhost:8000/admin
- Navigate to Hooked > Experiments and click `Export JSON` on your experiment
- Exporting may take a while, depending on the amount of data in your experiment. (Performance on production may be better than on your development server, but there is also a timeout)

### From command line

Alternately you can use the command line to export data:

- Default: `./manage.py exportexperiment %slug%`
  - %slug% is your experiment slug
- With indented JSON: `./manage.py exportexperiment --indent=4 %slug%`
- Output the results to a file: `./manage.py exportexperiment %slug% > my_data.json`

## Develop experiments

### Rules

Experiment rules are described in the rules that can be found in `src/hooked/rules`. Here you can configure the views that are shown in the client each round.

If you create new rules, add them to `src/hooked/rules/__init__.py`, so you can add them to your experiment in Django admin.

To customize behaviour, you can extend/adapt functions from the base class `src/hooked/rules/Base.py` in your own rules file.

### Views

In each experiment round a view is shown in the client. These are configured in `src/hooked/rules/views/*`

#### Tweaking views

If you want to make a minor adaption to an existing view, you can adapt the defaults in the view file. If you want to keep the defaults intact, you can adapt them in the action data (dict) in your rules, e.g:

```python
# /src/hooked/rules/custom_rules.py

action = SongSync.action(session)

# Minor change to config
actions['config']['recognition_time'] = 20
```

#### Extend views

To make major modifications, you can extend another view, e.g.:

```python
# /src/hooked/rules/views/custom_songsync.py

from .song_sync import SongSync

class CustomSongSync(SongSync):
    @staticmethod
    def calculate_score(session, result, data):
        # Custom score calculation here
```

Don't forget to add your new view to `src/hooked/rules/views/__init__.py`

#### New views

To create a new view, you add it in e.g. `src/hooked/rules/views/my_view.py` and add it to `src/hooked/rules/views/__init__.py`.

Use your new view in your experiment rules by importing it, e.g.:

```python
from .views import MyView
```

Check the client documentation for instructions for adding the view to the client.

## Troubleshooting

#### Bad request

Check if your server is in the .env `AML_ALLOWED_HOST` and `AML_CORS_ORIGIN_WHITELIST`

#### Admin assets not loading

- Make sure you collected the assets: `./manage.py collectstatic`
- Make sure the `/static/` folder is ProxyPassed in your Apache virtual host file and if the folder is served correctly

#### Media files not serving

- Make sure the `/upload/` folder is ProxyPassed in your Apache virtual host file and if the folder is served correctly

#### ip2country not working

- Check if the ip2country service is running: `curl http://localhost:8854?ip=172.217.168.238` - should return `{"status":"ok","country":"US"}`
