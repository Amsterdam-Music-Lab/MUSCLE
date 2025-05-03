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
import PluginCard from "./PluginCard";

// Dummy components for testing
const TestComponent = ({ label }: { label: string }) => <div>{label}</div>;
const AnotherComponent = ({ value }: { value: string }) => <span>{value}</span>;

const components = {
  TestComponent,
  AnotherComponent,
};

describe("PluginCard", () => {
  it("renders plugins with specified components", () => {
    render(
      <PluginCard
        plugins={[
          {
            name: "TestComponent",
            args: { label: "Hello" },
            title: "Section 1",
          },
          {
            name: "AnotherComponent",
            args: { value: "World" },
            title: "Section 2",
          },
        ]}
        components={components}
      />
    );

    expect(screen.getByText("Hello")).toBeInTheDocument();
    expect(screen.getByText("World")).toBeInTheDocument();
  });

  it("applies propsFn to plugin props", () => {
    render(
      <PluginCard
        plugins={[
          {
            name: "TestComponent",
            args: { label: "Dynamic" },
            propsFn: (args) => ({ title: `Title: ${args.label}` }),
          },
        ]}
        components={components}
      />
    );

    expect(screen.getByText("Title: Dynamic")).toBeInTheDocument();
  });

  it("warns if plugin has no name", () => {
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    render(
      <PluginCard
        plugins={[{ args: { label: "Missing" } } as any]}
        components={components}
      />
    );

    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining("nas no name")
    );
    warnSpy.mockRestore();
  });

  it("warns if component is not found", () => {
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    render(
      <PluginCard
        plugins={[{ name: "MissingComponent", args: {} }]}
        components={components}
      />
    );

    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Component "MissingComponent" not found.')
    );
    warnSpy.mockRestore();
  });

  it("renders children when provided", () => {
    render(
      <PluginCard plugins={[]} components={components}>
        <p>Fallback content</p>
      </PluginCard>
    );

    expect(screen.getByText("Fallback content")).toBeInTheDocument();
  });

  it("sorts plugins by the `order` property", () => {
    render(
      <PluginCard
        plugins={[
          { name: "TestComponent", args: { label: "Second" }, order: 2 },
          { name: "TestComponent", args: { label: "First" }, order: 1 },
          { name: "TestComponent", args: { label: "Third" }, order: 3 },
        ]}
        components={components}
      />
    );

    const labels = screen
      .getAllByText(/First|Second|Third/)
      .map((el) => el.textContent);
    expect(labels).toEqual(["First", "Second", "Third"]);
  });

  it("only renders plugins where visible is not false", () => {
    render(
      <PluginCard
        plugins={[
          {
            name: "TestComponent",
            args: { label: "Visible Plugin" },
            visible: true,
          },
          {
            name: "TestComponent",
            args: { label: "Hidden Plugin" },
            visible: false,
          },
          {
            name: "TestComponent",
            args: { label: "Default Visibility" }, // no visible field
          },
        ]}
        components={components}
      />
    );

    expect(screen.getByText("Visible Plugin")).toBeInTheDocument();
    expect(screen.getByText("Default Visibility")).toBeInTheDocument();
    expect(screen.queryByText("Hidden Plugin")).not.toBeInTheDocument();
  });
});
