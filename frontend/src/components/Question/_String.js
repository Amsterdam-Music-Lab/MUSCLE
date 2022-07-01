import React, { useRef, useEffect } from "react";
import classNames from 'classnames';

// String is a question view that lets you input text
const String = ({ question, value = "", onChange, emphasizeTitle = true }) => {
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
            <h3 className={classNames({title: emphasizeTitle})}>{question.question}</h3>
            <input
                type="text"
                value={value}
                ref={input}
                maxLength={question.max_length}
                onChange={handleChange}
                onKeyPress={handleChange}
            />
        </div>
    );
};

export default String;
