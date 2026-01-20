import { renderLabel } from "../../util/label";

interface RangeLimitsProps {
    minVal: string;
    maxVal: string;
}

const RangeLimits = ({ minVal, maxVal }: RangeLimitsProps) => {
    return (
        <div className="limits">
            <div>
                <span className="min">{renderLabel(minVal)}</span>
                <span className="max">{renderLabel(maxVal)}</span>
            </div>
        </div>
    )
};

export default RangeLimits;
