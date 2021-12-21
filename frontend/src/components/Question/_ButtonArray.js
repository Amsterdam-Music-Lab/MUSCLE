import React from "react";

import Button from "../Button/Button";

// ButtonArray is a question view for selecting a single option from a list of buttons
const ButtonArray = ({ question, value, active, onChange }) => {
    // const changeSelection = (value) => {
    //     console.log(value);
    // }
    
    return (
        <div className="aha__buttons buttons d-flex flex-wrap justify-content-left p-3 w-100">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className="title">{question.question}</h3>
            <div className="btn-group btn-group-toggle" role="group" data-toggle="buttons" aria-label="Button Array">
                {Object.keys(question.choices).map((val, index) => (
                    <ToggleButton
                        label={question.choices[val]}
                        value={val}
                        index={index}
                        name={question.key}
                        key={question.key+index}
                        onChange={onChange}
                    />
                ))}
            </div>
        </div>
    )
}

const ToggleButton = ({ label, value, index, name, onChange }) => {
    return (
        <label 
            className="btn btn-secondary btn-lg"
            onClick={() => {
                onChange(value);
            }}
            tabIndex="0"
            onKeyPress={() => {
                onChange(value);
            }}
        >
            <input className={value} type="radio" name={name} id={index} value={value}/>
            {label}
        </label>)
}

export default ButtonArray;