import Experiment from "./Experiment";

export default interface ExperimentCollection {
    id: number;
    slug: string;
    name: string;
    description: string;
    dashboard: Experiment[];
    redirect_to: Experiment | null;

    // New properties that do not yet exist in the backend
    next_experiment: Experiment | null;
    about_content: string;
}