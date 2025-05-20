/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ComponentType } from "react";

import { useEffect, useState, useCallback } from "react";
import classNames from "classnames";
import { Button, ButtonProps, Card } from "@/components/ui";
import styles from "./Overlay.module.scss";

export interface OverlayProps extends HTMLAttributes<HTMLDivElement> {
  /** Title of the overlay card */
  title?: string;

  Handle?: ComponentType<{ onClick: () => void }>;

  /** Text shown on the button to open the overlay. */
  handleText?: string;

  /** Text shown on the button used to close the overlay */
  closeButtonText?: string;

  /** Whether the overlay is open. Default false; */
  open?: boolean;

  /** Callback called when closing the overlay */
  onClose?: () => void;
}

/**
 * An modal overlay that can be opened and closed.
 */
export default function Overlay({
  open: activeInitial = false,
  onClose = () => {},
  title,
  handleText = "Open",
  Handle,
  closeButtonText = "Close",
  children,
}: OverlayProps) {
  const [active, setActive] = useState(activeInitial);

  const close = useCallback(() => {
    onClose();
    setActive(false);
  }, [onClose]);

  const open = () => setActive(true);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) close();
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    if (active) {
      document.addEventListener("keydown", handleKeyDown);
    } else {
      document.removeEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [active, close]);

  if (!Handle) {
    Handle = (props: ButtonProps) => (
      <Button
        allowMultipleClicks={true}
        className="primary"
        title={handleText}
        {...props}
      />
    );
  }

  return (
    <>
      <Handle onClick={open} />
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
              aria-label="Close"
              onClick={close}
            >
              ×
            </button>
            {title && <Card.Header title={title} />}

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
