import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";

import RangeLimits from "./_RangeLimits";
import RangeTitle from "./_RangeTitle";

/**
 * TextRange is a question view that makes you select a value within the given range, using a slider from a list of choices
 * Values are multiplied by 10 to be displayed as a slider.
 * This to ensure that the slider is centered initially, even if we don't have a center value
 *  */
const TextRange = ({ question, value, onChange, emphasizeTitle }) => {
    const emptyValue = !value;

    const keys = Object.keys(question.choices);
    const choices = Object.values(question.choices);

    const onSliderChange = (index) => onChange(keys[Math.round(index / 10)]);

    let sliderValue = 0;
    if (emptyValue) {
        sliderValue = Math.round(keys.length * 5) - 5;
    } else {
        sliderValue = keys.indexOf(value) * 10;
    }

    return (
        <div className={classNames("aha__text-range", { empty: emptyValue })}>

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
                max={(choices.length * 10) - 10}
                tooltip={false}
            />

            <RangeLimits
                minVal={choices[0]}
                maxVal={choices[choices.length - 1]}
            />
        </div>
    );
};

export default TextRange;
