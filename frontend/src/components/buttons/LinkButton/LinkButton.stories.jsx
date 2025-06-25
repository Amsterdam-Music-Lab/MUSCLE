/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import LinkButton from "./LinkButton";

export default {
  title: "Design System/Buttons/LinkButton",
  component: LinkButton,
};

export const ExternalLink = {
  args: {
    children: "Google",
    link: "https://google.com",
  },
};

export const InternalLink = {
  args: {
    children: "Google",
    link: "/",
  },
};

export const NoLink = {
  args: {
    children: "Google",
    onClick: () => {
      window.alert("Click!");
    },
  },
};

export const Size = {
  args: {
    children: "Google",
    link: "/",
    size: "lg",
    variant: "secondary",
  },
};
