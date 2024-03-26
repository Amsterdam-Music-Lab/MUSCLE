import React, {useEffect} from "react";
import Button from "../Button/Button";

// Explainer is an experiment view that shows a list of steps
// If the button has not been clicked, onNext will be called automatically after the timer expires (in milliseconds). If timer == null, onNext will only be called after the button is clicked.
const Explainer = ({ instruction, button_label, steps = [], timer = null, onNext }) => {

    useEffect( () => {
        if (timer != null) {
            const id = setTimeout(onNext, timer);
            return () => {clearTimeout(id)}; // if button has been clicked, clear timeout
        }
    }, [onNext, timer])

    return (
        <div data-testid="explainer" className="aha__explainer">
            <h3 className="title">{instruction}</h3>

            <ul>
                {steps.map((step, index) => (
                    <ExplainerItem
                        key={index}
                        number={step.number}
                        description={step.description}
                        delay={index * 250}
                    />
                ))}
            </ul>

            <div className="text-center">
                <Button
                    className="btn-primary anim anim-fade-in anim-speed-300"
                    onClick={onNext}
                    title={button_label}
                    style={{ animationDelay: steps.length * 300 + "ms" }}
                />
            </div>
        </div>
    );
};

// ExplainerItems renders an item in the explainer list, with optional icon or number
const ExplainerItem = ({ number = null, description, delay = 0 }) => (
    <li
        className="anim anim-fade-in-slide-left anim-speed-300"
        style={{ animationDelay: delay + "ms" }}
    >
        {number != null && <h4 className="number">{number}</h4>}
        <span>{description}</span>
    </li>
);

export default Explainer;
