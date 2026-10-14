const Visualization = ({percentile, type, rankClass}: {percentile: number, type: string, rankClass: string}) => {
    return (  
        <div className="aha__final-rank-bar-section">
            <div data-testid="final-rank-bar-cursor" className="aha__final-rank-bar-cursor" style={{ left: `${percentile}%` }}></div>
        </div>
    )
}

export default Visualization;