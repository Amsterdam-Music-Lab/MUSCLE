import RangeSlider from "./_RangeSlider";
import Question from "@/types/Question";

interface TextRangeProps {
    question: Question;
    value: string;
    onChange: (value: string) => void;
}

/**
 * TextRange is a question view that makes you select a value within the given range, using a slider from a list of choices
 * Values are multiplied by 10 to be displayed as a slider.
 * This to ensure that the slider is centered initially, even if we don't have a center value
 *  */
const TextRange = ({ question, value, onChange }: TextRangeProps) => {
    const choices = question.choices;

    if (!choices || choices.length === 0) {
        throw new Error("TextRange question must have choices");
    }

    const keys = choices.map(choice => choice.value);
    const labels = choices.map(choice => choice.label);

    const onSliderChange = (index: number) => onChange(keys[index]);

    return (
        <div className="aha__text_range">
            <RangeSlider 
                keys={keys}
                labels={labels}
                value={value}
                onSliderChange={onSliderChange}
            />
        </div>
    )
};

export default TextRange;
