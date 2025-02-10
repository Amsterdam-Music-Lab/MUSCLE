import ListenFeedback from "../components/Listen/ListenFeedback";

export default {
    title: "Listen/ListenFeedback",
    component: ListenFeedback,
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
        instruction: "Did you hear the audio?",
        duration: 10,
        onFinish: () => {
            alert("Finished listening");
        },
        buttons: {
            no: "No",
            yes: "Yes",
        },
        onNoClick: () => {
            alert("No clicked");
        },
        onYesClick: () => {
            alert("Yes clicked");
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
        color: "green",
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

export const WithoutButtons = {
    args: {
        ...Default.args,
        buttons: undefined,
        onNoClick: undefined,
        onYesClick: undefined,
    },
    decorators: [getDecorator],
};
