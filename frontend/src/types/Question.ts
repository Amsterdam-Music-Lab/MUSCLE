export enum QuestionViews {
    AUTOCOMPLETE = "AUTOCOMPLETE",
    BUTTON_ARRAY = "BUTTON_ARRAY",
    CHECKBOXES = "CHECKBOXES",
    DROPDOWN = "DROPDOWN",
    RADIOS = "RADIOS",
    RANGE = "RANGE",
    TEXT_RANGE = "TEXT_RANGE",
    ICON_RANGE = "ICON_RANGE",
    STRING = "STRING",
    NUMBER = "NUMBER"
}

export default interface Question {
    key: string;
    text: string;
    view: QuestionViews;
    value?: any;
    style?: any;
    explainer?: string;
    choices?: { [key: string]: string };
    min_values?: number;
    min_value?: number;
    max_value?: number;
    max_length?: number;
    input_type?: 'number' | 'text';
    result_id?: number;
}
