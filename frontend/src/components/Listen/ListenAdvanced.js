import React from "react";
import Circle from "../Circle/Circle";
import Button from "../Button/Button";

// ListenAdvanced is a base view for experiment views with 2 buttons
const ListenAdvanced = ({
    circleContent = null,
    introduction = "",
    instruction = "",
    duration = 0.01,
    color = "white",
    running = true,
    className = "",
    buttonsActive = true,
    button1Label = "No",
    button1Color = "red",
    button2Label = "Yes",
    button2Color = "teal",
    onButton1Click,
    onButton2Click,
    onFinish,
}) => {
    return (
        <div
            className={
                "aha__listen d-flex flex-column justify-content-center align-items-center " +
                className
            }
        >
            {/* Introduction */}
            {introduction && (
                <div className="introduction d-flex justify-content-center align-items-center">
                    <h5 className="text-center">{introduction}</h5>
                </div>
            )}

            {/* Circle */}
            <div className="circle">
                <Circle
                    key={instruction + duration}
                    running={running}
                    duration={duration}
                    onFinish={onFinish}
                    color={color}
                />
                <div className="circle-content">{circleContent}</div>
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
                        onClick={onButton1Click}
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
                        onClick={onButton2Click}
                        title={button2Label}
                    />
                )}
            </div>
        </div>
    );
};

export default ListenAdvanced;
