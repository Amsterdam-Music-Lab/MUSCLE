import Question from "@/types/Question";
import classNames from "classnames";

interface CheckboxesProps {
    question: Question;
    value: string;
    onChange: (value: string) => void;
}

/** Checkboxes is a question view for selecting multiple options from a list */
const Checkboxes = ({ question, value, onChange }: CheckboxesProps) => {

    const choices = question.choices;

    if (!choices || Object.keys(choices).length <= 0) {
        throw new Error("Checkboxes question must have choices");
    }

    const values = value ? value.split(",") : [];

    // Add/remove value
    const onToggle = (value: string) => {
        const index = values.indexOf(value);
        if (index === -1) {
            values.push(value);
        } else {
            values.splice(index, 1);
        }
        onChange(values.join(","));
    };

    return (
        <div className="aha__checkboxes">
            {Object.keys(choices).map((val, index) => (
                <Checkbox
                    key={index}
                    // This prop does not exist on Checkbox
                    name={question.key}
                    label={choices[val]}
                    value={val}
                    checked={values.includes(val)}
                    onChange={onToggle}
                />
            ))}
        </div>
    );
};

interface CheckboxProps {
    label: string;
    value: string;
    checked: boolean;
    onChange: (value: string) => void;
}

/** Checkbox is a single checkbox */
const Checkbox = ({ label, value, checked, onChange }: CheckboxProps) => {

    const handleKeyPress = (event: React.KeyboardEvent<HTMLDivElement>) => {
        // Enter or space
        if (event.key === "Enter" || event.key === " ") {
            onChange(value);
        }
    }

    return (
        <div
            className={classNames("checkbox", { checked })}
            onClick={() => onChange(value)}
            tabIndex={0}
            onKeyDown={handleKeyPress}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Checkboxes;
