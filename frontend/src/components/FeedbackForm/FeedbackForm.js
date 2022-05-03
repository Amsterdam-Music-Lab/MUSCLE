import React, { useState } from "react";
import Question from "../Question/Question";
import Button from "../Button/Button";


// FeedbackForm
const FeedbackForm = ({ formActive, form, buttonLabel, skipLabel, isSkippable, onResult }) => {

    const showSubmitButtons = form.filter( formElement => formElement.submits).length == 0;

    const [formValid, setFormValid] = useState(false);
    
    const onSubmit = () => {
        // Callback onResult with question data
        onResult({
            form
        });
    };

    const onChange = (value, question_key) => {
        console.log(form[question_key].value);
        form[question_key].value = value;
        if (form[question_key].submits) {
            onSubmit(form);
        }
        if (form.filter( formElement => formElement.value ) === form.length) {
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
                    />
                )
                )}
                {/* Continue button */}
                {showSubmitButtons && formValid && (
                <Button
                    onClick={() => {
                        onSubmit();
                    }}
                    className={"btn-primary anim anim-fade-in anim-speed-500"}
                    title={buttonLabel}
                />)}

                {/* Skip button */}
                {/* Only show skip-button when there is no value */}
                {isSkippable && showSubmitButtons && (
                    <Button
                        onClick={() => {
                            onSubmit("");
                        }}
                        className={"btn-gray anim anim-fade-in anim-speed-500"}
                        title={skipLabel}
                    />
                )}
            </form>
        </div>
    )
}

export default FeedbackForm;