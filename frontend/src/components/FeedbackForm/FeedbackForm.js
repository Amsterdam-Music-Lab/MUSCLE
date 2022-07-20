import React, { useState, useRef } from "react";
import Question from "../Question/Question";
import Button from "../Button/Button";

// FeedbackForm
const FeedbackForm = ({
    formActive,
    form,
    buttonLabel,
    skipLabel,
    isSkippable,
    onResult,
    emphasizeTitle = false,
}) => {
    const isSubmitted = useRef(false);
    const showSubmitButtons =
        form.filter((formElement) => formElement.submits).length === 0;

    const [formValid, setFormValid] = useState(false);

    const onSubmit = () => {
        // Prevent double submit
        if (isSubmitted.current){
            console.error("Multiple submits detected");
            return;
        }
        isSubmitted.current = true;

        // Callback onResult with question data
        onResult({
            form,
        });
    };

    const onChange = (value, question_key) => {
        form[question_key].value = value;
        if (form[question_key].submits) {
            onSubmit(form);
        }
        if (
            form.filter((formElement) => formElement.value).length ===
            form.length
        ) {
            setFormValid(true);
        }
    };

    return (
        <div className="aha__feedback d-flex justify-content-center">
            <form>
                {Object.keys(form).map((index) => (
                    <Question
                        key={index}
                        id={index}
                        active={formActive}
                        question={form[index]}
                        onChange={onChange}
                        emphasizeTitle={emphasizeTitle}
                    />
                ))}
                {/* Continue button */}
                {showSubmitButtons && formValid && (
                    <div className="center">
                        <Button
                            onClick={() => {
                                onSubmit();
                            }}
                            className={
                                "btn-primary anim anim-fade-in anim-speed-500"
                            }
                            title={buttonLabel}
                        />
                    </div>
                )}

                {/* Skip button */}
                {/* Only show skip-button when there is no value */}
                {isSkippable && showSubmitButtons && (
                    <div className="center">
                        <Button
                            onClick={() => {
                                onSubmit();
                            }}
                            className={
                                "btn-gray anim anim-fade-in anim-speed-500"
                            }
                            title={skipLabel}
                        />
                    </div>
                )}
            </form>
        </div>
    );
};

export default FeedbackForm;
