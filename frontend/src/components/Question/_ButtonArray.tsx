import classNames from "classnames";

import { renderLabel } from "../../util/label";
import { styleButton } from "@/util/stylingHelpers";
import useBoundStore from "@/util/stores";
import Question from "@/types/Question";
import { Theme as ITheme } from "@/types/Theme";

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
    theme: ITheme;
}

/** ButtonArray is a question view for selecting a single option from a list of buttons */
const ButtonArray = ({ question, disabled, onChange, value }: ButtonArrayProps) => {
    const theme = useBoundStore((state) => state.theme);

    const choices = question.choices;

    if (!choices || choices.length <= 0) {
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
                {choices.map((choice, index) => (
                    <ToggleButton
                        label={choice.label}
                        value={choice.value}
                        index={index}
                        color={choice.color}
                        name={question.key}
                        key={`${question.key}-${index}`}
                        onChange={buttonPress}
                        disabled={disabled}
                        checked={value === choice.value}
                        theme={theme}
                    />
                ))}
            </div>
        </div>
    )
}

/** ToggleButton is a single button in a ButtonArray */
const ToggleButton = ({ label, value, index, name, disabled, onChange, checked, theme }: ToggleButtonProps) => {
    const disabledClasses = disabled ? 'disabled' : '';
    const checkedClasses = checked ? 'checked' : '';
    const indexString = index.toString();
    const colorValue = theme? theme[color] : '#fabbacc';
    
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
                css={styleButton(colorValue)}
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
