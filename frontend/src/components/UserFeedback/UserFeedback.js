import React, { useState} from 'react';

import { postFeedback } from '../../API';
import Button from '../Button/Button';
import HTML from '../HTML/HTML';
import classNames from '@/util/classNames';

const UserFeedback = ({experimentSlug, participant, feedbackInfo, inline = true}) => {
    const [value, setValue] = useState('');
    const [showForm, setShowForm] = useState(true);

    const giveFeedback = async () => {
        const data = {
            experimentSlug: experimentSlug,
            feedback: value,
            participant
        }
        await postFeedback(data);
        setShowForm(false);
        return;
    }

    const handleChange = (event) => {
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
                        type="text"
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
)};

export default UserFeedback;
