/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { TutorialStep } from "@/types/tutorial";
import type { UseTuneTwinsProps } from "../useTuneTwins";
import type { TimelineConfig } from "@/types/timeline";
import type { LogoName } from "@/components/svg";

import { useMemo } from "react";
import { useOrientation } from "@/hooks/OrientationProvider";
import { useTuneTwins, TTComparisonResult, TTGameState } from "./useTuneTwins";
import { Timeline, ScoreFeedback, TutorialMessage } from "@/components/modules";
import { SquareLayout } from "@/components/layout";
import { Logo } from "@/components/svg";
import { Board } from "../Board";
import { AudioCard } from "../AudioCard";
import DevCardLabel from "./DevCardLabel";
import styles from "./TuneTwins.module.scss";

const CARD_CLASSES = {
  [TTComparisonResult.NO_MATCH]: styles.nomatch,
  [TTComparisonResult.LUCKY_MATCH]: styles.lucky,
  [TTComparisonResult.MISREMEMBERED]: styles.misremembered,
  [TTComparisonResult.MEMORY_MATCH]: styles.memory,
};

type TTFeedbackMessage =
  | "default"
  | "cardSelected"
  | "completedLuckyMatch"
  | "completedMemoryMatch"
  | "completedNoMatch"
  | "completedMisremembered"
  | "gameEnd";

const DEFAULT_FEEDBACK: Record<TTFeedbackMessage, string[]> = {
  default: ["Pick a card..."],
  cardSelected: ["Pick another card..."],
  completedLuckyMatch: [
    "Lucky guess!",
    "Lucky you!",
    "This is your lucky day!",
  ],
  completedMemoryMatch: ["Well done!", "Good job!", "Nice!", "Excellent!"],
  completedNoMatch: ["No match, try again!"],
  completedMisremembered: ["Nope, that's no match..."],
};

export interface TuneTwinsProps extends UseTuneTwinsProps {
  /** Feedback messages shown to the user after turning two cards */
  feedbackMessages?: Record<TTFeedbackMessage, string[]>;

  /** Name of the logo */
  logo?: LogoName;

  /** Whether to show the logo */
  showLogo?: boolean;

  /** Configuration of the timeline */
  timeline?: TimelineConfig;

  /** Whether to show the timeline, even if one is specified. */
  showTimeline?: boolean;
}

/**
 * The main component for the matching pairs game. It uses the useTuneTwins
 * hook to manage the game state and logic, and includes feedback and tutorials.
 */
export default function TuneTwins({
  feedbackMessages: msg = DEFAULT_FEEDBACK,
  timeline,
  showTimeline = true,
  showLogo = true,
  logo = "tunetwins",
  ...props
}: TuneTwinsProps) {
  const feedbackMessages = {
    [TTGameState.DEFAULT]: msg.default,
    [TTGameState.CARD_SELECTED]: msg.cardSelected,
    [TTGameState.COMPLETED_LUCKY_MATCH]: msg.completedLuckyMatch,
    [TTGameState.COMPLETED_MEMORY_MATCH]: msg.completedMemoryMatch,
    [TTGameState.COMPLETED_NO_MATCH]: msg.completedNoMatch,
    [TTGameState.COMPLETED_MISREMEMBERED]: msg.completedMisremembered,
    [TTGameState.GAME_END]: msg.gameEnd,
  };

  const {
    activeSteps,
    feedback,
    gameState,
    cards,
    turnScore,
    totalScore,
    endTurn,
    selectCard,
  } = useTuneTwins({
    ...props,
    feedbackMessages,
    cardClasses: CARD_CLASSES,
  });
  let tabCount = 0;

  // Avoid unneccessary re-renders of the Timeline and Logo components
  const MemoTimeline = useMemo(
    () => <Timeline timeline={timeline} />,
    [timeline]
  );
  const MemoLogo = useMemo(
    () => <Logo name={logo} fill="#ccc" className={styles.logo} />,
    [logo]
  );

  return (
    <SquareLayout
      portraitHeaderHeight={0.55}
      className={styles.container}
      fullscreen={true}
    >
      <SquareLayout.Header className={styles.header}>
        {/* Separate component mostly so that it picks up the orientation correctly */}
        <TuneTwinsHeader
          turnScore={turnScore}
          totalScore={totalScore}
          feedback={feedback}
          activeSteps={activeSteps}
        />
      </SquareLayout.Header>

      <SquareLayout.Square className={styles.main}>
        <Board
          columns={4}
          onClick={() => {
            if (gameState.startsWith("COMPLETED")) endTurn();
          }}
          items={cards.map((card, index) => {
            const sharedProps = {
              flipped: card.selected,
              disabled: card.disabled,
              label: <DevCardLabel children={card.data?.group} />,
            };
            if (!card.disabled) tabCount += 1;
            // Return cards (in a container div to isolate the transformations)
            return [
              <div key={card.id} className={card.className}>
                <AudioCard
                  key={card.id}
                  running={card.playing}
                  tabIndex={!card.disabled ? tabCount : undefined}
                  onClick={() => {
                    // This ensures that you can play the game with keyboard only.
                    // But not ideal: the first time this is executed the card is not
                    // selected yet because that requires another state update...
                    if (gameState.startsWith("COMPLETED")) endTurn();

                    // Note that nothing else should be called here. In particular,
                    // the hook onSelectCard is called via the hook beforeSelectCard.
                    // In this way, the useMatchingPairs hook can ensure that disabled
                    // cards do not respond (more principled than e.g. a .noEvents class)
                    selectCard(card.id);
                  }}
                  {...sharedProps}
                />
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

      {showLogo && (
        <SquareLayout.Aside className={styles.aside}>
          {MemoLogo}
        </SquareLayout.Aside>
      )}

      {timeline && showTimeline && (
        <SquareLayout.Footer className={styles.footer}>
          {MemoTimeline}
        </SquareLayout.Footer>
      )}
    </SquareLayout>
  );
}

interface TuneTwinsHeaderProps {
  turnScore?: number;
  totalScore?: number;
  feedback?: string;
  activeSteps?: TutorialStep[];
}

function TuneTwinsHeader({
  turnScore,
  totalScore,
  feedback,
  activeSteps,
}: TuneTwinsHeaderProps) {
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

      {activeSteps &&
        activeSteps.map((step) => <TutorialMessage key={step.id} {...step} />)}
    </>
  );
}
