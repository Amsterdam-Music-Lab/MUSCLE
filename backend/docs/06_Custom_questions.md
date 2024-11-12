# Custom questions
You can add questions to the MUSCLE infrastructure through the admin interface.

In the admin overview, you can see the question app with three models:
<img width="656" alt="The Question App" src="/assets/images/QuestionApp.png">

## Question Groups
Question Groups are sets of questions which are predefined, such as "Demographics" or question sets from the Goldsmith MSI questionnaire. We recommend not editing these, but you can add your own Question Group if you want to reuse the same set of questions in multiple experiments.
<img width="500" alt="Question Group" src="/assets/images/QuestionGroup.png">

## Question Series
Question Series are sets of questions you can attach to a given block in your experiment. If you click "Add", you will see the following form:
<img alt="Question Series" src="/assets/images/QuestionSeries.png">

You need to give the Question Series a descriptive name, and choose the block with which it is associated (important: the block will only display questions if its ruleset has a method that presents these questions to the participant), and an index, used for handling order if you have multiple `QuestionSeries` attached to a given block.

You can also choose whether or not the questions in the Question Series should be presented in randomized order.

To add questions to the Question Series, you can either select from a list of questions, or add all questions from a Question Group. You can then remove or add other questions as you wish.

## Questions
Questions are the actual question objects. Many questions are already configured. If you click "Add", you will see the following form:
<img alt="Question" src="/assets/images/Question.png">

On the top, you can choose the language(s) in which you wish to enter the question. The languages that are shown can be configured through the `MODELTRANSLATION_LANGUAGES` settings in Django. Note that it is not necessary to provide translations, but that a question will be much more reusable if it has translations to multiple languages.

Enter a descriptive question key, e.g., `favorite_food_open_question`. Note that the key can only contain letters, numbers, and underscores.

The Question is the actual question text that will be asked to the participant. Optionally, you can also add an Explainer with instructions to the participant, e.g., "Rate on a scale of 1 to 7".

Indicate the *Type* of question, which influences the widget participants will see:

- AutoCompleteQuestion will show a dropdown which will autocomplete if a participant starts typing

- BooleanQuestion will show yes/no buttons

- ChoiceQuestion will show a select menu (can be further configured as radio / dropdown etc.)

- LikertQuestion will show a slider with different answer options

- LikertQuestionIcon will show icons instead of text for different answer options

- NumberQuestion will show a number selector

- TextQuestion will show a text field - use this for open questions

Finally, you can indicate whether your question can be skipped by the participant.

Clicking "Save and continue editing" on all questions but `TextQuestion` will bring up another menu:
<img alt="adminList" src="/assets/images/QuestionChoice.png">

You can select different widgets:
- BUTTON_ARRAY: a horizontal array of buttons with the answer options (one answer possible)
- CHECKBOXES: a vertical array of checkboxes (multiple answers possible)
- DROPDOWN: a dropdown menu (one answer possible)
- RADIOS: a vertical array of radio buttons (one answer possible)

For CHECKBOXES, you also need to indicate how many answers need to be minimally checked before the participant can click the "submit" button

Finally, you can add Choices, which are again a combination of a descriptive key (consisting of letters, numbers, and underscores), and a translatable text. The index controls the order in which choices will appear.
