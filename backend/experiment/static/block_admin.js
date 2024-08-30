
document.addEventListener("DOMContentLoaded", (event) => {

    fixHeadings();

    // Get experiment id from URL
    match = window.location.href.match(/\/experiment\/block\/(.+)\/change/);
    experiment_id = match && match[1];

    let buttonAddDefaultQuestions = document.createElement("input");
    buttonAddDefaultQuestions.type = "button";
    buttonAddDefaultQuestions.value = "Add rules' defaults and save";
    buttonAddDefaultQuestions.addEventListener("click", addDefaultQuestions);

    let message = document.createElement("span");
    message.id = "id_message";
    message.className = "form-row";

    const questionSeriesSetGroup = document.querySelector('#questionseries_set-group');
    questionSeriesSetGroup.append(buttonAddDefaultQuestions, message);

    let selectRules = document.querySelector("#id_rules");
    selectRules.onchange = toggleButton;
    toggleButton();

    function toggleButton(e) {

        // Check if we are on a Change Experiment (not Add Experiment) and if selection for Experiment rules has not changed
        if (experiment_id && (selectRules[selectRules.selectedIndex] === selectRules.querySelector("option[selected]"))) {
            buttonAddDefaultQuestions.disabled = false;
            message.innerText = "";
        } else {
            buttonAddDefaultQuestions.disabled = true;
            message.innerText = "Save Block first";
        }
    }

    async function addDefaultQuestions() {

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let response = await fetch(`/experiment/add_default_question_series/${experiment_id}/`,
            { method: "POST", mode: 'same-origin', headers: { 'X-CSRFToken': csrftoken } })

        if (response.ok) {
            location.reload();
        }
    }
})

/** Function to fix the headings for tabular inline forms
  * @todo TODO: Remove this `fixHeadings` function once the issue with headings is fixed in `django-nested-admin`.
  * - https://github.com/theatlantic/django-nested-admin/issues/261
  * - https://github.com/theatlantic/django-nested-admin/pull/259
  */
function fixHeadings() {
    // Find the h2 element
    const h2Elements = document.querySelectorAll('.tabular h2.inline-heading');

    for (const h2Element of h2Elements) {

        // Get the next sibling node (which should be the text node)
        const textNode = h2Element.nextSibling;

        console.log(h2Element, textNode);

        // Check if the next sibling is a text node and contains non-whitespace content
        if (textNode && textNode.nodeType === Node.TEXT_NODE && textNode.textContent.trim()) {
            // Move the text content into the h2 element
            h2Element.textContent = textNode.textContent.trim() + h2Element.textContent;

            // Remove the original text node
            textNode.remove();
        }
    }
}
