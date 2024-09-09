
document.addEventListener("DOMContentLoaded", (event) => {

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
