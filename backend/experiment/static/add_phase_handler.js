document.addEventListener('formset:added', (event) => {
    if (event.detail.formsetName == 'phases') {
        const experimentId = document.querySelector('[id$=experiment]').value;
        fetch('/experiment/phase/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: 'experiment_id=' + experimentId
        }).then(response => {
            if (response.error) {
                alert(response.error);
            }
        });
    }
    
});
