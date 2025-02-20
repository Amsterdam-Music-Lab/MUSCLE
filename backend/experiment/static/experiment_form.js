document.addEventListener("DOMContentLoaded", function () {
    moveFields();
    enableDefaultQuestionButtons();
    initCollapsibleInlineForms();
    floatingSubmitRow();

    // TODO: Remove this in the future once the issue is fixed in django-select2
    // re-initialize django-select2 on form change
    reinitializeDjangoSelect2OnFormChange();
});

/**
 * move theme_config and active field to bottom of form
 */
function moveFields() {
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
}

function enableDefaultQuestionButtons() {
    const questionSeriesFieldsets = document.querySelectorAll('fieldset[aria-labelledby$="questionseries_set-heading"]');
    questionSeriesFieldsets.forEach(el => {
        const defaultQuestionsButton = el.querySelector('#default-questions');
        if (defaultQuestionsButton) {
            defaultQuestionsButton.addEventListener('click', addDefaultQuestions);
        }
    });
}

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
/**
 * Re-initialize django-select2 on form change.
 * This is needed because django-select2 is not re-initialized on new inlines.
 * Let's check again in the future if this issue is fixed in django-select2 
 * and remove this function.
 * See also: https://github.com/codingjoe/django-select2/pull/300
 * @returns {void}
 */
function reinitializeDjangoSelect2OnFormChange() {

    const $ = django.jQuery;

    return $(function () {
        $('.django-select2').djangoSelect2()

        // This part fixes new inlines not having the correct select2 widgets
        function handleFormsetAdded(row, formsetName) {
            // Converting to the "normal jQuery"
            var jqRow = django.jQuery(row)

            // Because select2 was already instantiated on the empty form, we need to remove it, destroy the instance,
            // and re-instantiate it.
            jqRow.find('.django-select2').parent().find('.select2-container').remove()
            jqRow.find('.django-select2').djangoSelect2('destroy');
            jqRow.find('.django-select2').djangoSelect2()
        }

        // See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/javascript/#supporting-versions-of-django-older-than-4-1
        django.jQuery(document).on('formset:added', function (event, $row, formsetName) {
            if (event.detail && event.detail.formsetName) {
                // Django >= 4.1
                handleFormsetAdded(event.target, event.detail.formsetName)
            } else {
                // Django < 4.1, use $row and formsetName
                handleFormsetAdded($row.get(0), formsetName)
            }
        })
        // End of fix
    })
}
