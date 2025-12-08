import classNames from "classnames";
import { renderLabel } from "../../util/label";
import Question from "@/types/Question";

interface ButtonArrayProps {
    question: Question;
    disabled: boolean;
    onChange: (value: string) => void;
    value: string;
}

interface ToggleButtonProps {
    label: string;
    value: string;
    index: number;
    name: string;
    disabled: boolean;
    onChange: (value: string) => void;
    checked: boolean;
}

/** ButtonArray is a question view for selecting a single option from a list of buttons */
const ButtonArray = ({ question, disabled, onChange, value }: ButtonArrayProps) => {

    const choices = question.choices;

    if (!choices || Object.keys(choices).length <= 0) {
        throw new Error("ButtonArray question must have choices");
    }

    const buttonPress = (value: string) => {
        if (disabled) {
            return;
        }
        else {
            onChange(value)
        }
    }

    return (
        <div className="aha__buttons buttons d-flex flex-wrap justify-content-center p-3 w-100">

            <div className={classNames("btn-group-toggle-custom", question.style)} role="group" data-toggle="buttons" aria-label="Button Array">
                {Object.keys(choices).map((val, index) => (
                    <ToggleButton
                        label={choices[val]}
                        value={val}
                        index={index}
                        name={question.key}
                        key={`${question.key}-${index}`}
                        onChange={buttonPress}
                        disabled={disabled}
                        checked={value === val}
                    />
                ))}
            </div>
        </div>
    )
}

/** ToggleButton is a single button in a ButtonArray */
const ToggleButton = ({ label, value, index, name, disabled, onChange, checked }: ToggleButtonProps) => {
    const disabledClasses = disabled ? 'disabled' : '';
    const checkedClasses = checked ? 'checked' : '';
    const indexString = index.toString();
    return (
        <label
            className={classNames("btn btn-secondary btn-lg", disabledClasses, checkedClasses)}
            tabIndex={0}
        >
            <input className={value}
                type="radio"
                role="button"
                name={name}
                id={indexString}
                value={value}
                checked={checked}
                aria-checked={checked}
                disabled={disabled}
                onChange={() => onChange(value)}
                onKeyUp={() => onChange(value)}
                data-testid={`toggle-button-${value}`}
            />
            {renderLabel(label)}
        </label>)
}

export default ButtonArray;
