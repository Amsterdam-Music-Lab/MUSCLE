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
        if (isSubmitted.current) {
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
        // for every non-skippable question, check that we have a value
        const validFormElements = form.filter(formElement => {
            if (formElement.is_skippable || (formElement.value && validateFormElement(formElement))) {
                return true;
            }
            return false;
        });
        if (validFormElements.length === form.length) setFormValid(true);
        else setFormValid(false);
    };

    function validateFormElement(formElement) {
        // For multiple choices in CHECKBOXES view, formElement.value is a string of comma-separated values
        if (formElement.view == "CHECKBOXES" && formElement.min_values && (formElement.value.split(",").length < formElement.min_values)) {
            return false;
        }
        return true;
    };

    return (
        <div className="aha__feedback justify-content-center">
            <form>
                {Object.keys(form).map((index) => (
                    <Question
                        key={index}
                        id={index}
                        disabled={!formActive}
                        question={form[index]}
                        onChange={onChange}
                        emphasizeTitle={emphasizeTitle}
                    />
                ))}
                {/* Continue button */}
                {showSubmitButtons && (

                    <div className="row justify-content-around">
                        {isSkippable && (
                            // skip button
                            <Button
                                onClick={() => {
                                    onSubmit();
                                }}
                                className={"btn-gray col-4 align-self-start"
                                }
                                title={skipLabel}
                            />)}
                        <Button
                            onClick={() => {
                                onSubmit();
                            }}
                            className={
                                "submit col-4"
                            }
                            disabled={!formValid}
                            title={buttonLabel}
                        />

                    </div>

                )}
            </form>
        </div>
    );
};

export default FeedbackForm;
