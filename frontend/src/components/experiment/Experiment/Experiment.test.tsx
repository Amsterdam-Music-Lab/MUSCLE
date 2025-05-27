/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { MemoryRouter } from "react-router-dom";
import { screen, waitFor } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { vi, it, expect, describe, beforeEach } from "vitest";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import Experiment from "./Experiment";

let mock = new MockAdapter(axios);

let mockUseParams = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => mockUseParams(),
  };
});

vi.mock("@/components/views", () => ({
  __esModule: true,
  Error: ({ message }) => <div>{message}</div>,
  ConsentView: (props: any) => (
    <div className="consent-text" data-testid="consent-mock">
      {props.text || "Mocked Consent"}
    </div>
  ),
  Loading: () => <div>Loading...</div>,
}));

const getBlock = (overrides = {}) => {
  return {
    slug: "some_slug",
    name: "Some Block",
    ...overrides,
  };
};

const block1 = getBlock({
  slug: "some_slug",
  name: "Some Block",
});

const theme = {
  backgroundUrl: "someurl.com",
  bodyFontUrl: "bodyFontUrl.com",
  description: "Description of the theme",
  headingFontUrl: "headingFontUrl.com",
  logo: {
    title: "Logo title",
    description: "Logo description",
    file: "logo.jpg",
    alt: "Logo alt",
    href: "https://www.example.com",
    rel: "noopener noreferrer",
    target: "_blank",
  },
  name: "Awesome theme",
  footer: {
    disclaimer: "disclaimer",
    logos: [
      {
        file: "some/logo.jpg",
        href: "some.url.net",
        alt: "Our beautiful logo",
      },
    ],
    privacy: "privacy",
  },
};

const blockWithAllProps = getBlock({
  image: "some_image.jpg",
  description: "Some description",
});

describe("Experiment", () => {
  beforeEach(() => {
    mockUseParams.mockReturnValue({ slug: "some_experiment" });
  });

  it("forwards to a single block if it receives an empty dashboard array", async () => {
    mock.onGet().replyOnce(200, { dashboard: [], nextBlock: block1 });

    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.queryByRole("menu")).toBeFalsy();
    });
  });

  it("shows a loading spinner while loading", () => {
    mock.onGet().replyOnce(200, new Promise(() => {}));
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    waitFor(() => {
      expect(document.querySelector(".loader-container")).not.toBeNull();
    });
  });

  it("shows a placeholder if no image is available", () => {
    mock.onGet().replyOnce(200, { dashboard: [block1], nextBlock: block1 });
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    waitFor(() => {
      expect(document.querySelector(".loader-container")).not.toBeNull();
    });
  });

  it("shows the image if it is available", () => {
    mock
      .onGet()
      .replyOnce(200, { dashboard: [blockWithAllProps], nextBlock: block1 });
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    waitFor(() => {
      expect(document.querySelector("img")).not.toBeNull();
    });
  });

  it("shows the description if it is available", () => {
    mock
      .onGet()
      .replyOnce(200, { dashboard: [blockWithAllProps], nextBlock: block1 });
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    waitFor(() => {
      const description = screen.getByText("Some description");
      expect(description).not.toBeNull();
    });
  });

  it("shows consent first if available", async () => {
    mock.onGet().replyOnce(200, {
      consent: { text: "<p>This is our consent form!</p>" },
      dashboard: [blockWithAllProps],
      nextBlock: block1,
    });
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(document.querySelector(".consent-text")).not.toBeNull();
    });
  });

  it("shows a footer if a theme with footer is available", async () => {
    mock.onGet().replyOnce(200, {
      dashboard: [blockWithAllProps],
      nextBlock: block1,
      theme,
    });
    render(
      <MemoryRouter>
        <Experiment />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(document.querySelector(".aha__footer")).not.toBeNull();
    });
  });
});
