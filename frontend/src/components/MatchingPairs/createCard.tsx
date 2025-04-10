/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import { type Card as CardData } from "@/types/Section";
import { AudioCard } from "./AudioCard";
import { VisualCard } from "./VisualCard";
import { Card } from "./Card";

export interface CreateCardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The view type */
  type: "visual" | "audio";
  
  /** The card data */
  card: CardData;

  /** Click handler */
  onClick?: () => void;

  /** A handler that registers user Clicks */
  registerUserClicks?: (x: number, y: number) => void;

  /** Whether the audio is playing */
  playing?: boolean;

  /** Whether to animate the cards */
  animate?: boolean;

  /** A react key */
  key?: string;
}

/**
 * Factory function that creates a card component based on the card type
 * 
 */
export default function createCard({
  type,
  card,
  onClick,
  registerUserClicks,
  playing = true,
  animate = true,
  key,
  ...cardProps
}: CreateCardProps): React.ReactElement {
  const props = {
    flipped: card.turned,
    seen: card.seen,
    disabled: card.inactive,
    noEvents: card.noevents,
    className: animate ? card.matchClass : '',
    onClick: (event) => {
      if(registerUserClicks) registerUserClicks(event.clientX, event.clientY);
      if(onClick) onClick();
    },
    ...cardProps
  }

  switch (type) {
    case 'visual':
      return <VisualCard src={card.url} alt={card.name} key={key} {...props} />;
  
    case 'audio':
      return <AudioCard running={playing} bars={animate ? 5 : 0} key={key} {...props} />;
  
    default:
      return <Card key={key}{...props} />;
  }
};
