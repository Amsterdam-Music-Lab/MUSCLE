import { Loading, ErrorView } from "../";
import classNames from "classnames";
import { useParticipantScores } from "@/API";
import { NarrowLayout } from "@/components/layout";
import { Cup, CupType } from "@/components/game";
import { URLS } from "@/config";
import { ParticipantLink } from "@/components/user";
import { Card, LinkButton } from "@/components/ui";
import styles from "./Profile.module.scss";

export interface ProfileViewProps {
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

function ScoreBadge({
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
const Profile = () => {
  // API hooks
  const [data, loadingData] = useParticipantScores<ProfileViewProps>();

  if (loadingData) return <Loading />;
  if (!data)
    return (
      <ErrorView message="An error occured while loading your profile..." />
    );

  data.scores.sort((a, b) =>
    a.finished_at === b.finished_at ? 0 : a.finished_at > b.finished_at ? -1 : 1
  );
  const results = data.scores;
  return (
    <NarrowLayout>
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
    </NarrowLayout>
  );
};

export default Profile;
