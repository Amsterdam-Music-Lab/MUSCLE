/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type IQuestion from "@/types/Question";

import { useState } from "react";
import { Question } from "@/components/question";
import { submitResultType } from "@/hooks/useResultHandler";
import { Button, Card } from "@/components/ui";

export interface SurveyViewProps {
  formActive: boolean;
  form: IQuestion[];
  buttonLabel: string;
  skipLabel: string;
  isSkippable: boolean;
  submitResult: submitResultType;
}

/** SurveyView */
export default function SurveyView({
  formActive,
  form,
  buttonLabel,
  skipLabel,
  isSkippable,
  submitResult,
  className,
  ...divProps
}: SurveyViewProps) {
  const showSubmitButtons =
    form.filter((formElement) => formElement.submits).length === 0;

  const [formValid, setFormValid] = useState(false);

  const onChange = (
    value: string | number | boolean,
    question_index: number
  ) => {
    form[question_index].value = value;
    if (form[question_index].submits) {
      submitResult();
    }
    // for every non-skippable question, check that we have a value
    const validFormElements = form.filter((formElement) => {
      if (
        formElement.is_skippable ||
        (formElement.value && validateFormElement(formElement))
      ) {
        return true;
      }
      return false;
    });
    setFormValid(validFormElements.length === form.length);
  };

  function validateFormElement(formElement: IQuestion) {
    // For multiple choices in CHECKBOXES view, formElement.value is a string of comma-separated values
    if (
      formElement.view === "CHECKBOXES" &&
      formElement.min_values &&
      formElement.value.split(",").length < formElement.min_values
    ) {
      return false;
    }
    return true;
  }

  return (
    <>
      <Card>
        <form>
          {form.map((question, index) => {
            return (
              <Card.Section key={index} title={question.question} titleTag="h2">
                <Question
                  id={index}
                  disabled={!formActive}
                  question={{ ...question, question: "" }}
                  onChange={onChange}
                />
              </Card.Section>
            );
          })}
        </form>
      </Card>

      {showSubmitButtons && (
        <>
          {isSkippable && (
            <Button
              title={skipLabel}
              onClick={submitResult}
              stretch={true}
              rounded={false}
              size="lg"
              variant="secondary"
            />
          )}

          <Button
            title={buttonLabel}
            onClick={submitResult}
            stretch={true}
            rounded={false}
            size="lg"
            variant="secondary"
            className={"submit"}
            disabled={formValid !== true}
          />
        </>
      )}
    </>
  );
}

SurveyView.viewName = "survey";
SurveyView.usesOwnLayout = false;
SurveyView.getViewProps = undefined;
