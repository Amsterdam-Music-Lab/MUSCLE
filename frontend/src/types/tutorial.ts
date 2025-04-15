/**
 * A tutorial object.
 * Note that it is not a list of steps, as this object may be extended
 * with other properties (e.g. description, title, ...)
 */
export interface Tutorial {
  /** Steps in the tutorial */
  steps: TutorialStep[];

  /** Whether to disable completed steps (default: true) */
  disableCompleted?: boolean;

  /** Allow multiple steps to be active at the same time? (default: false) */
  allowMultipleActiveSteps?: boolean;

  /** Whether to infer the order of the steps from the input (default: true) */
  inferOrder?: boolean;
}

export interface TutorialStep {
  /** A unique identifier for the step  */
  id: string;

  /** Title of the current step */
  title?: string;

  /** The content shown for this step */
  content?: string | React.ReactNode;

  /** Whether this step is visible */
  visible?: boolean;

  /** Whether this step has been completed */
  completed?: boolean;

  /** Order of the steps. */
  order?: number;
}
