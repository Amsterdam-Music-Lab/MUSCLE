import React from "react";

import classNames from "classnames";
import { renderLabel } from "../../util/label";

// ButtonArray is a question view for selecting a single option from a list of buttons
const ButtonArray = ({ question, active, onChange }) => {

    const buttonPress = (value) => {
        if (!active) {
            return;
        }
        else {
            onChange(value)
        }
    }


    return (
        <div className="aha__buttons buttons d-flex flex-wrap justify-content-center p-3 w-100">
            
            <div className={classNames("btn-group-toggle-custom", question.style)} role="group" data-toggle="buttons" aria-label="Button Array">
                {Object.keys(question.choices).map((val, index) => (
                    <ToggleButton
                        label={question.choices[val]}
                        value={val}
                        index={index}
                        name={question.key}
                        key={question.key+index}
                        onChange={buttonPress}
                        active={active}
                    />
                ))}
            </div>
        </div>
    )
}

const ToggleButton = ({ label, value, index, name, active, onChange }) => {
    const disabled = active? '' : 'disabled';
    return (
        <label
            className={classNames("btn btn-secondary btn-lg", disabled)}            
            tabIndex="0"            
        >
            <input className={value}
                type="radio"
                name={name}
                id={index}
                value={value}
                onClick={() => {                    
                    onChange(value);
                }}
                onKeyPress={() => {                    
                    onChange(value);
                }}            
            />
            {renderLabel(label)}
        </label>)
}

export default ButtonArray;
