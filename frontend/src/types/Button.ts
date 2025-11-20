enum buttonColorOptions {
    PRIMARY = 'colorPrimary',
    SECONDARY = 'colorSecondary',
    POSITIVE = 'colorPositive',
    NEGATIVE = 'colorNegative',
    NEUTRAL1 = 'colorNeutral1',
    NEUTRAL2 = 'colorNeutral2',
    NEUTRAL3 = 'colorNeutral3',
    GREY = 'colorGrey',
}

export default interface IButton {
    label: string;
    color: buttonColorOptions;
    link?: string;
}