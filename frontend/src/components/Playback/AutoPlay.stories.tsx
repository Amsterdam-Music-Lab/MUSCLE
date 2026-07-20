import AutoPlay from './Autoplay';

import music from "../../stories/assets/music.ogg";

export default {
    title: 'Playback/AutoPlay',
    component: AutoPlay,
    argTypes: {
        instruction: { control: 'text' },
        sections: { control: 'array' }, 
        showAnimation: { control: 'boolean' },
        playSection: { action: 'playSection' },
        startedPlaying: { action: 'startedPlaying' },
        finishedPlaying: { action: 'finishedPlaying' },
        responseTime: { control: 'number' },
        className: { control: 'text' },
    },
    decorators: [
        (Story) => (
            <div className='aha__trial' style={{ padding: '3rem', background: '#333' }}>
                <Story />
            </div>
        ),
    ],
} as Meta;

const Template: Story = (args) => <AutoPlay {...args} />;

export const Default = Template.bind({});
Default.args = {
    instruction: 'Listen to the audio',
    showAnimation: true,
    responseTime: 50,
    className: '',
    sections: Array.from(new Array(1), (_) => { return {
        link: music,
    }}),
};

export const WithoutAnimation = Template.bind({});
WithoutAnimation.args = {
    ...Default.args,
    showAnimation: false,
};

export const LongResponseTime = Template.bind({});
LongResponseTime.args = {
    ...Default.args,
    responseTime: 200,
};

export const CustomInstruction = Template.bind({});
CustomInstruction.args = {
    ...Default.args,
    instruction: 'This is a custom instruction for the AutoPlay component',
};

export const WithCustomClassName = Template.bind({});
WithCustomClassName.args = {
    ...Default.args,
    className: 'custom-class',
};
