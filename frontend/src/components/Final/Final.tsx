import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "@/components/Social/Social";

import { URLS } from "@/config";
import { finalizeSession } from "../../API";
import useBoundStore from "../../util/stores";
import ParticipantLink from "../ParticipantLink/ParticipantLink";
import UserFeedback from "../UserFeedback/UserFeedback";
import FinalButton from "./FinalButton";
import { Final as FinalAction } from "@/types/Action";
import classNames from "@/util/classNames";

export interface FinalProps extends FinalAction {
    onNext: () => void;
}

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
 */
const Final = ({
    block,
    participant,
    score,
    final_text,
    action_texts,
    button,
    onNext,
    show_participant_link,
    participant_id_only,
    show_profile_link,
    social,
    feedback_info,
    points,
    rank,
    logo,
    percentile,
}: FinalProps) => {

    const session = useBoundStore((state) => state.session);
    const navigate = useNavigate();

    useEffect(() => {
        finalizeSession({ session: session!, participant });
    }, [session, participant]);

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
                <div dangerouslySetInnerHTML={{ __html: final_text }} />
            </div>
            {button && (
                <div className="text-center pt-4">
                    <FinalButton
                        button={button}
                        onNext={onNext}
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
            {show_profile_link && (
                <div className=" mt-2 d-flex justify-content-center">
                    <a className="home text-center" href={URLS.AMLHome}>
                        {action_texts.all_experiments}
                    </a>
                    <div
                        data-testid="profile-link"
                        className="home text-center"
                        onClick={() => navigate(URLS.profile)}
                    >
                        {action_texts.profile}
                    </div>
                </div>
            )}
            {show_participant_link && (
                <ParticipantLink
                    participantIDOnly={participant_id_only}
                />
            )}
            {feedback_info && (<UserFeedback
                blockSlug={block.slug}
                participant={participant}
                feedbackInfo={feedback_info}
            />)}

        </div>
    );
};

export default Final;
