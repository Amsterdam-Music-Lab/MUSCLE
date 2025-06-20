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
import String from "./_String";
import Checkboxes from "./_Checkboxes";
import DropDown from "./_DropDown";
import AutoComplete from "./_AutoComplete";
import ButtonArray from "./_ButtonArray";

import { RadioQuestion } from "../RadioQuestion";
import { NumberInput, TextInput } from "@/components/inputs";

const inputComponents = {
  [QuestionViews.BUTTON_ARRAY]: ButtonArray,
  [QuestionViews.CHECKBOXES]: Checkboxes,
  [QuestionViews.DROPDOWN]: DropDown,
  [QuestionViews.AUTOCOMPLETE]: AutoComplete,
  [QuestionViews.RADIOS]: RadioQuestion,
  [QuestionViews.RANGE]: Range,
  [QuestionViews.TEXT_RANGE]: TextRange,
  [QuestionViews.ICON_RANGE]: IconRange,
  [QuestionViews.STRING]: String,
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
    // TODO this is not ideal. Should have QuestionViews.NUMBER and QuestionViews.TEXT
    case QuestionViews.STRING:
      return question.input_type === "number" ? (
        <NumberInput
          {...sharedProps}
          max={question.max_value}
          min={question.min_value}
        />
      ) : (
        <TextInput {...sharedProps} maxLength={question.max_length} />
      );
    default:
      const InputComponent = inputComponents[question.view];
      return <InputComponent {...sharedProps} question={question} />;
  }
}
