# Creating an experiment

## Admin interface
Make sure you're logged in to the admin interface (see previous step).

Then, next to "Experiments" click "Add".
<img width="1002" alt="AddExperiment" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/f71e77a1-1308-40f3-b8d5-e6f81f2ae0c0">

## The Experiment form
The form which appears lets you select the following fields:
1. a name for your new experiment (required)
2. a slug for the experiment (required). The slug is the part of the part of the URL which will be used to find the experiment from the frontend. In this case, the experiment will be available from `localhost:3000/someslug`.
3. a URL with more information about the experiment (optional)
4. a hashtag for posting about the experiment on social media (optional)
5. a preferred language in which the experiment should be shown (optional). If this field is left "Unset", this means that the language will be determined based on the user's browser settings. Otherwise, the set language will be shown, with a fallback to English in case no translation is available.
6. the rules of the experiment (required). This sets which logic the experiment follows. You can select implemented "rules" that have already been implemented in Python.
7. the number of rounds the experiment should run (optional). This is set to 10 by default, which is usually fine. Not all rules files use rounds to control when specific "phases" of the experiment start or end. Think of staircasing experiments, which will present more or less difficult stimuli depending on the user's responses. These rules just ignore the "Rounds" field.
8. bonus points (optional). Few experiments use this field, but you can use this to give bonus points to a participant who completed the experiment.
9. a playlist (optional). For most experiments (except for those which are questionnaires) you will want to select a playlist here.
<img width="828" alt="AddExperimentPart1" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/97d57e23-aa26-40db-83ec-a1312873fdf4">

10. an experiment series (optional). This is used to string several experiments together. Best to leave alone, may be deprecated.
11. questions (optional). You can select any questions you want to ask your participants before starting an audio experiment here.
<img width="992" alt="AddExperimentPart2" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/d8253af5-9be2-4428-a90a-9e612c863fb8">
