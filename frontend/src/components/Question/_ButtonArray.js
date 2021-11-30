import React from "react";

import Button from "../Button/Button";

// ButtonArray is a question view for selecting a single option from a list of buttons
const ButtonArray = ({ question, value, active, onChange }) => {
    
    return (
        <div className="aha__buttons buttons btn-group btn-group-toggle d-flex flex-wrap justify-content-around p-3 w-100" data-toggle="buttons">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className="title">{question.question}</h3>
            {Object.keys(question.choices).map((val, index) => (
                <label class="btn btn-secondary">
                    <input className={val} type="radio" name={question.key} id={index}/>
                    {question.choices[val]}
                </label>))}
                {/* <Button
                    key={index}
                    name={question.key}
                    title={question.choices[val]}
                    value={val}
                    padding="px-3"
                    onClick={onChange}
                    active={active}
                />
            )
            )} */}
        </div>
    )
}

export default ButtonArray;