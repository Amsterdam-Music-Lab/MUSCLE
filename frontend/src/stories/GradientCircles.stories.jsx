import GradientCircles from "@/components/GradientCircles/GradientCircles";

export default {
    title: "SVG/GradientCircles",
    component: GradientCircles,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {};

export const Blurred = {
    args: {
        blur: 30
    },
};

export const Aurora = {
    args: {
        blur: 30,
        numCircles: 100,
        animate: true,
        color1: "#000066",
        color2: "#00ff00"
    },
};

export const YellowPink = {
    args: {
        color1: '#FFB14C',
        color2: '#D843E2',
        gradientOffset: 0.35,
        animate: true,
        numCircles: 30
    },
};

export const RadiusAndDuration = {
    args: {
        animate: true,
        numCircles: 4,
        minRadiusFactor: .01,
        meanDuration: 2,
    },
};

