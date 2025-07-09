/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import FinalView from "./FinalView";

export default {
  title: "App/Views/FinalView",
  component: FinalView,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

function getFinalViewData(overrides = {}) {
  return {
    score: 100,
    percentile: 66,
    rank: {
      text: "Rank",
      class: "rank",
    },
    final_text: `
            <p>You outperformed 66% of the players</p>

            <table>
                <tr><td>This game</td><td>100</td></tr>
                <tr><td>Personal best</td><td>120</td></tr>
                <tr><td>Average score</td><td>80</td></tr>
            </table>
        `,
    points: "points",
    button: {
      text: "Button",
      link: "https://www.example.com",
    },
    logo: {
      image: "https://via.placeholder.com/150",
      link: "https://www.example.com",
    },
    social: {
      channels: [
        "facebook",
        "whatsapp",
        "twitter",
        "weibo",
        "share",
        "clipboard",
      ],
      url: "https://www.example.com",
      content: "Hey! Check out this cool experiment",
      tags: ["coolexperiment", "awesome"],
    },
    show_profile_link: true,
    action_texts: {
      all_experiments: "All experiments",
      profile: "Profile",
    },
    show_participant_link: true,
    participant_id_only: false,
    feedback_info: {
      header: "Feedback",
      button: "Submit",
      thank_you: "Thank you for your feedback!",
      contact_body:
        '<p>Please contact us at <a href="mailto:info@example.com">',
    },
    block: {
      slug: "test",
    },
    participant: "test",
    onNext: () => {
      alert("Next");
    },
    ...overrides,
  };
}

const getDecorator = (Story) => (
  <div
    style={{
      width: "100%",
      height: "100%",
      backgroundColor: "#aaa",
      padding: "1rem",
    }}
  >
    <Story />
  </div>
);

export const Default = {
  args: getFinalViewData(),
  decorators: [getDecorator],
};

// with relative button.link
export const RelativeButtonLink = {
  args: getFinalViewData({
    button: {
      text: "Play again",
      link: "/profile",
    },
  }),
  decorators: [getDecorator],
};

// with absolute button.link
export const AbsoluteButtonLink = {
  args: getFinalViewData({
    button: {
      text: "Button",
      link: "https://www.example.com",
    },
  }),
  decorators: [getDecorator],
};

// without button.link
export const NoButtonLink = {
  args: getFinalViewData({
    button: {
      text: "Button",
      link: "",
    },
  }),
  decorators: [getDecorator],
};

// final text html test
export const FinalViewTextHtml = {
  args: getFinalViewData({
    final_text: `
            <p>You outperformed 66% of the players</p>
            <table>
                <tr><td>This game</td><td>100</td></tr>
                <tr><td>Personal best</td><td>120</td></tr>
                <tr><td>Average score</td><td>80</td></tr>
            </table>
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <p>Lorem ipsum dolor sit amet, <i>consectetur adipiscing elit</i>. Nullam eget nunc nec nunc. Aenean nec nunc nec nunc. <b>Curabitur nec nunc nec nunc</b>. Donec nec nunc nec nunc. Sed nec nunc nec nunc. Vestibulum</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            <ol>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ol>
            <a href="https://www.example.com">Link</a>
            <img src="https://cataas.com/cat" alt="Placeholder">
            <pre><code>console.log("Hello, world!");</code></pre>
            <pre><code>
            function sum(a, b) {
                return a + b;
            }
            </code></pre>
        `,
  }),
  decorators: [getDecorator],
};

// no percentile, text centered
export const PlainText = {
  args: getFinalViewData({
    percentile: undefined,
    final_text: "<center>Well done!</center>",
  }),
  decorators: [getDecorator],
};
