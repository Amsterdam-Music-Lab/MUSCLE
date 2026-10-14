import { Suspense, lazy } from "react";
import { useNavigate } from "react-router-dom";

import Trophy from "@/components/Trophy/Trophy";
import Button from "@/components/Button/Button";
const Footer = lazy(() => import("@/components/Footer/Footer"));
import ParticipantLink from "@/components/ParticipantLink/ParticipantLink";
import ScoreCounter from "@/components/ScoreCounter/ScoreCounter";
import Social from "@/components/Social/Social";
import UserFeedback from "@/components/UserFeedback/UserFeedback";
import { FinalAction, SharedActionProps } from "@/types/Action";
import { URLS } from '@/API';
import HTML from "../HTML/HTML";
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
    const progress = getExperimentProgress(participant);

    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            {trophy && (
                <div className="text-center">
                    <Trophy className={trophy.className} label={trophy.label} image={reward.image} />
                    {trophy.description && (
                        <HTML innerClassName="aha__final-text" body={trophy.description} />
                        )
                    }
                </div>
            )}

            {finalText && (
                <HTML body={finalText} />
            )}
            
            {visualizationType && (
                <Visualization percentile={scores.relative.value} type={visualizationType} rankClass={trophy.class}/>
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
            {block.theme.footer!.logos && (
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
