/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";

import { useLingui } from "@lingui/react/macro";
import type { TutorialStep } from "@/types/tutorial";
import classNames from "classnames";
import styles from "./TutorialMessage.module.scss";
import { Variant } from "@/types/themeProvider";

interface TutorialMessageProps
  extends TutorialStep,
    Omit<HTMLAttributes<HTMLDivElement>, "content" | "id"> {
  variant: Variant;
}

export default function TutorialMessage({
  id,
  title,
  completed,
  content,
  visible,
  className,
  children,
  variant = "primary",
  ...divProps
}: TutorialMessageProps) {
  const { t } = useLingui();
  return (
    <div
      className={classNames(
        styles.container,
        variant && `text-fill-${variant}`,
        className
      )}
      {...divProps}
    >
      <p className={styles.message}>
        {title && (
          <span className={styles.title}>{title ?? t`Explanation`}</span>
        )}
        {content}
      </p>
      {children}
    </div>
  );
}
