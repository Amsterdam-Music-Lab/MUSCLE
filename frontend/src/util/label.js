import { romanNumeral } from "./roman";

export const LABEL_NUMERIC = "NUMERIC";
export const LABEL_ALPHABETIC = "ALPHABETIC";
export const LABEL_CUSTOM = "CUSTOM";
export const LABEL_ROMAN = "ROMAN";

/**
 * @deprecated This function is deprecated and will be removed in the future.
 * See also https://github.com/Amsterdam-Music-Lab/MUSCLE/pull/640
 * Get a player label, based on index, labelstyle and customLabels
 */
export const getPlayerLabel = (index, labelStyle, customLabels) => {
    index = parseInt(index);

    switch (labelStyle) {
        case LABEL_NUMERIC:
            return parseInt(index) + 1;
        case LABEL_ALPHABETIC:
            return String.fromCharCode(65 + index);
        case LABEL_ROMAN:
            return romanNumeral(index + 1);
        default:
            return customLabels[index] || "";
    }
};

export const renderLabel = (label, size="fa-lg") => {
    if (!label) return label
    if (label.startsWith('fa-')) return <span className={`fa-solid ${label} ${size}`}></span>
    else return label
}
