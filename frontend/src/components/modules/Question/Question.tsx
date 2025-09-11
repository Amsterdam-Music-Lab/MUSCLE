/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type IQuestion from "@/types/Question";
import classNames from "classnames";
import QuestionFieldFactory from "./QuestionFieldFactory";
import styles from "./Question.module.scss";
import { BaseFieldProps } from "@/components/forms/types";

export interface QuestionProps extends HTMLAttributes<HTMLDivElement> {
  question: IQuestion;

  /** Callback called whenever the input changes. */
  onChange: (updatedValue: string | number | boolean) => void;

  /** Optional properties passed on to the field component */
  fieldProps?: BaseFieldProps;

  divProps?: HTMLAttributes<HTMLDivElement>;

  className?: string;
}

/**
 * Question component that shows the question text and an input field.
 * It uses a factory component (`QuestionFieldFactory`) that renders a
 * particularly input field, based on the value of `question.view`:
 *
 * | View         | Rendered component                          |
 * |--------------|---------------------------------------------|
 * | STRING       | `TypedField`                                |
 * | RADIOS       | `RadioField` (wrapper of `OptionField`)     |
 * | CHECKBOXES   | `CheckboxField` (wrapper of `OptionField`)  |
 * | RANGE        | `SliderField`                               |
 * | _TEXT_RANGE_   | _Alias for `RANGE`_                       |
 * | ICON_RANGE   | `SliderField` with particular props optimized for icons |
 * | DROPDOWN     | `SelectField`                               |
 * | _AUTOCOMPLETE_ | _Alias for `DROPDOWN`_                    |
 *
 * Many question views result in option fields, where users select from amongst
 * several options: `RADIOS`, `CHECKBOXES`, `DROPDOWN`, `ICON_RANGE`, and
 * possibly `RANGE`. These options are specified as:
 *
 * ```ts
 * question.choices = {
 *  apple: "Apple",
 *  banana: "Banana",
 *  //...
 * }
 * ```
 *
 * `QuestionFieldFactory` then converts these `choices` to a more
 * conventional `options` property, that is accepted by all option-based
 * field components. This allows for things like disabling options:
 *
 * ```tsx
 *  <CheckboxField
 *    value="apple"
 *    options={[
 *      { value: "apple", label: "Apple" },
 *      { value: "banana", label: "Banana", disabled: true },
 *      //...
 *    ]} />
 * ```
 */
const Question = ({
  question: questionObj,
  onChange,
  className,
  divProps,
  ...fieldProps
}: QuestionProps) => {
  // Rename variables internally
  let { explainer, question } = questionObj;
  const expectedResponse = questionObj?.expected_response;

  // Emphasize title; bit hacky for compatibility. Should just be a field prop.
  let labelClassName = classNames(questionObj?.style ?? "");
  if (labelClassName.includes("emphasize-title")) {
    labelClassName = classNames(labelClassName, styles.emphasizeTitle);
  }
  return (
    <div
      className={classNames(styles.questionContainer, className)}
      {...divProps}
    >
      {explainer && <p className={styles.explainer}>{explainer}</p>}
      <div className={styles.question}>
        <QuestionFieldFactory
          question={questionObj}
          onChange={onChange}
          label={question}
          {...fieldProps}
          fieldWrapperProps={{
            ...(fieldProps.fieldWrapper ?? {}),
            labelClassName,
          }}
          tabIndex={0}
        />
      </div>

      {/* Will only be visible when the backend settings has TESTING=True */}
      {expectedResponse && (
        <p className={styles.expectedResponse}>
          <strong>Expected:</strong> {expectedResponse}
        </p>
      )}
    </div>
  );
};

export default Question;
