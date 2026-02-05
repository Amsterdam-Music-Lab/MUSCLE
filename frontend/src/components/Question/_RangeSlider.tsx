import Slider from "react-rangeslider";
import classNames from "classnames";
import { css } from '@emotion/react'

import RangeLimits from "./_RangeLimits";
import RangeTitle from "./_RangeTitle";
import useBoundStore from "@/util/stores";

interface RangeProps {
    keys: string[] | number[];
    labels: string[];
    value: string | number;
    onSliderChange: (sliderIndex: number) => void
    changePosition?: boolean
}

const RangeSlider = ({ keys, labels, value, onSliderChange, changePosition=false }: RangeProps) => {
    const emptyValue = value === "";
    let sliderValue = !emptyValue ? keys.indexOf(value) : Math.round((keys.length - 1)/2);

    const theme = useBoundStore((state) => state.theme);
    const sliderEmptyColor = theme["colorPrimary"];
    const sliderActiveColor = theme["colorSecondary"]
    
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
                labels={labels}
                sliderValue={sliderValue}
                emptyValue={emptyValue}
                changePosition={changePosition}
            />
            <div className={classNames({ empty: emptyValue })} data-testid="range-slider" role="slider">
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