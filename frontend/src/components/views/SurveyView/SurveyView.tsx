/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { FormEvent } from "react";
import type { Survey } from "@/components/application";
import type SurveyQuestion from "@/types/Question";

import { useState, useEffect } from "react";
import { Question } from "@/components/question";
import { Button, Card } from "@/components/ui";
import { NarrowLayout } from "@/components/layout";

function validateQuestion(question: SurveyQuestion) {
  // For multiple choices in CHECKBOXES view, question.value is a string of comma-separated values
  return !(
    question.view === "CHECKBOXES" &&
    question.min_values &&
    question.value.split(",").length < question.min_values
  );
}

function validateQuestions(questions: SurveyQuestion[]) {
  const validQuestions = questions.filter(
    (q) => q.is_skippable || (q.value && q.value !== "" && validateQuestion(q))
  );
  return validQuestions.length === questions.length;
}

export interface SurveyViewProps extends Survey {
  onChange: (updatedSurvey: Survey) => void;

  /** Callback called when submitting the form */
  onSubmit: (questions: SurveyQuestion[]) => void;

  /** Whether the survey is disabled */
  disabled?: boolean;
}

/**
 * SurveyView: shows an array of questions. Note that this is a controlled component:
 * the survey state is owned by Trial.
 */
export default function SurveyView({
  questions,
  onChange,
  onSubmit,
  disabled = false,
  skippable = false,
  submitLabel = "Submit",
  skipLabel = "Skip",
}: SurveyViewProps) {
  const [isValid, setIsValid] = useState(false);

  // Validate questions whenever questions changes
  useEffect(() => setIsValid(validateQuestions(questions)), [questions]);

  // Update state when the question's value changes
  const handleChange = (value, index) => {
    onChange((prev) => prev.map((q, i) => (i === index ? { ...q, value } : q)));
    if (questions[index].submits) onSubmit();
  };

  const handleSubmit = (e?: FormEvent) => {
    if (e) e.preventDefault();
    if (isValid) onSubmit(questions);
  };

  const showSubmitButtons = questions.filter((q) => q.submits).length === 0;

  return (
    <form onSubmit={handleSubmit}>
      <NarrowLayout>
        <Card>
          {questions.map((question, index) => {
            return (
              <Card.Section key={index} title={question.question} titleTag="h2">
                <Question
                  id={index}
                  disabled={disabled}
                  question={{
                    ...question,
                    value: questions[index].value,
                    // Hide question as it's already shown as the Card.Section title
                    question: "",
                  }}
                  onChange={handleChange}
                />
              </Card.Section>
            );
          })}
        </Card>

        {showSubmitButtons && (
          <>
            {skippable && (
              <Button
                title={skipLabel}
                onClick={handleSubmit}
                stretch={true}
                rounded={false}
                size="lg"
                variant="secondary"
              />
            )}

            <Button
              type="submit"
              title={submitLabel}
              // onClick={handleSubmit}
              stretch={true}
              rounded={false}
              size="lg"
              variant="secondary"
              disabled={isValid !== true}
            />
          </>
        )}
      </NarrowLayout>
    </form>
  );
}

SurveyView.viewName = "survey";
SurveyView.usesOwnLayout = true;
SurveyView.getViewProps = undefined;
