import React from "react";
import { Router } from 'react-router-dom'
import { unmountComponentAtNode } from "react-dom";
import { createMemoryHistory } from 'history'
import { render, screen, waitFor } from "@testing-library/react";

import App from './App';

let container = null;
let history = null;

beforeEach(() => {
    // setup a DOM element as a render target
    container = document.createElement("div");
    document.body.appendChild(container);
    history = createMemoryHistory();
});
  
afterEach(() => {
    // cleanup on exiting
    unmountComponentAtNode(container);
    container.remove();
    container = null;
    history = null;
});

describe('App', () => {
    test("renders an experiment with empty route", async() => { 
        history.push('/');
        render(
        <Router path={history.location} history={history}>
            <App />
        </Router>,
        container
        );
        await waitFor( () => {
            expect(document.querySelector('.aha__experiment') !== null);
        });
    });

    test("reroutes participant/reload/id/hash to experiment", async() => { 
        history.push('/participant/reload/42/blablabla');
        render(
        <Router path={history.location} history={history}>
            <App />
        </Router>,
        container
        );
        await waitFor( () => {
            expect(document.querySelector('.aha__experiment') !== null);
        });
    });

    test("gets profile", async() => { 
        history.push('/profile');
        render(
        <Router path={history.location} history={history}>
            <App />
        </Router>,
        container
        );
        await waitFor( () => {
            expect(document.querySelector('.aha__experiment') !== null);
        });
    });

});
