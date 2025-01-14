
document.addEventListener("DOMContentLoaded", (event) => {
    document.getElementById('default-questions').addEventListener("click", addDefaultQuestions);

    async function addDefaultQuestions(event) {
        const slug = event.currentTarget.name;

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let response = await fetch(`/experiment/block/${slug}/default_question_series/`,
            { method: "POST", mode: 'same-origin', headers: { 'X-CSRFToken': csrftoken } })

        if (response.ok) {
            location.reload();
        }
    }
})
