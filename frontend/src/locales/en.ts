/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

/**
 * Prefixer utility that prefixes all keys in an object with
 * the given prefix.
 *
 * ```ts
 * prefix("foo", { a: 2, b: 3 })
 * // { fooA: 2, fooB: 3 }
 * ```
 */
function prefix(prefix: string, object: Record<string, any>) {
  let prefixed = {};
  Object.keys(object).forEach((key) => {
    prefixed[`${prefix}.${key}`] = object[key];
  });
  return prefixed;
}

/**
 * All translations for component/modules/FeedbackForm
 */
const feedbackForm = prefix("feedbackForm", {
  submissionError: `An error has occured. Your feedback could not be stored. Please try again later, or share your feedback via email.`,
  emptyFeedback: "Please provide some feedback",
  placeholder: "Type your feedback...",
  submitMore: "Submit more feedback",
  submitted: "Your feedback was submitted.",
});

/**
 * Translations for common phrases
 */
const common = prefix("common", {
  submit: "Submit",
  next: "Next",
  continue: "Continue",
  cancel: "Cancel",
});

export const en = {
  ...common,
  ...feedbackForm,
};
