import classNames from "classnames";
import RangeSlider from "./_RangeSlider";
import Question from "@/types/Question";

interface IconRangeProps {
    question: Question;
    value: any;
    onChange: any;
}

const IconRange = ({ question, value, onChange}: IconRangeProps) => {
    const choices = question.choices;

    if (!choices || choices.length <= 0) {
        throw new Error("IconRange question must have choices");
    }

    const keys = choices.map(choice => choice.value);
    const labels = choices.map(choice => choice.label);

    const onSliderChange = (index: number) => {
        onChange(keys[index]);
    };

    return (
        <div className={classNames("aha__icon-range", question.style)}>
            <RangeSlider 
                keys={keys}
                labels={labels}
                value={value}
                onSliderChange={onSliderChange}
                changePosition={true}
            />
        </div>
    )
}

export default IconRange;
