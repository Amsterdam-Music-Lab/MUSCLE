import React, { useState} from 'react';

import { postFeedback } from '../../API';
import Button from '../Button/Button';
import HTML from '../HTML/HTML';

const UserFeedback = ({experimentSlug, participant, feedbackInfo}) => {
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
    
    return (
        <div className="aha__user-feedback">
        {showForm === true ? (
            <div className='user-feedback__wrapper'>
                <div className='user-feedback__header text-center'>{feedbackInfo.header}</div>
                <div className="user-feedback__form d-flex justify-content-center">
                    <textarea
                        className="user-feedback__input"
                        type="text"
                        onChange={handleChange}
                        value={value}
                    ></textarea>
                    <Button
                        title={feedbackInfo.button}
                        className={"btn-primary anim anim-fade-in anim-speed-500"}
                        onClick={giveFeedback}
                    />
                </div>
                <HTML body={feedbackInfo.contact_body}></HTML>
            </div>
        ) : (<h4 className="d-flex justify-content-center">{feedbackInfo.thank_you}</h4>)}
        </div>
)};

export default UserFeedback;