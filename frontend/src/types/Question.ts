export enum QuestionViews {
    AUTOCOMPLETE = "AUTOCOMPLETE",
    BUTTON_ARRAY = "BUTTON_ARRAY",
    CHECKBOXES = "CHECKBOXES",
    DROPDOWN = "DROPDOWN",
    NUMBER = "NUMBER",
    RADIOS = "RADIOS",
    RANGE = "RANGE",
    STRING = "STRING",
    TEXT_RANGE = "TEXT_RANGE",
}

export interface Choice {
    value: string | number;
    label: string;
    color?: string;
}

export default interface Question {
    key: string;
    text: string;
    view: QuestionViews;
    value?: any;
    style?: any;
    explainer?: string;
    expected_response?: string;
    choices?: Choice[];
    minValues?: number;
    minValue?: number;
    maxValue?: number;
    maxLength?: number;
    resultId?: number;
}
