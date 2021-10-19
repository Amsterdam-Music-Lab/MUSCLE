import React from "react";

import Button from "../Button/Button";

// ButtonArray is a question view for selecting a single option from a list of buttons
const ButtonArray = ({ question, value, active, onChange }) => {
    
    return (
        <div className="aha__buttons buttons d-flex flex-wrap justify-content-around p-3 w-100">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className="title">{question.question}</h3>
            {Object.keys(question.choices).map((val, index) => (
                <Button
                    key={index}
                    name={question.key}
                    title={question.choices[val]}
                    value={val}
                    padding="px-3"
                    onClick={onChange}
                    active={active}
                />
            )
            )}
        </div>
    )
}

export default ButtonArray;