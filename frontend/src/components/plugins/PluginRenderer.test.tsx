/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it, vi } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import PluginRenderer from "./PluginRenderer";

describe("PluginRenderer", () => {
  it("renders components by name", () => {
    render(
      <PluginRenderer
        plugins={[
          { name: "scores", args: { turnScoreLabel: "Hello" } },
          { name: "scores", args: { turnScore: 42 } },
        ]}
      />
    );

    expect(screen.getByText("Hello")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });

  it("applies getWrapperProps to plugin wrapper", () => {
    const Wrapper = ({ children, "data-tag": tag }: any) => (
      <div data-testid="wrapper" data-tag={tag}>
        {children}
      </div>
    );

    render(
      <PluginRenderer
        plugins={[
          {
            name: "logo",
            args: { name: "mcg" },
            getWrapperProps: (args) => ({ "data-tag": `tag-${args.name}` }),
          },
        ]}
        wrapper={Wrapper}
      />
    );

    expect(screen.getByTestId("wrapper")).toHaveAttribute(
      "data-tag",
      "tag-mcg"
    );
  });

  it("warns if component is not found", () => {
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    render(<PluginRenderer plugins={[{ name: "missing", args: {} }] as any} />);

    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining("Plugin component not found: missing")
    );
    warnSpy.mockRestore();
  });

  it("skips disabled and invisible plugins", () => {
    render(
      <PluginRenderer
        plugins={[
          {
            name: "scores",
            args: { turnScoreLabel: "Visible" },
            enabled: true,
          },
          { name: "scores", args: { turnScore: 100 }, enabled: false },
          {
            name: "scores",
            args: { turnScoreLabel: "Invisible" },
            isVisible: () => false,
          },
        ]}
      />
    );

    expect(screen.getByText("Visible")).toBeInTheDocument();
    expect(screen.queryByText("100")).not.toBeInTheDocument();
    expect(screen.queryByText("Invisible")).not.toBeInTheDocument();
  });

  it("sorts plugins by order", () => {
    render(
      <PluginRenderer
        plugins={[
          { name: "scores", args: { turnScoreLabel: "Second" }, order: 2 },
          { name: "scores", args: { turnScoreLabel: "First" }, order: 1 },
        ]}
      />
    );

    const items = screen
      .getAllByText(/First|Second/)
      .map((el) => el.textContent);
    expect(items).toEqual(["First", "Second"]);
  });

  it("groups by slot and renders with renderSlot", () => {
    const renderSlot = vi.fn((slot, children) => (
      <div data-testid={`slot-${slot}`}>{children}</div>
    ));

    render(
      <PluginRenderer
        plugins={[
          {
            name: "scores",
            args: { turnScoreLabel: "Header" },
            slot: "header",
          },
          { name: "scores", args: { turnScoreLabel: "99" }, slot: "footer" },
        ]}
        renderSlot={renderSlot}
      />
    );

    expect(screen.getByTestId("slot-header")).toBeInTheDocument();
    expect(screen.getByTestId("slot-footer")).toBeInTheDocument();
    expect(screen.getByText("Header")).toBeInTheDocument();
    expect(screen.getByText("99")).toBeInTheDocument();
  });
});
