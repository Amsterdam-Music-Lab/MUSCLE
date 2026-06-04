import Question from "@/types/Question";
import RangeSlider from "./_RangeSlider";

interface RangeProps {
    question: Question;
    value: number;
    onChange: (value: string) => void;
}

/** Range is a question view that makes you select a value within the given range, using a slider */
const Range = ({ question, value, onChange }: RangeProps) => {
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
        <div className="aha__range">
            <RangeSlider 
                choices={choices}
                value={value}
                onChange={onChange}
            />
        </div>
    );
};

export default Range;
