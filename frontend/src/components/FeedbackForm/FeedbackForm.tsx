import { useState } from "react";

import Question from "../Question/Question";
import Button from "../Button/Button";
import IButton from "@/types/Button";
import IQuestion from "@/types/Question";

interface FeedbackFormProps {
    formActive: boolean;
    form: IQuestion[];
    submitButton: IButton;
    skipButton: IButton;
    isSkippable: boolean;
    submitResult: () => void;
}

/** FeedbackForm */
const FeedbackForm = ({
    formActive,
    form,
    submitButton,
    skipButton,
    submitResult,
}: FeedbackFormProps) => {
    const [formValid, setFormValid] = useState(false);

    const onChange = (value: string | number | boolean, question_index: number) => {
        form[question_index].value = value;
        if (!submitButton) {
            submitResult();
        }
        // for every non-skippable question, check that we have a value
        const validFormElements = form.filter(formElement => {
            if (formElement.value && validateFormElement(formElement)) {
                return true;
            }
            return false;
        });
        if (validFormElements.length === form.length) setFormValid(true);
        else setFormValid(false);
    };

    function validateFormElement(formElement: IQuestion) {
        // For multiple choices in CHECKBOXES view, formElement.value is a string of comma-separated values
        if (formElement.view === "CHECKBOXES" && formElement.minValues && (formElement.value.split(",").length < formElement.minValues)) {
            return false;
        }
        return true;
    };

    return (
        <div className="aha__feedback justify-content-center">
            <form>
                {form.map((_question, index) => (
                    <Question
                        key={index}
                        id={index}
                        disabled={!formActive}
                        question={form[index]}
                        onChange={onChange}
                    />
                ))}
                {/* Continue button */}
                {submitButton && (

                    <div className="row justify-content-around">
                        {skipButton && (
                            // skip button
                            <Button
                                {...skipButton}
                                onClick={() => {
                                    submitResult();
                                }}
                                className={"=col-4 align-self-start"
                                }
                               
                            />)}
                        <Button
                            {...submitButton}
                            onClick={() => {
                                submitResult();
                            }}
                            className={
                                "submit col-4"
                            }
                            disabled={!formValid}
                        />

                    </div>

                )}
            </form>
        </div>
    );
};

export default FeedbackForm;
