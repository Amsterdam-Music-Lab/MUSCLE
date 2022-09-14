import React, { useEffect, useState } from "react";
import { LOGO_TITLE } from "../../config";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect,
    Link,
} from "react-router-dom";

const LOGO_URL = "/images/experiments/toontjehoger/logo.svg";

const Logo = ({ homeUrl }) => (
    <Link
        to={homeUrl}
        className="logo"
        style={{ backgroundImage: `url(${LOGO_URL}` }}
    >
        {LOGO_TITLE}
    </Link>
);

const Supporters = ({ intro }) => (
    <div className="supporters">
        <p>{intro}</p>
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
);

// ToontjeHoger is an experiment view that shows the ToontjeHoger home
const ToontjeHogerHome = ({ experiment, config, experiments }) => {
    return (
        <div className="aha__toontjehoger">
            <Logo homeUrl={`/${experiment.slug}`} />

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

            {/* Supporters */}
            <Supporters intro={config.supporters_intro} />
        </div>
    );
};

// ToontjeHoger is an experiment view that shows the ToontjeHoger home
const ToontjeHogerAbout = ({ experiment, config, experiments }) => {
    return (
        <div className="aha__toontjehoger">
            <Logo homeUrl={`/${experiment.slug}`} />

            <h1 style={{ textAlign: "center" }}>TODO!</h1>

            {/* Supporters */}
            <Supporters intro={config.supporters_intro} />
        </div>
    );
};

const ToontjeHoger = (props) => {
    return (
        <>
            <Switch>
                <Route path={`/${props.experiment.slug}/about`} exact>
                    <ToontjeHogerAbout {...props} />
                </Route>
                <Route path="*">
                    <ToontjeHogerHome {...props} />
                </Route>
            </Switch>
        </>
    );
};

export default ToontjeHoger;
