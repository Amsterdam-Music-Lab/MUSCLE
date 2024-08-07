// Show sessions for a specific experiment
const showBlockSessions = (id) => {
    document.getElementById(`show-sessions-${id}`).addEventListener("click", function () {
        document.querySelectorAll(`.experiment-${id}`).forEach(function (element) {
            element.classList.remove("hide");
        })
        document.getElementById("all-sessions").classList.remove("hide");
    })
}

// Show sessions for a specific participant
const showParticipantSessions = (id) => {
    document.getElementById(`participant-sessions-${id}`).addEventListener("click", function () {
        document.querySelectorAll(`.participant-session-${id}`).forEach(function (element) {
            element.classList.remove("hide");
        })
        document.getElementById("all-participants").classList.add("hide");
        document.getElementById("all-sessions").classList.remove("hide");
    })
}
