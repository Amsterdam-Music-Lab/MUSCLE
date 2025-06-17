import type Question from "@/types/Question";

import Slider from "react-rangeslider";
import classNames from "classnames";

interface RangeProps {
  question: Question;
  value: number;
  onChange: (value: number) => void;
}

/** Range is a question view that makes you select a value within the given range, using a slider */
const Range = ({ question, value, onChange }: RangeProps) => {
  const emptyValue = !value;

  if (
    (!question.min_value && question.min_value !== 0) ||
    (!question.max_value && question.max_value !== 0)
  ) {
    throw new Error(
      "min_value and max_value are required for the Range component"
    );
  }

  if (emptyValue) {
    value = (question.min_value + question.max_value) / 2;
  }
  return (
    <div className={classNames("aha__range", { empty: emptyValue })}>
      <p className="current-value">{emptyValue ? "↔" : value}</p>

      <Slider
        value={value}
        onChange={onChange}
        min={question.min_value}
        max={question.max_value}
        tooltip={false}
      />

      <div className="limits">
        <span className="min">{question.min_value}</span>
        <span className="max">{question.max_value}</span>
      </div>
    </div>
  );
};

export default Range;
