/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ReactNode } from "react";
import type { InputGroupProps } from "@/components/ui";

import { useRef } from "react";
import classNames from "classnames";
import { useParticipantLink } from "@/API";
import { Input, InputGroup, Button, InputLabel } from "@/components/ui";
import styles from "./ParticipantLink.module.scss";

export interface ParticipantLinkProps extends InputGroupProps {
  /** Label text shown in front of the component */
  label?: ReactNode;

  /** Whether to only show the id of the participant */
  participantIDOnly?: boolean;

  /** Default placeholder, should not be visible since the link is then shown */
  placeholder?: string;

  /** Placeholder shown when the link is loading */
  placeholderLoading?: string;

  /** Placeholder whenever an error occurs */
  placeholderError?: string;
}

/**
 * A component that allows you to copy the link to a participants page.
 */
export default function ParticipantLink({
  label,
  placeholder = "Participant link",
  placeholderLoading = "Loading...",
  placeholderError = "Something went wrong...",
  participantIDOnly = false,
  className,
  ...inputGroupProps
}: ParticipantLinkProps) {
  const [link, loadingLink] = useParticipantLink();
  const linkInput = useRef<HTMLInputElement>(null);

  const copyLink = () => {
    if (!linkInput.current) return;
    linkInput.current.select();
    linkInput.current.setSelectionRange(0, 99999); // For mobile
    navigator.clipboard.writeText(linkInput.current.value);
  };

  const formatLink = (url: string) => {
    const formatted = participantIDOnly ? url.split("/")[6] : url;
    return formatted;
  };

  return (
    <InputGroup
      className={classNames(styles.container, className)}
      {...inputGroupProps}
    >
      {label && <InputLabel htmlFor="participant-id">{label}</InputLabel>}

      <Input
        ref={linkInput}
        id="participant-id"
        placeholder={
          loadingLink
            ? placeholderLoading
            : !link
            ? placeholderError
            : placeholder
        }
        value={link ? formatLink(link.url) : ""}
        readOnly
        data-testid="participant-link"
      />

      <Button
        disabled={!link}
        onClick={copyLink}
        onKeyDown={copyLink}
        data-testid="copy-button"
      >
        {link?.copy_message ?? "Copy"}
      </Button>
    </InputGroup>
  );
}
