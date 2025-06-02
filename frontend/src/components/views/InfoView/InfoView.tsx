/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";

import { useEffect, useState } from "react";
import { Card, LinkButton } from "@/components/ui";
import { RenderHtml } from "@/components/utils";

/**
 * Calculate height for Info text to prevent overlapping browser chrome
 */
const getMaxHeight = () => {
  const height = document.documentElement?.clientHeight || window.innerHeight;
  const width = document.documentElement?.clientWidth || window.innerWidth;
  const correction = width > 720 ? 280 : 250;
  return height - correction;
};

function useMaxHeight() {
  const [maxHeight, setMaxHeight] = useState(getMaxHeight());

  useEffect(() => {
    const onResize = () => setMaxHeight(getMaxHeight());
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return maxHeight;
}

export interface InfoViewProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Title of the info card.
   */
  title: string;

  /**
   * HTML string that is rendered in the main section of the info card.
   */
  html?: string;

  /**
   * Text shown on the button. Note that the button is only shown
   * when either buttonLink or onButtonClick is specified.
   */
  buttonText?: string;

  /**
   * Link to follow when the button is clicked.
   */
  buttonLink?: string;

  /**
   * Callback called when the button is clicked.
   */
  onButtonClick?: () => void;

  /**
   * Whether to adjust the max height of the html content responsively.
   * Default false.
   */
  responsiveHeight: boolean;
}

/** Info is a block view that shows the Info text, and handles agreement/stop actions */
export default function InfoView({
  title,
  html,
  buttonText = "Continue",
  buttonLink,
  onButtonClick,
  responsiveHeight = false,
  ...divProps
}: InfoViewProps) {
  const maxHeight = useMaxHeight();
  const btnProps: any = {
    stretch: true,
    rounded: false,
    variant: "secondary",
  };
  if (buttonLink) btnProps.link = buttonLink;
  if (onButtonClick) btnProps.onClick = onButtonClick;

  return (
    <div {...divProps}>
      <Card>
        {title && <Card.Header title={title} />}
        {html && (
          <Card.Section>
            <RenderHtml
              html={html}
              data-testid="info-body"
              style={responsiveHeight ? { maxHeight } : {}}
            />
          </Card.Section>
        )}
      </Card>
      {(buttonLink || onButtonClick) && (
        <LinkButton {...btnProps}>{buttonText}</LinkButton>
      )}
    </div>
  );
}

InfoView.viewName = "viewName";
InfoView.usesOwnLayout = false;
InfoView.getViewProps = ({ action, onNext }) => ({
  html: action?.body,
  title: action?.heading,
  buttonText: action?.button_label,
  buttonLink: action?.button_link,
  onButtonClick: onNext,
});
InfoView.dependencies = ["action", "onNext"];
