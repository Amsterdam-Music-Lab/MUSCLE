import { vi, describe, afterEach, test, expect } from "vitest";
import { renderHook } from '@testing-library/react'
import { waitFor } from "@testing-library/react";
import useDisableRightClickOnTouchDevices from "./useDisableRightClickOnTouchDevices";

describe("useDisableRightClickOnTouchDevices", () => {

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    test("should prevent context menu on touch devices", async () => {
        vi.stubGlobal("ontouchstart", true);

        const mockEvent = new MouseEvent('contextmenu');
        mockEvent.preventDefault = vi.fn();

        const spy = vi.spyOn(mockEvent, 'preventDefault').mockImplementation(() => { });

        renderHook(() => useDisableRightClickOnTouchDevices());

        await waitFor(() => document.dispatchEvent(mockEvent));
        await waitFor(() => expect(spy).toHaveBeenCalledTimes(1));
    });

    test("should not prevent context menu on non-touch devices", () => {
        const mockEvent = new MouseEvent('contextmenu');
        mockEvent.preventDefault = vi.fn();

        const spy = vi.spyOn(mockEvent, 'preventDefault').mockImplementation(() => void 0);

        renderHook(() => useDisableRightClickOnTouchDevices());

        document.dispatchEvent(mockEvent);
        expect(spy).not.toHaveBeenCalled();
    });

});
