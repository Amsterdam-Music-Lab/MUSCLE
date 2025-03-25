import "react"

interface ScoreProps {
  score?: number;
  label?: string;
  units?: string;
  placeholder?: string;
}

/**
 * A large score with optional units as superscript and an optional label below.
 * When no score is passed, a placeholder text (default "??") is shown.
 */
const Score = ({ score, label = undefined, units = "pts", placeholder="??" }: ScoreProps) => {
  return (
    <div className="mcg-score">
      <div className="score position-relative">
        <div 
          className={`fw-black  d-inline-block ${score ? 'text-subtle-yellow-pink' : 'text-light-gray'}`} 
          style={{ lineHeight: .8, fontSize: "4em" }}>{score || placeholder}</div>
        {(units && score) && <span className="small fw-semibold text-subtle-yellow-pink  position-absolute">{units}</span>}
      </div>
      {label && <div className="label text-muted small fw-semibold">{label}</div>}
    </div>
  )
}

export default Score