import { BrowserRouter as Router } from "react-router-dom";

import ExperimentDashboard from "../components/Experiment/ExperimentDashboard/ExperimentDashboard";

export default {
    title: "Experiment/ExperimentDashboard",
    component: ExperimentDashboard,
    parameters: {
        layout: "fullscreen",
        docs: {
            description: {
                component: "This story shows the Experiment Dashboard with several blocks",
                story: "This story shows the component with the default props.",
            },
        },
    },
};

const TestData = {
    slug: 'my-experiment',
    name: 'My Experiment',
    description: 'This is the experiment description',
    dashboard: [
        {
            slug: 'first-block',
            name: 'First block',
            description: 'Description of the first block',
            image: {
                file: "/images/experiments/visual-matching-pairs/chimp.jpg",
            }
        }, {
            slug: 'second-block',
            name: 'Second block',
            description: 'Description of the second block',
            image: {
                file: "/images/experiments/visual-matching-pairs/pangolin.jpg",
            }
        } 
    ],
    nextBlock: {
        slug: 'first-block',
        name: 'First block'
    },
    aboutContent: 'This is some content for the about page',
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
    args: {experiment: getExperimentData()}
};

export const WithHeader = {
    decorators: [defaultDecorator],
    args: {experiment: getExperimentData({theme: {
            colorPrimary: "#39d7b8",
            header: {
            nextBlockButtonText: "Next",
            aboutButtonText: "About",
            score: {
                scoreClass: "platinum",
                scoreLabel: "42 points!",
            }
        }
    }})}
}
