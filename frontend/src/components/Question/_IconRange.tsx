import Slider from "react-rangeslider";
import classNames from "classnames";
import RangeTitle from "./_RangeTitle";
import Question from "@/types/Question";

interface IconRangeProps {
    question: Question;
    value: string;
    onChange: () => void;
}

const IconRange = ({ question, value, onChange}: IconRangeProps) => {
    const emptyValue = !value;

    if (!question.choices || Object.keys(question.choices).length <= 0) {
        throw new Error("IconRange question must have choices");
    }

    const keys = Object.keys(question.choices);
    const choices = Object.values(question.choices);

    const onSliderChange = (index: number) => {
        onChange(keys[index]);
    };

    let sliderValue = 0;
    if (emptyValue) {
        sliderValue = Math.round(keys.length / 2) - 1;
    } else {
        sliderValue = keys.indexOf(value);
    }

    return (
        <div className={classNames("aha__text-range", question.style, { empty: emptyValue })}>
            <RangeTitle
                // this prop does not exist on RangeTitle
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
