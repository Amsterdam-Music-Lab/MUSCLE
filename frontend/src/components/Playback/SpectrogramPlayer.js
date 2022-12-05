import React, { useCallback } from "react";
import MultiPlayer from "./MultiPlayer";

const SpectrogramPlayer = (props) => {
    const playSection = props.playSection;

    // extraContent callback can be used to add content to each player
    const extraContent = useCallback(
        (index) => {
            const spectrograms = props.playConfig.spectrograms;
            if (!spectrograms) {
                return <p>Warning: No spectrograms found</p>;
            }
            const labels = props.playConfig.spectrogram_labels;

            if (index >= 0 && index < spectrograms.length) {
                return (
                    <div className="spectrogram">
                        <img
                            src={spectrograms[index]}
                            alt="Spectrogram"
                            onClick={() => {
                                playSection(index);
                            }}
                        />
                        {labels && Array.isArray(labels) && labels.length > index && (
                            <span>{labels[index]}</span>
                        )}
                    </div>
                );
            } else {
                return <p>Warning: No spectrograms available for index {index}</p>;
            }
        },
        [props.playConfig.spectrograms, props.playConfig.spectrogram_labels, playSection]
    );

    return (
        <div className="aha__spectrogram-player">
            <MultiPlayer {...props} extraContent={extraContent} />
        </div>
    );
};

export default SpectrogramPlayer;
