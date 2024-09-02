/** Get a section url from given (nested) action
 * TODO: This function is not used anywhere in the codebase, should it be removed?
 */
export const getSectionUrl = (action) => {
    if (!action) {
        return "";
    }

    if (action.section && action.section.url) {
        return action.section.url;
    }

    if (action.next_round) {
        return getSectionUrl(action.next_round);
    }

    return "";
};
