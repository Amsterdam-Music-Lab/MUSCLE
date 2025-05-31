/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ProfileData } from "@/types/profile";
import { CupType, ScoreBadge } from "@/components/game";
import { ParticipantLink } from "@/components/user";
import { Card } from "@/components/ui";
import styles from "./ProfileView.module.scss";

function sortScores(scores: ProfileData["scores"]) {
  scores.sort((a, b) =>
    a.finished_at === b.finished_at ? 0 : a.finished_at > b.finished_at ? -1 : 1
  );
}

export interface ProfileViewProps {
  scores: ProfileData["scores"];
  title: string;
  summary: string;
  continue?: string;
  points?: string;
}

/** Profile loads and shows the profile of a participant for a given experiment */
export default function ProfileView({
  scores,
  title,
  summary,
  content,
  pointsUnit = "points",
}: ProfileViewProps) {
  if (scores) sortScores(scores);
  return (
    <>
      <Card>
        <Card.Header title={title}>{summary}</Card.Header>
        <Card.Section>
          {content}
          <ParticipantLink />
        </Card.Section>
      </Card>

      {scores && (
        <div
          className={styles.scroller}
          style={{ "--num-results": scores.length }}
        >
          <div className={styles.scores}>
            {scores.map((result, index) => (
              <ScoreBadge
                key={index}
                cupType={result.rank.class as CupType}
                cupLabel={result.rank.text}
                score={result.score}
                blockSlug={result.block_slug}
                blockName={result.block_name}
                date={result.date}
                points={pointsUnit}
              />
            ))}
          </div>
        </div>
      )}
    </>
  );
}

ProfileView.viewName = "profile";
ProfileView.usesOwnLayout = false;
ProfileView.getViewProps = undefined;
