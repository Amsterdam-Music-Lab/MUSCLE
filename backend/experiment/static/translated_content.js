document.addEventListener("DOMContentLoaded", function () {
    initTranslatedContentForms();
});

function initTranslatedContentForms() {

    const translatedContentForms = document.querySelectorAll(".djn-item[id^='translated_content']");
    const translatedContentParent = document.querySelector(".djn-group[id^='translated_content']");

    const tabsContainer = document.createElement('div');
    tabsContainer.className = 'tabs-container';
    const heading = translatedContentParent.querySelector('h2');
    heading.append(tabsContainer);

    const addNew = translatedContentParent.querySelector('.djn-add-item');
    addNew.querySelector('a').innerText = '';

    translatedContentForms.forEach(translatedContentForm => {
        const tabButton = document.createElement('button');
        tabButton.role = 'button';
        tabButton.innerText = 'lancode';
        tabButton.className = 'translated-content-tab';
        tabsContainer.appendChild(tabButton);


        tabButton.addEventListener('click', () => {
            form.classList.toggle('hidden');
            addNew.classList.toggle('hidden');

            const currentlyHidden = form.classList.contains('hidden');

        });
    });

    tabsContainer.appendChild(addNew);
}
