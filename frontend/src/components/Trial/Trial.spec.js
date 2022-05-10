import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";

import Trial from "./Trial";

let container = null;
const feedback_form = [
    {
        key: 'test_question',
        view: 'BUTTON_ARRAY',
        question: ['What is the average speed of a Swallow?'],
        choices: {'slow': '1 km/h', 'fast': '42 km/h'}
    }
]
let config = {
    'listen_first': false
}

beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it("can render itself", () => { 
    act(() => {
        render(<Trial
            form={feedback_form}
            config={config}
            />,
            container
        );
    });
    expect(document.querySelector('.aha__trial') !== null);
});

it("can set the class of the trial element", () => {
    act(() => {
        config.style = 'boolean'
        render(<Trial
            form={feedback_form}
            config={config}
            />,
            container
        )
    });
    expect(document.querySelector('.aha__trial.boolean') !== null);
    expect(document.querySelector('.aha__trial.neutral') === null);
});