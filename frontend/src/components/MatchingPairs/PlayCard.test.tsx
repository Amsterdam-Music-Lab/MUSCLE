import { vi, describe, it, expect } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import PlayCard from "./PlayCard";

vi.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn: (state: any) => any) => {
        const state = {
            theme: {
                colorPrimary: "#d843e2", colorSecondary: "#39d7b8"
            }
        };

        return fn(state);
    },
    useBoundStore: vi.fn()
}));

describe("PlayCard Component Tests", () => {
    const mockOnClick = vi.fn();
    const mockRegisterUserClicks = vi.fn();

    const sectionProps = {
        turned: false,
        noevents: false,
        inactive: false,
        seen: false,
        link: "test.jpg",
        label: "Test",
    };

    it("should render without crashing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={sectionProps} />);
    });

    it("should call onClick and registerUserClicks when clicked", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={sectionProps} />);
        fireEvent.click(screen.getByTestId("play-card"));
        expect(mockOnClick).toHaveBeenCalled();
        expect(mockRegisterUserClicks).toHaveBeenCalled();
    });

    it("should display the back of the card by default", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={sectionProps} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".back"))).toBe(true);
    });

    it("should display the front of the card when turned", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).toBe(true);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".front"))).not.toBe(true);
    });

    it("should display image for visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true, playMethod: 'NOAUDIO' }} view="visual" />);
        expect(document.body.contains(screen.getByAltText("Test"))).toBe(true);
    });

    it("should display histogram for non-visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} view="MATCHINGPAIRS" />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).toBe(true);
    });

    it("should display a disabled card when inactive", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, inactive: true }} />);
        expect(screen.getByTestId("play-card").classList.contains("disabled")).toBe(true);
    });

    it("should display a card with no events when noevents", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, noevents: true }} />);
        expect(screen.getByTestId("play-card").classList.contains("noevents")).toBe(true);
    });

    it("should display a card with fbmemory when memory", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} showAnimation={true} section={{ ...sectionProps, matchClass: 'fbmemory' }} />);
        expect(screen.getByRole("button").classList.contains("fbmemory")).toBe(true);
    });

    it("should display a card with fblucky when lucky", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} showAnimation={true} section={{ ...sectionProps, matchClass: 'fblucky' }} />);
        expect(screen.getByRole("button").classList.contains("fblucky")).toBe(true);
    });

    it("should display a card with fbnomatch when nomatch", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} showAnimation={true} section={{ ...sectionProps, matchClass: 'fbnomatch' }} />);
        expect(screen.getByRole("button").classList.contains("fbnomatch")).toBe(true);
    });

    it("should not apply matchClass when showAnimations is false", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} showAnimation={false} section={{ ...sectionProps, matchClass: 'fbnomatch' }} />);
        expect(screen.getByRole("button").classList.contains("fbnomatch")).not.toBe(true);
    })

    it("should display a card with seen when seen", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, seen: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".back").classList.contains("seen")).toBe(true);
    });

    it("should display a card with a histogram when turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).toBe(true);
    });

    it("should display a card with a histogram when turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).toBe(true);
    });

    it("should display a card without a histogram when not turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={sectionProps} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).not.toBe(true);
    });

    it("should display a card without a histogram when not turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={sectionProps} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).not.toBe(true);
    });
});
