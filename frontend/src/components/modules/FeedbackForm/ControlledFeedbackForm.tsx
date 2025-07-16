/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { SubmitEvent, HTMLAttributes, ReactNode } from "react";
import { t } from "@lingui/macro";
import classNames from "classnames";
import { Button } from "@/components/buttons";
import { TextAreaField } from "@/components/forms";
import styles from "./FeedbackForm.module.scss";

export interface ControlledFeedbackFormProps
  extends HTMLAttributes<HTMLFormElement> {
  /** Optional error message shown as an error of the textarea. */
  error?: string;

  /** Header shown above form */
  header?: ReactNode;

  /** Footer shown below the form */
  footer?: ReactNode;

  /** Callback to handle form submission */
  onSubmit?: (value: string) => void;

  /** Callback that handles changes to the input */
  onChange?: (value: string) => void;

  /** Number of rows of the texarea. Default 5. */
  rows?: number;
}

/**
 * Controlled component that shows a feedback form with one input field:
 * a large textarea for inputting feedback.
 */
export default function ControlledFeedbackForm({
  value,
  error,
  header,
  footer,
  onChange,
  onSubmit,
  rows = 5,
  className,
  children,
  ...formProps
}: ControlledFeedbackFormProps) {
  const handleSubmit = (event: SubmitEvent) => {
    event.preventDefault();
    if (onSubmit) onSubmit(value);
  };

  return (
    <>
      <form
        className={classNames(styles.form, className)}
        onSubmit={handleSubmit}
        {...formProps}
      >
        {header ?? t`Do you have any remarks or questions?`}
        <TextAreaField
          value={value}
          onChange={onChange}
          placeholder={t`Type your feedback...`}
          rows={rows}
          error={error}
          showError={true}
          className={styles.textarea}
        />
        <Button type="submit" variant="primary" stretch={true}>
          {t`Submit`}
        </Button>
        {footer}
      </form>
    </>
  );
}
