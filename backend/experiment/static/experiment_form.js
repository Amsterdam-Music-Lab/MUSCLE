document.addEventListener("DOMContentLoaded", function () {
    initCollapsibleInlineForms();
    initTabbedTranslation();
    floatingSubmitRow();
});

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

const initTabbedTranslation = () => {
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
