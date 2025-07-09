/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import { description } from "@/util/storybook";
import Question from "./Question";
import TQuestion from "@/types/Question";
type Story = StoryObj<typeof Question>;

function QuestionControlled({ question: initQuestion, ...args }) {
  const [question, setQuestion] = useState(initQuestion);
  const handleChange = (newValue) => {
    setQuestion({ ...question, value: newValue });
  };
  return <Question question={question} onChange={handleChange} {...args} />;
}

const meta: Meta<typeof Question> = {
  title: "Modules/Question",
  component: Question,
};

export default meta;

const fruits = {
  apple: "Apple",
  banana: "Banana",
  cherry: "Cherry",
  date: "Date",
  elderberry: "Elderberry",
  fig: "Fig",
  grape: "Grape",
  honeydew: "Honeydew",
  indianFig: "Indian Fig",
  jackfruit: "Jackfruit",
  kiwi: "Kiwi",
  lemon: "Lemon",
  mango: "Mango",
  nectarine: "Nectarine",
  orange: "Orange",
  papaya: "Papaya",
  quince: "Quince",
  raspberry: "Raspberry",
  strawberry: "Strawberry",
  tangerine: "Tangerine",
  "ugli fruit": "Ugli Fruit",
  "vanilla bean": "Vanilla Bean",
  watermelon: "Watermelon",
  xigua: "Xigua",
  yellowPassionFruit: "Yellow Passion Fruit",
  zucchini: "Zucchini",
};

const defaultQuestion: Partial<TQuestion> = {
  question: "What is your favourite fruit?",
  explainer: "Please describe or select your favourite fruit in some way.",
  choices: { apple: "Apple", banana: "Banana", cherry: "Cherry" },
};

export const String: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "STRING",
    },
  },
};

export const Disabled: Story = {
  ...description("Same example as above, but now disabled."),
  render: QuestionControlled,
  args: {
    ...String.args,
    disabled: true,
  },
};

export const Checkboxes: Story = {
  ...description(
    "See [Design System → Inputs → Option Field](?path=/docs/design-system-inputs-option-field--docs) for the input field."
  ),
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "CHECKBOXES",
    },
  },
};

export const Radios: Story = {
  ...description(
    "See [Design System → Inputs → Option Field](?path=/story/design-system-inputs-option-field) for the input field."
  ),
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "RADIOS",
    },
  },
};

export const Range: Story = {
  ...description(
    "Note that the question views `RANGE` and `TEXT_RANGE` are aliases and result in the exact same question. "
  ),
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "RANGE",
    },
    showIntermediateTickLabels: true,
  },
};

export const Likert: Story = {
  render: QuestionControlled,
  args: {
    question: {
      question:
        "How do you think about this statement: 'tomatoes are a kind of fruit.'?",
      choices: {
        strongly_disagree: "strongly disagree",
        disagree: "disagree",
        neutral: "neither agree nor disagree",
        agree: "agree",
        strongly_agree: "strongly agree",
      },
      view: "RANGE",
    },
    tickLabels: [
      "strongly disagree",
      undefined,
      "neutral",
      undefined,
      "strongly agree",
    ],
  },
};

export const IconRange = {
  render: QuestionControlled,
  args: {
    question: {
      question: "What is your favourit means of transport?",
      choices: { bike: "fa-bicycle", car: "fa-car", plane: "fa-plane" },
      view: "ICON_RANGE",
    },
  },
};

// Identical to Autocomplete!
export const Dropdown = {
  ...description(
    "Note that the question views `DROPDOWN` and `AUTOCOMPLETE` are aliases and result in the exact same question. "
  ),
  args: {
    question: {
      ...defaultQuestion,
      choices: fruits,
      view: "DROPDOWN",
    },
  },
};

export const EmphasizeTitle: Story = {
  args: {
    question: {
      ...defaultQuestion,
      view: "STRING",
      style: { "emphasize-title": true },
    },
  },
};

export const ExpectedResponse = {
  args: {
    question: {
      ...defaultQuestion,
      expected_response: "banana",
      view: "STRING",
    },
  },
};
// export const StringNumberRange = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       view: "STRING",
//       input_type: "number",
//       min_value: 1,
//       max_value: 42,
//     },
//     onChange: () => {},
//     value: "",
//   },
// };

// export const StringTextRange = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       view: "STRING",
//       input_type: "text",
//       max_length: 9,
//     },
//     onChange: () => {},
//     value: "",
//   },
// };
