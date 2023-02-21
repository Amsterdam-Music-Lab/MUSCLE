import React from "react";

import { renderLabel } from "../../util/label";

const RangeTitle = ({question, value, sliderValue, emptyValue, changePosition=false}) => {
    const nChoices = Object.keys(question.choices).length - 1;
    const position = - (nChoices - sliderValue * 2) / nChoices  * 115;
    return (
        <div>
            <h4 className="current-value" style={{position: 'relative', left: changePosition? position : '50px'}}>
            { emptyValue ? (
                renderLabel("fa-arrows-left-right", "2x")
            ) : (
                <span style={{color: question.config.colors[sliderValue]}}> {renderLabel(question.choices[value], "2x")}</span>
            )
            }
            </h4>
        </div> 
    )
}

export default RangeTitle;
    