export interface Header {
    nextExperimentButtonText: string;
    aboutButtonText: string;
};

export interface Logo {
    href: string;
    file: string;
    alt: string;
}

export interface Footer {
    disclaimer: string;
    logos: Logo[];
    privacy: string;
}

export default interface Theme {
    backgroundUrl: string;
    bodyFontUrl: string;
    description: string;
    headingFontUrl: string;
    logoUrl: string;
    name: string;
    footer: Footer | null;
    header: Header | null;
}
