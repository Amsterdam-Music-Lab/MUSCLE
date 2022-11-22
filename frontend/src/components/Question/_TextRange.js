import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";

import RangeLimits from "./_RangeLimits";
import RangeTitle from "./_RangeTitle";

// TextRange is a question view that makes you select a value within the given range, using a slider from a list of choices
const TextRange = ({ question, value, onChange, emphasizeTitle = false }) => {
    const emptyValue = !value;

    const keys = Object.keys(question.choices);
    const choices = Object.values(question.choices);

    const onSliderChange = (index) => {
        onChange(keys[index]);
    };

    let sliderValue = 0;
    if (emptyValue) {
        sliderValue = Math.round(keys.length / 2) - 1;
    } else {
        sliderValue = keys.indexOf(value);
    }

    return (
        <div className={classNames("aha__text-range", { empty: emptyValue })}>
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}

            <RangeTitle
                emphasizeTitle={emphasizeTitle}
                question={question}
                value={value}
                sliderValue={sliderValue}
                emptyValue={emptyValue}
            />

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={false}
            />

            <RangeLimits
                minVal={choices[0]}
                maxVal={choices[choices.length-1]}
                labels={question.config.icons? choices : undefined}
            />
        </div>
    );
};

export default TextRange;
