import Percentile from "@/components/Visualization/Percentile";
import ProgressBar from "@/components/ProgressBar/ProgressBar";
import { getTrophyColor } from "@/util/stylingHelpers";

const Visualization = ({value, label, type, className}: {value: number, label: string, type: string, className: string}) => {
    const backgroundColor = className? getTrophyColor(className): "";
    
    const render = (type: string) => {
        const props = {
            value,
            label,
            backgroundColor
        }
        switch(type) {
            case "progress":
                return <ProgressBar {...props} />
            default:
                return <Percentile {...props} />
        }   
    }
    
    return (  
        <div className="aha__result-visualization">
            {render(type)}
        </div>
    )
}

export default Visualization;