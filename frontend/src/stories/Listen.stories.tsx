import Listen from "../components/Listen/Listen";

export default {
    title: "Listen/Listen",
    component: Listen,
    parameters: {
        layout: "fullscreen",
    },
};

const getDecorator = (Story) => (
    <div style={{ width: "100%", height: "100vh", backgroundColor: "#ddd", padding: "1rem" }}>
        <Story />
    </div>
);

export const Default = {
    args: {
        instruction: "Listen to the audio",
        duration: 10,
        onFinish: () => {
            alert("Finished listening");
        },
    },
    decorators: [getDecorator],
};

export const WithCircleContent = {
    args: {
        ...Default.args,
        circleContent: <span>🎵</span>,
    },
    decorators: [getDecorator],
};

export const CustomColor = {
    args: {
        ...Default.args,
        color: "blue",
    },
    decorators: [getDecorator],
};

export const NotRunning = {
    args: {
        ...Default.args,
        running: false,
    },
    decorators: [getDecorator],
};

export const CustomClassName = {
    args: {
        ...Default.args,
        className: "wide-buttons",
    },
    decorators: [getDecorator],
};
