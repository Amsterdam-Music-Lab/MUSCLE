import Question from "@/types/Question";
import Input from "./_Input";

interface NumberProps {
    question: Question;
    value?: number;
    onChange: (value: number) => void;
}

/** Number is a question view that lets you input a number */
const Number = ({ question, value = undefined, onChange }: NumberProps) => {

    if ((!question.minValue && question.maxValue !== 0) || (!question.maxValue && question.maxValue !== 0)) {
        throw new Error('minValue and maxValue are required for the Number component');
    }

    // Input validation
    const validateChange = (currentValue: number) => {

        if (currentValue >= question.minValue && currentValue <= question.maxValue) {
            onChange(currentValue);
        }
    };

    return (
        <Input validateChange={validateChange} type="number" value={value}/>
    );
};

export default Number;
