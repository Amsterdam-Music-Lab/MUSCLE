/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState, useEffect, useRef } from "react";
import classNames from "classnames";
import { Button, Circle } from "@/components/ui";
import { Score as ScoreAction } from "@/types/Action";
import "./ScoreView.module.scss";

export interface ScoreViewProps extends ScoreAction {
  onNext: () => void;
}

/** Score is an block view that shows an intermediate and total score */
export default function ScoreView({
  last_song,
  score,
  score_message,
  total_score,
  texts,
  icon,
  feedback,
  timer,
  onNext,
}: ScoreViewProps) {
  const [showScore, setShowScore] = useState(0);
  // Use a ref to prevent doing multiple increments
  // when the render is skipped
  const scoreValue = useRef(0);

  useEffect(() => {
    const id = setTimeout(() => {
      // Score step
      const scoreStep = Math.max(
        1,
        Math.min(10, Math.ceil(Math.abs(scoreValue.current - score) / 10))
      );

      // Score are equal, stop
      if (score === scoreValue.current) {
        return;
      }
      // Add / subtract score
      scoreValue.current += Math.sign(score - scoreValue.current) * scoreStep;
      setShowScore(scoreValue.current);
    }, 50);

    return () => {
      window.clearTimeout(id);
    };
  }, [score, showScore]);

  useEffect(() => {
    let id = -1;
    if (timer) {
      id = setTimeout(() => {
        onNext();
      }, timer * 1000);
    }

    return () => {
      if (timer) {
        clearTimeout(id);
      }
    };
  }, [timer, onNext]);

  return (
    <div className="aha__score d-flex flex-column justify-content-center">
      <div
        className={classNames("score", {
          zero: score === 0,
          positive: score > 0,
          negative: score < 0,
        })}
      >
        <Circle />
        <div className="content">
          {!icon ? (
            <div>
              <h1>
                {score > 0 && "+"}
                {showScore}
              </h1>
              <h3>{score_message}</h3>
            </div>
          ) : (
            <span className={`fa-solid ${icon}`}></span>
          )}
        </div>
      </div>

      {total_score !== undefined && (
        <h4 className="total-score">
          {texts.score}: {total_score - score + showScore}
        </h4>
      )}

      {!timer && (
        <div className="d-flex flex-column justify-content-center align-items-center mt-3 mb-4">
          <Button
            key={"yes"}
            className="btn-primary"
            onClick={onNext}
            title={texts.next}
          />
        </div>
      )}

      {last_song && (
        <div className="previous-song">
          <h4>{texts.listen_explainer}</h4>
          <p>{last_song}</p>
        </div>
      )}

      {feedback && <p className="feedback">{feedback}</p>}
    </div>
  );
}
