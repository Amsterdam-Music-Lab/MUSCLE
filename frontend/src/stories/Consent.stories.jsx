import Consent from "../components/Consent/Consent";

const defaultArgs = {
    title: "This is the title",
    text: "This is the text",
    onNext: () => {
        console.log("Next button clicked");
    },
    confirm: "Confirm",
    deny: "Deny",
    block: {
        slug: "experiment-slug",
    },
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
    args: {
        ...getArgs(),
        title: "This is the Consent component's title",
        text: "<h2>This is the Consent component's text</h2><p>It can contain lists, headings, bold, italic and underlined text, you name it!</p><ul><li><b>Item 1</b></li><li><i>Item 2</i></li><li><u>Item 3</u></li></ul>",
        onNext: () => {
            console.log("On next triggered");
        },
        confirm: "Confirm",
        deny: "Deny",
        block: {
            slug: "experiment-slug",
        },
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
