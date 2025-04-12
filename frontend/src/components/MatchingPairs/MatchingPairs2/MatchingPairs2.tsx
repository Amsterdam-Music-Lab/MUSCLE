import { scoreIntermediateResult } from "@/API";
import { Card } from "@/types/Section";
import { ScoreFeedbackDisplay } from "@/types/Playback";
import MatchingPairsBoard from "./MatchingPairsBoard";
import MatchingPairsFeedback from "./MatchingPairsFeedback";
import TutorialOverlay from "./TutorialOverlay";
import { useTutorial } from "./useTutorial";
import {
  useMatchingPairs,
  CompareCardsProps,
  ComparisonResult,
} from "./useMatchingPairs";
import { processTutorial } from "./utils";

import styles from "./MatchingPairs2.module.scss";

// TODO
const CARD_CLASSES = {
  [ComparisonResult.NO_MATCH]: "fbnomatch",
  [ComparisonResult.LUCKY_MATCH]: "fblucky",
  [ComparisonResult.MISREMEMBERED]: "fbmisremembered",
  [ComparisonResult.MEMORY_MATCH]: "fbmemory",
};

// Function that effectively compares the cards.
const compareCards = async (
  card1: Card,
  card2: Card,
  { startOfTurn, participant, session }: CompareCardsProps
): Promise<[ComparisonResult, number] | void> => {
  const response = await scoreIntermediateResult({
    session,
    participant,
    result: {
      start_of_turn: startOfTurn,
      first_card: card1,
      second_card: card2,
    },
  });
  if (!response) throw new Error();

  switch (response.score) {
    case 0:
      return [ComparisonResult.NO_MATCH, response.score];
    case 10:
      return [ComparisonResult.LUCKY_MATCH, response.score];
    case 20:
      return [ComparisonResult.MEMORY_MATCH, response.score];
    case -10:
      return [ComparisonResult.MEMORY_MATCH, response.score];
    default:
      return;
  }
};

interface MatchingPairsProps {
  playSection: (index: number) => void;
  sections: Card[];
  playerIndex: number;
  showAnimation: boolean;
  finishedPlaying: () => void;
  scoreFeedbackDisplay?: ScoreFeedbackDisplay;
  submitResult: (result: any) => void;
  type: "visual" | "audio";
  tutorial?: { [key: string]: string };
}

const MatchingPairs2 = ({
  sections: initialCards,
  playerIndex,
  showAnimation,
  playSection,
  finishedPlaying,
  submitResult,
  tutorial = {},
  type,
}: MatchingPairsProps) => {
  // Tutorial
  let { showStep, completeStep, getActiveStep } = useTutorial({
    tutorial: processTutorial(tutorial),
  });
  const activeTutorialStep = getActiveStep();

  // Component state
  const { gameState, cards, score, total, endTurn, selectCard } =
    useMatchingPairs({
      cards: initialCards,
      compareCards,
      afterSelectPair: (result) => {
        showStep(`COMPLETED_${result}`);
      },
      onTurnEnd: () => finishedPlaying(),
      onGameEnd: () => submitResult({}),
    });

  // Check if the user is in between turns to show the hidden overlay
  const inBetweenTurns = Boolean(cards.filter((s) => s.turned).length === 2);

  return (
    <div className={styles.matchingPairs} onClick={() => endTurn()}>
      <div className={styles.mpContainer}>
        <div className={styles.mpHeader}>
          <MatchingPairsFeedback
            gameState={gameState}
            score={score}
            total={total}
          />
        </div>

        <div className={styles.mpMain}>
          <MatchingPairsBoard
            cards={cards}
            columns={4}
            playSection={playSection}
            checkMatchingPairs={selectCard}
            animate={showAnimation}
            type={type}
            playerIndex={playerIndex}
          />
        </div>
      </div>

      {activeTutorialStep && (
        <TutorialOverlay
          step={activeTutorialStep}
          style={{ display: inBetweenTurns ? "block" : "none" }}
          onClose={() => {
            finishTurn();
            completeStep(activeTutorialStep.id);
          }}
        />
      )}
    </div>
  );
};

export default MatchingPairs2;
