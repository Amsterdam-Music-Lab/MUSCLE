import type { CSSProperties } from "react";
import type {
	Timeline as ITimeline
} from "@/types/Timeline";

import Cup from "@/svg/Cup";
import Star from "@/svg/Star";
import useBoundStore from "@/util/stores";


export interface TimelineProps {
	/**
	 * A timeline object.
	 */
	timeline: ITimeline;

	/** Animate the symbols? */
	animate?: boolean;

	dotSize: number;
	trophySize: number;
}


export default function Timeline({
	timeline,
	animate = true,
	dotSize = 10,
	trophySize = 40,
	showSymbols = true,
}: TimelineProps) {

	const theme = useBoundStore((state) => state.theme);
	const fillCompleted = theme.colorPrimary;
	const fillUpcoming = theme.colorGrey;

	const currentStep = timeline.playedSessions % timeline.steps.length;

	const renderRewardImage = (image: string, size: number) => {
		const props = {
			size: size
		}

		switch(image) {
			case "cup":
				return (<Cup {... props}/>);
			case "star":
				return (<Star {... props}/>);
			default:
				return (<div></div>)
		}
	}

	return (
		<div className="aha__timeline" >
			{timeline.steps.map((step, idx) => {
				const fillColor = idx >= currentStep ? fillUpcoming: fillCompleted;
				const segmentColor = idx >= timeline.steps.length - 1 ? "" : idx >= currentStep - 1 ? fillUpcoming: fillCompleted;
				const size = step ? trophySize : dotSize;
				const margin = step ? 0 : "0.9em";
				return (
					<div className="aha__timeline-step" key={idx}>
												<div
							className="aha__timeline-spine-segment"
							style={{
								backgroundColor: segmentColor,

							}}
						/>
						<div className="aha__timeline-symbol" style={{backgroundColor: fillColor, border: `.2em solid hsl(from ${fillColor} h s 70%)`, width: size+10, height: size+10, top: margin, left: margin}}>
							{renderRewardImage(step.image || "", size)}
						</div>
						
					</div>
				);
			})}
		</div>
	);
}
