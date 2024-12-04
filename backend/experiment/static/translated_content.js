document.addEventListener("DOMContentLoaded", function () {
    initTabbedTranslation();
});

function initTabbedTranslation() {
    const tabButtons = document.querySelectorAll('.translated-content-tab');
    const forms = document.querySelectorAll('.translated-content-form');
    tabButtons[0].classList.toggle("active");
    forms.forEach(form => form.classList.toggle("hidden"));
    forms[0].classList.toggle("hidden");
    tabButtons.forEach(tabButton => {
        tabButton.addEventListener("click", () => {
            if (!tabButton.classList.contains("active")) {
                tabButtons.forEach( button => button.classList.toggle("active"));
                forms.forEach(form => {
                    form.classList.toggle("hidden");
                });
            }
        });
    });
}
