interface TimelineStep {
  image?: string;
  text?: string;
}

export interface Timeline {
  playedSessions: number;
  steps: TimelineStep[];
}