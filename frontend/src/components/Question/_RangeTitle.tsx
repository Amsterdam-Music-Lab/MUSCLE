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
    const position = sliderValue * 96 / (choices.length - 1) - 48; // position from -48% to 48%
    const theme = useBoundStore((state) => state.theme);
    const colors = choices.map((value) => value.color || "");

    const getLabelColor = () : string | undefined => {
        /* return the color hex value from theme if color is defined for the current sliderValue
            If only the first and last color are defined, return a gradient for the other sliderValues
        */
        if (theme && colors[0] && colors[choices.length - 1]) {
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
