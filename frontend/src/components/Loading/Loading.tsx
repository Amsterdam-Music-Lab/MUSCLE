import Circle from "../Circle/Circle";

export interface LoadingProps {
    duration?: number;
    loadingText?: string;
}

/**
 * Loading is a block view that shows a loading screen
 * It is normally set by code during loading of data
 */
const Loading = ({ duration = 2, loadingText = '' }: LoadingProps) => {
    return (
        <div className="aha__loading d-flex justify-content-center" data-testid="loading">
            <Circle
                duration={duration}
                startTime={0.1 * duration}
                running={false}
            />
            <div className="content">
                <h4>{loadingText}</h4>
            </div>
        </div>
    );
};

export default Loading;
