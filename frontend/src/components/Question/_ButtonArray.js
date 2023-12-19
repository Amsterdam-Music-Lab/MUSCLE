import React from "react";

import classNames from "classnames";
import { renderLabel } from "../../util/label";

// ButtonArray is a question view for selecting a single option from a list of buttons
const ButtonArray = ({ question, disabled, onChange }) => {

    const buttonPress = (value) => {
        if (disabled) {
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
                        key={question.key + index}
                        onChange={buttonPress}
                        disabled={disabled}
                    />
                ))}
            </div>
        </div>
    )
}

const ToggleButton = ({ label, value, index, name, disabled, onChange }) => {
    const disabledClasses = disabled ? 'disabled' : '';
    return (
        <label
            className={classNames("btn btn-secondary btn-lg", disabledClasses)}
            tabIndex="0"
        >
            <input className={value}
                type="radio"
                name={name}
                id={index}
                value={value}
                disabled={disabled}
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
