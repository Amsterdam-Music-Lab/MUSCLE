/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { screen, fireEvent } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { vi, describe, it, expect, beforeEach } from "vitest";
import ParticipantLink from "./ParticipantLink";

// Mock the useParticipantLink hook
vi.mock("@/API", () => ({ useParticipantLink: vi.fn() }));

const mockUseParticipantLink = vi.mocked(
  await import("@/API").then((m) => m.useParticipantLink),
  { shallow: true }
);

// Mock the clipboard API
const mockClipboard = {
  writeText: vi.fn(),
};
Object.defineProperty(navigator, "clipboard", {
  value: mockClipboard,
  configurable: true,
});

describe("ParticipantLink Component", () => {
  const mockLink = {
    url: "https://app.amsterdammusiclab.nl/experiment/participant/reload/123456/1a2b3c4d/",
    copy_message: "Copy Link",
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading placeholder when loadingLink is true", () => {
    mockUseParticipantLink.mockReturnValue([null, true]);
    render(<ParticipantLink />);
    const input = screen.getByTestId("participant-link") as HTMLInputElement;
    expect(input.placeholder).toBe("Loading...");
    expect(input.value).toBe("");
  });

  it("shows fallback placeholder when link is not set", () => {
    mockUseParticipantLink.mockReturnValue([null, false]);

    render(<ParticipantLink />);

    const input = screen.getByTestId("participant-link") as HTMLInputElement;
    expect(input.placeholder).toBe("Something went wrong...");
    expect(input.value).toBe("");
  });

  it("renders link when available", () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink />);
    expect(screen.getByRole("textbox")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Copy Link" })).toBeTruthy();
  });

  it("displays full link by default", () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink />);
    const textbox = screen.getByRole("textbox") as HTMLInputElement;
    expect(textbox.value).toBe(mockLink.url);
  });

  it("displays only participant ID when participantIDOnly is true", () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink participantIDOnly={true} />);
    const textbox = screen.getByRole("textbox") as HTMLInputElement;
    expect(textbox.value).toBe("123456");
  });

  it("copies link to clipboard when button is clicked", () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink />);
    fireEvent.click(screen.getByRole("button", { name: "Copy Link" }));
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(mockLink.url);
  });

  it("copies link to clipboard when button is activated with keyboard", async () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink />);
    const button = screen.getByRole("button", { name: "Copy Link" });
    await fireEvent.keyDown(button, { key: "Enter", code: 13, charCode: 13 });
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(mockLink.url);
  });

  it("selects input text when copying", () => {
    vi.mocked(mockUseParticipantLink).mockReturnValue([mockLink, false]);
    render(<ParticipantLink />);
    const input = screen.getByRole("textbox");
    const selectSpy = vi.spyOn(input, "select");
    const setSelectionRangeSpy = vi.spyOn(input, "setSelectionRange");
    fireEvent.click(screen.getByRole("button", { name: "Copy Link" }));
    expect(selectSpy).toHaveBeenCalled();
    expect(setSelectionRangeSpy).toHaveBeenCalledWith(0, 99999);
  });
});
