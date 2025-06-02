/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { screen, waitFor } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Block from "./Block";

const blockObj = {
  id: 24,
  slug: "test",
  name: "Test",
  playlists: [{ id: 42, name: "TestPlaylist" }],
  session_id: 42,
  label: "Patience!",
};

const explainerAction = {
  view: "EXPLAINER",
  instruction: "Instruction",
  title: "Some title",
};

const mockParticipantStore = {
  id: 1,
  hash: "00000000-0000-0000-0000-000000000000",
  csrf_token:
    "auSoWt7JA9fYyGE0Cc51tlYDnvGGxwo1HqVBsQHQ8dUE7QJZAjYZIieJc4kdYB4r",
  participant_id_url: "url",
  country: "nl",
};

const useExperimentMock = vi.fn();
const useBlockMock = vi.fn();
const getNextRoundMock = vi.fn();
const setErrorMock = vi.fn();
let mockUseParams = vi.fn();

vi.mock("@/API", () => ({
  useExperiment: (...args) => useExperimentMock(...args),
  useBlock: (...args) => useBlockMock(...args),
  getNextRound: (...args) => getNextRoundMock(...args),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => mockUseParams(),
  };
});

vi.mock("@/components/layout", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/layout")>()),
  ViewTransition: ({ ...props }) => (
    <div data-testid="view-transition" {...props} />
  ),
}));

vi.mock("@/components/application", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/application")>()),
  View: ({ name, onNext, ...props }) => (
    <div data-testid={`view-${name}`} onClick={onNext}>
      {JSON.stringify(props)}
    </div>
  ),
}));

vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: any) => {
    const state = {
      session: { id: 1 },
      participant: mockParticipantStore,
      setError: setErrorMock,
      setSession: vi.fn(),
      setHeadData: vi.fn(),
      resetHeadData: vi.fn(),
      setBlock: vi.fn(),
      setCurrentAction: vi.fn(),
    };

    return fn(state);
  },
  useBoundStore: vi.fn(),
}));

describe("Block Component", () => {
  beforeEach(() => {
    useExperimentMock.mockReset();
    useBlockMock.mockReset();
    getNextRoundMock.mockReset();
    setErrorMock.mockReset();
    mockUseParams.mockReturnValue({ slug: "test" });
  });

  // afterEach(() => {
  //   vi.clearAllMocks();
  // });

  it("renders loading state when loadingBlock is true", async () => {
    useExperimentMock.mockReturnValue([null, true]);
    useBlockMock.mockReturnValue([null, true]);
    const { getByTestId } = render(<Block />);
    expect(getByTestId("view-loading")).toBeInTheDocument();
  });

  it("renders error view if block is null after loading", async () => {
    useExperimentMock.mockReturnValue([null, false]);
    useBlockMock.mockReturnValue([null, false]);
    render(<Block />);
    await waitFor(() => {
      expect(setErrorMock).toHaveBeenCalledWith("Could not load a block");
    });
  });

  it("renders error view if experiment is null after loading", async () => {
    useExperimentMock.mockReturnValue([null, false]);
    useBlockMock.mockReturnValue([true, false]);
    render(<Block />);
    await waitFor(() => {
      expect(setErrorMock).toHaveBeenCalledWith(
        "Could not load the experiment"
      );
    });
  });

  it("renders the first step after loading block", async () => {
    useBlockMock.mockImplementation(() => [blockObj, false]);
    useExperimentMock.mockReturnValue([true, false]);
    getNextRoundMock.mockResolvedValueOnce({
      next_round: [{ ...explainerAction }], // Avoid sharing mutables between tests
    });
    render(<Block />);
    const view = await screen.findByTestId("view-explainer");
    expect(view.textContent).toContain("Instruction");
  });

  it("calls getNextRound when onNext is triggered by clicking the view", async () => {
    useBlockMock.mockImplementation(() => [blockObj, false]);
    useExperimentMock.mockReturnValue([true, false]);
    getNextRoundMock.mockResolvedValueOnce({
      next_round: [{ ...explainerAction }], // Avoid sharing mutables between tests
    });
    render(<Block />);
    const view = await screen.findByTestId("view-explainer");
    // Simulate user clicking the view, which triggers onNext
    view.click();
    await waitFor(() => {
      expect(getNextRoundMock).toHaveBeenCalled();
    });
  });

  it("calls setError if no valid round is returned", async () => {
    useBlockMock.mockImplementationOnce(() => [blockObj, false]);
    useBlockMock.mockImplementationOnce(() => [blockObj, false]);
    useExperimentMock.mockReturnValue([true, false]);
    getNextRoundMock.mockResolvedValueOnce(null);
    render(<Block />);
    await waitFor(() => {
      expect(setErrorMock).toHaveBeenCalled();
    });
  });
});
