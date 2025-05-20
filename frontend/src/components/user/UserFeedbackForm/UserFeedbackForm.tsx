/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ChangeEvent, HTMLAttributes, ReactNode } from "react";
import type { CardProps } from "@/components/ui";
import type { FeedbackInfo } from "@/types/Block";

import { useState } from "react";
import classNames from "classnames";
import { postFeedback } from "@/API";
import { Button, Card } from "@/components/ui";

import styles from "./UserFeedbackForm.module.scss";

interface FormProps extends HTMLAttributes<HTMLFormElement> {
  header?: string;
  handleSubmit?: (value: string) => void;
  buttonText?: string;
  contactInformation?: string;

  /** Number of rows of the texarea */
  rows?: number;
}

function Form({
  header,
  handleSubmit = () => {},
  buttonText = "Submit",
  contactInformation = "",
  className,
  rows = 5,
  ...formProps
}: FormProps) {
  const [value, setValue] = useState("");
  const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setValue(event.target.value);
  };

  return (
    <>
      <Card.Section flush={true}>
        <form className={classNames(styles.form, className)} {...formProps}>
          <textarea
            className={styles.textarea}
            placeholder="Type your feedback..."
            rows={rows}
            onChange={handleChange}
            value={value}
          />
          <div style={{ padding: "1em" }}>
            <Button
              title={buttonText}
              variant="primary"
              stretch={true}
              className={classNames(
                styles.button,
                "anim anim-fade-in anim-speed-500"
              )}
              onClick={() => handleSubmit(value)}
            />
          </div>
        </form>
      </Card.Section>
      <Card.Section>
        <div dangerouslySetInnerHTML={{ __html: contactInformation }} />
      </Card.Section>
    </>
  );
}

export interface UserFeedbackFormProps extends Omit<CardProps, "title"> {
  blockSlug: string;
  participant: any;
  feedbackInfo: FeedbackInfo;
  inline?: boolean;
  title?: ReactNode;
  wrapInCard?: boolean;
}

export default function UserFeedbackForm({
  blockSlug,
  participant,
  feedbackInfo,
  inline = true,
  wrapInCard = true,
  className,
  title = "Your Feedback",
  ...cardProps
}: UserFeedbackFormProps) {
  const [showForm, setShowForm] = useState(true);

  const handleSubmit = async (value: string) => {
    const data = {
      blockSlug,
      feedback: value,
      participant,
    };
    await postFeedback(data);
    setShowForm(false);
    return;
  };

  const content = showForm ? (
    <Form
      handleSubmit={handleSubmit}
      header={feedbackInfo.header}
      contactInformation={feedbackInfo.contact_body}
    />
  ) : (
    <Card.Section children={feedbackInfo.thank_you} />
  );

  return !wrapInCard ? (
    content
  ) : (
    <Card
      dividers={false}
      className={classNames(styles.container, className)}
      {...cardProps}
    >
      <Card.Header title={title} />
      {content}
    </Card>
  );
}
