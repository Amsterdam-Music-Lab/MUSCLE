import React, { useState, useRef, useCallback } from "react";
import Playback, { BUTTON } from "../Playback/Playback";
import Question, { AUTOCOMPLETE } from "../Question/Question";
import Button from "../Button/Button";
import useSingleToArray from "../../hooks/useSingleToArray";

const RECOGNIZE = "MAIN";
const QUESTION = "QUESTION";

const defaultPlayConfig = {
    auto_play: true,
};

// Plink is an experiment view, with two stages:
// - RECOGNIZE: Play audio, ask if participant recognizes the song
// - QUESTION: Optional questions when then participant doesnt know the song
const Plink = ({
    loadState,
    section,
    mainQuestion,
    choices,
    submitLabel,
    dontKnowLabel,
    extraQuestions,
    resultId,
    onResult,
}) => {
    // Component view
    const [view, setView] = useState(RECOGNIZE);
    
    // Sections array required for Playback component
    const sections = useSingleToArray(section);

    // Question data storage
    const [mainQuestionValue, setMainQuestionValue] = useState("");
    const extraQuestionValues = useRef([]);

    // Submit data
    const submitData = useCallback(() => {
        onResult(
            {
                result_id: resultId,
                main_question: mainQuestionValue,
                extra_questions: extraQuestionValues.current,
            },
            true
        );
    }, [mainQuestionValue, resultId, onResult]);

    // extra Questions mode
    // =================================
    const [questionIndex, setQuestionIndex] = useState(0);

    // Start the questions mode
    const startQuestions = useCallback(() => {
        // If there are not questions, just submit
        if (extraQuestions.length === 0) {
            submitData();
            return;
        }
        setMainQuestionValue("");
        setView(QUESTION);
    }, [submitData, extraQuestions]);

    // Load next question, or submit if there are no more questions
    const nextQuestion = () => {
        // Add value
        extraQuestionValues.current.push(questionValue);

        // Clear
        setQuestionValue("");

        // Next
        const nextIndex = questionIndex + 1;

        // No more questions, submit data
        if (nextIndex >= extraQuestions.length) {
            submitData();
            return;
        }

        // Go to next
        setQuestionIndex(nextIndex);
    };

    // Keep track of current extra question value
    const [questionValue, setQuestionValue] = useState("");

    // Render component based on view
    const getView = (view) => {
        switch (view) {
            case RECOGNIZE:
                return (
                    <div className="d-flex flex-column">
                        <Playback
                            playerType={BUTTON}
                            sections={sections}
                            playConfig={defaultPlayConfig}
                        />
                        <Question
                            question={{
                                view: AUTOCOMPLETE,
                                choices: choices,
                                question: mainQuestion,
                            }}
                            onChange={setMainQuestionValue}
                            id="main"
                        />
                        <div className="d-flex justify-content-between pt-4">
                            {/* Don't know */}
                            <Button
                                title={dontKnowLabel}
                                className="btn-gray"
                                onClick={startQuestions}
                            />
                            {/* Submit main question answer */}
                            <Button
                                title={submitLabel}
                                className="btn-primary"
                                active={mainQuestionValue}
                                onClick={submitData}
                            />
                        </div>
                    </div>
                );
            case QUESTION:
                return (
                    <div
                        key={extraQuestions[questionIndex].key}
                        className="d-flex flex-column align-items-center"
                    >
                        <Question
                            question={extraQuestions[questionIndex]}
                            onChange={setQuestionValue}
                            id="sub"
                            emphasizeTitle={true}
                        />
                        <Button
                            active={!!questionValue}
                            title={submitLabel}
                            className="btn-primary mt-4"
                            onClick={nextQuestion}
                        />
                    </div>
                );
            default:
                return <div>Unknown view: {view}</div>;
        }
    };

    return <div className="aha__plink">{getView(view)}</div>;
};

export default Plink;
