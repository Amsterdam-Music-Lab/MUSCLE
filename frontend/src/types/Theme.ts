export interface Header {
    nextExperimentButtonText: string;
    aboutButtonText: string;
    showScore: boolean;    
};

export default interface Theme {
    backgroundUrl: string;
    bodyFontUrl: string;
    description: string;
    headingFontUrl: string;
    logoUrl: string;
    name: string;
    footer: null;
    header: Header | null;
}
