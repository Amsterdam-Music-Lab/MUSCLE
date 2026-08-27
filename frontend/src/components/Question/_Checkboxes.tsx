import classNames from "classnames";
import { css } from '@emotion/react'

import { QuestionProps } from "@/types/Question";
import useBoundStore from "@/util/stores";


/** Checkboxes is a question view for selecting multiple options from a list */
const Checkboxes = ({ question, value, onChange, disabled }: QuestionProps) => {

    const choices = question.choices;

    if (!choices || choices.length <= 0) {
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
            {choices.map((choice, index) => (
                <Checkbox
                    key={index}
                    // This prop does not exist on Checkbox
                    name={question.identifier}
                    label={choice.label}
                    value={choice.value}
                    checked={values.includes(choice.value)}
                    onChange={onToggle}
                    color={choice.color || 'colorNeutral2'}
                    disabled={disabled}
                />
            ))}
        </div>
    );
};

interface CheckboxProps {
    label: string;
    value: string;
    color?: string;
    checked: boolean;
    onChange: (value: string) => void;
    disabled: boolean;
}

/** Checkbox is a single checkbox */
const Checkbox = ({ label, value, checked, onChange, color, disabled}: CheckboxProps) => {
    const theme = useBoundStore((state) => state.theme);
    const checkBoxColor = theme[color] || '';

    const styleCheckBox = (checkBoxColor: string) => {
            return css`
                &:hover {
                    i {
                        background-color: hsl(from ${checkBoxColor} h s 40%);
                    }
                    &.checked {
                        i {
                            background-color: hsl(from ${checkBoxColor} h s 40%);
                        }
                    }
                }
                &.checked {
                    i {
                        background-color: ${checkBoxColor};
                        border: 2px solid ${checkBoxColor};
                    }
                }
                &:focus {
                    outline: ${checkBoxColor} auto 2px;
                }
            `
        }

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
            css={styleCheckBox(checkBoxColor)}
            disabled={disabled}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Checkboxes;
