import React from "react";
import { createProfile } from "../../API.js";
import Question from "../Question/Question";
import Button from "../Button/Button.js";

// ProfileQuestion is a view that shows a question and handles storing the answer to the profile
// When the answer is stored, onNext is called to continue to the next round
const ProfileQuestion = ({ question, session, participant, button_label, skip_label, onNext }) => {
    const onSubmit = async (value) => {
        // Send data to server
        const result = await createProfile({
            question: question.key,
            answer: question.value,
            session: session.id,
            participant,
        });

        // Log error when createProfile failed
        if (!result || !result.status === "ok") {
            console.error("Could not store question");
        }

        // Continue
        onNext();
    };

    const onChange = (value) => {
        question.value = value;
    }

    return (
        <div>
            <Question question={question} onChange={onChange}/>
            {/* Continue button */}
            <Button
                onClick={() => {
                    onSubmit();
                }}
                className={"btn-primary anim anim-fade-in anim-speed-500"}
                title={button_label}
            />

            {/* Skip button */}
            {/* Only show skip-button when there is no value */}
            {skip_label && (
                <Button
                    onClick={() => {
                        onSubmit("");
                    }}
                    className={"btn-gray anim anim-fade-in anim-speed-500"}
                    title={skip_label}
                />
            )}
        </div>
    )
};

export default ProfileQuestion;
