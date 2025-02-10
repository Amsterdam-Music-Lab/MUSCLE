import Circle from "../components/Circle/Circle";

export default {
    title: "Circle/Circle",
    component: Circle,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 10,
        animateCircle: true,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NoAnimation = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 10,
        animateCircle: false,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NoRunning = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 10,
        animateCircle: true,
        running: false,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NoAnimationNoRunning = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 10,
        animateCircle: false,
        running: false,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const ShortDuration = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 1,
        animateCircle: true,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const LongDuration = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 60,
        animateCircle: true,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NoDuration = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 0,
        animateCircle: true,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const ThickStroke = {
    args: {
        radius: 100,
        strokeWidth: 20,
        color: "white",
        duration: 10,
        animateCircle: true,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "100%",
                    height: "100%",
                    backgroundColor: "#666",
                    padding: "1rem",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const OnTickOnFinish = {
    args: {
        radius: 100,
        strokeWidth: 5,
        color: "white",
        duration: 2,
        animateCircle: true,
        running: true,
        onTick: (t) => console.log("Tick", t),
        onFinish: () => console.log("Finished"),
    },
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "100%",
                    height: "100%",
                    padding: "1rem",
                    color: "white",
                    backgroundColor: "#666",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                }}
            >
                <p>Check the console</p>
                <Story />
            </div>
        ),
    ],
};
