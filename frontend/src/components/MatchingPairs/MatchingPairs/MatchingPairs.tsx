/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState } from "react";
import { scoreIntermediateResult } from "@/API";
import { Card as CardData } from "@/types/Section";
import { MatchingPairsProps as MatchingPairsInterfaceProps } from "../MatchingPairsv1/MatchingPairs";
import { ScoreFeedback } from "@/components/game";
import {
  useMatchingPairs,
  CompareCardsProps,
  MPCard as GenericMPCard,
  MPStates,
  UseMatchingPairsProps,
} from "../useMatchingPairs";
import { Tutorial, useTutorial } from "../useTutorial";
import { processTutorial } from "../utils";
import { Board } from "../Board";
import { VisualCard } from "../VisualCard";
import { AudioCard } from "../AudioCard";
import styles from "./MatchingPairs.module.scss";
import classNames from "classnames";

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

enum ComparisonResult {
  LUCKY_MATCH = "LUCKY_MATCH",
  MEMORY_MATCH = "MEMORY_MATCH",
  NO_MATCH = "NO_MATCH",
  MISREMEMBERED = "MISREMEMBERED",
}

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
  tutorial = TUTORIAL,
}: MatchingPairsProps) {
  // Game state that flags UI changes
  const [gameState, setGameState] = useState<GameState>(GameState.DEFAULT);

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

  // Tutorial
  // let { showStep, completeStep, getActiveStep } = useTutorial({ tutorial });
  // showStep("start");
  // const activeTutorialStep = getActiveStep();

  let feedback;
  const feedbackContentList = FEEDBACK[gameState]?.content;
  if (feedbackContentList) {
    const randomIdx = Math.floor(Math.random() * feedbackContentList.length);
    feedback = feedbackContentList[randomIdx];
  }

  return (
    <div className={styles.matchingPairs}>
      <div className={styles.mpContainer}>
        <div className={styles.mpHeader}>
          <ScoreFeedback
            turnScore={turnScore ?? undefined}
            totalScore={totalScore ?? 0}
          >
            {feedback}
            {/* <p>{activeTutorialStep?.content}</p> */}
          </ScoreFeedback>
        </div>

        <div className={styles.mpMain}>
          <Board
            columns={4}
            onClick={() => {
              if (gameState.startsWith("COMPLETED")) endTurn();
            }}
            items={cards.map((card) => {
              const sharedProps = {
                flipped: card.selected,
                disabled: card.disabled,
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
                      label={
                        card.data.group !== undefined && import.meta.env.DEV && (
                          <span style={{ opacity: 0.3 }} className="text-light">
                            {card.data?.group}
                          </span>
                        )
                      }
                      src={card.data?.src}
                      alt={card.data?.alt}
                      {...sharedProps}
                    />
                  ) : (
                    <AudioCard
                      key={card.id}
                      label={
                        card.data.group !== undefined && import.meta.env.DEV && (
                          <span style={{ opacity: 0.3 }} className="text-light">
                            {card.data?.group}
                          </span>
                        )
                      }
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
        </div>
      </div>
    </div>
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
    />
  );
}
