import classNames from "classnames";
import { css } from '@emotion/react'

import { QuestionProps } from "@/types/Question";
import useBoundStore from "@/util/stores";

interface RadioProps {
    label: string;
    value: string;
    checked: boolean;
    onChange: (value: string) => void;
    color?: string;
    disabled: boolean;
}

/** Radios is a question view for selecting a single option from a list */
const Radios = ({ question, value, onChange, disabled }: QuestionProps) => {
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
                    name={question.identifier}
                    label={choice.label}
                    value={choice.value}
                    checked={value === choice.value}
                    disabled={disabled}
                    onChange={onChange}
                    role="radio"
                    color={choice.color || 'colorPositive'}
                />
            ))}
        </div>
    );
};

/** Radio is a single option in a Radios question */
const Radio = ({ label, value, checked, onChange, color, disabled }: RadioProps) => {
        const theme = useBoundStore((state) => state.theme);
        const radioColor = theme[color] || "";
        const styleRadio = (radioColor: string) => {
            return css`
                &:hover {
                    i {
                        background-color: hsl(from ${radioColor} h s 40%);
                    }
                    &.checked {
                        i {
                            background-color: hsl(from ${radioColor} h s 40%);
                        }
                    }
                }
                &.checked {
                    i {
                        background-color: ${radioColor};
                        border: 2px solid ${radioColor};
                    }
                }
                &:focus {
                    outline: ${radioColor} auto 2px;
                }
            `
        }

    return (
        <div
            className={classNames("radio", { checked })}
            onClick={() => onChange(value)}
            tabIndex={0}
            role="radio"
            aria-checked={checked}
            onKeyDown={() => onChange(value)}
            css={styleRadio(radioColor)}
            disabled={disabled}
        >
            <i></i>
            <span>{label}</span>
        </div>
    );
};

export default Radios;
