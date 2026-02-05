import Question from "@/types/Question";
import Select from "react-select";

interface AutoCompleteProps {
    question: Question;
    value: string;
    onChange: (value: string) => void;
}

// When using Safari iOS the browser may scroll the page when using the react-select Select.
// Therefore we scroll back to top when the select is blurred
const scrollToTop = () => {
    window.scrollTo(0, 0);
};

// AutoComplete is a question view for selecting a single option from a dropdown list with autocompletion
const AutoComplete = ({ question, value, onChange }: AutoCompleteProps) => {

    const choices = question.choices;

    if (!choices || Object.keys(choices).length <= 0) {
        throw new Error("AutoComplete question must have choices");
    }

    const options = choices.map((choice) => ({
            value: choice.value,
            label: choice.label,
        }))
        .sort((a, b) => a.label.localeCompare(b.label));

    return (
        <div className="aha__autocomplete">
            <div className="control">
                <Select
                    options={options}
                    tabIndex={0}
                    name={question.key}
                    value={options.find((option) => option.value === value)}
                    onChange={(choice) => onChange(choice.value)}
                    onBlur={scrollToTop}
                />
            </div>
        </div>
    );
};

export default AutoComplete;
