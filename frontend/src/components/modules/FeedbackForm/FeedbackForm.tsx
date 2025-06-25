/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import type { ControlledFeedbackFormProps } from "./ControlledFeedbackForm";

import { useState } from "react";
import { t } from "@/util/i18n";
import { Button } from "@/components/buttons";
import ControlledFeedbackForm from "./ControlledFeedbackForm";
import styles from "./FeedbackForm.module.scss";

export interface FeedbackFormProps
  extends Omit<
    ControlledFeedbackFormProps,
    "error" | "value" | "onChange" | "onSubmit"
  > {
  onSubmit: (value: string) => void;
  /** A thanks message shown if the form is submitted successfully */
  thanks?: ReactNode;
}

/**
 * A feedback form that allows users to submit feedback about the experiment.
 * It consists of a large text field with a submit button. If the submission
 * is successful, it will show a thanks message.
 *
 * The onSubmit callback can be obtained from the `useSubmitFeedback` hook:
 *
 * ```tsx
 * function MyComponent({ blockSlug, participant }) {
 *  const onSubmit = useSubmitFeedback(blockSlug, participant)
 *  return <FeedbackForm onSubmit={onSubmit} />
 * }
 * ```
 */
export default function FeedbackForm({
  onSubmit,
  thanks,
  className,
  ...formProps
}: FeedbackFormProps) {
  const [value, setValue] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState();

  const handleSubmit = async (value: string) => {
    if (value === "") return setError(t("feedbackForm.emptyFeedback"));
    const result = await onSubmit(value);
    if (result?.status === "ok") {
      setSubmitted(true);
    } else {
      setError(t("feedbackForm.submissionError"));
    }
  };

  return !submitted ? (
    <ControlledFeedbackForm
      value={value}
      onSubmit={handleSubmit}
      onChange={setValue}
      error={error}
      {...formProps}
    />
  ) : (
    <>
      <p>
        <span className="fw-semibold text-fill-primary">
          {t("feedbackForm.submitted")}
        </span>{" "}
        {thanks}
      </p>

      <Button
        className={styles.moreFeedbackButton}
        size="sm"
        onClick={() => {
          setSubmitted(false);
          setError("");
          setValue();
        }}
      >
        {t("feedbackForm.submitMore")}
      </Button>
    </>
  );
}
