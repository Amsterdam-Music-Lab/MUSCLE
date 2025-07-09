/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import View, { BaseViewComponent } from "./View";

function getViewMock<P>({
  viewName,
  dependencies = [],
  usesOwnLayout = true,
  getViewProps = () => ({} as P),
}: BaseViewComponent<P>) {
  const ViewMock = Object.assign(
    (props: P) => (
      <div data-testid={`mock-${viewName}`}>{JSON.stringify(props)}</div>
    ),
    {
      viewName,
      dependencies,
      usesOwnLayout,
      getViewProps,
    }
  );
  return ViewMock;
}

const getConsentViewPropsGetter = vi.fn((props) => ({ foo: "bar" }));

// Mock all view components that View might render
vi.mock("@/components/views", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/views")>()),
  AboutView: getViewMock({ viewName: "about" }),
  LoadingView: getViewMock({ viewName: "loading" }),
  ProfileView: getViewMock({
    viewName: "profile",
    dependencies: ["participant"],
  }),
  ConsentView: getViewMock({
    viewName: "consent",
    getViewProps: (props) => getConsentViewPropsGetter(props),
  }),
}));

// Mock the store
const setErrorMock = vi.fn();
const getMockBlock = vi.fn(() => ({
  slug: "test-block",
  feedback_info: { show_float_button: false },
}));
const mockAction = { view: "LOADING" };
const mockSession = { id: 1 };
const getMockParticipant = vi.fn(() => ({ id: 1 }));

vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: any) =>
    fn({
      setError: setErrorMock,
      block: getMockBlock(),
      currentAction: mockAction,
      session: mockSession,
      participant: getMockParticipant(),
    }),
}));

describe("View component", () => {
  beforeEach(() => {
    setErrorMock.mockClear();
  });

  it("renders the correct view component", () => {
    render(<View name="loading" />);
    expect(screen.getByTestId("mock-loading")).toBeInTheDocument();
  });

  it("calls setError for invalid view name", () => {
    try {
      render(<View name="notAView" />);
    } catch (e) {}
    expect(setErrorMock).toHaveBeenCalledWith('Invalid view name "notAView"');
  });

  it("calls setError if required dependency is missing", () => {
    // Remove participant from the store
    getMockParticipant.mockReturnValue(undefined);
    try {
      render(<View name="profile" />);
    } catch (e) {}
    expect(setErrorMock).toHaveBeenCalledWith(
      expect.stringContaining('Required dependency "participant"')
    );
  });

  it("calls getViewProps with correct arguments", () => {
    render(<View name="consent" />);
    expect(screen.getByTestId("mock-consent").textContent).toContain(
      '"foo":"bar"'
    );
  });

  it("renders FloatingActionButton if block.feedback_info.show_float_button is true", () => {
    getMockBlock.mockReturnValue({
      ...getMockBlock(),
      feedback_info: { show_float_button: true },
    });
    render(<View name="loading" />);
    expect(screen.getByTestId("floating-action-button")).toBeInTheDocument();
  });
});
