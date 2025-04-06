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
        fill: {
            startColor: "#000066",
            endColor: "#00ff00"
        },
    },
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
};

export const RadiusAndDuration = {
    args: {
        animate: true,
        numCircles: 4,
        minRadiusFactor: .01,
        meanDuration: 2,
    },
};

