import { useState } from "react";

import classNames from "classnames";

import ButtonArray from "./_ButtonArray";
import { RadioQuestion } from "../RadioQuestion";
import Range from "./_Range";
import TextRange from "./_TextRange";
import IconRange from "./_IconRange";
import String from "./_String";
import Checkboxes from "./_Checkboxes";
import DropDown from "./_DropDown";
import AutoComplete from "./_AutoComplete";

import IQuestion, { QuestionViews } from "@/types/Question";

export interface QuestionProps {
    question: IQuestion;
    onChange: (value: string | number | boolean, id: number) => void;
    id: number;
    disabled?: boolean;
}

/** Question is a block view that shows a question and handles storing the answer */
const Question = ({
    question,
    onChange,
    id,
    disabled = false,
}: QuestionProps) => {
    const [value, setValue] = useState(question.value || "");

    const registerChange = (value: string | number | boolean) => {
        onChange(value, id);
        setValue(value);
    };

    // render view
    const render = (view: QuestionViews) => {
        const attrs = {
            value,
            question,
            disabled,
            onChange: registerChange,
        };

        switch (view) {
            case QuestionViews.BUTTON_ARRAY:
                return <ButtonArray {...attrs} />;
            case QuestionViews.CHECKBOXES:
                return <Checkboxes {...attrs} />;
            case QuestionViews.DROPDOWN:
                return <DropDown {...attrs} />;
            case QuestionViews.AUTOCOMPLETE:
                return <AutoComplete {...attrs} />;
            case QuestionViews.RADIOS:
                return <RadioQuestion {...attrs} />;
            case QuestionViews.RANGE:
                return <Range {...attrs} />;
            case QuestionViews.TEXT_RANGE:
                return <TextRange {...attrs} />;
            case QuestionViews.ICON_RANGE:
                return <IconRange {...attrs} />;
            case QuestionViews.STRING:
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
            <h3 className={classNames(question.style)}>{question.question}</h3>
            <div className="question">{render(question.view)}</div>
            {question.expected_response &&
                /* Will only be visible when the backend settings has TESTING=True */
                <p className="expected-response">{question.expected_response}</p>
            }
        </div>
    );
};

export default Question;
