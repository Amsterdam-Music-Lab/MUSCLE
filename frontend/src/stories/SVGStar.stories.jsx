import SVGStar from "@/components/SVG/SVGStar";

export default {
    title: "SVG/Star",
    component: SVGStar,
    parameters: {
        layout: "fullscreen",
    },
};

const decorator = (Story) => (
    <div style={{ padding: "1rem", background: "#f5f5f5" }}>
        <Story />
    </div>
);

export const Default = {
    args: {
        size: 100
    },
    decorators: [decorator]
};

export const ManyPoints = {
    args: {
        size: 100,
        numPoints: 8
    },
    decorators: [decorator]
};

export const LowSharpness = {
    args: {
        size: 100,
        sharpness: 0.3
    },
    decorators: [decorator]
};


export const StarSize = {
    args: {
        size: 100,
        starSize: .5
    },
    decorators: [decorator]
};

export const NoCircle = {
    args: {
        size: 100,
        sharpness: 0.3,
        showCircle: false,
    },
    decorators: [decorator]
};

export const Green = {
    args: {
        size: 100,
        fill: "#008800",
    },
    decorators: [decorator]
};

export const GreenGradientYellowStroke = {
    args: {
        size: 100,
        color1: "#006600",
        color2: "#00dd00",
        circleStroke: "#ffff00cc",
        circleStrokeWidth: .15,
    },
    decorators: [decorator]
};