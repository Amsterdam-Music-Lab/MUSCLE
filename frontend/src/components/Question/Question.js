import React, { useState } from "react";

import ButtonArray from "./_ButtonArray";
import Radios from "./_Radios";
import Range from "./_Range";
import TextRange from "./_TextRange";
import String from "./_String";
import Checkboxes from "./_Checkboxes";
import DropDown from "./_DropDown";

const BUTTON_ARRAY = "BUTTON_ARRAY";
const CHECKBOXES = "CHECKBOXES";
const DROPDOWN = "DROPDOWN";
const RADIOS = "RADIOS";
const RANGE = "RANGE";
const TEXT_RANGE = "TEXT_RANGE";
const STRING = "STRING";

// Question is an experiment view that shows a question and handles storing the answer
const Question = ({ question, onChange, id, active, style,emphasizeTitle }) => {
    const [value, setValue] = useState(question.value || "");

    const registerChange = (value) => {
        onChange(value, id);
        setValue(value);
    }

    // render view
    const render = (view) => {
        const attrs = {
            value,
            question,
            active,
            style,
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
            case RADIOS:
                return <Radios {...attrs} />;
            case RANGE:
                return <Range {...attrs} />;
            case TEXT_RANGE:
                return <TextRange {...attrs} />;
            case STRING:
                return <String {...attrs} />;

            default:
                return <div>Unknown question view {view}</div>;
        }
    };

    return (
        <div className="aha__question">
            <div className="question">{render(question.view)}</div>
        </div>
    );
};

export default Question;
