import Block from "./Block";
import Theme from "./Theme";

export interface Consent {
    text: string;
    title: string;
    confirm: string;
    deny: string;
    view: 'CONSENT';
}

export interface SocialMediaConfig {
    tags: string[];
    url: string;
    content: string;
    channels: string[];
}

export default interface ExperimentCollection {
    slug: string;
    name: string;
    description: string;
    dashboard: Block[];
    nextBlock: Block | null;
    aboutContent: string;
    consent?: Consent;
    theme?: Theme;
    totalScore: number;
    socialMediaConfig?: SocialMediaConfig;
}
