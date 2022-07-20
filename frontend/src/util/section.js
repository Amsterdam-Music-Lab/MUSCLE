 // Get a section url from given (nested) action
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
