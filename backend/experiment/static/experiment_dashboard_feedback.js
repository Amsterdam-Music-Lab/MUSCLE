// Show feedback for a specific experiment
const showBlockFeedback = (id) => {
    document.getElementById(`show-feedback-${id}`).addEventListener("click", function () {
        document.querySelectorAll(`.block-${id}`).forEach(function (element) {
            element.classList.remove("hide");
        })
        document.getElementById("all-feedback").showModal();
    })
}
