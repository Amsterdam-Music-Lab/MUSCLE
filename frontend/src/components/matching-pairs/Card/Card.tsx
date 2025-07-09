/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";
import type { Variant } from "@/types/themeProvider";
import { Children } from "react";
import classNames from "classnames";
import styles from "./Card.module.scss";

export interface CardProps extends Omit<HTMLAttributes<HTMLDivElement>, "id"> {
  /** Whether the card is flipped (i.e., the front is shown) */
  flipped?: boolean;

  /** Whether the card is disabled (i.e., not clickable) */
  disabled?: boolean;

  /** Theme variant for the front. Ignored when a CardFront child is found. */
  variantFront?: Variant;

  /** Theme variant for the back. Ignored when a CardBack child is found. */
  variantBack?: Variant;

  label?: ReactNode | string;
}

/**
 * A generic playing card with 3d effects. On hover the card is rotated slightly
 * as if a corner is lifted. When the card is flipped, a 180 degrees rotation is
 * animated. The front and back can be changed by passing Card.Front or Card.Back
 * children. AudioCard and VisualCard effectively descend from this component.
 */
function Card({
  flipped,
  disabled,
  className,
  children,
  variantFront = "primary",
  variantBack = "secondary",
  label,
  onClick = () => {},
  ...props
}: CardProps) {
  // Find child cards
  const childrenArray = Children.toArray(children);
  let front = childrenArray.find((child: any) => child.type === Card.Front);
  let back = childrenArray.find((child: any) => child.type === Card.Back);

  // Default Front
  if (!front) {
    front = (
      <Card.Front className={variantFront ? `fill-${variantFront}` : ""} />
    );
  }

  // DefaultBack
  if (!back) {
    back = (
      <Card.Back className={variantBack ? `fill-${variantBack}` : ""}>
        {label}
      </Card.Back>
    );
  }

  return (
    <div
      data-testid="playing-card"
      className={classNames(
        styles.card,
        {
          [styles.flipped]: flipped,
          [styles.disabled]: disabled,
        },
        className
      )}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick();
          e.currentTarget.blur();
        }
      }}
      {...props}
    >
      {flipped ? front : back}
    </div>
  );
}

interface CardFrontProps extends HTMLAttributes<HTMLDivElement> {}

Card.Front = function CardFront({ className, ...props }: CardFrontProps) {
  return (
    <div
      data-testid="front"
      className={classNames(styles.front, className)}
      {...props}
    />
  );
};

interface CardBackProps extends HTMLAttributes<HTMLDivElement> {}

Card.Back = function CardBack({ className, ...props }: CardBackProps) {
  return (
    <div
      data-testid="back"
      className={classNames(styles.back, className)}
      {...props}
    />
  );
};

export default Card;
