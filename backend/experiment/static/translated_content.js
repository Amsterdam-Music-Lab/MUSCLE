export function initTabbedTranslation() {
    console.log("hello init!")

    const translatedContentForms = document.querySelectorAll(".djn-item[id*='translated_content']");
    const translatedContentParent = document.querySelector(".djn-group[id*='translated_content']");
    translatedContentParent.classList.add(["translated-content"]);
    translatedContentForms[0].classList.toggle("hidden");

    const tabsContainer = document.createElement('div');
    tabsContainer.className = 'tabs-container';
    const heading = translatedContentParent.querySelector('h2');
    heading.innerText = '';
    heading.style = "background-color:white";
    heading.append(tabsContainer);

    const addNew = translatedContentParent.querySelector('.djn-add-item');
    addNew.querySelector('a').innerText = '';

    translatedContentForms.forEach(translatedContentForm => {
        translatedContentForm.classList.toggle("hidden");
        const langcode = translatedContentParent.querySelector(".field-langcode");
        translatedContentForm.querySelector('h3').remove(); // remove information about object type and id
        const langcodeText = langcode.querySelector('p').innerText;
        langcode.remove();
        const tabButton = document.createElement('a');
        tabButton.innerText = langcodeText;
        tabButton.className = "translated-content-tab";
        tabButton.draggable = 'true';
        if (!translatedContentForm.classList.contains("hidden")) {
            tabButton.classList.toggle("active");
        }
        tabsContainer.appendChild(tabButton);


        tabButton.addEventListener("click", () => {
            if (translatedContentForm.classList.contains("hidden")) {
                const currentForms = document.querySelectorAll(".djn-item[id^='translated_content']");
                currentForms.forEach(form => {
                    form.classList.toggle("hidden")
                });
                const tabs = document.querySelectorAll(".translated-content-tab");
                tabs.forEach(tab => {
                    tab.classList.toggle("active")
                })
            }
        });

        tabButton.addEventListener('dragStart', () => {
            console.log('dragged tab')
        });

    });
    tabsContainer.appendChild(addNew);
}
