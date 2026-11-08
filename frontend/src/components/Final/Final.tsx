import { Suspense, lazy } from "react";
import { useNavigate } from "react-router-dom";

import Button from "@/components/Button/Button";
const Footer = lazy(() => import("@/components/Footer/Footer"));
import HTML from "@/components/HTML/HTML";
import ParticipantLink from "@/components/ParticipantLink/ParticipantLink";
import ScoreCounter from "@/components/ScoreCounter/ScoreCounter";
const Social = lazy(() => import("@/components/Social/Social"));
const Timeline = lazy( () => import ("@/components/Timeline/Timeline"));
const Trophy = lazy(() => import("@/components/Trophy/Trophy"));
const UserFeedback = lazy(() => import("@/components/UserFeedback/UserFeedback"));
import Visualization from "@/components/Visualization/Visualization";
import { FinalView, SharedActionProps } from "@/types/Action";
import { URLS, useExperimentTimeline } from '@/API';

import useBoundStore from "@/util/stores";

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
const Final = (props: FinalView & SharedActionProps) => {
    const {
        block,
        participant,
        scores,
        trophy,
        finalText,
        visualizationType,
        timeline,
        actionTexts,
        button,
        onNext,
        showParticipantLink,
        participantIDOnly,
        showProfileLink,
        social,
        feedbackInfo,
        
    } = props;
    const navigate = useNavigate();

    const currentTimelineStep = timeline? timeline.playedSessions % timeline.steps.length : 0;
    const trophyImage = timeline.steps[currentTimelineStep - 1];


    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            {trophy && (
                <Suspense>
                    <div className="aha__trophy-container text-center">
                        {trophyImage && (
                            <Trophy className={trophy.className} label={trophy.label} image={trophyImage} />
                        )}
                        {trophy.description && (
                            <HTML innerClassName="aha__trophy-description" body={trophy.description} />
                            )
                        }
                    </div>
                </Suspense>
            )}

            {finalText && (
                <HTML innerClassName="aha__final-text" body={finalText} />
            )}
            
            {visualizationType && (
                <Visualization value={scores.relative.value} label={scores.relative.label} type={visualizationType} className={trophy.className}/>
            )}

            {scores && (
                <ScoreCounter scores={scores} />
            )}

            {timeline && timeline.steps.length > 1 && (
                <Suspense>
                    <Timeline timeline={timeline} />
                </Suspense>
            )}
            

            {social && (<Social
                social={social}
            />
            )}
            {showProfileLink && (
                <div className=" mt-2 d-flex justify-content-center">
                    <a className="home text-center" href={URLS.AMLHome}>
                        {actionTexts.allExperiments}
                    </a>
                    <div
                        data-testid="profile-link"
                        className="home text-center"
                        onClick={() => navigate(URLS.profile)}
                    >
                        {actionTexts.profile}
                    </div>
                </div>
            )}
            {showParticipantLink && (
                <ParticipantLink
                    participantIDOnly={participantIDOnly}
                />
            )}
            {feedbackInfo && (<UserFeedback
                blockIdentifier={block.identifier}
                participant={participant}
                feedbackInfo={feedbackInfo}
            />)}
                        {button && (
                <div className="text-center pt-4">
                    <Button
                        {...button}
                        onClick={onNext}
                    />
                </div>
            )}
            {(block.theme && block.theme.footer) && (
                <Suspense >
                    <Footer
                        logos={block.theme.footer!.logos}
                    />
                </Suspense>
            )}

        </div>
    );
};

export default Final;
