import React from "react";
import classNames from "classnames";
import Select from "react-select";

// AutoComplete is a question view for selecting a single option from a dropdown list with autocompletion
const AutoComplete = ({
    question,
    value,
    onChange,
    emphasizeTitle = false,
}) => {
    const options = Object.keys(question.choices).map((val, index) => ({
        value: val,
        label: question.choices[val],
    })).sort((a,b)=>(a.label.localeCompare(b.label)));

    return (
        <div className="aha__autocomplete">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className={classNames({ title: emphasizeTitle })}>
                {question.question}
            </h3>
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
