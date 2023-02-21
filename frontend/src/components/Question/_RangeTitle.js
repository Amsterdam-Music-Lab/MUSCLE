import React from "react";
import classNames from "classnames";

import { renderLabel } from "../../util/label";

const RangeTitle = ({emphasizeTitle, question, value, sliderValue, emptyValue}) => {
    return (
        <div>
        <h3 className={classNames({title: emphasizeTitle})}>{question.question}</h3>

            { question.config && question.config.icons ?
                ( emptyValue ?
                    <h4 className="current-value"> {renderLabel("fa-arrows-left-right", "2x")} </h4>
                    :
                    <h4 className="current-value"> <span style={{color: question.config.colors[sliderValue]}}> {renderLabel(question.choices[value], "2x")}</span></h4>
                )
                :
                <h4 className="current-value">{emptyValue ? "↔" : question.choices[value]}</h4>
            }
        </div> 
    )
}

export default RangeTitle;
    