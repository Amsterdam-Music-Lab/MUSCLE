import Histogram from "../components/Histogram/Histogram";

export default {
    title: "Histogram",
    component: Histogram,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        bars: 7,
        spacing: 6,
        interval: 100,
        running: true,
        marginLeft: 0,
        marginTop: 0,
        backgroundColor: undefined,
        borderRadius: "0.15rem",
    },
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "128px",
                    height: "128px",
                    margin: "1rem auto",
                    backgroundColor: "purple",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Random = {
    args: {
        bars: 7,
        spacing: 6,
        interval: 100,
        running: true,
        marginLeft: 0,
        marginTop: 0,
        backgroundColor: undefined,
        borderRadius: "0.15rem",
        random: true,
        interval: 150,
    },
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "128px",
                    height: "128px",
                    margin: "1rem auto",
                    backgroundColor: "purple",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};
