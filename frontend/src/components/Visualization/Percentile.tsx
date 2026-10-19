const Percentile = ({value, label="%", backgroundColor}: {value: number, label: string, backgroundColor: string}) => {
    return (  
        <div className="aha__final-rank-bar-section" style={{borderColor: `${backgroundColor}`}}>
            <div data-testid="final-rank-bar-cursor" className="aha__final-rank-bar-cursor" style={{ left: `${value}%`, background: `${backgroundColor}`}}></div>
        </div>
    )
}

export default Percentile;