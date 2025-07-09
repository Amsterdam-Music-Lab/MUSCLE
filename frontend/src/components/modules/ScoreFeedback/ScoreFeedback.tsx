/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import classNames from "classnames";
import { ScoreDisplay } from "@/components/modules";
import styles from "./ScoreFeedback.module.scss";

interface FeedbackProps extends HTMLAttributes<HTMLDivElement> {
    turnScore?: number;
    totalScore?: number;
    totalScoreLabel?: string;
    children?: React.ReactNode;
    center?: boolean;
}

export default function ScoreFeedback({
    turnScore,
    totalScore = 0,
    totalScoreLabel = "Total score",
    center = false,
    children,
    className,
    ...divProps
}: FeedbackProps) {
    return (
        <div
            className={classNames(styles.feedback, center && styles.center, className)}
            {...divProps}
        >
            <ScoreDisplay
                score={totalScore}
                label={totalScoreLabel}
                center={center}
                variant="secondary"
            />
            <div className={styles.message}>
                <span className="text">{children}</span>{" "}
                {turnScore !== undefined && (
                    <span className="font-weight-bold">
                        {turnScore === 0
                            ? "You got 0 points."
                            : turnScore > 0
                            ? `+${turnScore} points`
                            : `${turnScore} points`}
                    </span>
                )}
            </div>
        </div>
    );
}
