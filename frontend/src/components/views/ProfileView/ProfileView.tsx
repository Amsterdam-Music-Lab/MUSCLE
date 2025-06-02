/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import classNames from "classnames";
import { useParticipantScores } from "@/API";
import { Cup, CupType } from "@/components/game";
import { URLS } from "@/config";
import { ParticipantLink } from "@/components/user";
import { Card, LinkButton } from "@/components/ui";
import styles from "./ProfileView.module.scss";
import { View } from "@/components/application";

export interface ProfileViewData {
  messages: {
    title: string;
    summary: string;
    continue: string;
    points: string;
  };
  scores: {
    block_slug: string;
    block_name: string;
    score: number;
    date: string;
    rank: {
      class: string;
      text: string;
    };
    finished_at: string;
  }[];
}

interface ScoreBadgeProps extends HTMLAttributes<HTMLDivElement> {
  block_slug: string;
  block_name: string;
  score: number;
  date: string;
  cupLabel: string;
  cupType: CupType;
  finished_at: string;
}

export function ScoreBadge({
  blockName,
  blockSlug,
  score,
  date,
  cupType,
  cupLabel,
  className,
  points = "points",
  ...divProps
}: ScoreBadgeProps) {
  return (
    <Card className={classNames(styles.result, className)} {...divProps}>
      <Cup className={styles.cup} type={cupType} text={cupLabel} radius={150} />
      <Card.Header title={`${score} ${points}`}>
        <p>
          {blockName ?? `Block "${blockSlug}"`}{" "}
          <span className={styles.sep}>•</span> {date}{" "}
        </p>
        <LinkButton
          link={URLS.block.replace(":slug", blockSlug)}
          size="sm"
          stretch={true}
        >
          Go to {blockName ?? `Block "${blockSlug}"`}
        </LinkButton>
      </Card.Header>
    </Card>
  );
}

/** Profile loads and shows the profile of a participant for a given experiment */
export default function ProfileView() {
  // API hooks
  const [data, loadingData] = useParticipantScores<ProfileViewData>();

  if (loadingData) return <View name="loading" />;
  if (!data)
    return (
      <View
        name="error"
        message="An error occured while loading your profile..."
      />
    );

  data.scores.sort((a, b) =>
    a.finished_at === b.finished_at ? 0 : a.finished_at > b.finished_at ? -1 : 1
  );
  const results = data.scores;
  return (
    <>
      <Card>
        <Card.Header title={data.messages.title}>
          {data.messages.summary}
        </Card.Header>

        <Card.Section>
          {data.messages.continue}
          <ParticipantLink />
        </Card.Section>
      </Card>
      <div
        className={styles.scroller}
        style={{ "--num-results": results.length }}
      >
        <div className={styles.results}>
          {results.map((result, index) => (
            <ScoreBadge
              key={index}
              cupType={result.rank.class as CupType}
              cupLabel={result.rank.text}
              score={result.score}
              blockSlug={result.block_slug}
              blockName={result.block_name}
              date={result.date}
              points={data.messages.points}
            />
          ))}
        </div>
      </div>
    </>
  );
}

ProfileView.viewName = "profile";
ProfileView.usesOwnLayout = false;
ProfileView.getViewProps = undefined;
