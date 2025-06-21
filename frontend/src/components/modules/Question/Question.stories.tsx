/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
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

const defaultQuestion: Partial<TQuestion> = {
  question: "What is your favourite fruit?",
  explainer: "Please describe or select your favourite fruit in some way.",
  choices: { apple: "Apple", banana: "Banana", cherry: "Cherry" },
};

export const Default: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "STRING",
    },
  },
};

export const Disabled: Story = {
  render: QuestionControlled,
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const WithEmphasizeTitle: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "STRING",
      style: { "emphasize-title": true },
    },
  },
};

export const Checkboxes: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "CHECKBOXES",
    },
  },
};

export const Radios: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "RADIOS",
    },
  },
};

// export const Range = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       view: "RANGE",
//       value: "",
//       choices: ["Choice 1", "Choice 2", "Choice 3"],
//       min_value: 1,
//       max_value: 42,
//       style: {},
//     },
//     onChange: () => {},
//     id: 0,
//     active: true,
//   },
// };

export const Range: Story = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "RANGE",
    },
    fieldProps: {
      showIntermediateTickLabels: true,
    },
  },
};

// Currently identical to RANGE
export const TextRange = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      view: "TEXT_RANGE",
    },
  },
};

export const IconRange = {
  render: QuestionControlled,
  args: {
    question: {
      ...defaultQuestion,
      choices: { globe: "fa-globe", pencil: "fa-pencil", bike: "fa-bicycle" },
      view: "ICON_RANGE",
    },
  },
};

// export const IconRange = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       icon: "🌎",
//       view: "ICON_RANGE",
//       value: "",
//       choices: ["fa-globe", "fa-pencil", "fa-bicycle"],
//       min_value: 1,
//       max_value: 42,
//       style: {},
//     },
//     onChange: () => {},
//     id: 0,
//     active: true,
//   },
// };

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

// export const Dropdown = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       view: "DROPDOWN",
//       value: "",
//       choices: ["Choice 1", "Choice 2", "Choice 3"],
//       style: {},
//     },
//     onChange: () => {},
//     id: 0,
//     active: true,
//   },
// };

// export const Autocomplete = {
//   args: {
//     question: {
//       question: "This is the question",
//       explainer: "This is the explainer",
//       view: "AUTOCOMPLETE",
//       value: "",
//       choices: [
//         "Brazil",
//         "China",
//         "Germany",
//         "Japan",
//         "Netherlands",
//         "Turkey",
//         "United States",
//       ],
//       style: {},
//     },
//     onChange: () => {},
//     id: 0,
//     active: true,
//   },
//   decorators: [
//     (Story) => (
//       <div
//         style={{
//           width: "100%",
//           height: "100%",
//           backgroundColor: "#ddd",
//           padding: "1rem",
//           position: "relative",
//         }}
//       >
//         <Story />
//       </div>
//     ),
//   ],
// };
