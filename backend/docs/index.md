# Overview of the application

These pages contain documentation of the MUSic-related Citizen Science Listening Experiments (MUSCLE) infrastructure.

This application has been set up to run online listening experiments for music research. It presents questions, and typically audio stimuli, to participants, and collects their feedback.

The application consists of a backend in Django (Python), and a frontend in React (JavaScript). Upon load, the frontend makes a call to the backend's `experiment` endpoint. The `experiment` application contains `actions` (i.e., data to be serialized for frontend views: all actions have a corresponding frontend component), `questions` (i.e., texts for demographic questions or questions on musical expertise) and `rules` (i.e., the description of an experiment's logic). A call to `experiment/slug` will locate the rules associated with the slug, and return the rule's `first_round`. The `first_round` usually consists of a number of actions: an explanation of the experiment, a consent form (registered with the `Participant`), optionally a view to select a playlist, and will then create the `Session` for that experiment. Note that the `first_round` cannot contain any actions which require passing a `result_id`, as these require a `Session` to work.

The frontend will then request data for the next views via `session/next_round`, which is provided via the rules' `next_round` function. This typically contains a `Trial` or another view requesting user feedback. A `Result` is created for each user feedback, and its `result_id` is included in the response. It may also include a `section` id, to be loaded from the `section` endpoint. Once the user gives feedback, this is sent to the `result/score` endpoint, which registers the user's response, optionally assigns a score, and then makes another call to the rules' `next_round` function.

`Result`s can either be *profile* type results, i.e., they are demographic information associated with a participant, and not expected to change. There is an option to avoid asking profile questions multiple times through the `experiment.questions.utils.unasked_question` function. `Result`s can also be tied to a *session* instead, and ideally give insights into the phenomena an experiment is set up to test.

After each result, the participant may get feedback in a `Score` view, and at the end of the experiment, they will be presented with a `Final` view, which may include their final score, as well as links for sharing in social media, and a personalized link which gives them an overview of the experiments they participated in.

