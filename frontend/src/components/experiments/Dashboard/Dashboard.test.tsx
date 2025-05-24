/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type Block from "@/types/Block";
import { MemoryRouter } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Dashboard from "./Dashboard";

const getExperiment = (overrides = {}) => {
  return {
    id: 1,
    slug: "some_slug",
    name: "Some Experiment",
    description: "Some description",
    image: {},
    ...overrides,
  } as Block;
};

const experiment1 = getExperiment({
  id: 1,
  slug: "some_slug",
  name: "Some Experiment",
  description: null,
});
const experiment2 = getExperiment({
  id: 2,
  slug: "another_slug",
  name: "Another Experiment",
  description: "Some description",
});

const experimentWithDashboard = { dashboard: [experiment1, experiment2] };

const header = {
  nextBlockButtonText: "Next experiment",
  aboutButtonText: "About us",
};
const experimentWithTheme = {
  dashboard: [experiment1, experiment2],
  theme: {
    backgroundUrl: "some/url.com",
    bodyFontUrl: "font/url.com",
    description: "description of the theme",
    headingFontUrl: "another/font/url.com",
    logo: {
      title: "Logo title",
      description: "Logo description",
      file: "logo.jpg",
      alt: "Logo alt",
      href: "https://www.example.com",
      rel: "noopener noreferrer",
      target: "_blank",
    },
    name: "Experiment name",
    header: header,
  },
};

describe("Dashboard", () => {
  it("shows a dashboard of multiple experiments if it receives an array", async () => {
    render(
      <MemoryRouter>
        <Dashboard experiment={experimentWithDashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByRole("menu")).toBeTruthy();
    });
  });

  it("shows a placeholder if an experiment has no image", async () => {
    render(
      <MemoryRouter>
        <Dashboard experiment={experimentWithDashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByRole("menu")).toBeTruthy();
      expect(
        screen.getByRole("menu").querySelector(".placeholder")
      ).toBeTruthy();
    });
  });

  it("links to the experiment with the correct slug", async () => {
    render(
      <MemoryRouter>
        <Dashboard experiment={experimentWithDashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByRole("menu")).toBeTruthy();
      expect(
        screen.getByRole("menu").querySelector("a").getAttribute("href")
      ).toBe("/block/some_slug");
    });
  });

  it("links to the experiment with the correct slug and participant id if the participand id url is present", async () => {
    render(
      <MemoryRouter>
        <Dashboard
          experiment={experimentWithDashboard}
          participantIdUrl="some_id"
        />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByRole("menu")).toBeTruthy();
      expect(
        screen.getByRole("menu").querySelector("a").getAttribute("href")
      ).toBe("/block/some_slug?participant_id=some_id");
    });
  });

  it("does not show a header if no theme.header is present", () => {
    render(
      <MemoryRouter>
        <Dashboard
          experiment={experimentWithDashboard}
          participantIdUrl="some_id"
        />
      </MemoryRouter>
    );
    const aboutButton = screen.queryByText("About us");
    expect(aboutButton).toBeFalsy();
  });

  it("shows a header if a theme.header is present", async () => {
    render(
      <MemoryRouter>
        <Dashboard
          experiment={experimentWithTheme}
          participantIdUrl="some_id"
        />
      </MemoryRouter>
    );
    await screen.findByText("About us");
  });
});
