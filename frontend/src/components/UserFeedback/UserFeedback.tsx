import React, { useState } from 'react';

import { postFeedback } from '../../API';
import Button from '../Button/Button';
import HTML from '../HTML/HTML';
import classNames from '@/util/classNames';
import { FeedbackInfo } from '@/types/Block';
import Participant from "@/types/Participant";

interface UserFeedbackProps {
    blockSlug: string;
    participant: Participant;
    feedbackInfo: FeedbackInfo;
    inline?: boolean;
}

const UserFeedback = ({ blockSlug, participant, feedbackInfo, inline = true }: UserFeedbackProps) => {
    const [value, setValue] = useState('');
    const [showForm, setShowForm] = useState(true);

    const giveFeedback = async () => {
        const data = {
            blockSlug,
            feedback: value,
            participant
        }
        await postFeedback(data);
        setShowForm(false);
        return;
    }

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setValue(event.target.value);
    }

    const orientationClassNames = inline ? '' : 'aha__user-feedback--vertical'

    return (
        <div className={classNames("aha__user-feedback", orientationClassNames)}>
            {showForm === true ? (
                <div className='user-feedback__wrapper'>
                    <div className='user-feedback__header text-center'>{feedbackInfo.header}</div>
                    <div className="user-feedback__form">
                        <textarea
                            className="user-feedback__input"
                            onChange={handleChange}
                            value={value}
                        ></textarea>
                        <Button
                            title={feedbackInfo.button}
                            className={"user-feedback__button btn-primary anim anim-fade-in anim-speed-500"}
                            onClick={giveFeedback}
                        />
                    </div>
                    <HTML body={feedbackInfo.contact_body}></HTML>
                </div>
            ) : (<h4 className="d-flex justify-content-center">{feedbackInfo.thank_you}</h4>)}
        </div>
    )
};

export default UserFeedback;
