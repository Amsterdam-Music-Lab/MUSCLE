import { useRef, useEffect } from "react";

interface InputProps {
    type: 'number' | 'text';
    value: string | number | undefined;
    validateChange: (value: string | number) => void;
}

/** Number is a question view that lets you input a number */
const Input = ({ type, value, validateChange }: InputProps) => {
    const input = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (input.current) {
            input.current.focus();
        }
    }, []);

    // Input validation
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {

        if (!input.current) {
            return;
        }

        validateChange(input.current.value);
    };

    /** Key validation */
    const handleKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    }

    return (
        <div className="aha__input">
            <input
                type={type}
                value={value}
                ref={input}
                onChange={handleChange}
                onKeyDown={(e) => handleKey(e)}
            />
        </div>
    );

}

export default Input;