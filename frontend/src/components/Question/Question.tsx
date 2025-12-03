import { useState } from "react";

import classNames from "classnames";

import AutoComplete from "./_AutoComplete";
import ButtonArray from "./_ButtonArray";
import Checkboxes from "./_Checkboxes";
import DropDown from "./_DropDown";
import IconRange from "./_IconRange";
import Number from "./_Number";
import Radios from "./_Radios";
import Range from "./_Range";
import String from "./_String";
import TextRange from "./_TextRange";

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
                return <Radios {...attrs} />;
            case QuestionViews.RANGE:
                return <Range {...attrs} />;
            case QuestionViews.TEXT_RANGE:
                return <TextRange {...attrs} />;
            case QuestionViews.ICON_RANGE:
                return <IconRange {...attrs} />;
            case QuestionViews.STRING:
                return <String {...attrs} />;
            case QuestionViews.NUMBER:
                return <Number {...attrs} />;

            default:
                return <div>Unknown question view {view}</div>;
        }
    };

    return (
        <div className="aha__question">
            {question.explainer && (
                <p className="explainer">{question.explainer}</p>
            )}
            <h3 className={classNames(question.style)}>{question.text}</h3>
            <div className="question">{render(question.view)}</div>
        </div>
    );
};

export default Question;
