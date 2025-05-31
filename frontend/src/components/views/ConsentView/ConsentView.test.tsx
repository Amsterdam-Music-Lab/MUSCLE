import { render, fireEvent, waitFor } from "@testing-library/react";
import ConsentView, { ConsentViewProps } from "./ConsentView";
import { useConsent } from "@/API";
import { saveAs } from "file-saver";
import { vi, Mock, expect, it, describe } from "vitest";
import { MemoryRouter } from "react-router-dom";

global.Blob = vi.fn().mockImplementation((content, options) => ({
  content,
  options,
}));

global.URL.createObjectURL = vi.fn();

vi.mock("file-saver", () => ({
  saveAs: vi.fn(),
}));

vi.mock("@/API", () => ({
  createConsent: vi.fn(),
  useConsent: vi.fn(),
}));

// Mock the Circle and ListenCircle components
vi.mock("../LoadingView", () => ({
  LoadingView: () => <div data-testid="mock-loading">Loading...</div>,
}));

const mockExperiment = {
  slug: "test-experiment",
  name: "Test",
};

const defaultProps = {
  experiment: mockExperiment,
  consentHtml: "<p>Consent Text</p>",
  participant: { csrf_token: "42" },
  onConfirm: vi.fn(),
};

describe("Consent", () => {
  it("renders circle while loading", () => {
    (useConsent as Mock).mockReturnValue([null, true]);
    const { getByTestId } = render(<ConsentView {...defaultProps} />);
    expect(getByTestId("mock-loading")).toBeTruthy();
  });

  it("renders consent text when not loading", () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const { getByText } = render(
      <MemoryRouter>
        <ConsentView {...defaultProps} consentHtml={"<p>Lorem Ipsum</p>"} />
      </MemoryRouter>
    );
    expect(getByText("Lorem Ipsum")).toBeTruthy(true);
  });

  it("calls onNext when Agree button is clicked", async () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const onNext = vi.fn();
    const { getByText } = render(
      <MemoryRouter>
        <ConsentView
          {...defaultProps}
          confirmLabel="CONFIRM!"
          onConfirm={onNext}
        />
      </MemoryRouter>
    );
    fireEvent.click(getByText("CONFIRM!"));
    await waitFor(() => expect(onNext).toHaveBeenCalled());
  });

  it("triggers download when Download button is clicked", async () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const { getByTestId } = render(
      <MemoryRouter>
        <ConsentView {...defaultProps} />
      </MemoryRouter>
    );
    fireEvent.click(getByTestId("download-button"));
    await waitFor(() => expect(saveAs).toHaveBeenCalled());
  });

  it("auto advances if consent is already given", () => {
    (useConsent as Mock).mockReturnValue([true, false]);
    const onNext = vi.fn();
    render(
      <MemoryRouter>
        <ConsentView {...defaultProps} onConfirm={onNext} />
      </MemoryRouter>
    );
    expect(onNext).toHaveBeenCalled();
  });

  it("calculates style for consent text correctly", () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    Object.defineProperty(window, "innerHeight", {
      writable: true,
      configurable: true,
      value: 800,
    });
    const { getByTestId } = render(
      <MemoryRouter>
        <ConsentView {...defaultProps} />
      </MemoryRouter>
    );
    const consentText = getByTestId("consent-text");
    expect(consentText.style.height).toBe("500px");
  });
});
