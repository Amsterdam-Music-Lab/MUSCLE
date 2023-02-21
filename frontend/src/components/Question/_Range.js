import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";

// Range is a question view that makes you select a value within the given range, using a slider
const Range = ({ question, value, onChange}) => {
    const emptyValue = !value;

    if (emptyValue) {
        value = (question.min_value + question.max_value) / 2;
    }
    return (
        <div className={classNames("aha__range", { empty: emptyValue })}>
            <h1 className="current-value">{emptyValue ? "↔" : value}</h1>

            <Slider
                value={value}
                onChange={onChange}
                min={question.min_value}
                max={question.max_value}
                tooltip={false}
            />

            <div className="limits">
                <span className="min">{question.min_value}</span>
                <span className="max">{question.max_value}</span>
            </div>
        </div>
    );
};

export default Range;
