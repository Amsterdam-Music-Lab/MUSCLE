import classNames from "classnames";
import { API_ROOT } from "@/config";
import { Card } from "@/types/Section";
import Histogram from "../Histogram/Histogram";
import "./PlayCard.scss"

const PlayingCardFront = ({ src, name }: {src: string, name: string}) => {
  const url = src.startsWith("http") ? src : API_ROOT + src
  return (
    <div data-testid="front" className="front front--visual">
      <img src={url} alt={name} />
    </div>
  )
}

const PlayingCardBack = ({ seen, group }: { seen: boolean, group: number }) => {
  return (
    <div data-testid="back" className={classNames("back", { seen })}>
      {/* TODO: Remove this before merging PR */}
      <span className="d-flex flex-column justify-content-center text-white">
        {group}
      </span>
    </div>
  )
}

interface PlayCardProps {
  onClick: () => void;
  registerUserClicks: (x: number, y: number) => void;
  playing: boolean;
  section: Card;
  view: string;
  showAnimation: boolean;
}

const PlayCard = ({
  onClick,
  registerUserClicks,
  playing,
  section,
  view,
  showAnimation
}: PlayCardProps) => {
  const matchClass = showAnimation ? section.matchClass : '';
  const histogramBars = showAnimation ? 5 : 0;

  return (
    <div
      data-testid="play-card"
      className={
        classNames(
          "aha__play-card",
          matchClass,
          { turned: section.turned },
          { noevents: section.noevents },
          { disabled: section.inactive },
        )
      }
      onClick={event => {
        registerUserClicks(event.clientX, event.clientY);
        onClick();
      }}
      role="button"
    >
      { 
        section.turned === false
          ? <PlayingCardBack seen={section.seen} group={section.group} />
          : view === 'visual'
            ? <PlayingCardFront src={section.url} name={section.name} />
            : <Histogram
                running={playing}
                bars={histogramBars}
                backgroundColor="purple"
                borderRadius=".75rem"
                random={true}
                interval={200} />
      }
    </div>
  );
};

export default PlayCard;
