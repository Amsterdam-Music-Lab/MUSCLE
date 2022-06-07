import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";

import FeedbackForm from "./FeedbackForm";

let container = null;
const form = [
    {
        key: 'test_question',
        view: 'BUTTON_ARRAY',
        question: ['What is the average speed of a Swallow?'],
        choices: {'slow': '1 km/h', 'fast': '42 km/h'}
    }
]

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
        render(<FeedbackForm
            form={form}
            />,
            container
        );
    });
    expect(container.getElementsByClassName('aha__feedback') !== null);
});

it("can deactivate the form", () => { 
    const isActive = false;
    act(() => {
        render(<FeedbackForm
            formActive={isActive}
            form={form}
            />,
            container
        );
    });
    expect(container.getElementsByTagName('input')[0].getAttribute('active').toEqual(false));
});