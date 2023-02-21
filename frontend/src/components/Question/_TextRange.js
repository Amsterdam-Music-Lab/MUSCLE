import React from "react";
import Slider from "react-rangeslider";
import classNames from "classnames";
import { renderLabel } from "../../util/label";

// TextRange is a question view that makes you select a value within the given range, using a slider from a list of choices
const TextRange = ({ question, value, onChange }) => {
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
            { question.config && question.config.icons ?
                ( emptyValue ?
                    <h4 className="current-value"> {renderLabel("fa-arrows-left-right", "2x")} </h4>
                    :
                    <h4 className="current-value"> <span style={{color: question.config.colors[sliderValue]}}> {renderLabel(question.choices[value], "2x")}</span></h4>
                )
                :
                <h4 className="current-value">{emptyValue ? "↔" : question.choices[value]}</h4>
            }

            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={choices.length - 1}
                tooltip={false}
            />

            <div className="limits">

                { question.config && question.config.icons ?
                    <>
                    <span className="min" style={{color: question.config.colors[0]}}>{renderLabel(choices[0], "2x")}</span>
                    <span className="max" style={{color: question.config.colors[choices.length - 1]}}>
                        {renderLabel(choices[choices.length - 1], "2x")}
                    </span>
                    </>
                    :
                    <>
                    <span className="min">{choices[0]}</span>
                    <span className="max">
                        {choices[choices.length - 1]}
                    </span>
                    </>
                }
            </div>
        </div>
    );
};

export default TextRange;
