document.addEventListener("DOMContentLoaded", function () {
    initCollapsibleInlineForms();
    floatingSubmitRow();
});

function initCollapsibleInlineForms() {

    const collapsibleInlineForms = document.querySelectorAll('.inline-group');

    collapsibleInlineForms.forEach(collapsibleInlineForm => {
        const toggleButton = collapsibleInlineForm.querySelector('.inline-heading');
        const form = collapsibleInlineForm.querySelector('.djn-items');
        const addNew = collapsibleInlineForm.querySelector('.djn-add-item');

        let collapsedInfo = toggleButton.querySelector('#collapsed-info');

        if (!collapsedInfo) {
            // create text element in button to show that the form is collapsed
            collapsedInfo = document.createElement('small');
            collapsedInfo.id = 'collapsed-info';
            collapsedInfo.innerText = ' (-)';
            collapsedInfo.style.color = '#fff';
            toggleButton.appendChild(collapsedInfo);
        }

        toggleButton.addEventListener('click', () => {
            form.classList.toggle('hidden');
            addNew.classList.toggle('hidden');

            const currentlyHidden = form.classList.contains('hidden');

            if (currentlyHidden) {
                // create text element in button to show that the form is collapsed
                collapsedInfo.innerText = ' (+)';
            } else {
                // remove the text element in button to show that the form is expanded
                collapsedInfo.innerText = ' (-)';
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
        if (window.pageYOffset + window.innerHeight < submitRowOffset + 20) {
            submitRow.classList.add('floating');
        } else {
            submitRow.classList.remove('floating');
        }
    });
}
