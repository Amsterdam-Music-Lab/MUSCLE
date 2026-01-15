import { renderLabel } from "../../util/label";
import Question from "@/types/Question";

interface RangeTitleProps {
    question: Question;
    value: string;
    sliderValue: number;
    emptyValue: boolean;
    changePosition?: boolean;
}

const RangeTitle = ({ question, value, sliderValue, emptyValue, changePosition = false }: RangeTitleProps) => {

    const choices = question.choices;

    if (!choices || choices.length === 0) {
        throw new Error("RangeTitle question must have choices");
    }

    const nChoices = choices.length - 1;
    const position = - (nChoices - sliderValue * 2) / nChoices * 44;
    return (
        <div>
            <h4 className="current-value" style={{ position: 'relative', left: changePosition ? `${position}%` : '0%' }}>
                {emptyValue ? (
                    renderLabel("fa-arrows-left-right", "fa-2x")
                ) : (
<<<<<<< HEAD
                    <span className={`is-${value}`}> {renderLabel(choices.find(choice => choice.value === value).label, "fa-2x")}</span>
=======
                    <span className={`is-${value}`}> {renderLabel(choices.pick(choice => choice.value === value), "fa-2x")}</span>
>>>>>>> a27a92b23d3b8de2e6a60b899614c6233d1a187c
                )
                }
            </h4>
        </div>
    )
}

export default RangeTitle;
