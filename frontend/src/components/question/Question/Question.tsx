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
import QuestionInputFactory from "./QuestionInputFactory";
import styles from "./Question.module.scss";

export interface QuestionProps extends HTMLAttributes<HTMLDivElement> {
  question: IQuestion;

  /**
   * A unique identifier for the question. Will be passed to the
   * onChange callback.
   */
  id: number;

  /**
   * Callback called whenever the input changes. The callback
   * receives both the updatedValue and the id of the question.
   */
  onChange: (updatedValue: string | number | boolean, id: number) => void;

  /** Whether the question is disabled. Default false. */
  disabled?: boolean;
}

/**
 * Question component that shows the question text plus the input component.
 * It uses a factory component that the input based on the view specified in
 * question.view
 */
const Question = ({
  question: questionObj,
  onChange,
  id,
  disabled = false,
  className,
  ...divProps
}: QuestionProps) => {
  // Rename variables internally
  const {
    explainer,
    question,
    style: questionClassName,
    expected_response: expectedResponse,
  } = questionObj;
  return (
    <div
      className={classNames(styles.questionContainer, className)}
      {...divProps}
    >
      {explainer && <p className={styles.explainer}>{explainer}</p>}
      {question && (
        <p className={classNames(styles.questionText, questionClassName)}>
          {question}
        </p>
      )}
      <div className={styles.question}>
        <QuestionInputFactory
          question={questionObj}
          disabled={disabled}
          onChange={(updatedValue: string | number | boolean) =>
            onChange(updatedValue, id)
          }
        />
      </div>
      {expectedResponse && (
        /* Will only be visible when the backend settings has TESTING=True */
        <p className={styles.expectedResponse}>{expectedResponse}</p>
      )}
    </div>
  );
};

export default Question;
