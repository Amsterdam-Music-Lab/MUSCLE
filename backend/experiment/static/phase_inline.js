document.addEventListener('DOMContentLoaded', function() {
    const phaseContainer = document.querySelector('#phases-group');
    if (phaseContainer) {
        phaseContainer.addEventListener('click', function(event) {
            // Check if the clicked element is the "Add another" link
            if (event.target.matches('.add-row a')) {
                event.preventDefault();
                const experimentId = document.querySelector('[id$=experiment]').value;
                fetch('/experiment/phase/create/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: 'experiment_id=' + experimentId
                }).then(response => {
                    if (response.ok) {
                        window.location.reload()
                    } else {
                        alert(response.error || 'Error creating phase');
                    }
                });
            }
        });
    }
});