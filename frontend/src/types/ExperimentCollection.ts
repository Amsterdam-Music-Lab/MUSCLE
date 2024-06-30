import Block from "./Block";
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
    dashboard: Block[];
    nextExperiment: Block | null;
    aboutContent: string;
    consent?: Consent;
    theme?: Theme;
    totalScore: number;
}
