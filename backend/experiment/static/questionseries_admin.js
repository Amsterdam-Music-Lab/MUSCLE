
document.addEventListener("DOMContentLoaded", (event) => {

    async function getQuestionGroups(){

        let response = await fetch(`/question/question_groups/`)

        if (response.ok) {
            return await response.json()
        }
    }

    getQuestionGroups().then( (questionGroups) => {

        let buttonAddQuestionGroup = document.createElement("input")
        buttonAddQuestionGroup.type = "button"
        buttonAddQuestionGroup.value = "Add all questions in group"
        buttonAddQuestionGroup.addEventListener("click", addQuestionGroup)

        let selectQuestionGroup = document.createElement("select")

        Object.keys(questionGroups).sort().forEach( (group) => {
            option = document.createElement("option")
            option.innerText = group
            selectQuestionGroup.append(option)
        })

        document.querySelector('#questioninseries_set-group').append(buttonAddQuestionGroup, selectQuestionGroup)

        function addQuestionGroup() {

            // "Add another Question in series" is already created by Django
            let addQuestionAnchor = document.querySelector(".add-row a")

            questionGroups[selectQuestionGroup.value].forEach ( (questionKey) => {

                totalFormsInput = document.querySelector("#id_questioninseries_set-TOTAL_FORMS")
                totalFormsBefore = Number(totalFormsInput.value)
                addQuestionAnchor.click()
                totalForms = Number(totalFormsInput.value)

                if (totalForms == totalFormsBefore + 1) {
                    questionSelect = document.querySelector(`#id_questioninseries_set-${totalForms-1}-question`)
                    questionSelect.querySelector(`option[value=${questionKey}]`).selected = true
                    document.querySelector(`#id_questioninseries_set-${totalForms-1}-index`).value = totalForms
                }
            })
        }
    })
})
