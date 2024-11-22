# Creating an experiment

## Admin interface
Make sure you're logged in to the admin interface (see previous step).

Then, next to "Experiments" click "Add".
<img alt="AddExperiment" src="../assets/images/AddExperiment.png">

## The Experiment form
The form which appears lets you select the following fields:

1. a unique slug for your new experiment (required) If you test locally, the experiment will be available from `localhost:3000/someslug`.

2. a checkbox indicating whether the experiment is active

3. optional: a theme config (through which you can change the background, logos, etc.)

4. `Translated Content` containing information about the experiment, a consent file, and messages to be displayed on social media, in a given language.

5. Phases (required): a phase of your experiment, which may contain one or more blocks. Note that every experiment needs to have at least one phase with one block configured.

    If you select "dashboard", the phase will appear as a dashboard, from which users can select which block to play. If "dashboard" is false, the blocks will be presented in linear order to the participant. If you select "randomize", the blocks will be shuffled, either in the dashboard view, or the linear procedure.

    Within a phase, you have the option to add one or more **blocks**, with the following options:

    - Index: order in which block should appear in the phase (will be ignored when `phase.randomize` is set)

    - Slug: unique slug of the block

    - Rules: the ruleset for the block

    - Rounds: how many rounds should be presented to the participant (*used in some, but not all rulesets!*)

    - Bonus points: bonus points to be awarded to the participant under given conditions (*used by very few rulesets*)

    - Playlists: select one or more playlists to be associated with the block (*note that some rulesets require a very specific format for the playlist, this will be checked when you save the experiment, and may generate warnings*)

    - BlockTranslatedContent: a name and description of the block in a given language, will only be shown in the dashboard view

6. a Social Media Config to customize the tags and url which should be shown when participants share that they played the experiment on social media, as well as the channels in which they can share

