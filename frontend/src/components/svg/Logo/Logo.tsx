/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { CSSProperties, HTMLAttributes, SVGAttributes } from "react";
import classNames from "classnames";
import type { Variant } from "@/types/themeProvider";
import { useVariantFill } from "@/hooks/useVariantFill";
import type { Fill } from "@/types/svg";
import { logos as componentMap } from "./logos";
import styles from "./Logo.module.scss";

export type LogoType =
  | "logo" // Logo only
  | "wordmark"
  | "lockup" // Logo and text
  | "lockup-horizontal"
  | "lockup-vertical";

export interface LogoBaseProps {
  fill?: Fill;
  variant?: Variant;
  type?: LogoType;
  knockout?: boolean;
}

export interface SpecificLogoProps
  extends LogoBaseProps,
    Omit<SVGAttributes<SVGSVGElement>, "fill" | "width" | "height" | "type"> {}

export type LogoName = keyof typeof componentMap;

interface LogoProps extends LogoBaseProps, HTMLAttributes<HTMLDivElement> {
  name: LogoName;
}

/**
 * A logo component
 */
export default function Logo({
  name,
  variant,
  fill,
  type = "logo",
  knockout = false,
  className,
  style,
  ...props
}: LogoProps) {
  const Component = componentMap[name];
  const variantFill = useVariantFill(variant ?? "primary") ?? "#000";
  fill = fill ?? variantFill;
  return (
    <div
      className={classNames(
        styles.logo,
        knockout && styles.knockout,
        className
      )}
      style={
        {
          "--logo-bg-start-color":
            typeof fill == "object" ? fill?.startColor : undefined,
          "--logo-bg-end-color":
            typeof fill == "object" ? fill?.endColor : undefined,
          "--logo-bg-scale": typeof fill == "object" ? fill?.scale : undefined,
          "--logo-bg-angle": typeof fill == "object" ? fill?.angle : undefined,
          "--logo-bg-color": typeof fill == "string" ? fill : undefined,
          ...style,
        } as CSSProperties
      }
      {...props}
    >
      <Component fill={knockout ? "#fff" : fill} type={type} />
    </div>
  );
}
