import Explainer from "../components/Explainer/Explainer";
import useBoundStore from "@/util/stores";

export default {
    title: "Explainer/Explainer",
    component: Explainer,
    parameters: {
        layout: "fullscreen",
    },
};

const getExplainerArgs = (overrides = {}) => {
    const defaultArgs = {
        instruction: "This is the instruction",
        button: {
            label: "Next",
            color: "colorPrimary"
        },
        steps: [
            { number: 1, description: "This is the first step" },
            { number: 2, description: "This is the second step" },
            { number: 3, description: "This is the third step" },
        ],
        onNext: () => {},
        timer: null,
    }
    return { ...defaultArgs, ...overrides}
}

const explainerDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorBackground: 'black', colorText: 'white', colorPrimary: '#d843e2'});
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    )
}

export const Default = {
    args: getExplainerArgs(),
    decorators: [explainerDecorator],
};

export const WithOnClick = {
    args: getExplainerArgs({onNext: () => {
        alert("Next button clicked");
    }}),
    decorators: [explainerDecorator],
};

export const WithThreeSecondTimer = {
    args: getExplainerArgs({
        timer: 3000,
    }),
    decorators: [explainerDecorator],
};
