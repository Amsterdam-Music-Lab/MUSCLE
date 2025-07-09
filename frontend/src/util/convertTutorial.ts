import { type Tutorial } from "@/types/tutorial";

/**
 * Utility that creates a proper Tutorial instance from a tutorial returned
 * by the backend.
 */
export default function convertTutorial(tutorial: { [key: string]: string }) {
  const tutorialObj: Tutorial = { steps: [] };
  if (tutorial) {
    Object.keys(tutorial).forEach((id) => {
      const step = { id, content: tutorial[id] };
      tutorialObj.steps.push(step);
    });
  }
  return tutorialObj;
}
