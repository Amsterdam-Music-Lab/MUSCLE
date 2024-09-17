# Create a custom experiment ruleset

## createruleset command
To create a rules file for custom experiment, you can use the following command:
`./scripts/manage createruleset `

This will prompt you to provide an experiment name for your new experiment's ruleset. If no rules file by that name exists yet, the command will do the following:
- create a file `{ruleset_name}.py` in `experiment/rules`
- create a file `{ruleset_name}_test.py` in `experiment/rules/tests` - this implements a rudimentary unit test
- add references to your new rules file to `experiment/rules/__init__.py`

## Set up the experiment
Go to the admin interface at `localhost:8000/admin`. If you click on `Add` next to `Experiments`, you can verify that your rules now appear in the `Rules` dropdown. Give the experiment a name and assign a slug to it. Also, tie a playlist to it. Now you can see the experiment in action if you navigate to `localhost:3000/{your_slug}`. The experiment plays audio files and presents a `BooleanQuestion` "Do you like this song?" as many times as there are rounds in the experiment (you can adjust this in the admin interface), and then shows a `Final` action.

## The rules file
Open your new rules file `experiment/rules/{experiment_name}.py` and edit away! You can see some methods implemented for you.

### `__init__`
This method initializes questions to collect information on demographics or musical training from your participant. Note that you can easily change these questions through the admin interface.

### `first_round`
When the frontend first retrieves information about the experiment from the backend, this method will provide the actions to show during the setup of the experiment, i.e., before the experiment proper starts. Most experiments display some introductory information here (as an `Explainer`), as well as a consent form (`Consent`). Optionally, experimenters may choose to let participants choose between multiple playlists before starting the experiment (`Playlist`). All this information is optional.

### `next_round`
This is the centrepiece of your experiment's logic. You can check here in which round you are (`session.get_next_round()`), or whether all rounds defined in the experiment have been completed (`session.rounds_complete()`). The number of rounds passed is measured by the number of `Result` objects saved during the cause of the experiment session.

Most experiments present a `Final` action when the rounds are complete, and before that, `Trial` actions, with optionally some `Score` actions in between to show intermediate results to the participant. 
