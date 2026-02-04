import Question from "@/types/Question";
import RangeSlider from "./_RangeSlider";

interface RangeProps {
    question: Question;
    value: number;
    onChange: (value: number) => void;
}

/** Range is a question view that makes you select a value within the given range, using a slider */
const Range = ({ question, value, onChange }: RangeProps) => {
    if (question.minValue == null || question.maxValue == null || question.maxValue <= question.minValue) {
        throw new Error('valid minValue and maxValue are required for the Range component');
    }

    const onSliderChange = (value: number) => onChange(value + question.minValue!);

    const keys = Array.from(new Array(question.maxValue), (_, i) => i + question.minValue!);
    const labels = keys.map( value => value.toString());

    return (
        <div className="aha__range">
            <RangeSlider 
                keys={keys}
                labels={labels}
                value={value}
                onSliderChange={onSliderChange}
            />
            
        </div>
    );
};

export default Range;
