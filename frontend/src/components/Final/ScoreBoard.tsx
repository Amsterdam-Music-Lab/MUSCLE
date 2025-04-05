import classNames from "@/util/classNames";

// Local imports
import TuneTwins from "@/components/MCGTheme/logos/TuneTwins"
import Timeline, { TIMELINE_SYMBOLS, TimelineConfig } from "@/components/Timeline/Timeline";
import { SVGStar } from "@/components/SVG/SVGStar";
import { colors } from "@/components/MCGTheme/colors";
import ProgressBar from "@/components/MCGTheme/ProgressBar";
import Score from "@/components/MCGTheme/Score";

import "./ScoreBoard.scss";


const SectionLabel = ({ children, className, ...props }) => (
  <p className={classNames("d-block text-indigo-red fw-semibold mb-2", className)} {...props}>
    {children}
  </p>
)

const Trophy = ({ name }: { name: string }) => {
  if (!TIMELINE_SYMBOLS.includes(name)) return null;
  const Symbol = TIMELINE_SYMBOLS[name]
  return (
    <div className="position-absolute" style={{ right: "1em", zIndex: 20, top: "0em" }}>
      <Symbol
        fillFrom={colors["red"]}
        fillTo={colors["pink"]}
        size={110}
        strokeWidthFactor={.15} />
    </div>
  )
}

interface ScoreBoardProps {
  score: number;
  totalScore: number;
  percentile: number;
  timeline?: TimelineConfig;
  step?: number;
  percentileCutoff: number;
  showPercentile: boolean;
  showScores: boolean;
  showTimeline: boolean;
  showTrophy: true;
}

const ScoreBoard = ({
  score,
  totalScore,
  percentile,
  timeline = null,
  step = null,
  percentileCutoff = 30,
  showPercentile = true,
  showScores = true,
  showTimeline = true,
  showTrophy = true
}: FinalProps) => {

  const hasPercentile = typeof percentile === 'number' && percentile >= 0 && percentile <= 100;
  const hasTimeline = timeline !== null && step !== null;
  const hasTrophy = hasTimeline && timeline[step].trophy
  const trophyName = timeline[step].symbol
  const Trophy = hasTrophy ? TIMELINE_SYMBOLS[trophyName] || null : null;

  return (
    <div className="score-board card bg-inset-sm rounded-lg">

      {/* Capture this */}
      {/* A square card that fits inside the rounded card and should be captured */}
      {/* as an image for sharing on social media */}
      <div className="capture position-relative">

        {/* TuneTwins logo */}
        <div className="pl-2 px-4">
          <TuneTwins width="200px" />
        </div>

        {/* Star */}
        {showTrophy && hasTrophy &&
          <div className="trophy position-absolute d-flex justify-content-end w-100">
            <p class="label text-white font-weight-bolder">You've earned a star!</p>
            <div className="position-absolute">
              {Trophy &&
                <Trophy
                  fillFrom={colors["red"]}
                  fillTo={colors["pink"]}
                  size={100}
                  strokeWidthFactor={.15} />
              }
            </div>
          </div>
        }

        <div class="list-group list-group-flush bg-transparent">

          {/* Percentile */}
          {showPercentile && hasPercentile && percentile > 0 && (
            <div className="list-group-item p-4 bg-transparent">
              {percentile > percentileCutoff
                ?
                <><SectionLabel style={{ maxWidth: "70%" }}>
                  Congrats! You did better than{" "}
                  <span className="bolder">{`${Math.round(percentile)}%`}</span>{" "}
                  of players at this level
                </SectionLabel>
                  <ProgressBar progress={percentile} />
                </>
                : <>
                  <SectionLabel>{`Well done! You did better than <${percentileCutoff}% of people at this level.`}</SectionLabel>
                  <ProgressBar progress={percentileCutoff} />
                </>}
                
            </div>
          )}

          {/* Ranking */}
          {/* Note that falls back gracefully when score or totalScore are missing. */}
          {showScores && (
            <div class="list-group-item p-4 bg-transparent">
              {/* <SectionLabel>Your scores</SectionLabel> */}
              <div className="d-flex">
                <div style={{ width: "50%" }}><Score score={score} label="Last game" /></div>
                <div style={{ width: "50%" }}><Score score={totalScore} label="Total score" /></div>
              </div>
            </div>
          )}

          {/* Progress */}
          {showTimeline && hasTimeline && (
            <div class="list-group-item p-4 bg-transparent">
              {/* The label should depend on the step in the timeline */}
              <SectionLabel>Your progress...</SectionLabel>
              <Timeline timeline={timeline} step={step + 1} spine={true} />
            </div>
          )}
        </div>

      </div>
      {/* End of capture */}

      {/* Share and options */}
      <div class="list-group-item p-4 bg-transparent border-left-0 border-right-0 border-bottom-0">
        <button className="btn bg-indigo-red text-white rounded-lg px-4 py-1">Share</button>
      </div>
    </div>
  );
};

export default ScoreBoard;
