import { lazy, Suspense, useState } from "react";
import classNames from "classnames";

import Loading from "@/components/Loading/Loading";
const AutoComplete = lazy(() => import("./_AutoComplete"));
const ButtonArray = lazy(() => import("./_ButtonArray"));
const Checkboxes = lazy(() => import("./_Checkboxes"));
const DropDown = lazy(() => import("./_DropDown"));
const Number = lazy(() => import("./_Number"));
const Radios = lazy(() => import("./_Radios"));
const Range = lazy(() => import("./_Range"));
const String = lazy(() => import("./_String"));
const TextRange = lazy(() => import("./_TextRange"));
import IQuestion, { QuestionViews } from "@/types/Question";

interface FormProps {
    question: IQuestion;
    onChange: (value: string | number) => void;
    disabled: boolean;
}

/** Question is a block view that shows a question and handles storing the answer */
const Question = ({
    question,
    onChange,
    disabled = false,
}: FormProps) => {

    const [value, setValue] = useState(question.value || "");

    const registerChange = (newValue: string | number) => {
        onChange(newValue);
        setValue(newValue);
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
            case QuestionViews.AUTOCOMPLETE:
                return <AutoComplete {...attrs} />;
            case QuestionViews.BUTTON_ARRAY:
                return <ButtonArray {...attrs} />;
            case QuestionViews.CHECKBOXES:
                return <Checkboxes {...attrs} />;
            case QuestionViews.DROPDOWN:
                return <DropDown {...attrs} />;
            case QuestionViews.NUMBER:
                return <Number {...attrs} />;
            case QuestionViews.RADIOS:
                return <Radios {...attrs} />;
            case QuestionViews.RANGE:
                return <Range {...attrs} />;
            case QuestionViews.TEXT_RANGE:
                return <TextRange {...attrs} />;
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
            <h3 className={classNames(question.style)}>{question.text}</h3>
            <div className={classNames("question", {disabled: disabled})}>
                <Suspense fallback={<Loading/>}>
                    {render(question.view)}
                </Suspense>
            </div>
        </div>
    );
};

export default Question;
