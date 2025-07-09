/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { Button } from "@/components/buttons";
import InputGroup from "./InputGroup";
import { Input } from "../Input";
import { InputLabel } from "../InputLabel";

const decorator = (Story) => (
  <div
    style={{
      padding: "1rem",
      background: "#eee",
    }}
  >
    <Story />
  </div>
);

export default {
  title: "Design System/Inputs/InputGroup",
  component: InputGroup,
  tags: ["autodocs"],
  decorators: [decorator],
};

export const SingleChild = {
  args: {
    children: (
      <>
        <Input value="test" />
      </>
    ),
  },
};

export const TwoChild = {
  args: {
    children: (
      <>
        <Input value="test" /> <Button>Submit</Button>
      </>
    ),
  },
};

export const ThreeChildren = {
  args: {
    forwardVariant: false,
    children: (
      <>
        <InputLabel htmlFor="test">Label</InputLabel>
        <Input id="test" value="test" />
        <Button>Submit</Button>
      </>
    ),
  },
};

export const ManyChildren = {
  args: {
    variant: "secondary",
    children: [
      <InputLabel htmlFor="test">Label</InputLabel>,
      <Input id="test" value="test" />,
      <InputLabel htmlFor="test">Something else</InputLabel>,
      <Button>Submit</Button>,
    ],
  },
};
