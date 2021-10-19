import React from "react";
import classnames from "classnames";

// Checkboxes is a question view for selecting multiple options from a list
const Checkboxes = ({ question, value, onChange }) => {
    const values = value ? value.split(",") : [];

    // Add/remove value
    const onToggle = (value) => {
        const index = values.indexOf(value);
        if (index === -1) {
            values.push(value);
        } else {
            values.splice(index, 1);
        }
        onChange(values.join(","));
    };

    return (
        <div className="aha__checkboxes">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className="title">{question.question}</h3>
            {Object.keys(question.choices).map((val, index) => (
                <Checkbox
                    key={index}
                    name={question.key}
                    label={question.choices[val]}
                    value={val}
                    checked={values.includes(val)}
                    onChange={onToggle}
                />
            ))}
        </div>
    );
};

const Checkbox = ({ label, value, checked, onChange }) => {
    return (
        <div
            className={classnames("checkbox", { checked })}
            onClick={() => {
                onChange(value);
            }}
            tabIndex="0"
            onKeyPress={() => {
                onChange(value);
            }}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Checkboxes;
