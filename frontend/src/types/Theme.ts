import Image from "./Image";

export interface ScoreDisplayConfig {
  scoreClass: string;
  scoreLabel: string;
  noScoreLabel: string;
}

export interface Header {
  nextBlockButtonText: string;
  aboutButtonText: string;
  score: ScoreDisplayConfig;
}

export interface Logo {
  href: string;
  file: string;
  alt: string;
}

// export interface Footer {
//     disclaimer: string;
//     logos: Logo[];
//     privacy: string;
// }

export default interface Theme {
  backgroundUrl: string;
  bodyFontUrl: string;
  description: string;
  headingFontUrl: string;
  logo: Image;
  name: string;
  footer: Footer | null;
  header: Header | null;
}
