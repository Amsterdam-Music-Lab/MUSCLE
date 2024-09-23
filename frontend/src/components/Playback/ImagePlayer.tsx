import { useCallback } from "react";
import MultiPlayer from "./MultiPlayer";
import { PlaybackArgs } from "@/types/Playback";

interface ImagePlayerProps extends Pick<PlaybackArgs, "images" | "image_labels"> {
    playSection: (index: number) => void;
}

const ImagePlayer = (props: ImagePlayerProps) => {
    const playSection = props.playSection;

    // extraContent callback can be used to add content to each player
    const extraContent = useCallback(
        (index: number) => {
            const images = props.images;
            if (!images || images.length === 0) {
                return <p>Warning: No images found</p>;
            }
            const labels = props.image_labels;

            if (index >= 0 && index < images.length) {
                return (
                    <div className="image">
                        <img
                            src={images[index]}
                            alt="PlayerImage"
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
        [props.images, props.image_labels, playSection]
    );

    return (
        <div className="aha__image-player">
            <MultiPlayer {...props} extraContent={extraContent} />
        </div>
    );
};

export default ImagePlayer;
