const formSelector = "#experimentseriesgroup_set-group fieldset";
const formSetSelector = ".dynamic-experimentseriesgroup_set";
const orderFieldSelector = ".field-order input";

document.addEventListener("DOMContentLoaded", function () {
    autoOrderInlineGroups();
    observeFormChanges();
});

let experimentGroups = [];

async function autoOrderInlineGroups(event) {

    let changedGroup;

    if (event) {
        changedGroup = event.target.parentElement.parentElement.parentElement.parentElement;
    }

    // Wait for the dynamic elements to be fully loaded
    await waitForElements(`${formSelector} ${formSetSelector}`);

    // Select the experiment groups
    const oldExperimentGroups = experimentGroups.map(group => group.id);
    experimentGroups = document.querySelectorAll(`${formSelector} ${formSetSelector}`);

    // Sort the groups according to their order number
    experimentGroups = Array.from(experimentGroups).sort((a, b) => {
        let orderA = parseInt(a.querySelector(orderFieldSelector).value, 10);
        let orderB = parseInt(b.querySelector(orderFieldSelector).value, 10);

        if (changedGroup) {
            const groupId = changedGroup.id;
            const isGroupA = a.id === groupId;
            const isGroupB = b.id === groupId;
            const oldExperimentGroupIndex = oldExperimentGroups.indexOf(groupId)
            const oldValue = oldExperimentGroupIndex >= 0 ? oldExperimentGroupIndex + 1 : 0;
            let newValue = parseInt(changedGroup.querySelector(orderFieldSelector).value, 10);

            const newValueIsHigher = newValue > oldValue;
            newValue = newValueIsHigher ? newValue + .5 : newValue - .5;

            if (isGroupA) {
                orderA = newValue;
            }

            if (isGroupB) {
                orderB = newValue;
            }
        }

        return orderA - orderB;
    });

    // Temporarily disconnect the observer to avoid reacting to our DOM manipulations
    observer.disconnect();

    // Reorder the groups in the form
    let parent = document.querySelector(formSelector);

    // Event, set opacity of target element to 0
    if (event) {
        changedGroup.style.opacity = 0;

        // Wait for the animation to finish (300ms)
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    experimentGroups.forEach(group => {
        // Append moves the element, effectively reordering them
        parent.appendChild(group);

        // Attach change listener to order input
        attachOrderChangeListener(group);
    });

    if (event) {
        // Event, set opacity of target element to 1
        changedGroup.style.opacity = 1;

        // scroll to the changed group with a smooth animation
        changedGroup.scrollIntoView({ behavior: 'smooth' });
    }

    experimentGroups.forEach(group => {
        const indexOfGroup = experimentGroups.indexOf(group);

        // Set order values to match the new order
        group.querySelector(orderFieldSelector).value = indexOfGroup + 1;
    });

    // Reconnect the observer after the DOM manipulation
    observeFormChanges();
}

function attachOrderChangeListener(group) {
    const orderInput = group.querySelector(orderFieldSelector);

    // Use a flag to check if the listener has been attached
    if (!orderInput.hasEventListenerAttached) {
        orderInput.addEventListener('change', (event) => {
            if (hasOrderChanged()) {
                autoOrderInlineGroups(event);
            }
        });
        orderInput.hasEventListenerAttached = true;
    }
}

let observer; // Define observer globally to use across functions
function observeFormChanges() {
    observer = new MutationObserver(mutations => {
        autoOrderInlineGroups();
    });

    const config = { childList: true };
    const parent = document.querySelector(formSelector);
    observer.observe(parent, config);
}

async function waitForElements(selector) {
    while (document.querySelectorAll(selector).length === 0) {
        await new Promise(resolve => requestAnimationFrame(resolve));
    }
}

let lastOrderValues = [];
function hasOrderChanged() {
    const currentOrderValues = Array.from(document.querySelectorAll(`${formSelector} ${formSetSelector} ${orderFieldSelector}`)).map(input => input.value);
    const hasChanged = JSON.stringify(currentOrderValues) !== JSON.stringify(lastOrderValues);
    lastOrderValues = currentOrderValues;
    return hasChanged;
}
