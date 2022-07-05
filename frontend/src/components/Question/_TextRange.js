import React from "react";
import Slider from "react-rangeslider";
import classnames from "classnames";

// TextRange is a question view that makes you select a value within the given range, using a slider from a list of choices
const TextRange = ({ question, value, onChange }) => {
    const emptyValue = !value;

    const choices = Object.values(question.choices);

    const onSliderChange = (index) => {
        onChange(choices[index]);
    };


    let sliderValue = 0;
    if (emptyValue) {
        sliderValue = Math.round(choices.length / 2) - 1;
    } else {
        sliderValue = choices.indexOf(value);
    }

    return (
        <div className={classnames("aha__text-range", { empty: emptyValue })}>
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}

            <h3 className="title">{question.question}</h3>

            <h4 className="current-value">{emptyValue ? "↔" : value}</h4>

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={false}
            />

            <div className="limits">
                <span className="min">{choices[0]}</span>
                <span className="max">
                    {choices[choices.length - 1]}
                </span>
            </div>
        </div>
    );
};

export default TextRange;
