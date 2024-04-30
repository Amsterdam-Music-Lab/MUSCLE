import React from "react";
import { vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";

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

        

        it('renders itself with children', async () => {
            render(
                <DefaultPage className='aha__default' title="Default page title">
                    <Explainer { ...explainerProps} />
                </DefaultPage>
            )
            await screen.findByText('Default  page title');
        })
    })

    describe("with a theme", () => {
        vi.mock('../../util/stores', () => ({
            __esModule: true,
            default: (fn) => {
                const state = {
                    theme: {
                        header: {
                            nextExperimentButtonText
                        }
                    }
                };
                
                return fn(state);
            },
            useBoundStore: vi.fn()
        }));

        it('renders itself with children', async () => {
            render(
                <DefaultPage className='aha__default' title="Default page title">
                    <Explainer { ...explainerProps} />
                </DefaultPage>
            )
            await screen.findByText('Default page title');
        })
    })
    
});