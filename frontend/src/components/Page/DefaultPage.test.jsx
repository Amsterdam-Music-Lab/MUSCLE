import React from "react";
import { beforeEach, vi } from "vitest";
import { render, screen } from "@testing-library/react";

import DefaultPage from "./DefaultPage";
import Explainer from "@/components/Explainer/Explainer";

vi.mock("../../util/stores");

describe("DefaultPage Component Tests", () => {
    const explainerProps = {
        instruction: 'Some instruction',
        button_label: 'Next',
        steps: [],
        onNext: vi.fn(),
        timer: 1
    }

    const defaultProps = {
        className:'aha__default',
        title: "Default page title",
        logoClickConfirm: null,
        collectionSlug: 'some_collection',
        nextExperimentSlug: 'some_experiment',
    }

    describe("without a theme", () => {
        vi.mock('../../util/stores', () => ({
            __esModule: true,
            default: (fn) => {
                const state = {
                    theme: null
                };
                
                return fn(state);
            },
            useBoundStore: vi.fn()
        }));

        beforeEach(() => {
            render(
                <DefaultPage { ...defaultProps }>
                    <Explainer { ...explainerProps } />
                </DefaultPage>
            )
        })

        

        it.todo('renders itself with children');
        
        it.todo('does not shows a header');
    })

    describe("with a theme", () => {
        vi.mock('../../util/stores', () => ({
            __esModule: true,
            default: (fn) => {
                const state = {
                    theme: {
                        header: {
                            next_experiment_button_text: 'Next!',
                            about_button_text: 'All you ever wanted to know',
                            show_score: false
                        }
                    }
                };
                
                return fn(state);
            },
            useBoundStore: vi.fn()
        }));

        beforeEach(() => {
            render(
                <DefaultPage { ...defaultProps }>
                    <Explainer { ...explainerProps} />
                </DefaultPage>
            )
        });

        it.todo('renders itself with children');

        it.todo('shows a header');
    })
    
});