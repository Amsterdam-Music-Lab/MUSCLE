import Explainer from "../components/Explainer/Explainer";

export default {
    title: "Explainer/Explainer",
    component: Explainer,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        instruction: "This is the instruction",
        button_label: "Next",
        steps: [
            { number: 1, description: "This is the first step" },
            { number: 2, description: "This is the second step" },
            { number: 3, description: "This is the third step" },
        ],
        onNext: () => {
            console.log("Next button clicked");
        },
        timer: null,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithOnClick = {
    args: {
        instruction: "This is the instruction",
        button_label: "Next",
        steps: [
            { number: 1, description: "This is the first step" },
            { number: 2, description: "This is the second step" },
            { number: 3, description: "This is the third step" },
        ],
        onNext: () => alert("Next button clicked"),
        timer: null,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const WithThreeSecondTimer = {
    args: {
        instruction: "This is the instruction",
        button_label: "Next",
        steps: [
            { number: 1, description: "This is the first step" },
            { number: 2, description: "This is the second step" },
            { number: 3, description: "This is the third step" },
        ],
        onNext: () => alert("Next button clicked / timer expired after 3 seconds"),
        timer: 3000,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
