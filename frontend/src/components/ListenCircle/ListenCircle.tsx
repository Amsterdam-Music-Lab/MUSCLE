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
                <Histogram
                    running={histogramRunning}

                    // Set random to true (and interval to 200) temporarily to see the animation
                    // TODO: Remove random and interval props and fix Histogram to always use
                    // random bars when the audio play_method is not "BUFFER"
                    random={true}
                    interval={200}
                />
            </div>
        </>
    );
};

export default ListenCircle;
