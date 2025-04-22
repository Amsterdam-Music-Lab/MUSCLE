/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Tutorial, TutorialStep } from "@/types/tutorial";
import type { Card as CardData } from "@/types/Section";
import type { MatchingPairsProps as MatchingPairsInterfaceProps } from "../MatchingPairsv1/MatchingPairs";

import { useState, useEffect, useContext } from "react";
import classNames from "classnames";
import { scoreIntermediateResult } from "@/API";
import { useTutorial } from "@/hooks/useTutorial";
import { useOrientation } from "@/hooks/OrientationProvider";
import { SquareLayout } from "@/components/layout";
import {
  Timeline,
  getTimeline,
  ScoreFeedback,
  TutorialMessage,
} from "@/components/game";
import {
  useMatchingPairs,
  CompareCardsProps,
  MPCard as GenericMPCard,
  MPStates,
  UseMatchingPairsProps,
} from "../useMatchingPairs";
import { convertTutorial } from "../utils";
import { Board } from "../Board";
import { VisualCard } from "../VisualCard";
import { AudioCard } from "../AudioCard";
import styles from "./MatchingPairs.module.scss";
import { Logo } from "@/components/svg";

interface MPCard extends GenericMPCard {
  playing?: boolean;
  className?: string;
  data: CardData;
}

enum GameState {
  DEFAULT = "DEFAULT",
  CARD_SELECTED = "CARD_SELECTED",
  COMPLETED_LUCKY_MATCH = "COMPLETED_LUCKY_MATCH",
  COMPLETED_MEMORY_MATCH = "COMPLETED_MEMORY_MATCH",
  COMPLETED_NO_MATCH = "COMPLETED_NO_MATCH",
  COMPLETED_MISREMEMBERED = "COMPLETED_MISREMEMBERED",
  GAME_END = "GAME_END",
}

enum ComparisonResult {
  LUCKY_MATCH = "LUCKY_MATCH",
  MEMORY_MATCH = "MEMORY_MATCH",
  NO_MATCH = "NO_MATCH",
  MISREMEMBERED = "MISREMEMBERED",
}

const CARD_CLASSES = {
  [ComparisonResult.NO_MATCH]: styles.nomatch,
  [ComparisonResult.LUCKY_MATCH]: styles.lucky,
  [ComparisonResult.MISREMEMBERED]: styles.misremembered,
  [ComparisonResult.MEMORY_MATCH]: styles.memory,
};

const FEEDBACK = {
  [GameState.DEFAULT]: {
    content: ["Pick a card..."],
  },
  [GameState.CARD_SELECTED]: {
    content: ["Pick another card..."],
  },
  [GameState.COMPLETED_LUCKY_MATCH]: {
    content: ["Lucky guess!", "Lucky you!", "This is your lucky day!"],
  },
  [GameState.COMPLETED_MEMORY_MATCH]: {
    content: ["Well done!", "Good job!", "Nice!", "Excellent!"],
  },
  [GameState.COMPLETED_NO_MATCH]: {
    content: ["No match, try again!"],
  },
  [GameState.COMPLETED_MISREMEMBERED]: {
    content: ["Nope, that's no match..."],
  },
  [GameState.GAME_END]: {},
};

const TUTORIAL = {
  steps: [{ id: "start", content: "Welcome to the game!" }],
};

const DEFAULT_TIMELINE = getTimeline({
  symbols: [
    "dot",
    "dot",
    "star-4",
    "dot",
    "dot",
    "star-5",
    "dot",
    "dot",
    "star-6",
    "dot",
    "dot",
    "star-7",
  ],
});

// TODO: Not ideal that the comparison result is based on the score.
// But in backend/experiment/rules/matching_pairs.py the function calculate_intermediate_score
// does in fact also produce a string given_response; can't this be sent to the client as well?

/**
 * Function that compares two cards and returns the result of the comparison.
 * In this case, it sends a request to the server to get the score. The result
 * of the comparison is determined based on the score returned by the server.
 */
const compareCards = async (
  card1: MPCard,
  card2: MPCard,
  { startOfTurn, participant, session }: CompareCardsProps<MPCard>
): Promise<[ComparisonResult, number] | void> => {
  const response = await scoreIntermediateResult({
    session,
    participant,
    result: {
      start_of_turn: startOfTurn,
      first_card: { ...card1.data, seen: card1.hasBeenSelected },
      second_card: { ...card2.data, seen: card2.hasBeenSelected },
      // What was this used for?
      overlay_was_shown: false,
    },
  });
  if (!response) throw new Error();
  switch (response.score) {
    case 20:
      return [ComparisonResult.MEMORY_MATCH, response.score];
    case 10:
      return [ComparisonResult.LUCKY_MATCH, response.score];
    case 0:
      return [ComparisonResult.NO_MATCH, response.score];
    case -10:
      return [ComparisonResult.MISREMEMBERED, response.score];
    default:
      return;
  }
};

