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
import ISocial from "@/types/Social";
import Block, { FeedbackInfo } from "@/types/Block";
import Participant from "@/types/Participant";

export interface FinalProps {
    block: Block;
    participant: Participant;
    score: number;
    final_text: string | TrustedHTML;
    action_texts: {
        all_experiments: string;
        profile: string;
        play_again: string;
    }
    button: {
        text: string;
        link: string;
    };
    onNext: () => void;
    show_participant_link: boolean;
    participant_id_only: boolean;
    show_profile_link: boolean;
    social: ISocial;
    feedback_info?: FeedbackInfo;
    points: string;
    rank: {
        class: string;
        text: string;
    }
    logo: {
        image: string;
        link: string;
    };
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
    logo
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
                    <Rank cup={{ className: rank.class, text: rank.text }} score={{ score, label: points }} />
                </div>
            )}
            <div className="text-center">
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
