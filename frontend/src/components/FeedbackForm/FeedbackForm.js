import React, { useState, useEffect, useRef } from "react";
import Question from "../Question/Question";
import Button from "../Button/Button";


// FeedbackForm
const FeedbackForm = ({ formActive, form, buttonLabel, skipLabel, onResult }) => {

    const showSubmitButtons = form.filter( formElement => formElement.submits).length === 0;
    
    // if the form is longer than one question, disable the submit button until all form questions have been filled
    const [submitActive, setSubmitActive] = useState(form.length<2);
    
    const onSubmit = () => {
        // Callback onResult with question data
        onResult({
            form
        });
    };

    const onChange = (value, question_key) => {
        form[question_key].value = value;
        if (form.filter( formElement => formElement.value).length === form.length) {
            setSubmitActive(true);
        }
        if (form[question_key].submits) {
            onSubmit(form);
        }
    };


    return (
        <div className="aha__feedback">
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
                <center>
                {showSubmitButtons && (
                <Button
                    onClick={() => {
                        onSubmit(form);
                    }}
                    className={"btn-primary"}
                    title={buttonLabel}
                    active={submitActive}
                />)}

                {/* Skip button */}
                {/* Only show skip-button when there is no value */}
                {skipLabel && showSubmitButtons && (
                    <Button
                        onClick={() => {
                            onSubmit("");
                        }}
                        className={"btn-gray anim anim-fade-in anim-speed-500"}
                        title={skipLabel}
                    />
                )}
                </center>
            </form>
        </div>
    )
}

export default FeedbackForm;