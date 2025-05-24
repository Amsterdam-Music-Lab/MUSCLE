/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";
import type { Variant } from "@/types/themeProvider";
import classNames from "classnames";
import styles from "./Card.module.scss";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** Whether lines are drawn between sections */
  dividers?: boolean;

  /**
   * The spacing to use for the sections. Default "wide".
   */
  spacing?: "wide" | "narrow";
}

function Card({
  className,
  dividers = true,
  spacing = "wide",
  children,
  ...divProps
}: CardProps) {
  return (
    <article
      className={classNames(
        styles.card,
        dividers && styles.dividers,
        styles[spacing],
        className
      )}
      {...divProps}
    >
      {children}
    </article>
  );
}

export interface CardSectionProps
  extends Omit<HTMLAttributes<HTMLDivElement>, "title"> {
  title?: ReactNode;
  flush?: boolean;
  variant?: Variant;
  spacing: "wide" | "narrow";
  titleTag?: "h1" | "h2" | "h3" | "h4" | "h5" | "p" | "div";
  titleClass?: string;
}

Card.Section = ({
  flush = false,
  title,
  variant = "primary",
  spacing = "wide",
  className,
  children,
  titleTag = "h3",
  titleClass = styles.sectionTitle,
  ...divProps
}: CardSectionProps) => {
  const TitleTag = titleTag;
  return (
    <section
      className={classNames(
        styles.section,
        flush && styles.flush,
        styles[spacing],
        className
      )}
      {...divProps}
    >
      {title && (
        <TitleTag className={classNames(titleClass, `text-fill-${variant}`)}>
          {title}
        </TitleTag>
      )}
      {children && <div className={styles.sectionContent}>{children}</div>}
    </section>
  );
};

interface CardHeaderProps extends CardSectionProps {}

Card.Header = ({
  titleTag = "h2",
  titleClass = styles.cardTitle,
  className,
  ...cardSectionProps
}: CardHeaderProps) => {
  return (
    <Card.Section
      titleTag={titleTag}
      titleClass={titleClass}
      className={classNames(styles.cardHeader, className)}
      {...cardSectionProps}
    />
  );
};

interface CardOptionProps extends CardSectionProps {}

Card.Option = ({ className, ...cardSectionProps }: CardOptionProps) => {
  return (
    <Card.Section
      className={classNames(styles.cardOption, className)}
      {...cardSectionProps}
    />
  );
};

export default Card;
