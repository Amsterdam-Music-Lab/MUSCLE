/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { TutorialStep } from "@/types/tutorial";
import classNames from "classnames";
import styles from "./TutorialMessage.module.scss";

interface TutorialMessageProps
  extends TutorialStep,
    Omit<HTMLAttributes<HTMLDivElement>, "content" | "id"> {}

export default function TutorialMessage({
  id,
  title = "Explanation",
  completed,
  content,
  visible,
  className,
  children,
  ...divProps
}: TutorialMessageProps) {
  return (
    <div className={classNames(styles.container, className)} {...divProps}>
      <p className={styles.message}>
        {title && <span className={styles.title}>{title}</span>}
        {content}
      </p>
      {children}
    </div>
  );
}
