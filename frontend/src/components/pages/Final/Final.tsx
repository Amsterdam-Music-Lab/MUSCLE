/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { ScoreBoardProps } from "@/components/game/ScoreBoard/ScoreBoard";
import { useEffect } from "react";
import classNames from "classnames";
import { URLS } from "@/config";
import { finalizeSession } from "@/API";
import useBoundStore from "@/util/stores";
import { ParticipantLink } from "@/components/user";
import { UserFeedbackForm } from "@/components/user";
import { Final as FinalAction } from "@/types/Action";
import { InputGroup, InputLabel, LinkButton } from "@/components/ui";
import { ScoreBoard, getTimeline } from "@/components/game";
import styles from "./Final.module.scss";

export interface FinalProps
  extends FinalAction,
    Omit<ScoreBoardProps, "logo">,
    HTMLAttributes<HTMLDivElement> {
  onNext: () => void;
}

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

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
const Final = ({
  block,
  participant,
  final_text: _, //ignored?
  action_texts: userLinkTexts,
  button,
  onNext,
  show_participant_link,
  participant_id_only,
  show_profile_link,
  social: shareConfig,
  feedback_info,
  points,
  rank,
  logo,
  percentile,
  score: turnScore,
  totalScore, // TODO
  timeline, // TODO
  timelineStep = 0, // TODO
  className,
  ...divProps
}: FinalProps) => {
  const session = useBoundStore((state) => state.session);
  useEffect(() => {
    finalizeSession({ session: session!, participant });
  }, [session, participant]);

  return (
    <div className={classNames(styles.final, className)} {...divProps}>
      <ScoreBoard
        turnScore={turnScore}
        totalScore={totalScore}
        percentile={percentile}
        timeline={timeline}
        timelineStep={timelineStep}
        shareConfig={shareConfig}
      />

      {button && (
        <LinkButton
          link={button.link}
          onClick={() => { onNext() }}
          stretch={true}
          rounded={false}
          size="lg"
          variant="secondary"
        >
          {button.text}
        </LinkButton>
      )}

      {show_profile_link && (
        <InputGroup stretch={true}>
          <InputLabel style={{ flexGrow: 1 }}>User pages</InputLabel>
          <LinkButton link={URLS.AMLHome} outline={false}>
            {userLinkTexts.all_experiments}
          </LinkButton>
          <LinkButton outline={false} link={URLS.profile}>
            {userLinkTexts.profile}
          </LinkButton>
        </InputGroup>
      )}

      {show_participant_link && (
        <ParticipantLink participantIDOnly={participant_id_only} />
      )}

      {feedback_info && (
        <UserFeedbackForm
          blockSlug={block.slug}
          participant={participant}
          feedbackInfo={feedback_info}
        />
      )}

      {logo && (
        <div className="text-center pt-4">
          <a href={logo.link}>
            <img src={logo.image} width="100%" alt="Logo" />
          </a>
        </div>
      )}
    </div>
  );
};

export default Final;
