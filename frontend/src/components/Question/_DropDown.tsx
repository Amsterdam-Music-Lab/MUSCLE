import Question from "@/types/Question";

interface DropDownProps {
    question: Question;
    value: string;
    onChange: (value: string) => void;
}

/** DropDown is a question view for selecting a single option from a dropdown list */
const DropDown = ({ question, value, onChange }: DropDownProps) => {

    const choices = question.choices;

    if (!choices || Object.keys(choices).length <= 0) {
        throw new Error("DropDown question must have choices");
    }

    return (
        <div className="aha__dropdown">
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                tabIndex={0}
                name={question.key}
            >
                <option value=""></option>
                {Object.keys(choices).map((val, index) => (
                    <option value={val} key={index}>
                        {choices[val]}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default DropDown;
