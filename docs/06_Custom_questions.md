# Custom questions
You can add questions to the MUSCLE infrastructure through the admin interface.

In the admin overview, you can see the question app with three models:
<img width="656" alt="The Question App" src="../assets/images/QuestionApp.png">

## Choice Lists
Choice lists are collections of answer options for multiple choice questions, for example statements of preference for a Likert scale. The Choice Lists that are available are set through the `question.fixtures.choice_lists.yml` file in `yaml` format. These choice lists cannot be edited in the admin interface. You can add custom choice lists through the admin interface, however.
<img width="500" alt="Choice List" src="../assets/images/ChoiceList.png"> # TODO

## Question Lists
Question Lists are sets of questions you can attach to a given block in your experiment. If you click "Add", you will see the following form:
<img alt="Question List" src="../assets/images/QuestionList.png"> # TODO

You need to give the Question List a descriptive name, and choose the block with which it is associated (important: the block will only display questions if its ruleset has a method that presents these questions to the participant), and an index, used for handling order if you have multiple `QuestionList`s attached to a given block.

You can also choose whether or not the questions in the Question List should be presented in randomized order.

To add questions to the Question List, you can either select from a list of questions, or add all questions from a question bank, defined in the `question.fixtures` directory in `yaml` format. After creating a Question Link from a bank, you can remove questions or add other questions as you wish without affecting the original question bank.

## Questions
Questions are the actual question objects. Many questions are already configured through Python fixtures, and cannot be edited through the admin interface. You can duplicate preconfigured questions by selecting a question and select "Duplicate", or you can click "Add" to create a new question from scratch in the following form:
<img alt="Question" src="../assets/images/Question.png">

On the top, you can choose the language(s) in which you wish to enter the question. The languages that are shown can be configured through the `LANGUAGES` settings in Django. Note that it is not necessary to provide translations, but that a question will be much more reusable if it has translations to multiple languages.

Enter a descriptive question key, e.g., `favorite_food_open_question`. Note that the key can only contain letters, numbers, and underscores.

The Question is the actual question text that will be asked to the participant. Optionally, you can also add an Explainer with instructions to the participant, e.g., "Rate on a scale of 1 to 7".

Indicate the *Type* of question, which influences the widget participants will see:

- AutoComplete will show a dropdown which will autocomplete if a participant starts typing

- ButtonArray will show answer options as a row of buttons (note that this widget mostly makes sense for few and short answers, as in the "Boolean" Choice List)

- Checkmarks will show a list of options with checkmarks (multiple can be selected, specify if more than one option is required in "Min values")

- Dropdown will show a dropdown menu

- Icon Range will show a range slider with icons as answer options

- Number will show a number selector (specify minimum and maximum through `Min value` and `Max value` fields)

- Range will show a range slider with numbers (specify minimum and maximum through `Min value` and `Max value` fields)

- TextRange will show a slider with different answer options

- Text will show a text field - use this for open questions (secify maximum length through `Max length` field)

For all question types which present choices to the participant, you can then choose one of the preset choice lists, or add a new one by clicking the `+` button.

Finally, you can indicate whether your question can be skipped by the participant.

