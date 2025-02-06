# Overview of the different actions for experiments

The actions that can be used by experiments are formalized in `backend/experiment/actions`

## 1. Explainers
An Explainer presents some information to participants of an experiment. They can include a number of Steps, which may or may not be numbered.
[Preview](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/explainer--default)

## 2. Playlist
If there are multiple playlist tied to an experiment, the Playlist widget lets participants select one of them for use in the experiment.

## 3. Consent
This action is used to present a consent form to the user, and a button to agree, or quit the experiment.
The content of the consent agreement can be loaded from the rules file or uploaded from the admin interface.

A consent form uploaded from the admin interface will override the one loaded from the rules file, so that each instance of an experiment can have its own consent file.
Click on your experiment in the admin interface to upload your custom consent file at ```localhost:8000/admin/experiment```

Files loaded from the rules file must be placed in ```admin/experiment/templates/consent```
Files uploaded from the admin interface are placed in ```backend/upload/consent```

Allowed file formats:
- HTML (.html)
    - May contain django template tags
- MARKDOWN (.md)

### Initializing a Consent form
```
consent = Consent(
            experiment.consent,
            title=_('Informed consent'),
            confirm=_('I agree'),
            deny=_('Stop'),
            url='consent/<template file>'
            )
```

[Click here for an online editor for markdown files - (dillenger.io)](https://dillinger.io/)

## 4. Redirect
This action allows to redirect to another website.

## 5. Score
This action shows scores or messages to participants after trials.

## 6. Final
This action finishes the session for the participant, and shows a final score or message.

## 7. Trial
This action presents questions, audio and text to a user, and will be usually repeated multiple times ("rounds") in an experiment. It may contain any of the following elements:
- a Form object with one or multiple Questions
- a Playback object describing different player widgets
- a Html element to present any other kind of information, such as images or videos, to the participant

The next sections will give an overview of Form and Playback objects.
