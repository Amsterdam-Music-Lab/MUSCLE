import classNames from "classnames";
import { css } from '@emotion/react'

import Question from "@/types/Question";
import RangeSlider from "./_RangeSlider";

interface RangeProps {
    question: Question;
    value: number;
    onChange: (value: string) => void;
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
    
    if (question.minValue == null || question.maxValue == null || question.maxValue <= question.minValue) {
        throw new Error('valid minValue and maxValue are required for the Range component');
    }

    const keys = Array.from(new Array(question.maxValue + 1 - (question.minValue || 0)), (_, i) => i + (question.minValue || 0));
    const choices = keys.map( value => {
        return {
            value: value,
            label: value.toString()
        }
    });

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
