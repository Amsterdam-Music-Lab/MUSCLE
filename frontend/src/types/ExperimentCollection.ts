import Experiment from "./Experiment";

export default interface Consent {
    text: string;
    title: string;
    confirm: string;
    deny: string;
    render_format: string;
    view: 'CONSENT'
}

export default interface ExperimentCollection {
    slug: string;
    name: string;
    description: string;
    consent: Consent;
    info: string;
    dashboard: Experiment[];
    next_experiment: Experiment | null;
    about_content: string;
    debrief: string;
}
