import React from "react";

// DropDown is a question view for selecting a single option from a dropdown list
const DropDown = ({ question, value, onChange }) => {
    return (
        <div className="aha__dropdown">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className="title">{question.question}</h3>

            <select
                value={value}
                onChange={(e) => {
                    onChange(e.target.value);
                }}
                tabIndex="0"
            >
                <option value=""></option>
                {Object.keys(question.choices).map((val, index) => (
                    <option value={val} key={index}>
                        {question.choices[val]}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default DropDown;
