import { useState } from "react";
import classNames from "classnames";
import { css } from '@emotion/react'

import RangeLimits from "./_RangeLimits";
import RangeTitle from "./_RangeTitle";
import useBoundStore from "@/util/stores";
import { Choice } from "@/types/Question";

interface RangeProps {
    choices: Choice[];
    value: string | number;
    onChange: (value: string) => void;
    changePosition?: boolean;
}

const RangeSlider = ({ choices, value, onChange, changePosition=false }: RangeProps) => {

    const theme = useBoundStore((state) => state.theme);
    const [thumbColor, setThumbColor] = useState(theme["colorPrimary"]);
    const sliderBackground = theme["colorText"];

    const keys = choices.map(choice => choice.value);
    const labels = choices.map(choice => choice.label);

    const emptyValue = value === "";
    const sliderValue = emptyValue ? Math.round((keys.length - 1) / 2) : keys.indexOf(value);

    const onSliderChange = (event) => {
        const nextIndex = Number(event.target.value);
        const nextValue = keys[nextIndex];

        setThumbColor(theme["colorSecondary"]);

        if (nextValue !== undefined) {
            onChange(nextValue);
        }
    };
    
    const sliderStyle = () => {
        return css`
            .aha__slider {
                background-color: ${sliderBackground};
            }

            input[type=range]::-webkit-slider-thumb {
                background-color: ${thumbColor};
            }
            
            /* All the same stuff for Firefox */
            input[type=range]::-moz-range-thumb {
                background-color: ${thumbColor};
            }
        `
    }

    return (
        <div className="aha__range_slider" css={sliderStyle()}>

            <RangeTitle
                choices={choices}
                sliderValue={sliderValue}
                emptyValue={emptyValue}
                changePosition={changePosition}
            />
            <div className={classNames({ empty: emptyValue })} data-testid="range-slider">
                <input className="aha__slider" type="range"
                    onChange={onSliderChange}
                    min={0}
                    max={labels.length - 1}
                    value={sliderValue}
                />
            </div>

            <RangeLimits
                minVal={labels[0]}
                maxVal={labels[labels.length - 1]}
            />
        </div>
    );
}

export default RangeSlider;