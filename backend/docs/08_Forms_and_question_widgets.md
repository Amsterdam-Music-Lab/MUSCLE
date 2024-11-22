# Forms and question widgets

As mentioned before, a `Trial` may contain a `Form`, which present one or more questions to the user. We have a choice of multiple question widgets:

- [Autocomplete](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--autocomplete)  
- [ButtonArray](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--button-array)  
- [Checkboxes](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--checkboxes)  
- [Dropdown](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--dropdown)  
- [Radios](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--radios)  
- [TextRange](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--text-range)  
- [IconRange](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--icon-range)  
- [String](https://amsterdam-music-lab.github.io/MUSCLE/?path=/story/question--default)  

## Initializing a Question
An example of how a question is initialized in the Python backend:
```python
question = RadiosQuestion(
        key=key,
        question=_('Does this sound like song or speech to you?'),
        choices=[
            _('sounds exactly like speech'),
            _('sounds somewhat like speech'),
            _('sounds neither like speech nor like song'),
            _('sounds somewhat like song'),
            _('sounds exactly like song')],
        result_id=prepare_result(key, session, section=section, scoring_rule='LIKERT')
    )
```
The `key` is a short name of the question. With every question, we also send a `result_id`. This means we can already register information in the database, such as (in this case) the section this question refers to, or the scoring rule by which we assign a score after the participant gives a response.

## Initializing a Form
After defining the question above, we can then wrap it in a form as follows:
```python
form = Form([question])
```
