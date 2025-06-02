import { fireEvent, render, waitFor } from "@testing-library/react";
import ConsentView, { ConsentViewProps } from "./ConsentView";
import { useConsent } from "@/API";
import { saveAs } from "file-saver";
import { vi, Mock, expect, it, describe } from "vitest";

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

const getConsentViewProps: (
  overrides?: Partial<ConsentViewProps>
) => ConsentViewProps = (overrides) => ({
  title: "Consent",
  text: "<p>Consent Text</p>",
  experiment: mockExperiment,
  participant: { csrf_token: "42" },
  onNext: vi.fn(),
  confirm: "Agree",
  deny: "Disagree",
  ...overrides,
});

describe("Consent", () => {
  it("renders circle while loading", () => {
    (useConsent as Mock).mockReturnValue([null, true]); // Mock loading state
    const { getByTestId } = render(
      <ConsentView {...getConsentViewProps({ experiment: mockExperiment })} />
    );
    expect(getByTestId("mock-loading")).toBeTruthy();
  });

  it("renders consent text when not loading", () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const { getByText } = render(
      <ConsentView
        {...getConsentViewProps({
          text: "<p>Consent Text</p>",
          experiment: mockExperiment,
        })}
      />
    );

    expect(document.body.contains(getByText("Consent Text"))).toBe(true);
  });

  it("calls onNext when Agree button is clicked", async () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const onNext = vi.fn();
    const { getByText } = render(
      <ConsentView
        {...getConsentViewProps({
          confirm: "Agree",
          experiment: mockExperiment,
          onNext,
        })}
      />
    );
    fireEvent.click(getByText("Agree"));

    await waitFor(() => expect(onNext).toHaveBeenCalled());
  });

  it("triggers download when Download button is clicked", async () => {
    (useConsent as Mock).mockReturnValue([null, false]);
    const { getByTestId } = render(<ConsentView {...getConsentViewProps()} />);
    fireEvent.click(getByTestId("download-button"));

    await waitFor(() => expect(saveAs).toHaveBeenCalled());
  });

  it("auto advances if consent is already given", () => {
    (useConsent as Mock).mockReturnValue([true, false]);
    const onNext = vi.fn();
    render(
      <ConsentView
        {...getConsentViewProps({ experiment: mockExperiment, onNext })}
      />
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
    const { getByTestId } = render(<ConsentView {...getConsentViewProps()} />);
    const consentText = getByTestId("consent-text");
    expect(consentText.style.height).toBe("500px");
  });
});
