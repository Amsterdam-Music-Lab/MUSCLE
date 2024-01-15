import { render } from '@testing-library/react';
import { renderLabel } from "./label";

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
