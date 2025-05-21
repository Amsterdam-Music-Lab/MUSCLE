/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { TutorialStep } from "@/types/tutorial";
import type { UseTuneTwinsProps } from "../useTuneTwins";

import { useOrientation } from "@/hooks/OrientationProvider";
import { useTuneTwins, TTComparisonResult } from "../useTuneTwins";
import { Timeline, ScoreFeedback, TutorialMessage } from "@/components/game";
import { SquareLayout } from "@/components/layout";
import { Board } from "../Board";
import { AudioCard } from "../AudioCard";
import { Logo } from "@/components/svg";
import DevCardLabel from "./DevCardLabel";
import styles from "./TuneTwins.module.scss";

const CARD_CLASSES = {
  [TTComparisonResult.NO_MATCH]: styles.nomatch,
  [TTComparisonResult.LUCKY_MATCH]: styles.lucky,
  [TTComparisonResult.MISREMEMBERED]: styles.misremembered,
  [TTComparisonResult.MEMORY_MATCH]: styles.memory,
};

const DEFAULT_TIMELINE = {
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
};

interface TuneTwinsProps extends UseTuneTwinsProps {}

/**
 * The main component for the matching pairs game. It uses the useTuneTwins
 * hook to manage the game state and logic, and includes feedback and tutorials.
 */
export default function TuneTwins(props: TuneTwinsProps) {
  const {
    getActiveSteps,
    feedback,
    gameState,
    cards,
    turnScore,
    totalScore,
    endTurn,
    selectCard,
  } = useTuneTwins({
    ...props,
    cardClasses: CARD_CLASSES,
  });

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
                <AudioCard
                  key={card.id}
                  running={card.playing}
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
      <SquareLayout.Aside className={styles.aside}>
        <Logo name="tunetwins" fill="#ccc" className={styles.logo} />
      </SquareLayout.Aside>
      <SquareLayout.Footer className={styles.footer}>
        <Timeline timeline={DEFAULT_TIMELINE} step={3} />
      </SquareLayout.Footer>
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
