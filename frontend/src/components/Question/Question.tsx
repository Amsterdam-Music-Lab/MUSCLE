import React, { useState } from "react";

import classNames from "classnames";

import ButtonArray from "./_ButtonArray";
import Radios from "./_Radios";
import Range from "./_Range";
import TextRange from "./_TextRange";
import IconRange from "./_IconRange";
import String from "./_String";
import Checkboxes from "./_Checkboxes";
import DropDown from "./_DropDown";
import AutoComplete from "./_AutoComplete";

export const AUTOCOMPLETE = "AUTOCOMPLETE";
export const BUTTON_ARRAY = "BUTTON_ARRAY";
export const CHECKBOXES = "CHECKBOXES";
export const DROPDOWN = "DROPDOWN";
export const RADIOS = "RADIOS";
export const RANGE = "RANGE";
export const TEXT_RANGE = "TEXT_RANGE";
export const ICON_RANGE = "ICON_RANGE";
export const STRING = "STRING";

interface Question {
    view: string;
    value: any;
    style: any;
    question: string;
    explainer: string;
    expected_response: string;
}

interface QuestionProps {
    question: Question;
    onChange: (value: any, id: string) => void;
    id: string;
    active: boolean;
    emphasizeTitle?: boolean;
}


// Question is an experiment view that shows a question and handles storing the answer
const Question = ({
    question,
    onChange,
    id,
    disabled = false,
    emphasizeTitle = false,
}: QuestionProps) => {
    const [value, setValue] = useState(question.value || "");

    const registerChange = (value) => {
        onChange(value, id);
        setValue(value);
    };

    // render view
    const render = (view) => {
        const attrs = {
            value,
            question,
            disabled,
            style: question.style,
            emphasizeTitle,
            onChange: registerChange,
        };

        switch (view) {
            case BUTTON_ARRAY:
                return <ButtonArray {...attrs} />;
            case CHECKBOXES:
                return <Checkboxes {...attrs} />;
            case DROPDOWN:
                return <DropDown {...attrs} />;
            case AUTOCOMPLETE:
                return <AutoComplete {...attrs} />;
            case RADIOS:
                return <Radios {...attrs} />;
            case RANGE:
                return <Range {...attrs} />;
            case TEXT_RANGE:
                return <TextRange {...attrs} />;
            case ICON_RANGE:
                return <IconRange {...attrs} />;
            case STRING:
                return <String {...attrs} />;

            default:
                return <div>Unknown question view {view}</div>;
        }
    };

    return (
        <div className="aha__question">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className={classNames({title: emphasizeTitle})}>{question.question}</h3>
            <div className="question">{render(question.view)}</div>
            {question.expected_response &&
                /* Will only be visible when the backend settings has TESTING=True */
                <p className="expected-response">{question.expected_response}</p>
            }
        </div>
    );
};

export default Question;
