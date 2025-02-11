# Running an experiment

One you've setup your experiment in the admin interface, you can run it by navigating with the browser to:

`localhost:3000/{your_experiment_slug}`

## Running an experiment using a participant_id

This will set a cookie for the participant, which expires in 3 months. After that period, if the same participant starts another experiment, or another block in the same experiment, a new participant will be created in the database, making it impossible to link those results to the same participant.

To overcome this you can start an experiment with a `participant_id` in the URL. This can be any combination of letters and/or numbers.

`localhost:3000/{your_experiment_slug}?participant_id={participant_id}`

This way you can come back anytime to resume an experiment with a specific participant using the `participant_id` and link all results to the participant.

## Refreshing the browser

Be aware that refreshing the browser, while running a block of an experiment, will start a new session and restart the current block to the beginning.
