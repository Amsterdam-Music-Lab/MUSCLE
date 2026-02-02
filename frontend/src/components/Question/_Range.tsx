import classNames from "classnames";
import { css } from '@emotion/react'

import Question from "@/types/Question";
import useBoundStore from "@/util/stores";

interface RangeProps {
    question: Question;
    value: number;
    onChange: (value: number) => void;
}

/** Range is a question view that makes you select a value within the given range, using a slider */
const Range = ({ question, value, onChange }: RangeProps) => {
    const emptyValue = !value;
    const theme = useBoundStore((state) => state.theme);
    const sliderEmptyColor = theme["colorPrimary"];
    const sliderActiveColor = theme["colorSecondary"];
    const sliderBackground = theme["colorGrey"];
    
    const sliderStyle = () => {
        return css`
            input.aha__slider {
                background: ${sliderBackground}
            }

            input.aha__slider::-webkit-slider-thumb {
                background: ${sliderEmptyColor}
            }
        `
    }


    if ((!question.minValue && question.minValue !== 0) || (!question.maxValue && question.maxValue !== 0)) {
        throw new Error('minValue and maxValue are required for the Range component');
    }

    if (emptyValue) {
        value = (question.minValue + question.maxValue) / 2;
    }
    return (
        <div className={classNames("aha__range", { empty: emptyValue })} css={sliderStyle()}>
            <h1 className="current-value">{emptyValue ? "↔" : value}</h1>
            <input className="aha__slider" type="range"
                // value={value}
                // onChange={onChange}
                min={question.minValue}
                max={question.maxValue}
            />
            <div className="limits">
                <span className="min">{question.minValue}</span>
                <span className="max">{question.maxValue}</span>
            </div>
        </div>
    );
};

export default Range;
