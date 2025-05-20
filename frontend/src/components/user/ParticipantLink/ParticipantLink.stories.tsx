/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ParticipantLink from "./ParticipantLink";

export default {
  title: "User/ParticipantLink",
  component: ParticipantLink,
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#eee",
          padding: "3rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const Default = {
  args: {},
};
