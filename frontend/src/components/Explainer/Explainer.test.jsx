import React from 'react';
import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';

import Explainer from './Explainer';

describe('Explainer Component', () => {
    const props = {
        instruction: 'Some instruction',
        button_label: 'Next',
        steps: [],
        onNext: vi.fn(),
        timer: 1
    }

    it('renders with given props', () => {

        render(
            <Explainer {...props} />
        );
        expect(screen.getByTestId('explainer')).to.exist;
    })



});