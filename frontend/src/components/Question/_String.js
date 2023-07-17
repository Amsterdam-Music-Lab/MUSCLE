import React, { useRef, useEffect } from "react";

// String is a question view that lets you input text
const String = ({ question, value = "", onChange }) => {
    const input = useRef(null);

    // Input validation
    const handleChange = () => {
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

    // Key validation
    const handleKey = (e) => {
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
                onKeyPress={(e) => { handleKey(e) }}                
            />
        </div>
    );
};

export default String;
