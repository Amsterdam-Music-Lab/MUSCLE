import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import IconRange from './_IconRange';
import Question, {QuestionViews} from '@/types/Question';

// Mock the RangeTitle component
vi.mock('./_RangeTitle', () => ({
    default: () => <div data-testid="mock-range-title">Mock Range Title</div>
}));

// Mock the react-rangeslider component
vi.mock('react-rangeslider', () => ({
    default: ({ value, onChange, min, max }) => (
        <input
            type="range"
            data-testid="mock-slider"
            value={value}
            onChange={(e) => onChange(parseInt(e.target.value))}
            min={min}
            max={max}
        />
    )
}));

const mockQuestion: Question = {
    key: 'test-icon-range',
    view: QuestionViews.ICON_RANGE,
    question: "What is the question?",
    choices: [
        {value: '1', label: 'fa-face-grin-hearts'},
        {value: '2', label: 'fa-face-grin'},
        {value: '3', label: 'fa-face-smile'},
        {value: '4', label: 'fa-face-meh'},
        {value: '5', label: 'fa-face-frown'},
    ]
};

describe('IconRange', () => {
    it('renders without crashing', () => {
        render(<IconRange question={mockQuestion} value="" onChange={() => { }} />);
        expect(screen.getByTestId('mock-range-title')).toBeDefined();
        expect(screen.getByTestId('mock-slider')).toBeDefined();
    });

    it('throws an error when no choices are provided', () => {
        const invalidQuestion = { ...mockQuestion, choices: {} };
        expect(() => render(<IconRange question={invalidQuestion} value="" onChange={() => { }} />))
            .toThrow('IconRange question must have choices');
    });

    it('sets the correct initial value', () => {
        render(<IconRange question={mockQuestion} value="3" onChange={() => { }}  />);
        expect((screen.getByTestId('mock-slider') as HTMLInputElement).value).toBe('2');
    });

    it('sets the middle value when no value is provided', () => {
        render(<IconRange question={mockQuestion} value="" onChange={() => { }}  />);
        expect((screen.getByTestId('mock-slider') as HTMLInputElement).value).toBe('2');
    });

    it('applies the correct style', () => {
        const questionWithStyle = {...mockQuestion, style:{"gradient": true}}
        const { container } = render(<IconRange question={questionWithStyle} value="" onChange={() => { }}  />);

        const firstChild = container.firstChild;

        if (!firstChild) {
            throw new Error('IconRange container is null');
        }

        expect(firstChild).toHaveProperty('className', expect.stringContaining('aha__text-range'));
        expect((firstChild as HTMLElement).classList).toContain('gradient');
    });

    it('applies empty class when value is empty', () => {
        const { container } = render(<IconRange question={mockQuestion} value="" onChange={() => { }}  />);
        expect(container.firstChild).toHaveProperty('className', expect.stringContaining('empty'));
    });

    it('does not apply empty class when value is provided', () => {
        const { container } = render(<IconRange question={mockQuestion} value="3" onChange={() => { }}  />);
        expect(container.firstChild).toHaveProperty('className', expect.not.stringContaining('empty'));
    });
});
