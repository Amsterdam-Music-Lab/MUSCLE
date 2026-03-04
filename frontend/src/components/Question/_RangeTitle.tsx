import { Choice } from "@/types/Question";
import { renderLabel } from "@/util/label";
import { getGradientColor } from "@/util/gradient";
import useBoundStore from "@/util/stores";

interface RangeTitleProps {
    choices: Choice[];
    sliderValue: number;
    emptyValue: boolean;
    changePosition?: boolean;
}

const RangeTitle = ({ choices, sliderValue, emptyValue, changePosition = false }: RangeTitleProps) => {
    console.log(sliderValue, choices.length)
    const position = sliderValue * 96 / (choices.length - 1) - 48; // position in percent, with 2 % on each side as margin
    console.log(position);
    const theme = useBoundStore((state) => state.theme);
    const colors = choices.map((value) => value.color || "");

    const getLabelColor = () => {
        if (theme && colors[0]) {
            if (theme[colors[sliderValue]]) {
                return theme[colors[sliderValue]];
            } else {
                const minColor = theme[colors[0]];
                const maxColor = theme[colors[choices.length - 1]];
                return getGradientColor(minColor, maxColor, 0, choices.length, sliderValue)
            }
        }
    }

    const labelColor = getLabelColor();

    return (
        <div>
            <h4 className="current-value" style={{ position: 'relative', left: changePosition ? `${position}%` : '0%' }}>
                {emptyValue ? (
                    renderLabel("↔", "fa-2x")
                ) : (
                    <span style={{color: labelColor || "white"}}> {renderLabel(choices[sliderValue].label, "fa-2x")}</span>
                )
                }
            </h4>
        </div>
    )
}

export default RangeTitle;
