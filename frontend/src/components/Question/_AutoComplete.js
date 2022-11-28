import React from "react";
import Select from "react-select";

// AutoComplete is a question view for selecting a single option from a dropdown list with autocompletion
const AutoComplete = ({
    question,
    value,
    onChange,
}) => {
    const options = Object.keys(question.choices).map((val, index) => ({
        value: val,
        label: question.choices[val],
    }));

    return (
        <div className="aha__autocomplete">
            <div className="control">
                <Select
                    options={options}
                    tabIndex="0"
                    name={question.key}
                    value={options.find(option => option.value === value)}
                    onChange={(choice) => {
                        onChange(choice.value);
                    }}
                />
            </div>
        </div>
    );
};

export default AutoComplete;
