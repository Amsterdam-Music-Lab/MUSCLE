document.addEventListener("DOMContentLoaded", function () {
    initTabbedTranslation();
});

function initTabbedTranslation() {
    const parentElements = document.querySelectorAll('.translated-content-parent')
    parentElements.forEach(parent => {
        const tabButtons = parent.querySelectorAll('.translated-content-tab');
        const forms = parent.querySelectorAll('.translated-content-form');
        tabButtons[0].classList.add("active");
        forms.forEach(form => form.classList.add("hidden"));
        forms[0].classList.remove("hidden");
        tabButtons.forEach((tabButton, index) => {
            tabButton.addEventListener("click", () => {
                if (!tabButton.classList.contains("active")) {
                    tabButtons.forEach( button => button.classList.remove("active"));
                    tabButton.classList.add("active");
                    forms.forEach(form => {
                        form.classList.add("hidden");
                    });
                    forms[index].classList.remove("hidden");
                }
            });
        });
    });
}
