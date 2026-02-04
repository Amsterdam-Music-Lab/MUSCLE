import { renderLabel } from "../../util/label";

interface RangeTitleProps {
    labels: string[];
    sliderValue: number;
    emptyValue: boolean;
    changePosition?: boolean;
}

const RangeTitle = ({ labels, sliderValue, emptyValue, changePosition = false }: RangeTitleProps) => {
    const position = (sliderValue  - 1) * 90 / (labels.length - 1);
    return (
        <div>
            <h4 className="current-value" style={{ position: 'relative', left: changePosition ? `${position}%` : '0%' }}>
                {emptyValue ? (
                    renderLabel("↔", "fa-2x")
                ) : (
                    <span> {renderLabel(labels[sliderValue], "fa-2x")}</span>
                )
                }
            </h4>
        </div>
    )
}

export default RangeTitle;
