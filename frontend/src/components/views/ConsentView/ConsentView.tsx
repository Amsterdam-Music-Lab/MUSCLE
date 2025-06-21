/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type Participant from "@/types/Participant";

import { useEffect } from "react";
import { saveAs } from "file-saver";
import { routes } from "@/config";
import classNames from "classnames";
import { createConsent, useConsent } from "@/API";
import { Button, LinkButton } from "@/components/buttons";
import { Card } from "@/components/ui";
import { RenderHtml } from "@/components/utils";
import { LoadingView } from "../LoadingView";
import styles from "./ConsentView.module.scss";
import "@/scss/prose.scss";
export interface ConsentViewProps {
  /**
   * A html string with the consent text
   */
  consentHtml: string;

  /** The experiment slug */
  experimentSlug: string;

  /** The current participant */
  participant: Pick<Participant, "csrf_token">;

  /** Callback called when clicking the confirm button */
  onConfirm?: () => void;

  /** Title of the consent form. Default "Consent" */
  title?: string;

  /** Text shown on the confirm button */
  confirmLabel?: string;

  /** Text shown on the deny button */
  denyLabel?: string;
}

/**
 * Consent is an experiment view that shows the consent text,
 * and handles agreement/stop actions
 */
export default function ConsentView({
  experimentSlug,
  consentHtml,
  participant,
  onConfirm = () => {},
  title = "Consent",
  confirmLabel = "Agree",
  denyLabel = "Disagree",
}: ConsentViewProps) {
  const [consent, loadingConsent] = useConsent(experimentSlug);
  const urlQueryString = window.location.search;

  // Listen for consent, and auto advance if already given
  // TODO this is conflating the logic with the interface: this really is routing
  // behaviour that should be handled by the router/controller, not the view.
  // --> See e.g. Block.tsx which uses the useConsent hook to handle this.
  useEffect(() => {
    if (consent || new URLSearchParams(urlQueryString).get("participant_id")) {
      onConfirm();
    }
  }, [consent, onConfirm, urlQueryString]);

  // Store consent on agree and continue
  const onAgree = async () => {
    await createConsent({ experimentSlug, participant });
    onConfirm();
  };

  const onDownload = async () => {
    const doc = new DOMParser().parseFromString(consentHtml, "text/html");
    const txt = doc.body.textContent
      ? doc.body.textContent.split("  ").join("")
      : "";
    const blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
    saveAs(blob, "consent.txt");
  };

  // Loader in case consent is being loaded or it was already given
  if (loadingConsent || consent) {
    return <LoadingView />;
  }

  // Show consent
  return (
    <>
      <Card>
        <Card.Header title={title} />

        <Card.Section className={classNames(styles.consentHtml, "prose")}>
          <RenderHtml html={consentHtml} />
        </Card.Section>

        <Card.Section>
          <div className={styles.buttons}>
            <LinkButton link={routes.noconsent(experimentSlug)} outline={false}>
              {denyLabel}
            </LinkButton>
            <Button
              data-testid="download-button"
              onClick={onDownload}
              outline={false}
              variant="secondary"
            >
              Download consent form
            </Button>
          </div>
        </Card.Section>
      </Card>

      <Button
        variant="secondary"
        rounded={false}
        size="lg"
        onClick={onAgree}
        title={confirmLabel}
      />
    </>
  );
}

ConsentView.usesOwnLayout = false;
ConsentView.viewName = "consent";
ConsentView.getViewProps = ({ participant, onNext, experiment }) => ({
  experimentSlug: experiment.slug,
  consentHtml: experiment.consent.text,
  participant,
  onConfirm: onNext,
  title: experiment.consent.title,
  confirmLabel: experiment.consent.confirm,
  denyLabel: experiment.consent.deny,
});
ConsentView.dependencies = ["experiment", "participant", "onNext"];
