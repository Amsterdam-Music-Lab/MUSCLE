import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import PlayCard from "./PlayCard"; // Adjust the path as necessary

describe("PlayCard Component Tests", () => {
    const mockOnClick = vi.fn();
    const mockRegisterUserClicks = vi.fn();

    const sectionProps = {
        turned: false,
        noevents: false,
        inactive: false,
        seen: false,
        url: "test.jpg",
        name: "Test"
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
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".back"))).to.be.true;
    });

    it("should display the front of the card when turned", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.be.true;
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".front"))).to.not.be.true;
    });

    it("should display image for visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} view="visual" />);
        expect(document.body.contains(screen.getByAltText("Test"))).to.be.true;
    });

    it("should display histogram for non-visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} view="MATCHINGPAIRS" />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.be.true;
    });

    it("should display a disabled card when inactive", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, inactive: true }} />);
        expect(screen.getByTestId("play-card").classList.contains("disabled")).to.be.true;
    });

    it("should display a card with no events when noevents", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, noevents: true }} />);
        expect(screen.getByTestId("play-card").classList.contains("noevents")).to.be.true;
    });

    it("should display a card with fbmemory when memory", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fbmemory' }} />);
        expect(screen.getByTestId("play-card").classList.contains("memory")).to.be.true;
    });

    it("should display a card with fblucky when lucky", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fblucky' }} />);
        expect(screen.getByTestId("play-card").classList.contains("lucky")).to.be.true;
    });

    it("should display a card with fbnomatch when nomatch", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fbnomatch' }} />);
        expect(screen.getByTestId("play-card").classList.contains("nomatch")).to.be.true;
    });

    it("should display a card with seen when seen", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, seen: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".back").classList.contains("seen")).to.be.true;
    });

    it("should display a card with a histogram when turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.be.true;
    });

    it("should display a card with a histogram when turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={{ ...sectionProps, turned: true }} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.be.true;
    });

    it("should display a card without a histogram when not turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={sectionProps} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.not.be.true;
    });

    it("should display a card without a histogram when not turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={sectionProps} />);
        expect(document.body.contains(screen.getByTestId("play-card").querySelector(".aha__histogram"))).to.not.be.true;
    });
});
