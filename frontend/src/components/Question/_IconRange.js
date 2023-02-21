import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";

const IconRange = ({ question, value, onChange }) => {

    return (
        <div className={classNames("aha__text-range", { empty: emptyValue })}>
            <h4 className="current-value"> <span style={{color: question.config.colors[sliderValue]}}> {renderLabel(question.choices[value], "2x")}</span></h4>

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={true}
            />
        </div>
    )
}

export default IconRange;
