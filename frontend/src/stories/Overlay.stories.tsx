import type { Meta, StoryObj } from '@storybook/react';
import Overlay from '@/components/Overlay/Overlay';
import { useState } from 'react';
import Button from '@/components/Button/Button';

const meta: Meta<typeof Overlay> = {
    title: 'Overlay/Overlay',
    component: Overlay,
    parameters: {
    },
    decorators: [
        (Story, context) => {
            const [isOpen, setIsOpen] = useState(false);

            return (
                <div style={{ width: '100%', minHeight: '100vh', height: '100%', backgroundColor: '#f5f5f5', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    <Button
                        onClick={() => setIsOpen(true)}
                        title="Open Overlay"
                        className='primary'
                        clickOnce={false}
                    />

                    <Story
                        args={{
                            ...context.args,
                            isOpen,
                            onClose: () => setIsOpen(false),
                        }}
                    />
                </div>
            )
        }
    ],
};

export default meta;
type Story = StoryObj<typeof Overlay>;

const defaultOverlayProps = {
    isOpen: false,
    title: 'Tutorial',
    content: 'This is a tutorial.',
    onClose: () => { },
};

export const Default: Story = {
    args: {
        ...defaultOverlayProps,
    },
};

export const WithLongContent: Story = {
    args: {
        ...defaultOverlayProps,
        content: (
            <div>
                <h3>Welcome to our app!</h3>
                <p>Here's how to get started:</p>
                <ol>
                    <li>First, create your profile</li>
                    <li>Then, explore our features</li>
                    <li>Finally, start creating!</li>
                </ol>
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
            </div>
        ),
    },
};

export const CustomTitle: Story = {
    args: {
        ...defaultOverlayProps,
        title: '🎉 Getting Started',
        content: 'Welcome to our awesome app!',
    },
};
