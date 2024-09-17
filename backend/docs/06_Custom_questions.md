# Custom questions

## The backend directory
To add questions that haven't yet been added to the MUSCLE infrastructure, you'll have to navigate to the backend directory. It has the following file structure:
```bash
.
├── aml
├── experiment
├── locale
├── logs
├── participant
├── requirements
├── requirements.in
├── result
├── section
├── session
└── upload
```

The backend is written in Python, so a little bit of familiarity with programming is required. Within the backend directory, go to the `experiment` directory. Within, you find the following file structure:
```bash
.
├── actions
├── fixtures
├── management
├── migrations
├── questions
├── rules
├── standards
├── templates
└── tests
```

The files in the `rules` directory specify the logic of experiments. We'll turn to those later.

The files in the `questions` directory contain the questions, as Python classes. For instance, if you look into the file `goldsmiths.py` you'll see the following:
<img width="720" alt="Screenshot 2023-11-14 at 14 30 51" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/723f1add-602c-4e34-ae01-4b683af56157">

We have different question types available, all imported from `backend/experiment/actions/forms.py`:
- NumberQuestion (number field)
- TextQuestion (text field)
- BooleanQuestion (yes/no buttons)
- ButtonArrayQuestion (more than 2 buttons)
- RadiosQuestion (radio buttons)
- DropdownQuestion (dropdown menu)
- AutoCompleteQuestion (dropdown menu with autocomplete)
- RangeQuestion (slider)
- LikertQuestion (slider in which chosen category is displayed on top)

As you can see, the Goldsmith's Musical Sophistication Index uses many LikertQuestions. LikertQuestions can be initialized with a `key` and a `question` argument. The key helps us find the responses to the question back in the database, so it's a good idea to use a unique, recognizable key. The key should not contain other characters than numbers, letters and underscores.

The `question` is the prompt shown to a participant. Here, it is wrapped in a translation tag (represented by `_( )`): this means the question can be translated into different languages.

If you wish to add questions to the infrastructure, you are of course welcome to so in a fork of the project. However, if you think the questions may be of interest to other users, consider making a [git branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) and contribute to this repository with a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
