/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { BaseFieldProps } from "@/components/forms/types";
import Question, { QuestionViews } from "@/types/Question";
import ButtonArray from "./_ButtonArray";

import {
  CheckboxField,
  RadioField,
  SelectField,
  SliderField,
  TypedField,
} from "@/components/forms";

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

export interface QuestionFieldFactoryProps extends BaseFieldProps {
  question: Question;
  onChange: (updatedValue: string | number | boolean) => void;
}

/**
 * Factory component that renders the input of a particular question.
 */
export default function QuestionFieldFactory({
  question,
  ...fieldProps
}: QuestionFieldFactoryProps) {
  const sharedProps = {
    value: question.value,
    ...fieldProps,
  };

  //————————————————————————————————

  switch (question.view) {
    case QuestionViews.STRING:
      return (
        <TypedField
          {...sharedProps}
          type={question.input_type}
          min={question?.min_value}
          max={question?.max_value}
          maxLength={question?.max_length}
        />
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

    case QuestionViews.AUTOCOMPLETE:
    case QuestionViews.DROPDOWN: {
      const { options } = getOptions(question);
      return <SelectField {...sharedProps} options={options} />;
    }

    case QuestionViews.BUTTON_ARRAY:
      return <ButtonArray {...sharedProps} question={question} />;

    default:
      throw Error(`Unknown question view "${question.view}"`);
  }
}
