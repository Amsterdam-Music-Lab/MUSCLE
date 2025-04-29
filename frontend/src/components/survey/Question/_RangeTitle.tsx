import type Question from "@/types/Question";

import { renderLabel } from "@/util/label";

interface RangeTitleProps {
    question: Question;
    value: string;
    sliderValue: number;
    emptyValue: boolean;
    changePosition?: boolean;
}

const RangeTitle = ({ question, value, sliderValue, emptyValue, changePosition = false }: RangeTitleProps) => {

    if (!question.choices || Object.keys(question.choices).length === 0) {
        throw new Error("RangeTitle question must have choices");
    }

    const nChoices = Object.keys(question.choices).length - 1;
    const position = - (nChoices - sliderValue * 2) / nChoices * 44;
    return (
        <div>
            <h4 className="current-value" style={{ position: 'relative', left: changePosition ? `${position}%` : '0%' }}>
                {emptyValue ? (
                    renderLabel("fa-arrows-left-right", "fa-2x")
                ) : (
                    <span className={`is-${value}`}> {renderLabel(question.choices[value], "fa-2x")}</span>
                )
                }
            </h4>
        </div>
    )
}

export default RangeTitle;
