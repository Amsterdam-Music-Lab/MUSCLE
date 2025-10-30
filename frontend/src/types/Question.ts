export enum QuestionViews {
    AUTOCOMPLETE = "AUTOCOMPLETE",
    BUTTON_ARRAY = "BUTTON_ARRAY",
    CHECKBOXES = "CHECKBOXES",
    DROPDOWN = "DROPDOWN",
    ICON_RANGE = "ICON_RANGE",
    NUMBER = "NUMBER",
    RADIOS = "RADIOS",
    RANGE = "RANGE",
    STRING = "STRING",
    TEXT_RANGE = "TEXT_RANGE",
}

export default interface Question {
    key: string;
    text: string;
    view: QuestionViews;
    value?: any;
    style?: any;
    explainer?: string;
    expected_response?: string;
    choices?: { [key: string]: string };
    submits?: boolean;
    is_skippable?: boolean;
    min_values?: number;
    min_value?: number;
    max_value?: number;
    max_length?: number;
    input_type?: 'number' | 'text';
    result_id?: number;
}
