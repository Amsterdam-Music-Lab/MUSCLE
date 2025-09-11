export interface ProfileData {
  messages: {
    title: string;
    summary: string;
    continue: string;
    points: string;
  };
  scores: {
    block_slug: string;
    block_name: string;
    score: number;
    date: string;
    rank: {
      class: string;
      text: string;
    };
    finished_at: string;
  }[];
}
