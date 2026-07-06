import { QuestionProps } from "@/types/Question";

/** DropDown is a question view for selecting a single option from a dropdown list */
const DropDown = ({ question, value, onChange, disabled }: QuestionProps) => {
    const choices = question.choices;

    if (!choices || choices.length <= 0) {
        throw new Error("DropDown question must have choices");
    }

    return (
        <div className="aha__dropdown">
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                tabIndex={0}
                name={question.identifier}
                disabled={disabled}
            >
                <option value=""></option>
                {choices.map((choice, index) => (
                    <option value={choice.value} key={index}>
                        {choice.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default DropDown;
