import Trophy from "./Trophy";

export default {
    title: "Trophy/Trophy",
    component: Trophy,
    parameters: {
        layout: "fullscreen",
    },
};

const getDecorator = (Story) => (
    <div
        style={{ width: "100%", height: "100%", backgroundColor: "#9e9fa1", padding: "1rem" }}
    >
        <Story />
    </div>
)

export const Default = {
    args: {
        className: "gold",
        label: "Gold!"
    },
    decorators: [getDecorator]
};


// silver cup
export const SilverCup = {
    args: {
        label: "Silver",
        className: "silver",
    },
    decorators: [getDecorator],
};

// bronze cup
export const BronzeCup = {
    args: {
        label: "Bronze",
        className: "bronze",
    },
    decorators: [getDecorator],
};

// plastic cup
export const PlasticCup = {
    args: {
        label: "Plastic",
        className: "plastic",
    },
    decorators: [getDecorator],
};


// diamond cup
export const DiamondCup = {
    args: {
        label: "Diamond",
        className: "diamond",
    },
    decorators: [getDecorator],
};

// platinum
export const PlatinumCup = {
    args: {
        label: "Platinum",
        className: "platinum",
    },
    decorators: [getDecorator],
};