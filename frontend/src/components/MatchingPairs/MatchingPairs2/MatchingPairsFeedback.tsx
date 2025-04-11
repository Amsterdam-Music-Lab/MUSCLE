import classNames from "classnames";
import { GameState } from "./useMatchingPairs";

export interface FeedbackState {
  content?: (string | React.ReactNode)[];
  className?: string;
}

export type FeedbackConfig = Record<GameState, FeedbackState>;

export const defaultFeedbackConfig: FeedbackConfig = {
  [GameState.DEFAULT]: {
    content: ["Pick a card..."],
  },
  [GameState.FIRST_CARD_SELECTED]: {
    content: ["Pick another card..."],
  },
  [GameState.COMPLETED_LUCKY_MATCH]: {
    content: ["Lucky guess!", "Lucky you!", "This is your lucky day!"],
    className: "fblucky",
  },
  [GameState.COMPLETED_MEMORY_MATCH]: {
    content: ["Well done!", "Good job!", "Nice!", "Excellent!"],
    className: "fbmemory",
  },
  [GameState.COMPLETED_NO_MATCH]: {
    content: ["No match, try again!"],
    className: "fbnomatch",
  },
  [GameState.COMPLETED_MISREMEMBERED]: {
    content: ["Nope, that's no match..."],
    className: "fbmisremembered",
  },
  [GameState.TURN_COMPLETED]: {},
  [GameState.BOARD_COMPLETED]: {},
};

interface MatchingPairsFeedbackProps {
  gameState: GameState;
  score: number;
  total?: number;
  config?: FeedbackConfig;
}

export default function MatchingPairsFeedback({
  gameState = GameState.DEFAULT,
  score,
  total,
  config = defaultFeedbackConfig,
}: MatchingPairsFeedbackProps) {
  const opts = config[gameState];
  const feedbackClass = opts.className ?? "";
  const contentList = opts.content ?? [];
  const randomIdx = Math.floor(Math.random() * contentList.length);
  const content = contentList[randomIdx];
  return (
    <div
      className={classNames(
        "matching-pairs__score-feedback",
        "d-flex",
        "flex-column",
        "justify-content-center"
      )}
    >
      {total && (
        <>
          <div className="label pb-2 d-none d-md-inline-block">Total score</div>
          <div
            data-testid="score"
            className={`matching-pairs__score ${
              total === 0 ? "zero" : total > 0 ? "positive" : "negative"
            }`}
          >
            <span className="value">
              <span className="sign">{total >= 0 ? "" : "-"}</span>
              {Math.abs(total)}
            </span>
            <span className="points">points</span>
          </div>
        </>
      )}

      <div
        className={classNames(
          "matching-pairs__feedback",
          "pt-2",
          feedbackClass
        )}
        style={{ minHeight: "4em" }}
      >
        <span className="text">{content}</span>{" "}
        {feedbackClass !== "" && (
          <span className="font-weight-bold">
            {score === 0
              ? "You got 0 points."
              : score > 0
              ? `+${score} points`
              : `${score} points`}
          </span>
        )}
      </div>
    </div>
  );
}
