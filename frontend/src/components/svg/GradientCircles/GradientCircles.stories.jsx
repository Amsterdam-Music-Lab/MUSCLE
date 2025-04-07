import { GradientCircles } from "@/components/svgs";

export default {
    title: "SVG/GradientCircles",
    component: GradientCircles,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"]
};

const decorator = (Story) => (
    <div style={{ minHeight: "300px" }}>
        <Story />
    </div>
);

export const Default = {
    decorators: [decorator]
};

export const Blurred = {
    args: {
        blur: 30
    },
    decorators: [decorator]
};

export const Aurora = {
    args: {
        blur: 30,
        numCircles: 100,
        animate: true,
        fill: {
            startColor: "#000066",
            endColor: "#00ff00"
        },
    },
    decorators: [decorator]
};

export const YellowPink = {
    args: {
        fill: { 
            startColor: "#FFB14C",
            endColor: "#D843E2",
            scale: 1.3
        },
        animate: true,
        numCircles: 30
    },
    decorators: [decorator]
};

export const RadiusAndDuration = {
    args: {
        animate: true,
        numCircles: 4,
        minRadiusFactor: .01,
        meanDuration: 2,
    },
    decorators: [decorator]
};

