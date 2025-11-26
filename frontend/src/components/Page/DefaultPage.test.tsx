import { it, describe, vi } from "vitest";
import { render, screen } from "@testing-library/react";

import DefaultPage from "./DefaultPage";
import Explainer from "@/components/Explainer/Explainer";

vi.mock("../../util/stores");

describe("DefaultPage Component Tests", () => {
    const explainerProps = {
        instruction: 'Some instruction',
        button: {label: 'Next', color: "#fabacc"},
        steps: [],
        onNext: vi.fn(),
        timer: 1
    }

    const defaultProps = {
        className: 'aha__default',
        title: "Default page title",
        experimentSlug: 'some_experiment',
        nextBlockSlug: 'some_experiment',
    }

    it('renders itself with children', async () => {
        render(
            <DefaultPage {...defaultProps}>
                <Explainer {...explainerProps} />
            </DefaultPage>
        )
        await screen.findByText('Some instruction');
    })

});
