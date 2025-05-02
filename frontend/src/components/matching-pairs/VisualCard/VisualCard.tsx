/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import classNames from "classnames";
import { API_ROOT } from "@/config";
import Card, { type CardProps } from "../Card/Card";
import styles from "./VisualCard.module.scss";

interface VisualCardProps extends CardProps {
  /** Source of the image */
  src: string;

  /** Alt text */
  alt: string;
}

/**
 * A visual card that contains an image at the front.
 */
export default function VisualCard({
  src,
  alt,
  className,
  variantFront = "primary",
  ...cardProps
}: VisualCardProps) {
  // Todo perhaps even check if the URL exists?
  const url = src.startsWith("http") ? src : API_ROOT + src;
  return (
    <Card className={classNames(styles.visual, className)} {...cardProps}>
      <Card.Front className={variantFront ? `fill-${variantFront}` : ""}>
        <img src={url} alt={alt} />
      </Card.Front>
    </Card>
  );
}
