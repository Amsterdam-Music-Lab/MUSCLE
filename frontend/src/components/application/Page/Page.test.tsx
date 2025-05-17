import { it, describe, vi } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { Explainer } from "@/components/views";
import Page from "./Page";

vi.mock("@/util/stores");

describe("Page Component Tests", () => {
  const explainerProps = {
    instruction: "Some instruction",
    button_label: "Next",
    steps: [],
    onNext: vi.fn(),
    timer: 1,
  };

  const defaultProps = {
    className: "aha__default",
    title: "Default page title",
    // experimentSlug: "some_experiment", // Unsupported arguments?
    // nextBlockSlug: "some_experiment", // Unsupported arguments?
  };

  it("renders itself with children", async () => {
    const { findByText } = render(
      <Page {...defaultProps}>
        <Explainer {...explainerProps} />
      </Page>
    );
    await findByText("Some instruction");
  });
});
