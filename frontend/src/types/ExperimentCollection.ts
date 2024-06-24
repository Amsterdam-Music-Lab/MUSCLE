import Experiment from "./Block";
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
    nextExperiment: Experiment | null;
    aboutContent: string;
    consent?: Consent;
    theme?: Theme;
    totalScore: Number;
}
