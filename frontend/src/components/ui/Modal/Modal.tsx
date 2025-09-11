/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ComponentType } from "react";
import type { ButtonProps } from "@/components/buttons";
import { useEffect, useState, useCallback } from "react";
import classNames from "classnames";
import { Button } from "@/components/buttons";
import { Card, CardProps } from "@/components/ui";
import styles from "./Modal.module.scss";

export interface ModalProps extends CardProps {
  /** Title of the modal */
  title?: string;

  Handle?: ComponentType<{ onClick: () => void }>;

  /** Text shown on the button that opens the modal. */
  handleText?: string;

  /** Text shown on the close button */
  closeButtonText?: string;

  /** Whether the modal is open. Default false; */
  open?: boolean;

  /** Callback called when closing the modal */
  onClose?: () => void;

  /** Whether to wrap the content in a Card.Section */
  wrapInCardSection: boolean;
}

/**
 * An modal window that can be opened and closed.
 */
export default function Modal({
  open: activeInitial = false,
  onClose = () => {},
  handleText = "Open",
  Handle,
  children,
  fullWidth = false,
  Wrapper = ModalCard,
  ...wrapperProps
}: ModalProps) {
  const [active, setActive] = useState(activeInitial);

  const handleClose = useCallback(() => {
    onClose();
    setActive(false);
  }, [onClose]);

  const handleOpen = () => setActive(true);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) handleClose();
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") handleClose();
    };
    if (active) {
      document.addEventListener("keydown", handleKeyDown);
    } else {
      document.removeEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [active, handleClose]);

  if (!Handle) {
    Handle = (props: ButtonProps) => (
      <Button className="primary" title={handleText} {...props} />
    );
  }

  return (
    <>
      <Handle onClick={handleOpen} />

      <div
        className={classNames(styles.modalContainer, active && styles.active)}
        onClick={(e) => e.stopPropagation()}
      >
        <div
          className={classNames(styles.modal, fullWidth && styles.fullWidth)}
        >
          <Wrapper onClose={handleClose} {...wrapperProps}>
            {children}
          </Wrapper>
        </div>
      </div>
      <div
        className={classNames(styles.overlay, active && styles.active)}
        role="presentation"
        aria-hidden={!active}
        onClick={handleOverlayClick}
      />
    </>
  );
}

function ModalCard({
  title,
  onClose,
  showCloseIcon = true,
  showFooter = true,
  wrapInCardSection = true,
  closeButtonText = "Close",
  children,
  ...cardProps
}) {
  return (
    <Card {...cardProps}>
      {showCloseIcon && (
        <button
          className={styles.closeIcon}
          aria-label="Close"
          onClick={onClose}
        >
          ×
        </button>
      )}

      {title && <Card.Header title={title} />}

      {children && wrapInCardSection ? (
        <Card.Section>{children}</Card.Section>
      ) : (
        children
      )}

      {showFooter && (
        <Card.Section>
          <Button
            onClick={onClose}
            className="primary"
            title={closeButtonText}
          />
        </Card.Section>
      )}
    </Card>
  );
}
