/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Question, { QuestionViews } from "@/types/Question";
import DropDown from "./_DropDown";
import AutoComplete from "./_AutoComplete";
import ButtonArray from "./_ButtonArray";

import { CheckboxField, NumberInput, RadioField, SliderField, TextInput } from "@/components/forms";

const inputComponents = {
    [QuestionViews.BUTTON_ARRAY]: ButtonArray,
    [QuestionViews.DROPDOWN]: DropDown,
    [QuestionViews.AUTOCOMPLETE]: AutoComplete,
};

/**
 * Utility that coerces question.choices into the options format:
 * an array of objects.
 */
function getOptions(question: Question, warn: boolean = true) {
    const choices = question.choices;
    if (warn && (!choices || Object.keys(choices).length === 0)) {
        throw new Error(`Question with view "${question.view}" must have choices`);
    }
    const values = Object.keys(choices);
    const options = values.map((value) => ({ value, label: choices[value] }));
    return { choices, options, values };
}

export interface QuestionInputFactoryProps {
    question: Question;
    onChange: (updatedValue: string | number | boolean) => void;
    disabled: boolean;
    fieldProps: any;
}

/**
 * Factory component that renders the input of a particular question.
 */
export default function QuestionInputFactory({
    question,
    onChange,
    disabled,
    fieldProps,
}: QuestionInputFactoryProps) {
    const sharedProps = {
        value: question.value,
        onChange,
        disabled,
        ...fieldProps,
    };

    //————————————————————————————————

    switch (question.view) {
        case QuestionViews.STRING:
            // TODO This would ideally be e.g. QuestionViews.NUMBER and QuestionViews.TEXT
            return question.input_type === "number" ? (
                <NumberInput {...sharedProps} max={question.max_value} min={question.min_value} />
            ) : (
                <TextInput {...sharedProps} maxLength={question.max_length} />
            );

        //————————————————————————————————

        case QuestionViews.RADIOS:
        case QuestionViews.CHECKBOXES: {
            const { options } = getOptions(question);
            if (question.view === QuestionViews.RADIOS) {
                return (
                    <RadioField
                        {...sharedProps}
                        name={question.key ?? "radios"}
                        options={options}
                    />
                );
            } else {
                return (
                    <CheckboxField
                        {...sharedProps}
                        value={question.value ?? []}
                        name={question.key ?? "checkbox"}
                        options={options}
                    />
                );
            }
        }

        //————————————————————————————————

        case QuestionViews.RANGE:
        case QuestionViews.TEXT_RANGE: {
            const { options } = getOptions(question);
            return <SliderField {...sharedProps} options={options} />;
        }

        //————————————————————————————————

        case QuestionViews.ICON_RANGE: {
            const { options: opts } = getOptions(question);
            const options = opts.map(({ value, label }) => ({
                value,
                label: <span className={`fa ${label}`} style={{ fontSize: "2em" }} />,
            }));
            return (
                <SliderField
                    options={options}
                    {...sharedProps}
                    showIntermediateTickLabels={true}
                    showTickLabelsInside={true}
                    thumbSize="3em"
                />
            );
        }

        //————————————————————————————————

        default:
            const InputComponent = inputComponents[question.view];
            return <InputComponent {...sharedProps} question={question} />;
    }
}
