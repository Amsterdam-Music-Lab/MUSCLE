import Histogram from "../Histogram/Histogram";
import CountDown from "../CountDown/CountDown";

interface AnimatedCircleContentProps {
    duration: number;
    countDownRunning?: boolean;
    histogramRunning?: boolean;
}

const AnimatedCircleContent = ({
    duration,
    countDownRunning = true,
    histogramRunning = true
}: AnimatedCircleContentProps) => {
    return (
        <>
            <CountDown duration={duration} running={countDownRunning} />
            <div className="aha__histogram-container">
                <Histogram running={histogramRunning} />
            </div>
        </>
    );
};

export default AnimatedCircleContent;
