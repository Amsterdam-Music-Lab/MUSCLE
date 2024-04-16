import Experiment from "./Experiment";

export default interface ExperimentCollection {
    slug: string;
    name: string;
    description: string;
    dashboard: Experiment[];
    next_experiment: Experiment | null;
    about_content: string;
}