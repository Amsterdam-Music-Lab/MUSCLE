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
import DashboardView from "./DashboardView";

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

const dashboard = [experiment1, experiment2];

const experimentWithDashboard = { dashboard };

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

describe("DashboardView", () => {
  it("shows a dashboard of multiple experiments if it receives an array", async () => {
    render(
      <MemoryRouter>
        <DashboardView dashboard={dashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByTestId("dashboard-experiments")).toBeTruthy();
    });
  });

  it.skip("shows a placeholder if an experiment has no image", async () => {
    // Disabled
    render(
      <MemoryRouter>
        <DashboardView dashboard={dashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByTestId("dashboard-experiments")).toBeTruthy();
      expect(
        screen
          .getByTestId("dashboard-experiments")
          .querySelector(".placeholder")
      ).toBeTruthy();
    });
  });

  it.skip("links to the experiment with the correct slug", async () => {
    // Doesn't work any longer since Card.Option relies on onClick

    render(
      <MemoryRouter>
        <DashboardView dashboard={dashboard} />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByTestId("dashboard-experiments")).toBeTruthy();
      expect(
        screen
          .getByTestId("dashboard-experiments")
          .querySelector("a")
          .getAttribute("href")
      ).toBe("/block/some_slug");
    });
  });

  it.skip("links to the experiment with the correct slug and participant id if the participand id url is present", async () => {
    // Doesn't work any longer since Card.Option relies on onClick

    render(
      <MemoryRouter>
        <DashboardView dashboard={dashboard} participantIdUrl="some_id" />
      </MemoryRouter>
    );
    await waitFor(() => {
      expect(screen.getByTestId("dashboard-experiments")).toBeTruthy();
      expect(
        screen.getByRole("menu").querySelector("a").getAttribute("href")
      ).toBe("/block/some_slug?participant_id=some_id");
    });
  });

  it("does not show a header if no theme.header is present", () => {
    render(
      <MemoryRouter>
        <DashboardView
          {...experimentWithDashboard}
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
        <DashboardView header={header} />
      </MemoryRouter>
    );
    await screen.findByText("About us");
  });
});
