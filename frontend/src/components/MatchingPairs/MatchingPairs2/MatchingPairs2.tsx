import { scoreIntermediateResult } from "@/API";
import useBoundStore from "@/util/stores";

import { Card } from "@/types/Section";
import Session from "@/types/Session";
import Participant from "@/types/Participant";

import { ScoreFeedbackDisplay } from "@/types/Playback";
import MatchingPairsBoard from "./MatchingPairsBoard";
import MatchingPairsFeedback from "./MatchingPairsFeedback";
import TutorialOverlay from "./TutorialOverlay";
import { useTutorial } from "./useTutorial";
import { useMatchingPairs, isTurnComplete } from "./useMatchingPairs";
import { processTutorial } from "./utils";

import styles from "./MatchingPairs2.module.scss";

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
  playSection,
  sections: initialCards,
  playerIndex,
  showAnimation,
  finishedPlaying,
  submitResult,
  tutorial = {},
  type,
}: MatchingPairsProps) => {
  // Variables bound to global store
  const block = useBoundStore((s) => s.block);
  const participant = useBoundStore((s) => s.participant) as Participant;
  const session = useBoundStore((s) => s.session) as Session;

  // Function that effectively compares the cards.
  const compareCards = async (
    card1: Card,
    card2: Card,
    { startOfTurn }
  ): Promise<number | void> => {
    const scoreResponse = await scoreIntermediateResult({
      session,
      participant,
      result: {
        start_of_turn: startOfTurn,
        first_card: card1,
        second_card: card2,
      },
    });
    if (!scoreResponse) throw new Error();
    return scoreResponse.score;
  };

  // Tutorial
  let { showStep, completeStep, getActiveStep } = useTutorial({
    tutorial: processTutorial(tutorial),
  });
  const activeTutorialStep = getActiveStep();

  // Component state
  const { gameState, cards, score, total, finishTurn, flipCard } =
    useMatchingPairs({
      initialCards,
      initialScore: block?.bonus_points || 0,
      compareCards,
      onFinishTurn: finishedPlaying,
      onFinishGame: () => submitResult({}),
      onMatch: showStep,
    });

  // Check if the user is in between turns to show the hidden overlay
  const inBetweenTurns = Boolean(cards.filter((s) => s.turned).length === 2);

  return (
    <div
      className={styles.matchingPairs}
      onClick={() => {
        if (isTurnComplete(gameState)) finishTurn();
      }}
    >
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
            checkMatchingPairs={flipCard}
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
