import type { Meta, StoryObj } from '@storybook/react';
import Social from '@/components/Social/Social';
import ISocial from '@/types/Social';

const meta: Meta<typeof Social> = {
    title: 'Social/Social',
    component: Social,
    parameters: {
        layout: 'centered',
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', padding: '1rem', backgroundColor: '#f5f5f5' }}>
                <Story />
            </div>
        ),
    ],
};

export default meta;
type Story = StoryObj<typeof Social>;

const defaultSocialProps: ISocial = {
    channels: ['facebook', 'twitter', 'whatsapp', 'weibo', 'share', 'clipboard'],
    url: 'https://example.com/share',
    content: 'Check out this awesome content!',
    tags: ['storybook', 'testing', 'react'],
};

export const AllChannels: Story = {
    args: {
        social: defaultSocialProps,
    },
};

export const SocialMediaOnly: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            channels: ['facebook', 'twitter', 'whatsapp', 'weibo'],
        },
    },
};

export const MinimalChannels: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            channels: ['facebook', 'twitter'],
        },
    },
};

export const SystemShareOnly: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            channels: ['share', 'clipboard'],
        },
    },
};

export const CustomContent: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            content: '🎉 Amazing news! Join us for this special event!',
            tags: ['event', 'special', 'celebration'],
        },
    },
};

export const LongUrl: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            url: 'https://example.com/very/long/url/with/multiple/parameters?param1=value1&param2=value2&param3=value3',
        },
    },
};

export const NoTags: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            tags: [],
        },
    },
};

export const SingleChannel: Story = {
    args: {
        social: {
            ...defaultSocialProps,
            channels: ['facebook'],
        },
    },
};
