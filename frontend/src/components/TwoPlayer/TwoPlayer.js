import React, { useState, useRef, useEffect } from "react";
import * as audio from "../../util/audio";
import Button from "../Button/Button";
import PlayerSmall from "../PlayButton/PlayerSmall";
import { MEDIA_ROOT } from "../../config";

// TwoPlayer is a base view for experiment views with 2 buttons
const TwoPlayer = ({
    introduction = "",
    instruction = "",
    className = "",
    section1,
    section2,
    button1Label = "Fragment A",
    button1Color = "teal",
    button2Label = "Fragment B",
    button2Color = "blue",
    section1Color = "teal",
    section1Label = "A",
    section2Color = "blue",
    section2Label = "B",
    listenFirst = false,
    onButton1Click,
    onButton2Click,
}) => {
    const section1Played = useRef(0);
    const section2Played = useRef(0);
    const cancelEvents = useRef(null);

    const [buttonsActive, setButtonsActive] = useState(!listenFirst);
    const [playing, setPlaying] = useState(0);

    const playSection = (nr = 0) => {
        if (playing === nr || nr === 0) {
            setPlaying(0);
            audio.pause();
        } else {
            setPlaying(nr);
            switch (nr) {
                case 1:
                    playMedia(MEDIA_ROOT + section1.url);
                    section1Played.current++;
                    break;
                case 2:
                    playMedia(MEDIA_ROOT + section2.url);
                    section2Played.current++;
                    break;
                default:
                // nothing
            }

            // enable buttons when both sections started playing
            if (
                section1Played.current > 0 &&
                section2Played.current > 0 &&
                !buttonsActive
            ) {
                setButtonsActive(true);
            }
        }
    };

    const cancelActiveEvents = () => {
        // cancel events
        if (cancelEvents.current) {
            cancelEvents.current();
            cancelEvents.current = null;
        }
    };

    useEffect(() => {
        cancelActiveEvents();
    }, []);

    const playMedia = (url) => {
        audio.pause();

        cancelActiveEvents();
        cancelEvents.current = audio.listenOnce("ended", setPlaying);

        audio.loadUntilAvailable(url, () => {
            audio.setVolume(1);
            audio.playFrom(0);
        });
    };

    return (
        <div
            className={
                "aha__two-player d-flex flex-column justify-content-center align-items-center " +
                className
            }
        >
            {/* Introduction */}
            {introduction && (
                <div className="introduction d-flex justify-content-center align-items-center">
                    <h5 className="text-center">{introduction}</h5>
                </div>
            )}

            {/* Players */}
            <div className="players d-flex flex-row justify-content-around align-items-center mb-4 mt-3 w-100">
                <PlayerSmall
                    colorClass={section1Color}
                    label={section1Label}
                    playing={playing === 1}
                    onClick={() => {
                        playSection(1);
                    }}
                />
                <PlayerSmall
                    colorClass={section2Color}
                    label={section2Label}
                    playing={playing === 2}
                    onClick={() => {
                        playSection(2);
                    }}
                />
            </div>

            {/* Instruction */}
            {instruction && (
                <div className="instruction d-flex justify-content-center align-items-center">
                    <h3 className="text-center">{instruction}</h3>
                </div>
            )}

            {/* Buttons */}
            <div className="buttons d-flex flex-wrap justify-content-around p-3 w-100">
                {/* Button1 */}
                {onButton1Click && (
                    <Button
                        key={"button1"}
                        className={"btn-" + button1Color}
                        padding="px-3"
                        active={buttonsActive}
                        onClick={() => {
                            onButton1Click({
                                section1_played: section1Played.current,
                                section2_played: section2Played.current,
                            });
                        }}
                        title={button1Label}
                    />
                )}

                {/* Button2 */}
                {onButton2Click && (
                    <Button
                        key={"button2"}
                        className={"btn-" + button2Color}
                        padding="px-3"
                        active={buttonsActive}
                        onClick={() => {
                            onButton2Click({
                                section1_played: section1Played.current,
                                section2_played: section2Played.current,
                            });
                        }}
                        title={button2Label}
                    />
                )}
            </div>
        </div>
    );
};

export default TwoPlayer;
