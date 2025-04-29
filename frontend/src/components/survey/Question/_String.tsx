import Question from "@/types/Question";
import { useRef, useEffect } from "react";

interface StringProps {
    question: Question;
    value?: string;
    onChange: (value: string) => void;
}

/** String is a question view that lets you input text */
const String = ({ question, value = "", onChange }: StringProps) => {
    const input = useRef<HTMLInputElement>(null);

    if (question.input_type === 'number' && ((!question.min_value && question.min_value !== 0) || (!question.max_value && question.max_value !== 0))) {
        throw new Error('min_value and max_value are required for the String component with input type is "number"');
    }

    if (question.input_type === 'text' && !question.max_length && question.max_length !== 0) {
        throw new Error('max_length is required for the String component with input type is "text"');
    }

    // Input validation
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {

        if (!input.current) {
            return;
        }

        switch (question.input_type) {
            case 'number':
                if (input.current.value >= question.min_value && input.current.value <= question.max_value) {
                    onChange(input.current.value);
                }
                break;
            case 'text':
                if (question.max_length && input.current.value.length > question.max_length) {
                    break;
                }
                onChange(input.current.value);
                break;
            default:
                onChange(input.current.value);
        }
    };

    /** Key validation */
    const handleKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    }

    useEffect(() => {
        if (input.current) {
            input.current.focus();
        }
    }, []);

    return (
        <div className="aha__string">
            <input
                type={question.input_type}
                value={value}
                ref={input}
                onChange={handleChange}
                onKeyDown={(e) => handleKey(e)}
            />
        </div>
    );
};

export default String;
