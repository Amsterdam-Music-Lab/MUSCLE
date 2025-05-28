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
import { URLS } from "@/config";
import { createConsent, useConsent } from "@/API";
import { Button, Card, LinkButton } from "@/components/ui";
import { LoadingView } from "../LoadingView";

import styles from "./ConsentView.module.scss";

export interface ConsentViewProps {
  title: string;
  text: string;
  experiment: any;
  participant: Pick<Participant, "csrf_token">;
  onNext: () => void;
  confirm: string;
  deny: string;
}

/** Consent is an experiment view that shows the consent text, and handles agreement/stop actions */
export default function ConsentView({
  title,
  text,
  experiment,
  participant,
  onNext,
  confirm,
  deny,
}: ConsentProps) {
  const [consent, loadingConsent] = useConsent(experiment.slug);
  const urlQueryString = window.location.search;

  // Listen for consent, and auto advance if already given
  useEffect(() => {
    if (consent || new URLSearchParams(urlQueryString).get("participant_id")) {
      onNext();
    }
  }, [consent, onNext, urlQueryString]);

  // Click on agree button
  const onAgree = async () => {
    // Store consent
    await createConsent({ experiment, participant });

    // Next!
    onNext();
  };

  const onDownload = async () => {
    const doc = new DOMParser().parseFromString(text, "text/html");
    const txt = doc.body.textContent
      ? doc.body.textContent.split("  ").join("")
      : "";
    const blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
    saveAs(blob, "consent.txt");
  };

  // Loader in case consent is being loaded
  // or it was already given
  if (loadingConsent || consent) {
    return <LoadingView />;
  }

  // Calculate height for consent text to prevent overlapping browser chrome
  const height =
    (document &&
      document.documentElement &&
      document.documentElement.clientHeight) ||
    window.innerHeight;

  const width =
    (document &&
      document.documentElement &&
      document.documentElement.clientWidth) ||
    window.innerWidth;

  const correction = width > 720 ? 300 : 250;

  // Show consent
  return (
    <>
      <Card>
        <Card.Header title={title} />

        <Card.Section>
          <div
            data-testid="consent-text"
            style={{ height: height - correction }}
            dangerouslySetInnerHTML={{ __html: text }}
          />
        </Card.Section>

        <Card.Section>
          <div className={styles.buttons}>
            <LinkButton link={URLS.AMLHome} outline={false}>
              {deny}
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
        title={confirm}
      />
    </>
  );
}

ConsentView.usesOwnLayout = false;
ConsentView.viewName = "consent";
ConsentView.getViewProps = ({ participant, onNext, experiment }) => ({
  title: experiment.consent.title, // ?
  text: experiment.consent.text, // ?
  experiment,
  participant,
  onNext,
  confirm: experiment.consent.confirm, //?
  deny: experiment.consent.deny, //?
});
ConsentView.dependencies = ["experiment", "participant", "onNext"];
