import React from "react";
import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';

import { QuestionViews } from "@/types/Question";

import Trial from "./Trial";

vi.mock("../../util/stores");

const feedback_form = {
    form: [{
        key: 'test_question',
        view: QuestionViews.BUTTON_ARRAY,
        question: ['What is the average speed of a Swallow?'],
        choices: { 'slow': '1 km/h', 'fast': '42 km/h' }
    },
    ]
}

let config = {
    'listen_first': false
}

describe('Trial', () => {

    it("can render itself", () => {
        render(<Trial
            feedback_form={feedback_form}
            config={config}
        />);
        expect(screen.queryByRole('presentation')).to.exist;
    });

    it("can set the class of the trial element", () => {
        config.style = 'boolean';
        render(<Trial
            feedback_form={feedback_form}
            config={config}
        />
        )
        const presentation = screen.queryByRole('presentation');
        expect(presentation.classList.contains('boolean')).toBe(true);
    });
});
