/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { RenderHtml } from "@/components/utils";
import FeedbackForm from "./FeedbackForm";
import { description } from "@/util/storybook";

export default {
  title: "Modules/User/FeedbackForm",
  component: FeedbackForm,
};

const mockOnSubmitSuccess = async (value) => ({ status: "ok" });
const mockOnSubmitFailure = async (value) => null;

export const Default = {
  ...description(
    "This mocks the behaviour of when the form is submitted successfully."
  ),
  args: {
    onSubmit: mockOnSubmitSuccess,
  },
};

export const SubmissionFailed = {
  ...description(
    "Type something and submit the form to see the behaviour when submission fails."
  ),
  args: { ...Default.args, onSubmit: mockOnSubmitFailure },
};

export const CustomMessages = {
  ...description(
    "The property names are shown between square brackets. You can pass any `ReactNode.`"
  ),
  args: {
    ...Default.args,
    header: "[header] Please share your feedback",
    footer: (
      <RenderHtml html='[footer] Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions' />
    ),
    thanks: "[thanks] Thank you very much for sharing your feedback!",
  },
};
