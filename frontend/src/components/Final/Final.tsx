import { Suspense, lazy } from "react";
import { useNavigate } from "react-router-dom";

import Button from "@/components/Button/Button";
const Footer = lazy(() => import("@/components/Footer/Footer"));
import HTML from "@/components/HTML/HTML";
import ParticipantLink from "@/components/ParticipantLink/ParticipantLink";
import ScoreCounter from "@/components/ScoreCounter/ScoreCounter";
const Social = lazy(() => import("@/components/Social/Social"));
const Trophy = lazy(() => import("@/components/Trophy/Trophy"));
const UserFeedback = lazy(() => import("@/components/UserFeedback/UserFeedback"));
import Visualization from "@/components/Visualization/Visualization";
import { FinalAction, SharedActionProps } from "@/types/Action";
import { URLS, useExperimentProgress } from '@/API';

import useBoundStore from "@/util/stores";

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
const Final = (props: FinalAction & SharedActionProps) => {
    const {
        block,
        participant,
        scores,
        trophy,
        finalText,
        visualizationType,
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
    const progress = useExperimentProgress(block.experimentIdentifier);

    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            {trophy && (
                <Suspense>
                    <div className="aha__trophy-container text-center">
                        <Trophy className={trophy.className} label={trophy.label} image={progress.currentReward? progress.currentReward.image : undefined} />
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
                <Visualization percentile={scores.relative.value} type={visualizationType} rankClass={trophy.className}/>
            )}

            {scores && (
                <ScoreCounter scores={scores} />
            )}
            
            
            {button && (
                <div className="text-center pt-4">
                    <Button
                        {...button}
                        onClick={onNext}
                    />
                </div>
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
