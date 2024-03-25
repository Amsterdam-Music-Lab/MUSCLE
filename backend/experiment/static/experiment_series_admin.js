document.addEventListener("DOMContentLoaded", function() {
    autoOrderInlineGroups();
    observeFormChanges();
});

async function autoOrderInlineGroups(event) {
    // Wait for the dynamic elements to be fully loaded
    await waitForElements("#experimentseriesgroup_set-group .dynamic-experimentseriesgroup_set");

    // Select the experiment groups
    let experimentGroups = document.querySelectorAll("#experimentseriesgroup_set-group .dynamic-experimentseriesgroup_set");

    // Sort the groups according to their order number
    experimentGroups = Array.from(experimentGroups).sort((a, b) => {
        let orderA = parseInt(a.querySelector(".field-order input").value, 10);
        let orderB = parseInt(b.querySelector(".field-order input").value, 10);
        return orderA - orderB;
    });

    // Temporarily disconnect the observer to avoid reacting to our DOM manipulations
    observer.disconnect();

    // Reorder the groups in the form
    let parent = document.querySelector("#experimentseriesgroup_set-group fieldset");

    let changedGroup;

    // Event, set opacity of target element to 0
    if (event) {
        changedGroup = event.target.parentElement.parentElement.parentElement.parentElement;
        changedGroup.style.opacity = 0;

        // Wait for the animation to finish (300ms)
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    experimentGroups.forEach(group => {
        parent.appendChild(group); // Append moves the element, effectively reordering them
        attachOrderChangeListener(group); // Attach change listener to order input
    });

    if (event) {
        // Event, set opacity of target element to 1
        changedGroup.style.opacity = 1;
        
        // scroll to the changed group with a smooth animation
        changedGroup.scrollIntoView({ behavior: 'smooth' });
    }

    // Reconnect the observer after the DOM manipulation
    observeFormChanges();
}

function attachOrderChangeListener(group) {
    const orderInput = group.querySelector(".field-order input");

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
    const parent = document.querySelector("#experimentseriesgroup_set-group fieldset");
    observer.observe(parent, config);
}

async function waitForElements(selector) {
    while (document.querySelectorAll(selector).length === 0) {
        await new Promise(resolve => requestAnimationFrame(resolve));
    }
}

let lastOrderValues = [];
function hasOrderChanged() {
    const currentOrderValues = Array.from(document.querySelectorAll("#experimentseriesgroup_set-group .dynamic-experimentseriesgroup_set .field-order input"))
                                    .map(input => input.value);
    const hasChanged = JSON.stringify(currentOrderValues) !== JSON.stringify(lastOrderValues);
    lastOrderValues = currentOrderValues;
    return hasChanged;
}
