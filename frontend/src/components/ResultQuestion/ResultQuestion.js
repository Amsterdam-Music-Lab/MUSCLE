import React from "react";
import Question from "../Question/Question";
import Button from "../Button/Button";

// ResultQuestion is a view that shows a question and returns the data to the onResult callback
// This view can be used to get data during an experiment, instead of storing it to the user profile
const ResultQuestion = ({ question, button_label, skip_label, onResult }) => {
    const onSubmit = (value) => {
        // Callback onResult with question data
        onResult({
            question: {
                key: question.key,
                answer: value,
            },
        });
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

export default ResultQuestion;
