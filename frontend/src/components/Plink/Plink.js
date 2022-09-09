import React, { useState, useRef, useCallback } from "react";
import Playback, { BUTTON } from "../Playback/Playback";
import Question, { AUTOCOMPLETE, DROPDOWN } from "../Question/Question";
import Explainer from "../Explainer/Explainer";
import Button from "../Button/Button";
import useSingleToArray from "../../hooks/useSingleToArray";

const RECOGNIZE = "MAIN";
const QUESTION_INTRO = "QUESTION_INTRO";
const QUESTION = "QUESTION";

const defaultPlayConfig = {
    auto_play: true,
};

// Plink is an experiment view, with two stages:
// - RECOGNIZE: Play audio, ask if participant recognizes the song
// - QUESTION_INTRO: A short introduction to the extra questions, shown once
// - QUESTION: Optional questions when then participant doesnt know the song
const Plink = ({
    section,
    mainQuestion,
    choices,
    submitLabel,
    dontKnowLabel,
    extraQuestions,
    extraQuestionsIntro,
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

        // Optionally show the extra question intro text
        if (showExtraQuestionsIntroOnce()){
            setView(QUESTION_INTRO);
            return;
        }

        // Show questions
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
                        <div className="mb-3">
                            <Playback
                                playerType={BUTTON}
                                sections={sections}
                                playConfig={defaultPlayConfig}
                            />
                        </div>
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
            case QUESTION_INTRO:
                return (
                    <Explainer {...extraQuestionsIntro} onNext={startQuestions} />
                )
            case QUESTION:
                return (
                    <div
                        key={extraQuestions[questionIndex].key}
                        className="plink-extra-questions d-flex flex-column align-items-center"
                    >
                        <div className="mb-3">
                            <Playback
                                playerType={BUTTON}
                                sections={sections}
                            />
                        </div>
                        <Question                            
                            question={window.innerWidth > 500 ? extraQuestions[questionIndex] : Object.assign({}, extraQuestions[questionIndex], {"view": DROPDOWN})}
                            onChange={setQuestionValue}
                            id="sub"
                        />
                        <Button
                            active={!!questionValue}
                            title={submitLabel}
                            className="btn-primary mt-3"
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


// Retrieve if the extra questions intro should be shown
// Also set the value so the intro only shows one time per session
const showExtraQuestionsIntroOnce = ()=>{
    const storageKey = 'aml_toontjehoger_plink_extra_question_intro'
    const doShow = null === window.sessionStorage.getItem(storageKey);

    if (doShow){
        window.sessionStorage.setItem(storageKey, 'shown')
    }

    return doShow;
}

export default Plink;
