document.addEventListener('DOMContentLoaded', function() {

    const colorGroups = document.querySelectorAll('.color-picker-group');

    colorGroups.forEach(group => {
        const colorSelect = group.querySelector('.color-select');
        const colorPicker = group.querySelector('.color-picker');
        const colorText = group.querySelector('.color-text');
        const colorCircle = group.querySelector('.color-circle');
        const resetButton = group.querySelector('.color-reset');

        // Function to update the color circle and apply border styles
        function updateColorDisplay(selectedColor, origin) {
            colorCircle.style.backgroundColor = selectedColor;

            // Clear all borders
            colorSelect.style.border = '';
            colorPicker.style.border = '';
            colorText.style.border = '';

            // Apply green border to the origin input
            if (origin === 'select') {
                colorSelect.style.border = '2px solid green';
            } else if (origin === 'picker') {
                colorPicker.style.border = '2px solid green';
            } else if (origin === 'text') {
                colorText.style.border = '2px solid green';
            }
        }

        // Event listener for color select
        colorSelect.addEventListener('change', function() {
            const selectedValue = colorSelect.value;
            colorText.value = selectedValue;
            updateColorDisplay(selectedValue, 'select');
        });

        // Event listener for color picker
        colorPicker.addEventListener('input', function() {
            const selectedValue = colorPicker.value;
            colorText.value = selectedValue;
            updateColorDisplay(selectedValue, 'picker');
        });

        // Event listener for text input
        colorText.addEventListener('input', function() {
            const selectedValue = colorText.value;
            updateColorDisplay(selectedValue, 'text');
        });

        // Event listener for reset button
        resetButton.addEventListener('click', function() {
            colorSelect.value = '';
            colorPicker.value = '';
            colorText.value = '';
            colorCircle.style.backgroundColor = 'transparent';
            colorSelect.style.border = '';
            colorPicker.style.border = '';
            colorText.style.border = '';
        });

        function initialize() {
            const selectedValue = colorText.value;

            // if looks like a hex value, update the color picker and text input
            if (selectedValue.match(/^#[0-9A-F]{6}$/i)) {
                updateColorDisplay(selectedValue, 'picker');
            } else {

                updateColorDisplay(selectedValue, 'select');
            }
        }

        initialize();
    });

    function updateAndInjectCSSVariables() {
        // look for all inputs with the class color-picker-widget
        const colorPickerWidgets = document.querySelectorAll('.color-picker-widget');

        const cssVariables = [];

        // loop through each input
        colorPickerWidgets.forEach(widget => {
            // get the name and value of each input
            const name = widget.name;
            const value = widget.value;

            // if the value is not empty, add it to the cssVariables array
            if (value !== '') {
                const escapedValue = value.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                cssVariables.push(`--${name}: ${escapedValue};`);
            }
        });

        // inject the cssVariables into the document
        const cssVariablesString = cssVariables.join(' ');
        const style = document.createElement('style');
        style.innerHTML = `:root { ${cssVariablesString} }`;
        document.head.appendChild(style);
    }

    updateAndInjectCSSVariables();
});
