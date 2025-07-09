/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { en } from "@/locales/en";

/**
 * Translation function to future-proof the application. Currently
 * there is not translation in place, but using `t` will make transitioning
 * easier later.
 *
 * Translations are specified in for example `/locales/en.ts`. In practice
 * you use the translator as follows:
 *
 * ```ts
 * // Code in some feedback component
 * setError("Your input cannot be empty");
 * // --> becomes
 * setError(t("feedback.error.empty"))
 * ```
 *
 * You can provide variables as follows:
 *
 * ```ts
 * // en["validation.minLength"] = "Must be at least {{ min }} characters."
 * t("validation.minLength", { min: 3 })
 * ```
 */
export const t = (key: string, vars: Record<string, string | number> = {}) => {
  let str = en[key as keyof typeof en] || `[${key}]`;
  Object.entries(vars).forEach(([k, v]) => {
    str = str.replaceAll(`{{${k}}}`, String(v));
  });
  return str;
};
