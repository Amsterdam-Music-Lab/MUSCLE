import Question from "@/types/Question";
import Input from "./_Input";

interface StringProps {
    question: Question;
    value?: string;
    onChange: (value: string) => void;
}

/** String is a question view that lets you input text */
const String = ({ question, value = "", onChange }: StringProps) => {
    
    if (!question.max_length && question.max_length !== 0) {
        throw new Error('max_length is required for the String component with input type is "text"');
    }

    // Input validation
    const validateChange = (currentValue: string) => {

        if (currentValue.length < question.max_length) {
            onChange(currentValue);
        }
    };

    return (
        <Input validateChange={validateChange} type="text" value={value}/>
    );
};

export default String;
