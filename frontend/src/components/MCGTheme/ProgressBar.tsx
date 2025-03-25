import "react"
import "./ProgressBar.scss";

interface ProgressBarProps {
  progress: number;
}

/**
 * Displays a progress bar using bootstrap's progress bar utility.
 * 
 */
const ProgressBar = ({ progress = 0 }: ProgressBarProps) => {
  const value = Math.round(progress);
  return (
    <div class="mcg-progress-bar progress rounded-sm bg-inset-sm" style={{height: "2.5em"}}>
      <div
        class="progress-bar bg-indigo-red rounded-sm pr-2 text-right"
        role="progressbar"
        style={{ width: `${value}%` }}
        aria-valuenow={value}
        aria-valuemin="0"
        aria-valuemax="100">
        {`${value}%`}
      </div>
    </div>
  )
}

export default ProgressBar