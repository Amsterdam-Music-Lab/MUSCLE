import Experiment from "./Experiment";
import Theme from "./Theme";

export interface Consent {
    text: string;
    title: string;
    confirm: string;
    deny: string;
    view: 'CONSENT';
}

export default interface ExperimentCollection {
    slug: string;
    name: string;
    description: string;
    dashboard: Experiment[];
    next_experiment: Experiment | null;
    about_content: string;
    consent?: Consent;
    theme?: Theme;
}
