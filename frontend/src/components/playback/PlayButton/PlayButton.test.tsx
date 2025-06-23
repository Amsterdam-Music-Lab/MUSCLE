/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { render, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import PlayButton from "./PlayButton";

// Needed to test disabling behaviour of the component
import buttonStyles from "@/components/buttons/Button/Button.module.scss";

describe("PlayButton Component", () => {
  it("renders correctly", () => {
    const { getByRole } = render(<PlayButton />);
    expect(getByRole("button")).toBeTruthy();
  });

  it("applies correct classes when playing", () => {
    const { container, getByRole } = render(<PlayButton playing={true} />);
    const button = getByRole("button");
    const icon = container.querySelector(".fa");
    expect(button.getAttribute("data-state")).toBe("playing");
    expect(icon.classList.contains("fa-play")).toBeFalsy();
    expect(icon.classList.contains("fa-stop")).toBeTruthy();
  });

  it("applies correct classes when not playing", () => {
    const { container, getByRole } = render(<PlayButton playing={false} />);
    const button = getByRole("button");
    const icon = container.querySelector(".fa");
    expect(button.getAttribute("data-state")).toBe("stopped");
    expect(icon.classList.contains("fa-play")).toBeTruthy();
    expect(icon.classList.contains("fa-stop")).toBeFalsy();
  });

  it("disabled when playing and disableWhenPlaying is true", () => {
    const { getByRole } = render(
      <PlayButton disabled={false} playing={true} disableWhenPlaying={true} />
    );
    const button = getByRole("button");
    expect(button.classList.contains(buttonStyles.disabled)).toBeTruthy();
  });

  it("disabled when playing and disableWhenPlaying is false", () => {
    const { getByRole } = render(
      <PlayButton disabled={false} playing={true} disableWhenPlaying={false} />
    );
    const button = getByRole("button");
    expect(button.classList.contains(buttonStyles.disabled)).toBeFalsy();
  });

  it("applies custom className", () => {
    const { getByRole } = render(<PlayButton className="custom-class" />);
    expect(getByRole("button").classList.contains("custom-class")).toBe(true);
  });

  it("calls onClick when clicked and not disabled", () => {
    const mockPlaySection = vi.fn();
    const { getByRole } = render(<PlayButton onClick={mockPlaySection} />);
    fireEvent.click(getByRole("button"));
    expect(mockPlaySection).toHaveBeenCalledWith(0);
  });

  it("does not call onClick when clicked and disabled", () => {
    const mockPlaySection = vi.fn();
    const { getByRole } = render(
      <PlayButton playing={false} onClick={mockPlaySection} disabled={true} />
    );
    fireEvent.click(getByRole("button"));
    expect(mockPlaySection).not.toHaveBeenCalled();
  });

  it("does not call onClick when playing and disableWhenPlaying=true", () => {
    const mockPlaySection = vi.fn();
    const { getByRole } = render(
      <PlayButton
        playing={true}
        onClick={mockPlaySection}
        disableWhenPlaying={true}
        disabled={false}
      />
    );
    fireEvent.click(getByRole("button"));
    expect(mockPlaySection).not.toHaveBeenCalled();
  });

  it("calls onClick on keyDown", async () => {
    const mockPlaySection = vi.fn();
    const { getByRole } = render(<PlayButton onClick={mockPlaySection} />);
    const button = getByRole("button");
    button.focus();
    await fireEvent.keyDown(button, {
      key: "Enter",
      code: "Enter",
      charCode: 13,
    });
    expect(mockPlaySection).toHaveBeenCalledWith(0);
  });

  it("has correct tabIndex", () => {
    const { getByRole } = render(<PlayButton />);
    expect(getByRole("button").getAttribute("tabIndex")).toBe("0");
  });
});
