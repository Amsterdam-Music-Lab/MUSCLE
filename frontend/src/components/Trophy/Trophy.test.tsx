import { render } from '@testing-library/react';
import Trophy from './Trophy';
import { describe, expect, it } from 'vitest';


describe('Trophy Component', () => {
    it('renders with the correct class and text', () => {
        const trophyProps = {
            className: 'gold',
            label: 'Gold Cup',
            image: 'cup'
        };

        const { container } = render(<Trophy {...trophyProps} />);

        const trophyElement = container.querySelector('.aha__trophy');

        // Check if the main div has the correct classes
        expect(trophyElement.classList.contains('gold')).toBe(true);

        // Check if the h4 element contains the correct text
        expect(document.body.contains(getByText('Gold Cup'))).toBe(true);
    });

    it('does not have offsetCup class when text is empty', () => {
        const rank = {
            className: 'silver',
            label: '',
        };

        const { getByTestId } = render(<Cup {...rank} />);

        const cupElement = getByTestId('cup');

        // Check if the main div has the correct classes
        expect(cupElement.classList.contains('aha__cup')).toBe(true);
        expect(cupElement.classList.contains('silver')).toBe(true);
        expect(cupElement.classList.contains('offsetCup')).toBe(false);

        // Check if the h4 element contains the correct text
        const cupText = getByTestId('cup-text');
        expect(document.body.contains(cupText)).toBe(true);
        expect(cupText.textContent).toBe('');
    });

    it('shows an animation', () => {
        const rank = {
            className: 'bronze',
            label: 'Bronze Cup',
        };

        const { getByTestId } = render(<Trophy {...rank} />);

        const cupElement = getByTestId('cup-animation');

        // Check if the cup div is present
        expect(document.body.contains(cupElement)).toBe(true);
    });
});
