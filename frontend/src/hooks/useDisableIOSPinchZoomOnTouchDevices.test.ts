import { vi, describe, test, expect, afterEach } from "vitest";
import { renderHook } from '@testing-library/react'
import { waitFor } from "@testing-library/react";
import useDisableIOSPinchZoomOnTouchDevices from "./useDisableIOSPinchZoomOnTouchDevices";

describe("useDisableIOSPinchZoomOnTouchDevices", () => {
    afterEach(() => {
        vi.unstubAllGlobals();
    });

    test("should prevent gesturestart on touch devices", async () => {
        vi.stubGlobal("ontouchstart", true);

        const mockEvent = new Event('gesturestart');
        mockEvent.preventDefault = vi.fn();

        const spy = vi.spyOn(mockEvent, 'preventDefault').mockImplementation(() => { });

        renderHook(() => useDisableIOSPinchZoomOnTouchDevices());

        await waitFor(() => document.dispatchEvent(mockEvent));
        await waitFor(() => expect(spy).toHaveBeenCalledTimes(1));
    });

    test("should not prevent gesturestart on non-touch devices", () => {
        const mockEvent = new Event('gesturestart');
        mockEvent.preventDefault = vi.fn();

        const spy = vi.spyOn(mockEvent, 'preventDefault').mockImplementation(() => { });

        renderHook(() => useDisableIOSPinchZoomOnTouchDevices());

        document.dispatchEvent(mockEvent);
        expect(spy).not.toHaveBeenCalled();
    });
});
