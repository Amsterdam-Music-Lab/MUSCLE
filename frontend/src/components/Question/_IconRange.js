import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";

import RangeLimits from "./_RangeLimits";
import RangeTitle from "./_RangeTitle";
import { renderLabel } from "../../util/label";

const IconRange = ({ question, value, onChange, emphasizeTitle }) => {
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
            <RangeTitle
                emphasizeTitle={emphasizeTitle}
                question={question}
                value={value}
                sliderValue={sliderValue}
                emptyValue={emptyValue}
                changePosition={true}
            />

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={false}
            />
        </div>
    )
}

export default IconRange;
