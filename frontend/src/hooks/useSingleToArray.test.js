import { renderHook } from '@testing-library/react-hooks';
import useSingleToArray from './useSingleToArray'; // Adjust the import path as necessary

describe('useSingleToArray', () => {

    it('should return an array with the initial value', () => {
        const initialValue = 'test';
        const { result } = renderHook(() => useSingleToArray(initialValue));
        expect(result.current).toEqual([initialValue]);
    });

    it('should update the array when the value changes', () => {
        const { result, rerender } = renderHook(({ value }) => useSingleToArray(value), {
            initialProps: { value: 'initial' },
        });

        expect(result.current).toEqual(['initial']);

        // Update the value
        rerender({ value: 'updated' });
        expect(result.current).toEqual(['updated']);
    });

    it('handles null and undefined correctly', () => {
        const { result, rerender } = renderHook(({ value }) => useSingleToArray(value), {
            initialProps: { value: null },
        });

        expect(result.current).toEqual([null]);

        rerender({ value: undefined });
        expect(result.current).toEqual([undefined]);
    });

});
