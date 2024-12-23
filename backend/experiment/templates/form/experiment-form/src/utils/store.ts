import { StateCreator, create } from "zustand";

import { Experiment } from "../types/types";

interface ExperimentSlice {
  experiments: Experiment[];
  experiment?: Experiment;
  setExperiments: (experiments: Experiment[]) => void;
  setExperiment: (experiment: Experiment) => void;
}

const createExperimentSlice: StateCreator<ExperimentSlice> = (set) => ({
  experiments: [],
  experiment: undefined,
  setExperiments: (experiments) => set(() => ({ experiments })),
  setExperiment: (experiment) => set(() => ({ experiment })),
});

export const useBoundStore = create<ExperimentSlice>((...args) => ({
  ...createExperimentSlice(...args),
}));

export default useBoundStore;
