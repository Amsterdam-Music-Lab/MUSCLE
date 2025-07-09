/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import ConsentView from "./ConsentView";
import { NarrowLayout } from "@/components/layout";

type Story = StoryObj<typeof ConsentView>;

const decorator = (StoryComponent: Story) => (
  <NarrowLayout>
    <StoryComponent />
  </NarrowLayout>
);

export default {
  title: "App/Views/ConsentView",
  component: ConsentView,
  decorators: [decorator],
} as Meta<typeof ConsentView>;

export const Default = {
  args: {
    experimentSlug: "experiment-slug",
    text: "This is the text",
    onConfirm: () => {
      console.log("Next button clicked");
    },
    consentHtml:
      "<p>This is the ConsentView component's text.</p><p>It can contain lists, headings, bold, italic and underlined text, you name it!</p><ul><li><b>Item 1</b></li><li><i>Item 2</i></li><li><u>Item 3</u></li></ul>",
  },
  decorators: [],
};

export const CustomLabels = {
  args: {
    ...Default.args,
    title: "Please give informed consent",
    confirmLabel: "I give consent",
    denyLabel: "I do not give consent",
  },
  decorators: [],
};

const lipsum =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec interdum lacus sed placerat semper. Suspendisse sodales scelerisque elit, ut venenatis ipsum ultricies ut. Praesent ac mollis mi. Duis diam sem, iaculis a lectus eget, facilisis gravida est. Donec imperdiet dui vulputate tortor dapibus commodo. Praesent eros nulla, gravida vitae leo sit amet, finibus elementum velit. Nullam placerat dignissim neque. Sed libero lacus, fermentum quis pulvinar vel, sodales vitae ex. Proin vel dui purus. Vivamus fermentum urna non ipsum ultricies, eget tempor mi ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum eleifend lacus ex, vel aliquet odio imperdiet eget. Mauris quis leo accumsan, molestie est sed, aliquam ex. Integer neque quam, auctor et varius scelerisque, sodales sit amet augue. Cras eget nisl orci.";

export const LongDocument = {
  args: {
    ...Default.args,
    consentHtml: `
    <p>Dear participant,</p>

    <p>You are about to participate in a music game! It’s important that you read about the procedures before you contribute. Make sure to read the information below carefully.</p>

    <hr />

    <p class="text-muted"><strong>Information brochure for TuneTwins:</strong> Testing music memory in different cultures with a music game</p>
    
    <h3>Purpose</h3>
    <p>${lipsum}</p>

    <h3>Who can participate?</h3>
    <p>${lipsum}</p>

    <h3>More information</h3>
    <ul>
      <li>Dolor ipsum dolor sit amet</li>
      <li>Consectetur adipiscing elit</li>
      <li>Donec interdum lacus sed placerat semper</li>
      <li>Suspendisse sodales scelerisque elit</li>
      </ul>

    <h3>Procedure</h3>
    <p>${lipsum}</p>
    `,
  },
};
