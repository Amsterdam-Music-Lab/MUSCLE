document.addEventListener('DOMContentLoaded', function() {
    const typeSelector = document.querySelector('select#id_type');
    controlVisibility(typeSelector.value);
    typeSelector.addEventListener('change', (event) => controlVisibility(event.target.value));
})

showFields = (fieldSelectors) => {
    hideFields(['.field-profile_scoring_rule', '.field-min_value', '.field-max_value', '.field-max_length', '.field-choices', '.field-min_values']);
    fieldSelectors.forEach( fieldSelector => {
        document.querySelector(fieldSelector).toggleAttribute('hidden')
    })
}

hideFields = (fieldSelectors) => {
    fieldSelectors.forEach( fieldSelector => {
        document.querySelector(fieldSelector).setAttribute('hidden', true)
    })
}

controlVisibility = (selected) => {
    switch(selected) {
        case "AutoCompleteQuestion":
        case "ButtonArrayQuestion":
        case "DropdownQuestion":
        case "IconRangeQuestion":
        case "RadiosQuestion":
        case "TextRangeQuestion":
            showFields([".field-choices", ".field-profile_scoring_rule"]);  
            break;
        case "CheckboxQuestion":
            showFields([".field-choices", ".field-profile_scoring_rule", ".field-min_values"]);  
            break;
        case "NumberQuestion":
        case "RangeQuestion":
            showFields([".field-min_value", ".field-max_value"]);  
            break;
        case "TextQuestion":
            showFields([".field-max_length"]);
            break;
        default:
            showFields([]);
    }
}