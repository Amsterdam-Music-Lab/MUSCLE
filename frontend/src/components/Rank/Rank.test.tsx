import { render } from '@testing-library/react';
import Rank from './Rank';
import { describe, expect, it } from 'vitest';


describe('Rank Component', () => {
    it('renders with the correct class and text', () => {
        const rank = {
            class: 'gold',
            text: 'Gold Rank',
        };

        const { getByTestId, getByText } = render(<Rank rank={rank} />);

        const rankElement = getByTestId('rank');

        // Check if the main div has the correct classes
        expect(rankElement.classList.contains('aha__rank')).toBe(true);
        expect(rankElement.classList.contains('gold')).toBe(true);
        expect(rankElement.classList.contains('offsetCup')).toBe(true);

        // Check if the h4 element contains the correct text
        expect(document.body.contains(getByText('Gold Rank'))).toBe(true);
    });

    it('does not have offsetCup class when text is empty', () => {
        const rank = {
            class: 'silver',
            text: '',
        };

        const { getByTestId } = render(<Rank rank={rank} />);

        const rankElement = getByTestId('rank');

        // Check if the main div has the correct classes
        expect(rankElement.classList.contains('aha__rank')).toBe(true);
        expect(rankElement.classList.contains('silver')).toBe(true);
        expect(rankElement.classList.contains('offsetCup')).toBe(false);

        // Check if the h4 element contains the correct text
        const rankText = getByTestId('rank-text');
        expect(document.body.contains(rankText)).toBe(true);
        expect(rankText.textContent).toBe('');
    });

    it('renders the cup div', () => {
        const rank = {
            class: 'bronze',
            text: 'Bronze Rank',
        };

        const { getByTestId } = render(<Rank rank={rank} />);

        const cupElement = getByTestId('cup-animation');
        
        // Check if the cup div is present
        expect(document.body.contains(cupElement)).toBe(true);
    });
});