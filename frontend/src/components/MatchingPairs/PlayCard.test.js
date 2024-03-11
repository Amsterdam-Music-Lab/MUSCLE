import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import PlayCard from "./PlayCard"; // Adjust the path as necessary

describe("PlayCard Component Tests", () => {
    const mockOnClick = jest.fn();
    const mockRegisterUserClicks = jest.fn();

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
        expect(screen.getByTestId("play-card").querySelector(".back")).toBeInTheDocument();
    });

    it("should display the front of the card when turned", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).toBeInTheDocument();
        expect(screen.getByTestId("play-card").querySelector(".front")).not.toBeInTheDocument();
    });

    it("should display image for visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} view="visual" />);
        expect(screen.getByAltText("Test")).toBeInTheDocument();
    });

    it("should display histogram for non-visual matching pairs view", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, turned: true }} view="MATCHINGPAIRS" />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).toHaveClass("aha__histogram");
    });

    it("should display a disabled card when inactive", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, inactive: true }} />);
        expect(screen.getByTestId("play-card")).toHaveClass("disabled");
    });

    it("should display a card with no events when noevents", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, noevents: true }} />);
        expect(screen.getByTestId("play-card")).toHaveClass("noevents");
    });

    it("should display a card with fbmemory when memory", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fbmemory' }} />);
        expect(screen.getByTestId("play-card")).toHaveClass("fbmemory");
    });

    it("should display a card with fblucky when lucky", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fblucky' }} />);
        expect(screen.getByTestId("play-card")).toHaveClass("fblucky");
    });

    it("should display a card with fbnomatch when nomatch", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, matchClass: 'fbnomatch' }} />);
        expect(screen.getByTestId("play-card")).toHaveClass("fbnomatch");
    });

    it("should display a card with seen when seen", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} section={{ ...sectionProps, seen: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".back")).toHaveClass("seen");
    });

    it("should display a card with a histogram when turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={{ ...sectionProps, turned: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).toBeInTheDocument();
    });

    it("should display a card with a histogram when turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={{ ...sectionProps, turned: true }} />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).toBeInTheDocument();
    });

    it("should display a card without a histogram when not turned and playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing section={sectionProps} />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).not.toBeInTheDocument();
    });

    it("should display a card without a histogram when not turned and not playing", () => {
        render(<PlayCard onClick={mockOnClick} registerUserClicks={mockRegisterUserClicks} playing={false} section={sectionProps} />);
        expect(screen.getByTestId("play-card").querySelector(".aha__histogram")).not.toBeInTheDocument();
    });
});
