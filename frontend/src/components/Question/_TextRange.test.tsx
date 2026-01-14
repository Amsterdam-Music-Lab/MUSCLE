import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import TextRange from './_TextRange'; // Adjust the import path as necessary
import Question, { QuestionViews } from '@/types/Question';

describe('TextRange Component', () => {
    const mockQuestion: Question = {
        question: 'Test Question',
        explainer: 'Test Explainer',
        view: QuestionViews.TEXT_RANGE,
        choices: [
            {value: '1', label: 'Choice 1'},
            {value: '2', label: 'Choice 2'},
            {value: '3', label: 'Choice 3'},
        ],
        value: '2',
    };

    it('renders correctly with empty value', () => {
        render(
            <TextRange question={mockQuestion} value="" onChange={() => { }} />
        );

        const slider = document.querySelector('.rangeslider');
        expect(slider).toBeTruthy();
        expect(slider?.getAttribute('aria-valuemin')).toBe('0');
        expect(slider?.getAttribute('aria-valuenow')).toBe('10'); // Index 1 * 10 = 10
        expect(slider?.getAttribute('aria-valuemax')).toBe('20'); // (3 choices * 10) - 10 = 20
    });

    it('renders correctly with a min, max and current value', () => {
        render(
            <TextRange question={mockQuestion} value="3" onChange={() => { }} />
        );

        let slider = document.querySelector('.rangeslider');
        expect(slider).toBeTruthy();
        expect(slider?.getAttribute('aria-valuemin')).toBe('0');
        expect(slider?.getAttribute('aria-valuenow')).toBe('20');
        expect(slider?.getAttribute('aria-valuemax')).toBe('20'); // (3 choices * 10) - 10 = 20

        render(
            <TextRange question={mockQuestion} value="3" onChange={() => { }} />
        );
    });

    it('renders RangeTitle with correct props', () => {
        render(
            <TextRange question={mockQuestion} value="2" onChange={() => { }} />
        );

        const limits = document.querySelector('.limits');
        expect(limits).toBeTruthy();
        expect(limits?.textContent).toBe('Choice 1Choice 3');
    });

    it('applies empty class when value is empty', () => {
        const { container } = render(
            <TextRange question={mockQuestion} value="" onChange={() => { }} />
        );

        expect(container.firstChild).toBeTruthy();

        if (!container.firstChild) {
            throw new Error('First child is null');
        }

        expect(container.firstChild.classList.contains('empty')).toBe(true);
    });

    it('does not apply empty class when value is set', () => {
        const { container } = render(
            <TextRange question={mockQuestion} value="2" onChange={() => { }} />
        );

        if (!container.firstChild) {
            throw new Error('First child is null');
        }

        expect(container.firstChild.classList.contains('empty')).toBe(false);
    });
});
