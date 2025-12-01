import Button from "../components/Button/Button";
import useBoundStore from "@/util/stores";

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2', colorSecondary: '#39d7b8', colorPositive: '#00b612', colorNegative: '#fa5577', colorNeutral1: '#ffb14c'});

    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    );
};

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
    decorators: [StoreDecorator]
};

export const Inactive = {
    args: {
        label: "Click me",
        onClick: () => {},
        disabled: true,
    },
    decorators: [StoreDecorator],
};

export const WithValue = {
    args: {
        label: "Click me",
        onClick: () => {},
        value: "value",
    },
    decorators: [StoreDecorator],
};

export const Primary = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorPrimary'
    },
    decorators: [StoreDecorator]
};

export const Secondary = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorSecondary'
    },
    decorators: [StoreDecorator],
};

export const Positive = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorPositive'
    },
    decorators: [StoreDecorator]
};

export const Negative = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorNegative',
    },
    decorators: [StoreDecorator],
};

export const Neutral = {
    args: {
        label: "Click me",
        onClick: () => {},
        color: 'colorNeutral1',
    },
    decorators: [StoreDecorator],
};

export const WithAlternativePadding = {
    args: {
        label: "Click me",
        onClick: () => {},
        padding: "px-2",
    },
    decorators: [StoreDecorator],
};

export const WithOnClick = {
    args: {
        label: "Click me",
        onClick: () => alert("Clicked!"),
    },
    decorators: [StoreDecorator],
};

export const Link = {
    args: {
        label: "Click me",
        link: "https://www.example.com"
    },
    decorators: [StoreDecorator]
}
