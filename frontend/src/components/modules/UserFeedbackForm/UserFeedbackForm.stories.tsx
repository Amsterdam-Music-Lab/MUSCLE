/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import UserFeedbackForm from "./UserFeedbackForm";

export default {
  title: "Modules/User/UserFeedbackForm",
  component: UserFeedbackForm,
};

export const Default = {
  args: {
    blockSlug: "test",
    participant: "test",
    feedbackInfo: {
      header: "Feedback",
      button: "Submit",
      thank_you: "Thank you for your feedback!",
      contact_body:
        '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
    },
    inline: true,
  },
};

export const Vertical = {
  args: {
    blockSlug: "test",
    participant: "test",
    feedbackInfo: {
      header: "Feedback",
      button: "Submit",
      thank_you: "Thank you for your feedback!",
      contact_body:
        '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
    },
    inline: false,
  },
};
