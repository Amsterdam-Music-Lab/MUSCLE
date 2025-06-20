import Question from "./Question";

const decorator = (Story) => (
  <div style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export default {
  title: "Modules/Question",
  component: Question,
  decorators: [decorator],
};

export const Default = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      value: "",
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const WithOnChange = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      value: "",
      style: {},
    },
    onChange: (value, id) => alert(`Question ${id} changed to ${value}`),
    id: 0,
    active: true,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const WithDisabledTrue = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      value: "",
      style: {},
    },
    onChange: () => {},
    id: 0,
    disabled: true,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const WithEmphasizeTitle = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      value: "",
      style: { "emphasize-title": true },
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const Checkboxes = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "CHECKBOXES",
      value: "",
      choices: ["Choice 1", "Choice 2", "Choice 3"],
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
};

export const Dropdown = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "DROPDOWN",
      value: "",
      choices: ["Choice 1", "Choice 2", "Choice 3"],
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
};

export const Autocomplete = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "AUTOCOMPLETE",
      value: "",
      choices: [
        "Brazil",
        "China",
        "Germany",
        "Japan",
        "Netherlands",
        "Turkey",
        "United States",
      ],
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
          position: "relative",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const Radios = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "RADIOS",
      value: "",
      choices: ["Choice 1", "Choice 2", "Choice 3"],
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
};

export const Range = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "RANGE",
      value: "",
      choices: ["Choice 1", "Choice 2", "Choice 3"],
      min_value: 1,
      max_value: 42,
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
};

export const TextRange = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "TEXT_RANGE",
      value: "",
      choices: ["Choice 1", "Choice 2", "Choice 3"],
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
};

export const IconRange = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      icon: "🌎",
      view: "ICON_RANGE",
      value: "",
      choices: ["fa-globe", "fa-pencil", "fa-bicycle"],
      min_value: 1,
      max_value: 42,
      style: {},
    },
    onChange: () => {},
    id: 0,
    active: true,
  },
  decorators: [
    (Story) => {
      return (
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#ddd",
            padding: "3rem",
            position: "relative",
          }}
        >
          <Story />
        </div>
      );
    },
  ],
};

export const StringNumberRange = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      input_type: "number",
      min_value: 1,
      max_value: 42,
    },
    onChange: () => {},
    value: "",
  },
  decorators: [
    (Story) => {
      return (
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#ddd",
            padding: "3rem",
            position: "relative",
          }}
        >
          <Story />
        </div>
      );
    },
  ],
};

export const StringTextRange = {
  args: {
    question: {
      question: "This is the question",
      explainer: "This is the explainer",
      view: "STRING",
      input_type: "text",
      max_length: 9,
    },
    onChange: () => {},
    value: "",
  },
  decorators: [
    (Story) => {
      return (
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#ddd",
            padding: "3rem",
            position: "relative",
          }}
        >
          <Story />
        </div>
      );
    },
  ],
};
