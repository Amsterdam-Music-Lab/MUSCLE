import Question from "@/types/Question";
import Input from "./_Input";

interface StringProps {
    question: Question;
    value?: string;
    onChange: (value: string) => void;
}

/** String is a question view that lets you input text */
const String = ({ question, value = "", onChange }: StringProps) => {
    
    if (!question.maxLength) {
        throw new Error('maxLength is required for the String component');
    }

    // Input validation
    const validateChange = (currentValue: string) => {

        if (currentValue.length < question.maxLength) {
            onChange(currentValue);
        }
    };

    return (
        <Input validateChange={validateChange} type="text" value={value}/>
    );
};

export default String;
