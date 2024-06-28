import React, { useEffect, useState, useRef } from "react";
import { LOGO_TITLE } from "@/config";
import { Switch, Route, Link } from "react-router-dom";
import Cup from "../Cup/Cup";

const LOGO_URL = "/images/experiments/toontjehoger/logo.svg";

const Logo = ({ homeUrl }) => (
    <Link to={homeUrl} className="logo" style={{ backgroundImage: `url(${LOGO_URL}` }}>
        {LOGO_TITLE}
    </Link>
);

const Share = ({ score, label, message }) => {
    const getLink = (url) =>
        url
            .replace("%URL%", encodeURIComponent(window.location))
            .replace(
                "%TEXT%",
                encodeURIComponent(
                    message.replace("%SCORE%", score).replace("%URL%", window.location)
                )
            );

    return (
        <div className="share">
            <h5>{label}</h5>
            <div className="social">
                <a
                    href={getLink("http://twitter.com/share?url=%URL%&text=%TEXT%")}
                    className="twitter fa-brands fa-twitter"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    twitter
                </a>
                <a
                    href={getLink("http://www.facebook.com/sharer.php?u=%URL%&t=%TEXT%")}
                    className="facebook fa-brands fa-facebook"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    facebook
                </a>
                <a
                    href={getLink("whatsapp://send?text=%TEXT%%20%URL%")}
                    data-action="share/whatsapp/share"
                    className="whatsapp fa-brands fa-whatsapp"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Whatsapp
                </a>
            </div>
        </div>
    );
};

const Supporters = ({ intro }) => (
    <div className="supporters">
        <p
            dangerouslySetInnerHTML={{
                __html: intro,
            }}
        />
        <div className="organizations">
            <a
                href="https://www.knaw.nl"
                target="_blank"
                rel="noopener noreferrer"
                className="knaw"
            >
                <img src="/images/experiments/toontjehoger/logo-knaw-white.svg" alt="KNAW" />
            </a>
            <a href="https://www.uva.nl" target="_blank" rel="noopener noreferrer" className="uva">
                <img src="/images/experiments/toontjehoger/logo-uva-white.svg" alt="UvA" />
            </a>
            <a
                href="https://www.mcg.uva.nl/"
                target="_blank"
                rel="noopener noreferrer"
                className="mcg"
            >
                <img
                    src="/images/experiments/toontjehoger/logo-mcg-white.webp"
                    alt="Music Cognition Group"
                />
            </a>
            <a
                href="https://www.amsterdammusiclab.nl"
                target="_blank"
                rel="noopener noreferrer"
                className="aml"
            >
                <img src="/images/logo-full-white.svg" alt="Amsterdam Music Lab" />
            </a>
        </div>
    </div>
);

const useAnimatedScore = (targetScore) => {
    const [score, setScore] = useState(0);

    const scoreValue = useRef(0);

    useEffect(() => {
        if (targetScore === 0) {
            return;
        }

        let id = -1;

        const nextStep = () => {
            // Score step
            const scoreStep = Math.max(
                1,
                Math.min(10, Math.ceil(Math.abs(scoreValue.current - targetScore) / 10))
            );

            // Scores are equal, stop
            if (targetScore === scoreValue.current) {
                return;
            }

            // Add / subtract score
            scoreValue.current += Math.sign(targetScore - scoreValue.current) * scoreStep;
            setScore(scoreValue.current);

            id = setTimeout(nextStep, 50);
        };
        id = setTimeout(nextStep, 50);

        return () => {
            window.clearTimeout(id);
        };
    }, [targetScore]);

    return score;
};

const Score = ({ score, label, scoreClass }) => {
    const currentScore = useAnimatedScore(score);

    return (
        <div className="score">
            <Cup cup={{ className: scoreClass }} />
            <h3>
                {currentScore ? currentScore + " " : ""}
                {label}
            </h3>
        </div>
    );
};

const Privacy = ({ description }) => (
    <div className="privacy">
        <p
            dangerouslySetInnerHTML={{
                __html: description,
            }}
        />
    </div>
);

