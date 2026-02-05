import Consent from "../components/Consent/Consent";
import useBoundStore from "@/util/stores";

const theme = { colorPositive: '#00b612', colorNegative: '#fa5577', colorGrey: '#bdbebf'};

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme(theme);
};

const defaultArgs = {
    title: "This is the title",
    text: "This is the text",
    onNext: () => {
        console.log("Next button clicked");
    },
    confirmButton: {
        label: "Confirm",
        color: "colorPositive"
    },
    denyButton: {
        label: "Deny",
        color: "colorNegative"
    },
    experiment: {
        slug: "experiment-slug",
        theme: theme
    }
};

const getArgs = (args = {}) => ({ ...defaultArgs, ...args });

export default {
    title: "Consent/Consent",
    component: Consent,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: defaultArgs,
    decorators: [
        (Story) => {
            StoreDecorator(); 
            return (
                <div
                    style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
                >
                    <Story />
                </div>
            )
        }
    ],
};
