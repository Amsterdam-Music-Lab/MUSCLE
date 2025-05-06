/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { CSSProperties, HTMLAttributes, SVGAttributes } from "react";
import type { LogoName } from "../Logo/Logo";
import classNames from "classnames";
import styles from "./Logos.module.scss";
import Logo from "../Logo/Logo";

interface LogosProps extends HTMLAttributes<HTMLDivElement> {
  logos: LogoName[];
  height?: number;
}

export default function Logos({
  logos,
  height = 2,
  className,
  ...divProps
}: LogosProps) {
  return (
    <div
      className={classNames(styles.logos, className)}
      style={{ "--logos-gap": `${height}em` }}
      {...divProps}
    >
      {logos.map((name) => (
        <Logo
          key={name}
          name={name}
          className={styles.logo}
          fill="#fff"
          style={{ height: `${name == "nwo" ? 1.75 * height : height}em` }}
        />
      ))}
    </div>
  );
}
