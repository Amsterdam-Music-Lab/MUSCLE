document.addEventListener("DOMContentLoaded", function () {
    const formElement = document.querySelector('#experiment_form');
    const submitRow = document.querySelectorAll('.submit-row')[1]
    const activeField = document.querySelector('.form-row.field-active');
    const themeConfigField = document.querySelector('.form-row.field-theme_config');
    const fieldsetWrapper = document.createElement('fieldset');
    fieldsetWrapper.classList.add("aligned");
    themeConfigField.remove();
    fieldsetWrapper.append(themeConfigField);
    activeField.remove();
    fieldsetWrapper.append(activeField);
    formElement.insertBefore(fieldsetWrapper, submitRow);
    const questionSeriesFieldsets = document.querySelectorAll('fieldset[aria-labelledby*="questionseries_set-heading"]');
    questionSeriesFieldsets.forEach(el => {
        const defaultQuestionsButton = el.querySelector('#default-questions');
        if (defaultQuestionsButton) {
            defaultQuestionsButton.addEventListener('click', addDefaultQuestions);
        }
    });
    floatingSubmitRow();
});

async function addDefaultQuestions(event) {
    const slug = event.currentTarget.name;

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let response = await fetch(`/experiment/block/${slug}/default_question_series/`,
        { method: "POST", mode: 'same-origin', headers: { 'X-CSRFToken': csrftoken } })

    if (response.ok) {
        location.reload();
    }
}

function initCollapsibleInlineForms() {

    const collapsibleInlineForms = document.querySelectorAll('.inline-group:not([data-inline-model*="translatedcontent"])');

    collapsibleInlineForms.forEach(collapsibleInlineForm => {
        const toggleButton = collapsibleInlineForm.querySelector('.inline-heading');
        const form = collapsibleInlineForm.querySelector('.djn-items');
        const addNew = collapsibleInlineForm.querySelector('.djn-add-item');

        let collapsedInfo = toggleButton.querySelector('#collapsed-info');

        if (!collapsedInfo) {
            // create text element in button to show that the form is collapsed
            collapsedInfo = document.createElement('small');
            collapsedInfo.id = 'collapsed-info';

            collapsedInfo.innerText = ' \u25b2';
            collapsedInfo.style.color = '#fff';
            collapsedInfo.style.fontSize = '.75rem';
            toggleButton.appendChild(collapsedInfo);
        }

        toggleButton.addEventListener('click', () => {
            form.classList.toggle('hidden');
            addNew.classList.toggle('hidden');

            const currentlyHidden = form.classList.contains('hidden');

            if (currentlyHidden) {
                // create text element in button to show that the form is collapsed
                collapsedInfo.innerText = ' \u25bc';
            } else {
                // remove the text element in button to show that the form is expanded
                collapsedInfo.innerText = ' \u25b2';
            }
        });
    });
}

function floatingSubmitRow() {
    const submitRow = document.querySelector('.submit-row');

    if (!submitRow) {
        console.error('No submit row found');
        return;
    }

    const submitRowOffset = submitRow.offsetTop;

    window.addEventListener('scroll', function () {
        if (window.scrollY + window.innerHeight < submitRowOffset + 20) {
            submitRow.classList.add('floating');
        } else {
            submitRow.classList.remove('floating');
        }
    });
}
