/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import type { ShareConfig } from "@/types/share";
import { ExpandableButton } from "../ExpandableButton";
import ShareOptions from "./ShareOptions";

const meta: Meta<typeof ShareOptions> = {
  title: "UI/Social",
  component: ShareOptions,
  parameters: {
    layout: "centered",
  },
  decorators: [
    (Story) => (
      <div style={{ width: "100%", padding: "1rem" }}>
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof ShareOptions>;

const defaultSocialProps: ShareConfig = {
  channels: ["facebook", "twitter", "whatsapp", "weibo", "share", "clipboard"],
  url: "https://example.com/share",
  content: "Check out this awesome content!",
  tags: ["storybook", "testing", "react"],
};

export const AllChannels: Story = {
  args: {
    config: defaultSocialProps,
  },
};

export const SocialMediaOnly: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      channels: ["facebook", "twitter", "whatsapp", "weibo"],
    },
  },
};

export const MinimalChannels: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      channels: ["facebook", "twitter"],
    },
  },
};

export const SystemShareOnly: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      channels: ["share", "clipboard"],
    },
  },
};

export const CustomContent: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      content: "🎉 Amazing news! Join us for this special event!",
      tags: ["event", "special", "celebration"],
    },
  },
};

export const LongUrl: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      url: "https://example.com/very/long/url/with/multiple/parameters?param1=value1&param2=value2&param3=value3",
    },
  },
};

export const NoTags: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      tags: [],
    },
  },
};

export const SingleChannel: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      channels: ["facebook"],
    },
  },
};

export const Expandable: Story = {
  args: {
    config: {
      ...defaultSocialProps,
      channels: ["facebook", "twitter", "whatsapp", "weibo"],
    },
  },
  decorators: [
    (Story) => (
      <div style={{ width: "100%", padding: "1rem" }}>
        <ExpandableButton title="Share" rounded={true}>
          <Story />
        </ExpandableButton>
      </div>
    ),
  ],
};
