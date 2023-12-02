
document.addEventListener("DOMContentLoaded", (event) => {

	let fieldLabel = document.querySelector(".field-questions > div > label")
	let groups = document.querySelectorAll(".field-questions > div > ul > li")
	let questions = document.querySelectorAll("#id_questions label")

	let buttons = [
		{"text": "Show all", "eventListener": showAll(true)},
		{"text": "Hide all", "eventListener": showAll(false)},
		{"text": "Select all", "eventListener": selectAll(true)},
		{"text": "Unselect all", "eventListener": selectAll(false)},
		{"text": "Rules' defaults", "eventListener": setDefaultQuestions}
	]

	let buttonsColumn = document.createElement("div")
	buttonsColumn.className = "buttons-column"
	fieldLabel.append(buttonsColumn)

	buttons.forEach( (button) => {
		let btn = createButton()
		btn.innerText = button.text
		btn.addEventListener("click", button.eventListener)
		buttonsColumn.append(btn)
	})
	
	groups.forEach( (group) => {

		let buttonsRow = document.createElement("span")
		buttonsRow.className = "buttons-row"

		let btn = createButton()
		btn.innerText = "Select group"
		btn.addEventListener("click", selectGroup(group, true))
		buttonsRow.append(btn)

		btn = createButton()
		btn.innerText = "Unselect group"
		btn.addEventListener("click", selectGroup(group, false))
		buttonsRow.append(btn)

		buttonsRow.style.display = "none"
		group.querySelector("ul").style.display = "none"
		group.insertBefore(buttonsRow, group.childNodes[1])

		btn = createButton()
		btn.innerText = "Show"
		btn.className += " button-show-hide"
		btn.addEventListener("click", toggleShowHide)
		group.insertBefore(btn, group.childNodes[0])

	})

	function createButton(){
		let btn = document.createElement("button")
		btn.className = "button"
		btn.type = "button"
		return btn
	}

	function showAll(show) {
		return () => groups.forEach(group => showGroup(group, show))
	}

	function showGroup(group, show) {
		let questionList = group.querySelector("ul")
		questionList.style.display = show ? "" : "none"

		let showHideButton = group.querySelector(".button-show-hide")
		showHideButton.innerText = show ? "Hide" : "Show"

		let selectButtonRow = group.querySelector(".buttons-row")
		selectButtonRow.style.display = show ? "" : "none"
	}

	function selectGroup(group, checked) {
		let checkbxs = group.querySelectorAll("input")
		return () => checkbxs.forEach(c => c.checked = checked)
	}

	function selectAll(checked){
		return () => groups.forEach(group => {
			selectGroup(group, checked)() 
			showGroup(group, true)
		})
	}

	function toggleShowHide() {

		let group = this.parentElement
		let questionList = group.querySelector("ul")

		if (questionList.style.display == "" || questionList.style.display == "block") {
			showGroup(group, false)
		} else if (questionList.style.display == "none") {
			showGroup(group, true)
		}
	}

	// Question text presented in experiment admin must include question key in parenthesis, e.g. (dgf_country_of_origin)
	async function setDefaultQuestions() {

	    // Selected Rules
		let rules = document.getElementById("id_rules").value

		let defaultQuestions = []

		if (rules) {
			//Get default question list
			let url=`/experiment/default_questions/${rules}/`
			let response = await fetch(url)

			if (response.ok) {
				let json_data = await response.json()
				defaultQuestions = json_data['default_questions']
			}
		}

		// Uncheck all questions
		selectAll(false)()

		// Check questions present in the default questions list
		for (const question of questions) {
			for (const defaultQuestion of defaultQuestions) {
				if (question.textContent.includes(`(${defaultQuestion})`) > 0) {
					question.querySelector("input").checked = true
				}
			}
		}	
	}

})


