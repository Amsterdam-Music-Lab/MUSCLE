# Creating an experiment

## Admin interface
In the admin interface, next to "Experiments" click "Add".

<img alt="Add Experiment" style="height:400px" src="../assets/images/ExperimentAdd.png">

## The Experiment form
You will see an empty form:
![Empty Experiment form](../assets/images/ExperimentEmptyForm.png)

In an Experiment form, you can configure three different types of experiment:

- an experiment with a single block: this is the most frequent type of experiment. A **block** is tied to a ruleset. Rulesets are defined through Python code (located in `backend.experiment.rules`).
- a *linear* experiment with multiple blocks, organized in one or more phases: a **phase** is a collection of blocks. The order of the blocks can be set to random. You could, for instance, have one phase with a block showing some introductory questions, then a phase with a number of randomized blocks (for instance, a just noticeable difference paradigm tied to different audio stimuli), and then a concluding phase with another block with a questionnaire.
- an experiment in **dashboard mode**, with a single phase and multiple blocks, in which participants can choose the order in which they step through different blocks.

## Overview of the fields in the Experiment form
The first field, `Slug`, is a unique slug for your new experiment (required) If you test locally, and put `someslug` in this field, the experiment will be available from `localhost:3000/someslug`. After that, you find a section relating to texts of the experiment, a section of phases and blocks (here, you can set whether or not the experiment will be shown in "dashboard mode"), optionally, questions tied to each block, a section of social media configurations, and a section for theme configuration ("ThemeConfig").

#### Experiment texts
The next section, headed by tabs, are the experiment texts that may be shown about the experiment:

- Language of the content
- Index: Priority of showing the content in this language (lower is higher priority)
- Name of the experiment (only shown to participants in *dashboard mode*)
- Description of the experiment (only shown to participants in *dashboard mode*)
- Consent: a consent file to be shown to the user prior to the experiment
- About content: background of the experiment (only shown to participants in *dashboard mode*)
- Social media message: message with which participants can post their results to social media. The placeholders `{points}` and `{experiment_name}` will be filled out automatically when a participant clicks the button. Note that not all social media platforms support setting the message from a share button; Facebook for instance doesn't allow this. See `Social Media Config` below for more sharing options.
- Disclaimer: a notice in the footer about who is behind the experiment (only shown to participants in *dashboard mode* if a `ThemeConfig` is linked)
- Privacy: privacy notice in the footer about treatment of the data (only shown to participants in *dashboard mode* if a `ThemeConfig` is linked)

Note that you need to *save* the experiment before seeing the changes to this section take effect. After that, if you click "+", you can add texts in another language. If you add a Dutch translation, a participant with browser setting stating preference for Dutch will get to see these Dutch texts. If the participant's preferred language is not available, the text with the lowest index will be shown as a fallback.

Note that only setting `Slug` and `Name` (bold face) are required before saving the experiment. `Index` is also a required field, but comes with a default (0).

![Slug and Texts](../assets/images/ExperimentForm1&2.jpg)

#### Phases and blocks
Phases (required): a phase of your experiment, which may contain one or more blocks. Note that every experiment needs to have at least one phase with one block configured.

![Empty Phase and Block](../assets/images/ExperimentPhaseBlockEmpty.png)

If you select "dashboard", the phase will appear in *dashboard mode*, from which users can select which block to play. If "dashboard" is unchecked, the blocks will be presented in linear order to the participant. If you select "randomize", the blocks will be shuffled, either in the dashboard view, or the linear procedure.

Within a phase, you have the option to add one or more **blocks**. Click "Add a new block". This will show you the following options:

- Index: order in which block should appear in the phase (will be ignored when the phase's `randomize` checkbox is checked)
- Slug: unique slug of the block
- Rules: the ruleset for the block
- Rounds (optional): how many rounds should be presented to the participant (*used in some, but not all rulesets!*)
- Bonus points (optional): bonus points to be awarded to the participant under given conditions (*used by very few rulesets*)
- Playlists (optional): select one or more playlists to be associated with the block (*note that some rulesets require a very specific format for the playlist, this will be checked when you save the experiment, and may generate warnings*)
- ThemeConfig (optional): You can change background, fonts and logos used for the block here.
- Block Texts: a name and description of the block in a given language, will only be shown in the dashboard view. `Name` is prefilled based on the Experiment name and the block slug. The languages of the `Block Texts` section correspond to the languages set for the experiment on top.

![Configuring a Block](../assets/images/ExperimentBlock.png)

#### Block questions (optional)
Within each block, you also see the option to add **Question Series**. This can mainly be used to add default questions (configured in the Python rules file), and to add or remove a given set of questions from them. To create new questions, refer to the [next section](/06_Custom_questions/).

Note that you need to *save the experiment* in which *block rules have been set* before you clicking "Add default questions" has an effect. You can click "Save and continue editing" to stay on the Experiment form.

![Add default questions](../assets/images/ExperimentQuestionInline.png)

#### Social Media Config (optional)
A Social Media Config can be used to customize the tags and url which should be shown when participants share that they played the experiment on social media, as well as the platforms for which share buttons will be shown. Note that the *text* that will be used for sharing by default is configured on the top of the Experiment form.

![Social media configuration](../assets/images/ExperimentSocialMedia.png)

#### Theme Configuration (optional)
You can change the background, fonts and logos used for the experiment here. For detailed information on this, see the [Custom Theme](/07_Custom_theme/) documentation.

#### Active field
The last field of the Experiment form is a checkbox indicating whether the experiment is active. This will always be checked by default. If you uncheck it, a request to `localhost:3000/{myslug}` will give you a blank screen stating `Experiment not found`. That way, you can close an experiment from further responses.
