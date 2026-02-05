import Block from "./Block";
import Theme from "./Theme";

import IButton from "@/types/Button";

export interface Consent {
    text: string;
    title: string;
    confirmButton: IButton;
    denyButton: IButton;
    view: 'CONSENT';
}

export interface SocialMediaConfig {
    tags: string[];
    url: string;
    content: string;
    channels: Array<'facebook' | 'whatsapp' | 'twitter' | 'weibo' | 'share' | 'clipboard'>;
}

export default interface Experiment {
    slug: string;
    name: string;
    description: string;
    dashboard: Block[];
    nextBlock: Block | null;
    aboutContent: string;
    consent?: Consent;
    theme?: Theme;
    accumulatedScore: number;
    playedSessions: number;
    socialMediaConfig?: SocialMediaConfig;
}
