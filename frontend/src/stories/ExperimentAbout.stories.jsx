import { BrowserRouter as Router } from "react-router-dom";

import ExperimentAbout from "../components/Experiment/ExperimentAbout/ExperimentAbout";

export default {
    title: "Experiment/ExperimentAbout",
    component: ExperimentAbout,
    parameters: {
        layout: "fullscreen",
        docs: {
            description: {
                component: "This story shows the Experiment About page",
                story: "This story shows the component with the default props.",
            },
        },
    },
};

const TestData = {
    slug: "my-experiment",
    name: "My Experiment",
    backButtonText: "Back",
    aboutContent: "<h1>This is some content for the about page</h1><div>With some more text</div>",
    theme: {
        colorPrimary: "#39d7b8"
    }
}

const getExperimentData = (overrides = {}) => {
    return {
        ...TestData,
        ...overrides
    }
}

const defaultDecorator = (Story) => (
    <div
        style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#ddd",
            padding: "1rem",
        }}
    >
        <Router>
            <Story />
        </Router>
    </div>
)

export const Default = {
    decorators: [defaultDecorator],
    args: {...getExperimentData()}
};