/** ToontjeHoger is an block view that shows the ToontjeHoger home */
const ToontjeHogerHome = ({ block, config, experiments }) => {
    return (
        <div className="aha__toontjehoger">
            <Logo homeUrl={`/${block.slug}`} />

            {/* Hero */}
            <div className="hero">
                <div className="intro">
                    <h1>{config.payoff}</h1>
                    <p>{config.intro}</p>
                    <div className="actions">
                        {config.main_button_label && (
                            <Link className="btn btn-lg btn-primary" to={config.main_button_url}>
                                {config.main_button_label}
                            </Link>
                        )}
                        {config.intro_read_more && (
                            <Link
                                className="btn btn-lg btn-outline-primary"
                                to={`/${block.slug}/about`}
                            >
                                {config.intro_read_more}
                            </Link>
                        )}
                    </div>
                </div>

                <div className="results">
                    <Score
                        score={config.score}
                        scoreClass={config.score_class}
                        label={config.score_label}
                    />

                    <Share
                        score={config.score}
                        label={config.share_label}
                        message={config.share_message}
                    />
                </div>
            </div>

            {/* Blocks */}
            <div className="experiments">
                <ul>
                    {experiments.map((experiment) => (
                        <li
                            key={experiment.slug}
                            style={{
                                borderBottom: `5px solid ${experiment.color}`,
                            }}
                        >
                            <Link to={"/" + experiment.slug}>
                                <div
                                    className="image"
                                    style={{
                                        backgroundImage: `url(${experiment.image})`,
                                        backgroundColor: experiment.color,
                                    }}
                                ></div>
                                <h3>{experiment.title}</h3>
                                <p>{experiment.description}</p>
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Supporters */}
            <Supporters intro={config.supporters_intro} />

            {/* Privacy */}
            <Privacy description={config.privacy_description} />
        </div>
    );
};

/** ToontjeHoger is an block view that shows the ToontjeHoger home */
const ToontjeHogerAbout = ({ block, config }) => {
    return (
        <div className="aha__toontjehoger about">
            <Logo homeUrl={`/${block.slug}`} />
            {/* Project */}
            <div className="project">
                <h3 className="title">{config.intro_read_more}</h3>
                <h5 className="mb-3">{config.about_title}</h5>
                <p>{config.about_intro}</p>
                <p
                    dangerouslySetInnerHTML={{
                        __html: config.about_description,
                    }}
                />
            </div>
            {/* Streamer */}
            <div className="streamer">
                <h3>
                    <i>{config.about_streamer}</i>
                </h3>
            </div>

            {/* More */}
            <div className="project mb-4">
                <h3 className="title">{config.about_more_title}</h3>
                <p
                    dangerouslySetInnerHTML={{
                        __html: config.about_more_description,
                    }}
                />
            </div>

            {/* Colofon */}
            <div className="colofon">
                <h3 className="title">{config.about_colofon_title}</h3>
                <p
                    dangerouslySetInnerHTML={{
                        __html: config.about_colofon_description,
                    }}
                />
            </div>

            {/* Portrait */}
            <div className="group-portrait">
                <img
                    src="/images/experiments/toontjehoger/mcg-group-portrait.webp"
                    alt="Music Cognition Group"
                />
                <p
                    dangerouslySetInnerHTML={{
                        __html: config.portrait_description,
                    }}
                />
            </div>

            {/* Supporters */}
            <Supporters intro={config.supporters_intro} />

            {/* Privacy */}
            <Privacy description={config.privacy_description} />
        </div>
    );
};

const ToontjeHoger = (props) => {
    return props.block ? (
        <>
            <Switch>
                <Route path={`/${props.block.slug}/about`} exact>
                    <ToontjeHogerAbout {...props} />
                </Route>
                <Route path="*">
                    <ToontjeHogerHome {...props} />
                </Route>
            </Switch>
        </>
    ) : null;
};

export default ToontjeHoger;
