import React from 'react';
import './ProgressBar.scss';

interface ProgressBarProps {
    /**
     * Current progress value (0-100)
     */
    value: number;
    /**
     * Maximum value (defaults to 100)
     */
    max?: number;
    /**
     * Show percentage text (defaults to true)
     */
    showPercentage?: boolean;
    /**
     * Optional label text to display above progress bar
     */
    label?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({
    value,
    max = 100,
    showPercentage = false,
    label,
}) => {
    const clampedValue = Math.min(Math.max(0, value), max);
    const percentage = Math.round((clampedValue / max) * 100);

    return (
        <div className={`aml__progress-bar`}>
            <div className={`aml__progress-bar-container`}>
                <div
                    className="aml__progress-bar-fill"
                    style={{ width: `${percentage}%` }}
                />
                <div className={`aml__progress-bar-content`}>
                    {label && (
                        <span className="aml__progress-bar-content-text">
                            {label}
                        </span>
                    )}
                    {showPercentage && (
                        <span className="aml__progress-bar-content-percentage">
                            {percentage}%
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProgressBar;
