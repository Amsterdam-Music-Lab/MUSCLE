// Hide all sessions
const closeSessions = () => {   
    document.getElementById("all-sessions").classList.add("hide");
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
    document.getElementById("results-" + id).classList.remove("hide");   
}

// Hide all results
const closeResults = () => {
    document.querySelectorAll(".show-results").forEach(function (element) {
        element.classList.add("hide");
    })
}

// Attach event to show all participants button
document.getElementById("show-participants").addEventListener("click", () => {                                    
    document.getElementById("all-participants").classList.remove("hide");
})

// Attach event to show all sessions button
document.getElementById("show-sessions").addEventListener("click", () => {                                    
    document.getElementById("all-sessions").classList.remove("hide");
    document.querySelectorAll(".session-row").forEach(function (element) {
        element.classList.remove("hide");
    })
})
