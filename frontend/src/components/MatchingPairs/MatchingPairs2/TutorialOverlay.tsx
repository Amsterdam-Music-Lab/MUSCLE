/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Overlay from "@/components/Overlay/Overlay";
import { type TutorialStep } from "./useTutorial";

interface TutorialOverlayProps extends React.HTMLAttributes<HTMLDivElement> {
  step: TutorialStep;
  onClose?: () => void;
}

function TutorialOverlay({
  step,
  onClose = () => null,
  onClick = () => null,
  ...props
}: TutorialOverlayProps) {
  return (
    <>
      <div
        data-testid="overlay"
        className="matching-pairs__overlay"
        onClick={(e) => {
          onClose();
          onClick(e);
        }}
        {...props}
      />

      <Overlay
        isOpen={step.visible ?? false}
        title={step.title}
        content={step.content}
        onClose={onClose}
      />
    </>
  );
}

export default TutorialOverlay;
