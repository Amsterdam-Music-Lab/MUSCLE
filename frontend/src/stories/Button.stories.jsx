import Button from "../components/Button/Button";
import useBoundStore from "@/util/stores";

const ButtonDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2', colorSecondary: '#39d7b8', colorPositive: '#00b612', colorNegative: '#fa5577', colorNeutral1: '#ffb14c'});
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    );
}

export default {
    title: "Button/Button",
    component: Button,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: "colorPrimary"
    },
    decorators: [ButtonDecorator]
};

export const Inactive = {
    args: {
        label: "Click me",
        onClick: () => {},
        disabled: true,
    },
    decorators: [ButtonDecorator],
};

export const WithValue = {
    args: {
        label: "Click me",
        onClick: () => {},
        value: "value",
    },
    decorators: [ButtonDecorator],
};

export const Primary = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorPrimary'
    },
    decorators: [ButtonDecorator]
};

export const Secondary = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorSecondary'
    },
    decorators: [ButtonDecorator],
};

export const Positive = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorPositive'
    },
    decorators: [ButtonDecorator]
};

export const Negative = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorNegative',
    },
    decorators: [ButtonDecorator],
};

export const Neutral = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorNeutral1',
    },
    decorators: [ButtonDecorator],
};

export const WithAlternativePadding = {
    args: {
        label: "Click me",
        onClick: () => {},
        padding: "px-2",
    },
    decorators: [ButtonDecorator],
};

export const WithOnClick = {
    args: {
        label: "Click me",
        onClick: () => alert("Clicked!"),
    },
    decorators: [ButtonDecorator],
};

export const Link = {
    args: {
        label: "Click me",
        link: "https://www.example.com"
    },
    decorators: [ButtonDecorator]
}
