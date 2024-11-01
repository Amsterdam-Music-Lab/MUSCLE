// Hide all sessions
const closeSessions = () => {
    document.getElementById("all-sessions").close();
    document.querySelectorAll(".session-row").forEach(function (element) {
        element.classList.add("hide");
    })
}

// Hide all participants
const closeParticipants = () => {
    document.getElementById("all-participants").classList.add("hide");
}

// Show results for specific session
const showResults = (id) => {
    const results = document.getElementById("results-" + id);
    results.showModal();
}

// Hide all results
const closeResults = (id) => {

    if (id) {
        const results = document.getElementById("results-" + id);
        results.close();

        return;
    }

    document.querySelectorAll(".show-results").forEach(function (element) {
        element.close();
    })
}

// Attach event to show all participants button
document.getElementById("show-participants").addEventListener("click", () => {
    document.getElementById("all-participants").classList.remove("hide");
})

// Attach event to show all sessions button
document.getElementById("show-sessions").addEventListener("click", () => {
    document.getElementById("all-sessions").showModal();
    document.querySelectorAll(".session-row").forEach(function (element) {
        element.classList.remove("hide");
    })
})
