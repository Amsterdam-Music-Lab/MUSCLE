import React, { useRef, useEffect } from "react";

// String is a question view that lets you input text
const String = ({ question, value = "", onChange }) => {
    const input = useRef(null);

    const handleChange = () => {
        onChange(input.current.value);
    };

    useEffect(() => {
        if (input.current) {
            input.current.focus();
        }
    }, []);

    return (
        <div className="aha__string">
            <input
                type="text"
                value={value}
                ref={input}
                maxLength={question.max_length}
                onChange={handleChange}
                onKeyPress={(e) => { e.key === 'Enter' && e.preventDefault(); }}
            />
        </div>
    );
};

export default String;
