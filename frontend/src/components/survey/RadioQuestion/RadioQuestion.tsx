import type Question from "@/types/Question";
import { RadioInput } from "@/components/ui";

interface RadioQuestionProps extends HTMLAttributes<HTMLDivElement> {
  question: Question;
  value: string;
  onChange: (value: string) => void;
}

/**
 * Radios is a question view for selecting a single option from a list
 */
export default function RadioQuestion({
  question,
  value,
  onChange = () => {},
}: RadioQuestionProps) {
  const choices = question.choices;
  if (!choices || Object.keys(choices).length <= 0) {
    throw new Error("Radio questions must have choices");
  }
  const keys = Object.keys(choices).sort((a, b) => a - b);
  return (
    <RadioInput
      value={value}
      values={keys}
      labels={keys.map((key) => choices[key])}
      onChange={onChange}
    />
  );
}
