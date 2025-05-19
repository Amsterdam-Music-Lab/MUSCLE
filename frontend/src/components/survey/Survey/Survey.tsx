import type { HTMLAttributes, ReactNode } from "react";
import type IQuestion from "@/types/Question";

import { useState } from "react";
import classNames from "classnames";
import { Question } from "../Question";
import { submitResultType } from "@/hooks/useResultHandler";
import { Button, Card } from "@/components/ui";
import { NarrowLayout } from "@/components/layout";
import styles from "./Survey.module.scss";

interface SurveyProps extends HTMLAttributes<HTMLDivElement> {
  formActive: boolean;
  form: IQuestion[];
  buttonLabel: string;
  skipLabel: string;
  isSkippable: boolean;
  submitResult: submitResultType;
}

// TODO move to views?

/** Survey */
const Survey = ({
  formActive,
  form,
  buttonLabel,
  skipLabel,
  isSkippable,
  submitResult,
  className,
  ...divProps
}: SurveyProps) => {
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
    <NarrowLayout className={classNames(className)} {...divProps}>
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

      {/* Continue button */}
      {showSubmitButtons && (
        <>
          {isSkippable && (
            // skip button
            <Button
              onClick={() => {
                submitResult();
              }}
              stretch={true}
              rounded={false}
              size="lg"
              variant="secondary"
              title={skipLabel}
            />
          )}

          <Button
            onClick={() => {
              submitResult();
            }}
            stretch={true}
            rounded={false}
            size="lg"
            variant="secondary"
            className={"submit"}
            allowMultipleClicks={true}
            disabled={formValid !== true}
            title={buttonLabel}
          />
        </>
      )}
    </NarrowLayout>
  );
};

export default Survey;
