import Slider from "react-rangeslider";
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
    const sliderEmptyColor = theme["colorPrimary"];
    const sliderActiveColor = theme["colorSecondary"]

    const keys = choices.map(choice => choice.value);
    const labels = choices.map(choice => choice.label);

    const emptyValue = value === "";
    let sliderValue = !emptyValue ? keys.indexOf(value) : Math.round((keys.length - 1)/2);

    const onSliderChange = (index: number) => {
        onChange(keys[index]);
    };
    
    const sliderStyle = () => {
        return css`
            .rangeslider__handle {
                background: ${sliderActiveColor}
            }
            
            .empty div.rangeslider__handle {
                background: ${sliderEmptyColor}
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
            <Slider
                value={sliderValue}
                onChange={onSliderChange}
                min={0}
                max={keys.length-1}
                tooltip={false}
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