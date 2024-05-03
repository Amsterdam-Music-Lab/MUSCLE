const PLAYLIST_VALIDATION_MESSAGES_ID = 'playlistValidationMessages';
const PLAYLIST_VALIDATION_MESSAGES_CLASS = 'playlist-validation-messages';

function getSelectedRulesId() {
    return document.querySelector('select#id_rules').value;
}

function getSelectedPlaylistIds() {
    const checkboxes = document.querySelectorAll('ul#id_playlists input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(checkbox => checkbox.value);
}

// on document load, no jquery
document.addEventListener('DOMContentLoaded', function() {

    // validate playlist rules on change of playlist checkboxes
    const playlistInputs = document.querySelectorAll('ul#id_playlists input[type="checkbox"]');
    playlistInputs.forEach(playlistInput => {
        playlistInput.addEventListener('change', (e) => {
            const rulesId = getSelectedRulesId();
            const selectedPlaylistIds = getSelectedPlaylistIds();
            validateExperimentPlaylistRules(rulesId, selectedPlaylistIds);
        });
    });

    // validate playlist rules on change of rules select
    const rulesSelect = document.querySelector('select#id_rules');
    rulesSelect.addEventListener('change', (e) => {
        const rulesId = getSelectedRulesId();
        const selectedPlaylistIds = getSelectedPlaylistIds();
        validateExperimentPlaylistRules(rulesId, selectedPlaylistIds);
    });

    const rulesId = getSelectedRulesId();
    const selectedPlaylistIds = getSelectedPlaylistIds();

    // create a new empty div element to hold validation messages
    const validationMessages = document.createElement('div');

    validationMessages.id = PLAYLIST_VALIDATION_MESSAGES_ID;
    validationMessages.className = PLAYLIST_VALIDATION_MESSAGES_CLASS;

    const playlistsFormRow = document.querySelector('ul#id_playlists')
    playlistsFormRow.appendChild(validationMessages);

    // run validation on initialization to warn user straight away of potential issues
    validateExperimentPlaylistRules(rulesId, selectedPlaylistIds);
});

async function validateExperimentPlaylistRules(rulesId, playlists) {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const response = await fetch(`/experiment/validate_playlist/${rulesId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ playlists })
    });

    const data = await response.json();
    const message = data.message || 'No message was given';
    const warnings = data.warnings || [];
    const errors = data.errors || [];

    const validationMessages = document.getElementById(PLAYLIST_VALIDATION_MESSAGES_ID);
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
        errors.forEach(playlistErrors => {
            const playlistErrorsList = document.createElement('ul');
            
            const heading = document.createElement('h3');
            heading.textContent = playlistErrors.playlist;
            playlistErrorsList.appendChild(heading);
            
            playlistErrors.errors.forEach(error => {
                const li = document.createElement('li');
                li.className = 'alert alert--error mt-2'
                li.textContent = error;
                playlistErrorsList.appendChild(li);
            });

            validationMessages.appendChild(playlistErrorsList);
        });
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