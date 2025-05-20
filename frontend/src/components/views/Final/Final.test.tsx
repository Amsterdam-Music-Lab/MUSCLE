/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { vi, expect, describe, it } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { BrowserRouter } from "react-router-dom";
import * as API from "@/API";

import Block from "@/types/Block";
import Theme from "@/types/Theme";
import Image from "@/types/Image";
import Final, { FinalProps } from "./Final";

vi.mock("@/components/plugins", () => ({
  __esModule: true,
  PluginRenderer: ({ plugins }: any) => (
    <div data-testid="plugin-renderer">
      {plugins?.map((p: any, i: number) => (
        <div key={i} data-testid={`plugin-${p?.name || "unknown"}`}>
          {JSON.stringify(p?.args)}
        </div>
      ))}
    </div>
  ),
}));

vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: (state: any) => any) => {
    const state = {
      setSession: vi.fn(),
      session: 1,
      participant: "participant-id",
    };

    return fn(state);
  },
  useBoundStore: vi.fn(),
}));

vi.mock("@/API", () => ({
  finalizeSession: vi.fn(),
}));

vi.mock("@/config", () => {
  return {
    SILENT_MP3: "",
    API_ROOT: "",
    URLS: {
      AMLHome: "/aml",
      profile: "/profile",
    },
  };
});

vi.mock("@/config/frontend", () => ({
  __esModule: true,
  default: {
    final: {
      plugins: [
        { name: "scoreboard" },
        { name: "linkButton" },
        { name: "userFeedback" },
      ],
    },
  },
}));

let mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const logoImageObj = {
  title: "Logo",
  description: "Logo description",
  file: "https://example.com/logo.png",
  alt: "Logo alt text",
  href: "https://example.com",
  rel: "noopener noreferrer",
  target: "_blank",
} as Image;

const themeObj = {
  backgroundUrl: "https://example.com/background.jpg",
  bodyFontUrl: "https://example.com/font.ttf",
  description: "theme description",
  headingFontUrl: "https://example.com/font.ttf",
  logo: logoImageObj,
  name: "Test Theme",
  footer: null,
  header: null,
} as Theme;

const feedbackInfoObj = {
  header: "Feedback Header",
  button: "Feedback Button",
  contact_body: "Contact Body",
  thank_you: "Thank You",
  show_float_button: true,
} as Block["feedback_info"];

const blockObj = {
  id: 24,
  slug: "test",
  name: "Test",
  playlists: [{ id: "my-playlist", name: "TestPlaylist" }],
  session_id: 42,
  loadingText: "Patience!",
  description: "Test description",
  rounds: 1,
  class_name: "test-class",
  theme: themeObj,
  bonus_points: 0,
  feedback_info: feedbackInfoObj,
  loading_text: "Loading...",
} as Block;

const participantObj = {
  id: 1,
  hash: "hash",
  csrf_token: "csrf_token",
  participant_id_url: "https://example.com/participant",
  country: "NL",
};

const defaultProps = {
  block: blockObj,
  participant: participantObj,
  button: { text: "Next", link: "/next" },
  onNext: vi.fn(),
  score: 100,
  action_texts: {
    all_experiments: "All Blocks",
    profile: "Profile",
    play_again: "Play Again",
  },
  show_participant_link: true,
  participant_id_only: false,
  show_profile_link: true,
  social: {
    channels: [
      "facebook",
      "whatsapp",
      "twitter",
      "weibo",
      "share",
      "clipboard",
    ],
    url: "https://example.com",
    content: "Check this out!",
    tags: ["test", "vitest"],
  },

  // Duplicate; also in block?
  feedback_info: feedbackInfoObj,
} as FinalProps;

describe("Final Component", () => {
  it("renders default plugins", () => {
    render(
      <BrowserRouter>
        <Final {...defaultProps} />
      </BrowserRouter>
    );
    expect(screen.getByTestId("plugin-scoreboard")).toBeInTheDocument();
    expect(screen.getByTestId("plugin-linkButton")).toBeInTheDocument();
    expect(screen.getByTestId("plugin-userFeedback")).toBeInTheDocument();
  });

  it("passes correct data to scoreboard plugin", () => {
    render(
      <Final
        {...defaultProps}
        participant="p1"
        block={{ slug: "b" }}
        score={42}
        totalScore={100}
        percentile={80}
        timeline={[1, 2, 3]}
        timelineStep={2}
      />
    );
    const scoreboard = screen.getByTestId("plugin-scoreboard");
    const args = JSON.parse(scoreboard.textContent!);
    expect(args.turnScore).toBe(42);
    expect(args.totalScore).toBe(100);
    expect(args.percentile).toBe(80);
    expect(args.timeline).toEqual([1, 2, 3]);
    expect(args.timelineStep).toBe(2);
  });

  it("passes correct data to linkButton plugin", () => {
    render(
      <BrowserRouter>
        <Final
          {...defaultProps}
          button={{ text: "Go!", link: "/next-link" }}
          onNext={() => {}}
        />
      </BrowserRouter>
    );
    const linkButton = screen.getByTestId("plugin-linkButton");
    const args = JSON.parse(linkButton.textContent!);
    expect(args.link).toBe("/next-link");
    expect(args.children).toBe("Go!");
  });

  it("passes correct data to userFeedback plugin", () => {
    render(
      <BrowserRouter>
        <Final
          {...defaultProps}
          feedback_info={{
            header: "Feedback Header",
            button: "Feedback Button",
            contact_body: "Contact Body",
            thank_you: "Thank You",
            show_float_button: true,
          }}
        />
      </BrowserRouter>
    );
    const userFeedback = screen.getByTestId("plugin-userFeedback");
    const args = JSON.parse(userFeedback.textContent!).feedbackInfo;
    expect(args.header).toBe("Feedback Header");
    expect(args.button).toBe("Feedback Button");
    expect(args.contact_body).toBe("Contact Body");
    expect(args.thank_you).toBe("Thank You");
    expect(args.show_float_button).toBe(true);
  });

  it("does not render userFeedback plugin if feedback_info is missing", () => {
    render(<Final {...defaultProps} feedback_info={undefined} />);
    expect(screen.queryByTestId("plugin-userFeedback")).not.toBeInTheDocument();
  });
});
