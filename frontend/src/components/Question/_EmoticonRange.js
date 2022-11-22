import React from "react";
import Slider from "react-rangeslider";

import classNames from "classnames";

const EmoticonRange = ({ question, value, onChange, emphasizeTitle = false }) => {
    return (
        <div className={classNames("aha__text-range", { empty: emptyValue })}>
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}

            <RangeLimits
                minVal={choices[0]}
                maxVal={choices[choices.length-1]}
                labels={question.config.icons? choices : undefined}
            />

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={false}
            />
        </div>
    );
}