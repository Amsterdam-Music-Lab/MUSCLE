import { BrowserRouter as Router } from "react-router-dom";

import Final from "./Final";
import useBoundStore from "@/util/stores";

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: "#d843e2", colorSecondary: "#39d7b8", colorGrey: '#bdbebf'});
};

export default {
    title: "Final/Final",
    component: Final,
    parameters: {
        layout: "fullscreen",
    },
};

function getFinalData(overrides = {}) {
    return {
        scores: {
            session: {
                value: 100,
                label: "points"
            },
            relative: {
                value: 66,
                label: "%"
            }
        },
        rank: {
            label: "Platinum",
            className: "platinum",
            description: `<h4>Awesome!</h4>`
        },
        finalText: `
            <p>You outperformed 66% of the players</p>

            <table>
                <tr><td>This game</td><td>100</td></tr>
                <tr><td>Personal best</td><td>120</td></tr>
                <tr><td>Average score</td><td>80</td></tr>
            </table>
        `,
        visualizationType: "cup",
        timeline: {
            playedSessions: 2,
            steps: [
                "",
                "",
                "star",
                "",
                "",
                "star",
            ]
        },
        button: {
            label: "Button",
            link: "https://www.example.com",
        },
        show_profile_link: true,
        action_texts: {
            all_experiments: "All experiments",
            profile: "Profile",
        },
        show_participant_link: true,
        participant_id_only: false,
        block: {
            identifier: "test",
        },
        participant: "test",
        onNext: () => { alert("Next"); },
        ...overrides,
    };
}

const getDecorator = (Story) => {
    StoreDecorator();
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
        >
            <Router>
                <Story />
            </Router>
        </div>
    );
}

export const Default = {
    args: getFinalData(),
    decorators: [getDecorator],
};

// with relative button.link
export const RelativeButtonLink = {
    args: getFinalData({
        button: {
            label: "Play again",
            link: "/profile",
        },
    }),
    decorators: [getDecorator],
};

// with absolute button.link
export const AbsoluteButtonLink = {
    args: getFinalData({
        button: {
            label: "Button",
            link: "https://www.example.com",
        },
    }),
    decorators: [getDecorator],
};

// without button.link
export const NoButtonLink = {
    args: getFinalData({
        button: {
            text: "Button",
            link: "",
        },
    }),
    decorators: [getDecorator],
};



// final text html test
export const FinalTextHtml = {
    args: getFinalData({
        finalText: `
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <p>Lorem ipsum dolor sit amet, <i>consectetur adipiscing elit</i>. Nullam eget nunc nec nunc. Aenean nec nunc nec nunc. <b>Curabitur nec nunc nec nunc</b>. Donec nec nunc nec nunc. Sed nec nunc nec nunc. Vestibulum</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            <ol>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ol>
            <a href="https://www.example.com">Link</a>
            <img src="https://cataas.com/cat" alt="Placeholder">
            <pre><code>console.log("Hello, world!");</code></pre>
            <pre><code>
            function sum(a, b) {
                return a + b;
            }
            </code></pre>
        `,
    }),
    decorators: [getDecorator],
};

// no percentile, text centered
export const PlainText = {
    args: getFinalData({
        percentile: undefined,
        final_text: '<center>Well done!</center>'
    }),
    decorators: [getDecorator]
}