/** A component that shows card labels, but only in development */
const DevCardLabel = ({ children }) =>
  children !== undefined &&
  import.meta.env.DEV && (
    <div
      style={{ opacity: 0.5 }}
      className="text-light d-flex flex-column justify-content-center small"
    >
      {children}
    </div>
  );

// Type of the hook used for typing callbacks like afterSelectPair
type UseMPProps = UseMatchingPairsProps<ComparisonResult, MPCard>;

interface MatchingPairsProps {
  /** Cards to be used in the game */
  cards: MPCard[];

  /** Type: visual or audio matching pairs */
  type: "visual" | "audio";

  /** Animate the card based on the comparison result */
  animate: boolean;

  /** Called when a card is selected */
  onSelectCard?: (card: MPCard) => void;

  onTurnEnd: (states: MPStates<MPCard>) => void;

  /** Called when the game ends */
  onGameEnd?: (states: MPStates<MPCard>) => void;

  /**
   * If set, after selecting two cards, the board is automatically reset
   * after this number of seconds. Defaults to 10 seconds.
   */
  endTurnAfterInterval?: number;

  /** Tutorial object */
  tutorial?: Tutorial;
}

/**
 * The main component for the matching pairs game. It uses the useMatchingPairs
 * hook to manage the game state and logic, and includes feedback and tutorials.
 */
export default function MatchingPairs({
  cards: initialCards,
  type,
  animate = true,
  onSelectCard = () => {},
  onTurnEnd: onTurnEndCallback = () => {},
  onGameEnd: onGameEndCallback = () => {}, // submitResult,
  endTurnAfterInterval = 10,
  tutorial = TUTORIAL,
}: MatchingPairsProps) {
  // Game state that flags UI changes
  const [gameState, setGameState] = useState<GameState>(GameState.DEFAULT);

  // Tutorial
  let { showStep, completeStep, getActiveSteps } = useTutorial({
    tutorial,
  });

  const beforeSelectCard: UseMPProps["beforeSelectCard"] = ({ card }) => {
    setGameState(GameState.CARD_SELECTED);
    onSelectCard(card);
  };

  const afterSelectFirstCard: UseMPProps["afterSelectFirstCard"] = ({
    card,
  }) => {
    setGameState(GameState.CARD_SELECTED);
    return (prev: MPCard[]) =>
      prev.map((c) => (c.id === card.id ? { ...c, playing: true } : { ...c }));
  };

  const afterSelectPair: UseMPProps["afterSelectPair"] = ({
    result,
    card1,
    card2,
  }) => {
    setGameState(GameState[`COMPLETED_${result}`]);

    // Show tutorial
    showStep(result.toLocaleLowerCase());
    return (prev: MPCard[]) =>
      prev.map((c) => {
        if (c.id === card1.id)
          return {
            ...c,
            playing: undefined,
            className: classNames(animate && CARD_CLASSES[result]),
          };
        if (c.id === card2.id)
          return {
            ...c,
            playing: true,
            className: classNames(animate && CARD_CLASSES[result]),
          };
        return { ...c };
      });
  };

  const onTurnEnd: UseMPProps["onTurnEnd"] = (states) => {
    setGameState(GameState.DEFAULT);
    onTurnEndCallback(states);

    // Finish tutorial step
    getActiveSteps().map((step) => completeStep(step.id));

    // Return cards updater
    return (prev: MPCard[]) =>
      prev.map((c) => ({
        ...c,
        playing: undefined,
        className: undefined,
      }));
  };

  const onGameEnd: UseMPProps["onGameEnd"] = (states: MPStates<MPCard>) => {
    setGameState(GameState.GAME_END);
    onGameEndCallback(states);
  };

  // Hook up the actual matching pairs game
  const { cards, turnScore, totalScore, endTurn, selectCard } =
    useMatchingPairs<ComparisonResult, MPCard>({
      cards: initialCards,
      compareCards,
      successfulComparisons: [
        ComparisonResult.LUCKY_MATCH,
        ComparisonResult.MEMORY_MATCH,
      ],
      beforeSelectCard,
      afterSelectFirstCard,
      afterSelectPair,
      onTurnEnd,
      onGameEnd,
    });

  // Automatically reset the board after a specified time interval
  useEffect(() => {
    if (!endTurnAfterInterval || !gameState.startsWith("COMPLETED")) return;
    const timeout = setTimeout(endTurn, endTurnAfterInterval * 1000);
    return () => clearTimeout(timeout); // cleanup on unmount or if matched changes
  }, [gameState, endTurn]);

  // Feedback meessage
  let feedback;
  const feedbackContentList = FEEDBACK[gameState]?.content;
  if (feedbackContentList) {
    const randomIdx = Math.floor(Math.random() * feedbackContentList.length);
    feedback = feedbackContentList[randomIdx];
  }

  const orientation = useOrientation();
  // const orientation = useContext(OrientationContext);
  console.log(orientation);
  // useEffect(() => {
  //   console.log("orientation", orientation);
  // }, [orientation]);
  // const orientation = "portrait";

  return (
    <SquareLayout
      portraitHeaderHeight={0.55}
      className={styles.container}
      fullscreen={true}
    >
      <SquareLayout.Header className={styles.header}>
        {/* Separate component mostly so that it picks up the orientation correctly */}
        <MPHeader
          turnScore={turnScore}
          totalScore={totalScore}
          feedback={feedback}
          activeSteps={getActiveSteps()}
        />
      </SquareLayout.Header>
      <SquareLayout.Square className={styles.main}>
        <Board
          columns={4}
          onClick={() => {
            if (gameState.startsWith("COMPLETED")) endTurn();
          }}
          items={cards.map((card) => {
            const sharedProps = {
              flipped: card.selected,
              disabled: card.disabled,
              label: <DevCardLabel children={card.data?.group} />,
            };

            // Return cards (in a container div to isolate the transformations)
            return [
              <div
                key={card.id}
                className={card.className}
                onClick={() => {
                  // Note that nothing else should be called here. In particular,
                  // the hook onSelectCard is called via the hook beforeSelectCard.
                  // In this way, the useMatchingPairs hook can ensure that disabled
                  // cards do not respond (more principled than e.g. a .noEvents class)
                  selectCard(card.id);
                }}
              >
                {type === "visual" ? (
                  <VisualCard
                    src={card.data?.src}
                    alt={card.data?.alt}
                    {...sharedProps}
                  />
                ) : (
                  <AudioCard
                    key={card.id}
                    running={card.playing}
                    {...sharedProps}
                  />
                )}
              </div>,

              // Hide slots when card is not disabled so the visual effects
              // look cleaner
              {
                invisible: card.disabled === false,
              },
            ];
          })}
        />
      </SquareLayout.Square>
      <SquareLayout.Aside className={styles.aside}>
        <Logo name="tunetwins" fill="#ccc" className={styles.logo} />
      </SquareLayout.Aside>
      <SquareLayout.Footer className={styles.footer}>
        <Timeline timeline={DEFAULT_TIMELINE} step={3} />
      </SquareLayout.Footer>
    </SquareLayout>
  );
}

