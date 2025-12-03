import Question from "@/types/Question";
import Input from "./_Input";

interface NumberProps {
    question: Question;
    value?: number;
    onChange: (value: number) => void;
}

/** Number is a question view that lets you input a number */
const Number = ({ question, value = undefined, onChange }: NumberProps) => {

    if ((!question.min_value && question.min_value !== 0) || (!question.max_value && question.max_value !== 0)) {
        throw new Error('min_value and max_value are required for the Number component');
    }

    // Input validation
    const validateChange = (currentValue: number) => {

        if (currentValue >= question.min_value && currentValue <= question.max_value) {
            onChange(currentValue);
        }
    };

    return (
        <Input validateChange={validateChange} type="number" value={value}/>
    );
};

export default Number;
