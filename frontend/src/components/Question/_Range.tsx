import Slider from "react-rangeslider";
import classNames from "classnames";
import Question from "@/types/Question";

interface RangeProps {
    question: Question;
    value: number;
    onChange: (value: number) => void;
}

/** Range is a question view that makes you select a value within the given range, using a slider */
const Range = ({ question, value, onChange }: RangeProps) => {
    const emptyValue = !value;

    if ((!question.minValue && question.minValue !== 0) || (!question.maxValue && question.maxValue !== 0)) {
        throw new Error('minValue and maxValue are required for the Range component');
    }

    if (emptyValue) {
        value = (question.minValue + question.maxValue) / 2;
    }
    return (
        <div className={classNames("aha__range", { empty: emptyValue })}>
            <h1 className="current-value">{emptyValue ? "↔" : value}</h1>

            <Slider
                value={value}
                onChange={onChange}
                min={question.minValue}
                max={question.maxValue}
                tooltip={false}
            />

            <div className="limits">
                <span className="min">{question.minValue}</span>
                <span className="max">{question.maxValue}</span>
            </div>
        </div>
    );
};

export default Range;