interface MPHeaderProps {
  turnScore?: number;
  totalScore?: number;
  feedback?: string;
  activeSteps?: TutorialStep[];
}

function MPHeader({
  turnScore,
  totalScore,
  feedback,
  activeSteps,
}: MPHeaderProps) {
  const orientation = useOrientation();
  return (
    <>
      <ScoreFeedback
        className={styles.feedback}
        turnScore={turnScore ?? undefined}
        totalScore={totalScore ?? 0}
        totalScoreLabel="Total score"
        center={orientation === "portrait"}
      >
        {feedback}
      </ScoreFeedback>

      {activeSteps.map((step) => (
        <TutorialMessage key={step.id} {...step} />
      ))}
    </>
  );
}

/** Only meant as an interface between MP2 and the rest of the application */
export function MatchingPairsInterface({
  playSection,
  sections,
  playerIndex,
  showAnimation,
  finishedPlaying,
  scoreFeedbackDisplay: _ignored,
  submitResult,
  tutorial,
  view,
}: MatchingPairsInterfaceProps) {
  // TODO Tutorial
  // tutorial = {
  //   lucky_match:
  //     "You got a matching pair, but you didn't hear both cards before. This is considered a lucky match. You get 10 points.",
  //   memory_match: "You got a matching pair. You get 20 points.",
  //   misremembered:
  //     "You thought you found a matching pair, but you didn't. This is considered a misremembered pair. You lose 10 points.",
  //   no_match:
  //     "This was not a match, so you get 0 points. Please try again to see if you can find a matching pair.",
  // };
  const cards = sections.map(
    (section, index) =>
      ({
        id: index,
        data: { ...section },
      } as MPCard)
  );
  return (
    <MatchingPairs
      cards={cards}
      type={view === "visual" ? "visual" : "audio"}
      animate={showAnimation}
      onGameEnd={() => submitResult({})}
      onTurnEnd={() => finishedPlaying()}
      onSelectCard={(card) => {
        playSection(card.id);
        // TODO set card.playing to true if playerIndex === index?
      }}
      tutorial={convertTutorial(tutorial)}
    />
  );
}
