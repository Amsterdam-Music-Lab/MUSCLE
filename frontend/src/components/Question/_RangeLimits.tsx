import { renderLabel } from "../../util/label";

interface RangeLimitsProps {
    minVal: string | number;
    maxVal: string | number;
}

const RangeLimits = ({ minVal, maxVal }: RangeLimitsProps) => {
    return (
        <div className="limits">
            <div>
                <span className="min">{renderLabel(minVal.toString())}</span>
                <span className="max">{renderLabel(maxVal.toString())}</span>
            </div>
        </div>
    )
};

export default RangeLimits;
