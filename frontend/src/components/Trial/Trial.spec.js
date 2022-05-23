import React from "react";
import { cleanup, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import Trial from "./Trial";

const feedback_form = {
    form: [{
        key: 'test_question',
        view: 'BUTTON_ARRAY',
        question: ['What is the average speed of a Swallow?'],
        choices: {'slow': '1 km/h', 'fast': '42 km/h'}
    },
    ]
}

let config = {
    'listen_first': false
}

describe('Trial', () => {
    afterEach(cleanup);

    it("can render itself", () => { 
        render(<Trial
            feedback_form={feedback_form}
            config={config}
            />);
        expect(screen.queryByRole('trial')).toBeInTheDocument();
    });

    it("can set the class of the trial element", () => {
        config.style = 'boolean'
        render(<Trial
            feedback_form={feedback_form}
            config={config}
            />
        )
        expect(screen.queryByRole('trial')).toHaveClass('boolean');
    });
});