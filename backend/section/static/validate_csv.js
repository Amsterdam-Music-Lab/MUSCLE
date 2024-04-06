// on document laod, no jquery
document.addEventListener('DOMContentLoaded', function() {

    // name=csv
    const csvInput = document.querySelector('textarea[name="csv"]');
    csvInput.addEventListener('blur', (e) => validateCSV(e.target.value));

    const csvFormRow = document.querySelector('.form-row.field-csv');
    
    // create a new empty div element to hold validation messages
    const validationMessages = document.createElement('div');
    validationMessages.id = 'csvValidationMessages';
    validationMessages.className = 'csv-validation-messages';
    csvFormRow.appendChild(validationMessages);

    // run validation on initialization to warn user straight away of potential issues
    validateCSV(csvInput.value);
});

async function validateCSV(csv) {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    const response = await fetch('/section/validate_csv/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ csv })
    });

    const data = await response.json();
    const message = data.message || 'No message was given';
    const warnings = data.warnings || [];
    const errors = data.errors || [];

    const validationMessages = document.getElementById('csvValidationMessages');
    validationMessages.innerHTML = '';

    if (warnings.length > 0) {
        const warningsList = document.createElement('ul');
        warnings.forEach(warning => {
            const li = document.createElement('li');
            li.className = 'alert alert--warning mt-2'
            li.textContent = warning;
            warningsList.appendChild(li);
        });
        validationMessages.appendChild(warningsList);
    }

    if (errors.length > 0) {
        const errorsList = document.createElement('ul');
        errors.forEach(error => {
            const li = document.createElement('li');
            li.className = 'alert alert--error mt-2'
            li.textContent = error;
            errorsList.appendChild(li);
        });
        validationMessages.appendChild(errorsList);
    }

    const messageUl = document.createElement('ul');
    const messageLi = document.createElement('li');
    const alertClassName = errors.length > 0 ? 'alert--error' : warnings.length > 0 ? 'alert--warning' : 'alert--success';
    messageLi.className = `alert ${alertClassName} mt-2 bold`
    messageLi.textContent = message;
    messageUl.appendChild(messageLi);
    validationMessages.appendChild(messageUl);

    if (errors)

    return true;
}
