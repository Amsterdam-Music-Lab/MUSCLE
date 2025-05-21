import { vi, describe, beforeEach, afterEach, test, expect } from "vitest";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import * as API from "@/API";

import TuneTwins from "./TuneTwins";

let mock: MockAdapter;

// vi.mock("@/API", () => ({
//   scoreIntermediateResult: vi.fn().mockResolvedValue({ score: 10 }), // mock default
// }));

const initialState = {
  participant: 1,
  session: 1,
  setError: vi.fn(),
  block: { bonus_points: 0 },
};

vi.mock("../../util/stores", () => ({
  __esModule: true,
  default: (fn: any) => {
    return fn(initialState);
  },
  useBoundStore: vi.fn(),
}));

describe.skip("TuneTwins Component", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    mock = new MockAdapter(axios);
    mock.onPost().reply(200, { score: 10 });
  });

  afterEach(() => {
    mock.restore();
  });

  let mockSections = [
    {
      id: 1,
      content: "Card 1",
      url: "/cat-01.jpg",
      inactive: false,
      turned: false,
      noevents: false,
      seen: false,
    },
    {
      id: 2,
      content: "Card 2",
      url: "/cat-02.jpg",
      inactive: false,
      turned: false,
      noevents: false,
      seen: false,
    },
    {
      id: 3,
      content: "Card 1",
      url: "/cat-01.jpg",
      inactive: false,
      turned: false,
      noevents: false,
      seen: false,
    },
    {
      id: 4,
      content: "Card 2",
      url: "/cat-02.jpg",
      inactive: false,
      turned: false,
      noevents: false,
      seen: false,
    },
  ];

  const baseProps = {
    playSection: vi.fn(),
    playerIndex: 0,
    finishedPlaying: vi.fn(),
    onFinish: vi.fn(),
    stopAudioAfter: 4.0,
    showAnimation: false,
    tutorial: {
      lucky_match: "Lucky match tutorial content",
      memory_match: "Memory match tutorial content",
      no_match: "No match tutorial content",
      misremembered: "Misremembered tutorial content",
    },
  };

  test("renders correctly", () => {
    const { getByText } = render(
      <TuneTwins sections={mockSections} setPlayerIndex={vi.fn()} />
    );
    // Not a very good test: if the text changes, this fails.
    expect(getByText("Pick a card...")).not.toBeNull();
  });

  test("flips a card when clicked", async () => {
    render(
      <TuneTwins
        {...baseProps}
        sections={mockSections}
        setPlayerIndex={vi.fn()}
      />
    );
    const cards = screen.getAllByRole("button");

    fireEvent.click(cards[0]);

    await waitFor(() =>
      expect(cards[0].classList.contains("turned")).toBe(true)
    );
  });

  test("updates score after a match", async () => {
    mock.onPost().replyOnce(200, { score: 10 });
    const { getByText } = render(
      <TuneTwins
        {...baseProps}
        sections={mockSections}
        setPlayerIndex={vi.fn()}
      />
    );
    const cards = screen.getAllByRole("button");

    fireEvent.click(cards[0]);
    fireEvent.click(cards[2]);

    await waitFor(() => expect(getByText("Score: 52")).not.toBeNull());
  });

  test("has a blocking overlay in-between turns", async () => {
    mock.onPost().replyOnce(200, { score: 0 });
    render(
      <TuneTwins
        {...baseProps}
        sections={mockSections}
        setPlayerIndex={vi.fn()}
      />
    );
    const cards = screen.getAllByRole("button");

    await waitFor(() =>
      expect(screen.getByTestId("overlay").style.display).toBe("none")
    );

    fireEvent.click(cards[0]);
    fireEvent.click(cards[1]);

    await new Promise((r) => setTimeout(r, 1));
    expect(screen.getByTestId("overlay").style.display).toBe("block");
  });

  test("calls scoreIntermediateResult after each turn", async () => {
    mock.onPost().reply(200, { score: 10 });
    const spy = vi.spyOn(API, "scoreIntermediateResult");
    render(
      <TuneTwins
        {...baseProps}
        sections={mockSections}
        tutorial={undefined}
        setPlayerIndex={vi.fn()}
      />
    );
    const cards = screen.getAllByTestId("play-card");

    mock.onPost().reply(200, { score: 10 });
    fireEvent.click(cards[0]);
    fireEvent.click(cards[2]);
    await new Promise((r) => setTimeout(r, 1));

    fireEvent.click(screen.getByTestId("overlay"));
    await new Promise((r) => setTimeout(r, 1));

    await waitFor(() => screen.getByText("Pick a card"));
    expect(spy).toHaveBeenCalled();

    // cleanup spy
    spy.mockRestore();
  });

  test("ends the game when all pairs are matched", async () => {
    const expectedFirstScore = initialState.block.bonus_points + 10;
    const expectedSecondScore = expectedFirstScore + 20;

    mock.onPost().reply(200, { score: 10 });
    const submitResult = vi.fn();
    render(
      <TuneTwins
        {...baseProps}
        sections={mockSections}
        setPlayerIndex={vi.fn()}
        submitResult={submitResult}
      />
    );
    const cards = screen.getAllByTestId("play-card");

    fireEvent.click(cards[0]);
    fireEvent.click(cards[2]);
    await new Promise((r) => setTimeout(r, 1));
    fireEvent.click(screen.getByTestId("overlay"));
    await new Promise((r) => setTimeout(r, 1));

    waitFor(() => {
      expect(screen.getByTestId("score").textContent).toBe(
        `Score: ${expectedFirstScore}`
      );
      expect(cards[0].classList.contains("disabled")).toBe(true);
      expect(cards[2].classList.contains("disabled")).toBe(true);
    });

    mock.onPost().reply(200, { score: 20 });
    fireEvent.click(cards[1]);
    fireEvent.click(cards[3]);
    await new Promise((r) => setTimeout(r, 1));
    fireEvent.click(screen.getByTestId("overlay"));
    await new Promise((r) => setTimeout(r, 1));
    waitFor(() => {
      expect(screen.getByTestId("score").textContent).toBe(
        `Score: ${expectedSecondScore}`
      );
      expect(cards[1].classList.contains("disabled")).toBe(true);
      expect(cards[3].classList.contains("disabled")).toBe(true);
      expect(submitResult).toHaveBeenCalled();
    });
  });

  // These tests should probably be part of the UI, not the game component?

  // test('displays three columns when sections length is less than or equal to 6', () => {
  //     const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
  //     const { container } = render(<TuneTwins {...baseProps} sections={sections} />);
  //     expect(container.querySelector('.playing-board--three-columns')).not.toBeNull();
  // });

  // test('displays four columns when sections length is greater than 6', () => {
  //     const sections = new Array(7).fill({}).map((_, index) => ({ id: index }));
  //     const { container } = render(<TuneTwins {...baseProps} sections={sections} />);
  //     expect(container.querySelector('.playing-board--three-columns')).toBeNull();
  // });

  test("displays score feedback when scoreFeedbackDisplay is not HIDDEN", () => {
    const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
    const { container } = render(
      <TuneTwins
        {...baseProps}
        sections={sections}
        scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP}
      />
    );
    expect(
      container.querySelector(".matching-pairs__score-feedback")
    ).not.toBeNull();
  });

  test("does not display score feedback when scoreFeedbackDisplay is HIDDEN", () => {
    const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
    const { container } = render(
      <TuneTwins
        {...baseProps}
        sections={sections}
        scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.HIDDEN}
      />
    );
    expect(
      container.querySelector(".matching-pairs__score-feedback")
    ).toBeNull();
  });

  test("displays score feedback on the top when scoreFeedbackDisplay is LARGE_TOP", () => {
    const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
    const { container } = render(
      <TuneTwins
        {...baseProps}
        sections={sections}
        scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP}
      />
    );
    expect(
      container.querySelector(
        ".matching-pairs__score-feedback--small-bottom-right"
      )
    ).toBeNull();
  });

  test("displays score feedback on the bottom right when scoreFeedbackDisplay is SMALL_BOTTOM_RIGHT", () => {
    const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
    const { container } = render(
      <TuneTwins
        {...baseProps}
        sections={sections}
        scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT}
      />
    );
    expect(
      container.querySelector(
        ".matching-pairs__score-feedback--small-bottom-right"
      )
    ).not.toBeNull();
  });
});
