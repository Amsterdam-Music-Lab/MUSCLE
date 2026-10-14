import classNames from "classnames";

import { getTrophyColor } from "@/util/stylingHelpers"
import { Trophy as TrophyProps} from "@/types/Action";

// Trophy shows a reward earned by the participant, colored according to their performance
const Trophy = ({ className, label, image= "cup" }: TrophyProps) => {
    const trophyColor = className? getTrophyColor(className): "";

    return (
        <div
            className={classNames("aha__trophy", className)}
            style={{backgroundColor: trophyColor, boxShadow: `13px 0 64px ${trophyColor}`}}
            data-testid="trophy"
        >
            <div className={classNames("aha__trophy-image", image)} data-testid="trophy-animation" />
            <h4 data-testid="trophy-text">{label}</h4>
        </div >
    )
};

export default Trophy;
