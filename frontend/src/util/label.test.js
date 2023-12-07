import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { getPlayerLabel, LABEL_NUMERIC, LABEL_ALPHABETIC, LABEL_ROMAN, LABEL_CUSTOM, renderLabel } from "./label";

describe('getPlayerLabel', () => {

    it('returns numeric label correctly', () => {
        expect(getPlayerLabel(0, LABEL_NUMERIC)).toBe(1);
        expect(getPlayerLabel(1, LABEL_NUMERIC)).toBe(2);
    });

    it('returns alphabetic label correctly', () => {
        expect(getPlayerLabel(0, LABEL_ALPHABETIC)).toBe('A');
        expect(getPlayerLabel(25, LABEL_ALPHABETIC)).toBe('Z');
    });

    it('returns roman label correctly', () => {
        expect(getPlayerLabel(0, LABEL_ROMAN)).toBe('I');
        expect(getPlayerLabel(3, LABEL_ROMAN)).toBe('IV');
    });

    it('returns custom label correctly', () => {
        const customLabels = ['One', 'Two', 'Three'];
        expect(getPlayerLabel(0, LABEL_CUSTOM, customLabels)).toBe('One');
        expect(getPlayerLabel(2, LABEL_CUSTOM, customLabels)).toBe('Three');
    });

    it('returns empty string for unknown label style', () => {
        expect(getPlayerLabel(1, 'UNKNOWN')).toBe('');
    });

});


describe('renderLabel', () => {

    it('renders FontAwesome label correctly', () => {
        const { container } = render(renderLabel('fa-user', 'fa-lg'));
        expect(container.querySelector('span.fa-solid.fa-user.fa-lg')).not.toBeNull();
    });

    it('returns non-FontAwesome label as is', () => {
        const label = 'NonFontAwesomeLabel';
        const { getByText } = render(renderLabel(label));
        expect(getByText(label)).toBeInTheDocument();
    });

    it('handles empty or undefined labels correctly', () => {
        expect(renderLabel('')).toBe('');
        expect(renderLabel(undefined)).toBe(undefined);
    });

});
