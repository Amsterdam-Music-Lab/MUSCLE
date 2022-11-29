import React from "react";
import Select from "react-select";

// When using Safari iOS the browser may scroll the page when using the react-select Select.
// Therefore we scroll back to top when the select is blurred
const scrollToTop = () => {
    window.scrollTo(0, 0);
};

// AutoComplete is a question view for selecting a single option from a dropdown list with autocompletion
const AutoComplete = ({ question, value, onChange, emphasizeTitle = false }) => {
    const options = Object.keys(question.choices)
        .map((val, index) => ({
            value: val,
            label: question.choices[val],
        }))
        .sort((a, b) => a.label.localeCompare(b.label));

    return (
        <div className="aha__autocomplete">
            <div className="control">
                <Select
                    options={options}
                    tabIndex="0"
                    name={question.key}
                    value={options.find((option) => option.value === value)}
                    onChange={(choice) => {
                        onChange(choice.value);
                    }}
                    onBlur={scrollToTop}
                />
            </div>
        </div>
    );
};

export default AutoComplete;
