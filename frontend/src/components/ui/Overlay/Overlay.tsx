/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";

import { useEffect, useState } from "react";
import classNames from "classnames";
import { Button, Card } from "@/components/ui";
import styles from "./Overlay.module.scss";

export interface OverlayProps extends HTMLAttributes<HTMLDivElement> {
  /** Title of the overlay card */
  title?: string;

  /** Text shown on the button to open the overlay. */
  openButtonText?: string;

  /** Text shown on the button used to close the overlay */
  closeButtonText?: string;

  /** Whether the overlay is open. Default false; */
  open?: boolean;

  /** Callback called when closing the overlay */
  onClose: () => void;
}

/**
 * An modal overlay that can be opened and closed.
 */
export default function Overlay({
  open: activeInitial = false,
  onClose,
  title = "Tutorial",
  openButtonText = "Open",
  closeButtonText = "Close",
  children,
}: OverlayProps) {
  const [active, setActive] = useState(activeInitial);

  const close = () => {
    onClose();
    setActive(false);
  };
  const open = () => setActive(true);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) close();
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") close();
  };

  useEffect(() => {
    if (active) {
      document.addEventListener("keydown", handleKeyDown);
    } else {
      document.removeEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [active]);

  return (
    <>
      <Button
        onClick={open}
        title={openButtonText}
        className="primary"
        allowMultipleClicks={true}
      />
      <div
        className={classNames(styles.overlay, active && styles.active)}
        aria-hidden={!open}
        role="presentation"
        onClick={handleOverlayClick}
      >
        <div className={styles.content} onClick={(e) => e.stopPropagation()}>
          <Card>
            <button
              className={styles.closeIcon}
              aria-label="Close overlay"
              onClick={close}
            >
              ×
            </button>
            <Card.Header title={title} />

            <Card.Section>{children}</Card.Section>

            <Card.Section>
              <Button
                onClick={close}
                className="primary"
                title={closeButtonText}
                allowMultipleClicks={true}
              />
            </Card.Section>
          </Card>
        </div>
      </div>
    </>
  );
}
