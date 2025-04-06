import SVGDot from "@/components/SVG/SVGDot";

export default {
    title: "SVG/Dot",
    component: SVGDot,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"]
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


export const Gradient = {
    args: {
        size: 100,
        fill: { startColor: "#ff0000", endColor: "#0000ff", angle: 30 }
    },
    decorators: [decorator]
};
