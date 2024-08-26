import Histogram from "../Histogram/Histogram";
import CountDown from "../CountDown/CountDown";

interface ListenCircleProps {
    duration: number;
    countDownRunning?: boolean;
    histogramRunning?: boolean;
}

const ListenCircle = ({
    duration,
    countDownRunning = true,
    histogramRunning = true
}: ListenCircleProps) => {
    return (
        <>
            <CountDown duration={duration} running={countDownRunning} />
            <div className="aha__histogram-container">
                <Histogram running={histogramRunning} />
            </div>
        </>
    );
};

export default ListenCircle;
