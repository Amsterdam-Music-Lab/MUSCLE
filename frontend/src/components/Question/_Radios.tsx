import Question from "@/types/Question";
import classNames from "classnames";

interface RadiosProps {
    question: Question;
    value: string;
    onChange: (value: string) => void;
}

interface RadioProps {
    label: string;
    value: string;
    checked: boolean;
    onChange: (value: string) => void;
}

/** Radios is a question view for selecting a single option from a list */
const Radios = ({ question, value, onChange }: RadiosProps) => {

    const choices = question.choices;

    if (!choices || choices.length <= 0) {
        throw new Error("Radios question must have choices");
    }

    return (
        <div className="aha__radios">
            {choices.sort((a, b) => a.label - b.label).map((choice, index) => (
                <Radio
                    key={index}
                    // This prop does not exist on Radio
                    name={question.key}
                    label={choice.label}
                    value={choice.value}
                    checked={value === choice.value}
                    onChange={onChange}
                    role="radio"
                />
            ))}
        </div>
    );
};

/** Radio is a single option in a Radios question */
const Radio = ({ label, value, checked, onChange }: RadioProps) => {
    return (
        <div
            className={classNames("radio", { checked })}
            onClick={() => onChange(value)}
            tabIndex={0}
            role="radio"
            aria-checked={checked}
            onKeyDown={() => onChange(value)}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Radios;
