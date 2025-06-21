/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { QuestionProps } from "./Question";

import { QuestionViews } from "@/types/Question";
import Range from "./_Range";
import TextRange from "./_TextRange";
import IconRange from "./_IconRange";
import DropDown from "./_DropDown";
import AutoComplete from "./_AutoComplete";
import ButtonArray from "./_ButtonArray";

import {
  CheckboxField,
  NumberInput,
  RadioField,
  TextInput,
} from "@/components/inputs";

const inputComponents = {
  [QuestionViews.BUTTON_ARRAY]: ButtonArray,
  [QuestionViews.DROPDOWN]: DropDown,
  [QuestionViews.AUTOCOMPLETE]: AutoComplete,
  [QuestionViews.RANGE]: Range,
  [QuestionViews.TEXT_RANGE]: TextRange,
  [QuestionViews.ICON_RANGE]: IconRange,
};

export interface QuestionInputFactoryProps
  extends Pick<QuestionProps, "question" | "onChange" | "disabled"> {}

/**
 * Factory component that renders the input of a particular question.
 */
export default function QuestionInputFactory({
  question,
  onChange,
  disabled,
}: QuestionInputFactoryProps) {
  const sharedProps = { value: question.value, onChange, disabled };
  switch (question.view) {
    case QuestionViews.STRING:
      // TODO This would ideally be e.g. QuestionViews.NUMBER and QuestionViews.TEXT
      return question.input_type === "number" ? (
        <NumberInput
          {...sharedProps}
          max={question.max_value}
          min={question.min_value}
        />
      ) : (
        <TextInput {...sharedProps} maxLength={question.max_length} />
      );

    case QuestionViews.RADIOS:
    case QuestionViews.CHECKBOXES:
      const choices = question.choices;
      if (!choices || Object.keys(choices).length == 0) {
        throw new Error(
          `Question with view "${question.view}" must have choices`
        );
      }

      // Coerce into right data format: options as a list of objects
      const values = Object.keys(choices);
      const options = values.map((value) => ({ value, label: choices[value] }));

      if (question.view == QuestionViews.RADIOS) {
        return (
          <RadioField {...sharedProps} name={question.key} options={options} />
        );
      } else {
        return (
          <CheckboxField
            {...sharedProps}
            value={question.value ?? []}
            name={question.key}
            options={options}
          />
        );
      }

    default:
      const InputComponent = inputComponents[question.view];
      return <InputComponent {...sharedProps} question={question} />;
  }
}
