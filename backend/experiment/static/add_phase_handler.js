document.addEventListener('formset:added', (event) => {
    if (event.detail.formsetName == 'phases') {
        fetch('phase/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
        }).then(response => {
            if (response.error) {
                console.error(response.error);
            } else { window.location.reload(); }
        });
    }
});
