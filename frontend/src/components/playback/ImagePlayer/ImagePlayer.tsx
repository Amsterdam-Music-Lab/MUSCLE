/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PlaybackArgs } from "@/types/Playback";
import type { MultiPlayerProps } from "../MultiPlayer";
import { useCallback } from "react";
import { MultiPlayer } from "../MultiPlayer";
import classNames from "@/util/classNames";
import styles from "./ImagePlayer.module.scss";

export interface ImagePlayerProps extends MultiPlayerProps {
  /**
   * An list of image source
   */
  images: PlaybackArgs["images"];

  imageLabels: PlaybackArgs["image_labels"];
}

export default function ImagePlayer({
  playSection,
  numSections,
  images,
  imageLabels,
  className,
  ...multiPlayerProps
}: ImagePlayerProps) {
  const hasLabels = imageLabels && Array.isArray(imageLabels);

  function extraContent(index: number) {
    if (!images || images.length === 0) {
      return <p>Warning: No images found</p>;
    }

    if (index >= 0 && index < images.length) {
      return (
        <ImagePlayerImg
          src={images[index]}
          onClick={() => playSection(index)}
          label={(hasLabels && imageLabels[index]) ?? undefined}
        />
      );
    } else {
      return <p>Warning: No spectrograms available for index {index}</p>;
    }
  }

  const extraContentCallback = useCallback(extraContent, [
    images,
    imageLabels,
    playSection,
    hasLabels,
  ]);

  return (
    <MultiPlayer
      playSection={playSection}
      numSections={numSections}
      extraContent={extraContentCallback}
      className={classNames(styles.imagePlayer, className)}
      {...multiPlayerProps}
    />
  );
}

interface ImagePlayerImgProps {
  src: string;
  label: string;
  onClick: () => void;
}

function ImagePlayerImg({ src, label, onClick }: ImagePlayerImgProps) {
  return (
    <div className={styles.image}>
      <img src={src} alt="PlayerImage" onClick={onClick} />
      {label && <span className={styles.label}>{label}</span>}
    </div>
  );
}
