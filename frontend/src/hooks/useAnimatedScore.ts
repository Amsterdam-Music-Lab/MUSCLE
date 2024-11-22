import { useEffect, useState } from "react";

const useAnimatedScore = (targetScore: number) => {
    const [score, setScore] = useState(0);

    useEffect(() => {
        if (targetScore === 0) {
            setScore(0);
            return;
        }

        let animationFrameId: number;

        const nextStep = () => {
            setScore((prevScore) => {
                const difference = targetScore - prevScore;
                const scoreStep = Math.max(1, Math.min(10, Math.ceil(Math.abs(difference) / 10)));

                if (difference === 0) {
                    cancelAnimationFrame(animationFrameId);
                    return prevScore;
                }

                const newScore = prevScore + Math.sign(difference) * scoreStep;
                animationFrameId = requestAnimationFrame(nextStep);
                return newScore;
            });
        };

        // Start the animation
        animationFrameId = requestAnimationFrame(nextStep);

        // Cleanup function to cancel the animation frame
        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, [targetScore]);

    return score;
};

export default useAnimatedScore;