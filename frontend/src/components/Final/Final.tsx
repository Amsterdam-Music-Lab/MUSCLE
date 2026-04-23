import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "@/components/Social/Social";
import Button from "../Button/Button";
import ParticipantLink from "../ParticipantLink/ParticipantLink";
import UserFeedback from "../UserFeedback/UserFeedback";
import FinalButton from "./FinalButton";
import { FinalAction, SharedActionProps } from "@/types/Action";
import classNames from "@/util/classNames";
import useBoundStore from "@/util/stores";
import { URLS } from '@/API';

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
const Final = (props: FinalAction & SharedActionProps) => {
    const {
        block,
        participant,
        score,
        finalText,
        actionTexts,
        button,
        onNext,
        showParticipantLink,
        participantIDOnly,
        showProfileLink,
        social,
        feedbackInfo,
        points,
        rank,
        logo,
        percentile
    } = props;
    const session = useBoundStore((state) => state.session);
    const navigate = useNavigate();

    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            {rank && (
                <div className="text-center">
                    <Rank cup={{ className: rank?.class, text: rank.text }} score={{ score, label: points }} />
                </div>
            )}
            {(typeof percentile === 'number' && percentile >= 0 && percentile <= 100) && (
                <div className={classNames("aha__final-rank-bar-section", rank?.class)}>
                    <div data-testid="final-rank-bar-cursor" className="aha__final-rank-bar-cursor" style={{ left: `${percentile}%` }}></div>
                </div>
            )}
            <div className="aha__final-text">
                <div dangerouslySetInnerHTML={{ __html: finalText }} />
            </div>
            {button && (
                <div className="text-center pt-4">
                    <Button
                        {...button}
                        onClick={onNext}
                    />
                </div>
            )}
            {logo && (
                <div className="text-center pt-4">
                    <a href={logo.link}>
                        <img src={logo.image} width="100%" alt="Logo" />
                    </a>
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
                blockSlug={block.slug}
                participant={participant}
                feedbackInfo={feedbackInfo}
            />)}

        </div>
    );
};

export default Final;
