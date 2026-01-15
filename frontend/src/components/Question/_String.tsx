import Question from "@/types/Question";
import Input from "./_Input";

interface StringProps {
    question: Question;
    value?: string;
    onChange: (value: string) => void;
}

/** String is a question view that lets you input text */
const String = ({ question, value = "", onChange }: StringProps) => {
    
    if (!question.maxLength && question.maxLength !== 0) {
<<<<<<< HEAD
        throw new Error('maxLength is required for the String component');
=======
        throw new Error('maxLength is required for the String component with input type is "text"');
>>>>>>> a27a92b23d3b8de2e6a60b899614c6233d1a187c
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
