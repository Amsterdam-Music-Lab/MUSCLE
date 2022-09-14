import React, { useEffect, useState } from "react";
import { LOGO_TITLE } from "../../config";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect,
} from "react-router-dom";

const LOGO_URL = "/images/experiments/toontjehoger/logo.svg";

// ToontjeHoger is an experiment view that shows the ToontjeHoger home
const ToontjeHogerHome = ({ config, experiments }) => {
    return (
        <div className="aha__toontjehoger">
            <div
                className="logo"
                style={{ backgroundImage: `url(${LOGO_URL}` }}
            >
                {LOGO_TITLE}
            </div>

            {/* Hero */}
            <div className="hero">
                <div className="intro">
                    <h1>{config.payoff}</h1>
                    <p>{config.intro}</p>
                    <div className="actions">
                        {config.main_button_label && (
                            <a
                                className="btn btn-lg btn-primary"
                                href={config.main_button_url}
                            >
                                {config.main_button_label}
                            </a>
                        )}
                        {config.intro_read_more && (
                            <a
                                className="btn btn-lg btn-outline-primary"
                                href="#about"
                            >
                                {config.intro_read_more}
                            </a>
                        )}
                    </div>
                </div>
            </div>

            {/* Experiments */}
            <div className="experiments">
                <ul>
                    {experiments.map((experiment) => (
                        <li
                            key={experiment.slug}
                            style={{
                                borderBottom: `5px solid ${experiment.color}`,
                            }}
                        >
                            <a href={"/" + experiment.slug}>
                                <div
                                    className="image"
                                    style={{
                                        backgroundImage: `url(${experiment.image})`,
                                        backgroundColor: experiment.color,
                                    }}
                                ></div>
                                <h3>{experiment.title}</h3>
                                <p>{experiment.description}</p>
                            </a>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Support */}
            <div className="supporters">
                <p>{config.supporters_intro}</p>
                <div className="organizations">
                    <a
                        href="https://www.knaw.nl"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="knaw"
                    >
                        <img
                            src="/images/experiments/toontjehoger/logo-knaw-white.svg"
                            alt="KNAW"
                        />
                    </a>
                </div>
            </div>
        </div>
    );
};

const ToontjeHoger = (props) => {
    return (
        <>
            <Switch>
                <Route path="about">About</Route>
                <Route path="*">
                    <ToontjeHogerHome {...props} />
                </Route>
            </Switch>
        </>
    );
};

export default ToontjeHoger;
