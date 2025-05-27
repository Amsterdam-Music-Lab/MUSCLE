/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type Participant from "@/types/Participant";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as EmailValidator from "email-validator";
import classNames from "classnames";
import { URLS } from "@/config";
import useBoundStore from "@/util/stores";
import { shareParticipant } from "@/API";
import { LoadingView } from "../LoadingView";
import { NarrowLayout, NarrowLayoutProps } from "@/components/layout";
import { Button, Card, Input, InputGroup, LinkButton } from "@/components/ui";
import styles from "./StoreProfile.module.scss";

interface StoreProfileProps extends NarrowLayoutProps {
  title?: string;
}

// StoreProfile enables participants to store their profile for later access
export default function StoreProfile({
  title,
  ...layoutProps
}: StoreProfileProps) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");

  const validEmail = email && EmailValidator.validate(email);
  const participant = useBoundStore((state) => state.participant);

  const sendLink = async (participant: Participant) => {
    if (validEmail) {
      const result = await shareParticipant({ email, participant });
      if (!result) {
        alert("An error occurred while sending the link. Try again later.");
      } else {
        alert("You will receive an e-mail shortly");
      }
      navigate(URLS.profile);
    }
  };

  if (!participant) {
    return <LoadingView />;
  }

  return (
    <NarrowLayout {...layoutProps}>
      <Card>
        <Card.Header title="Personal link">
          We will send you a personal link by email, which provides access to
          your profile at a later moment or on another system.
        </Card.Header>
        <Card.Section>
          <InputGroup>
            <Input
              className="mb-3 w-100"
              type="email"
              placeholder="name@example.com"
              required
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
              }}
            />
          </InputGroup>
        </Card.Section>
      </Card>

      <div className={styles.buttons}>
        <LinkButton
          link={URLS.profile}
          stretch={true}
          size="lg"
          rounded={false}
        >
          Cancel
        </LinkButton>

        <Button
          key={Math.random()}
          className={classNames({ disabled: !validEmail })}
          onClick={() => sendLink(participant)}
          variant="secondary"
          stretch={true}
          size="lg"
          rounded={false}
        >
          Send me the link
        </Button>
      </div>
    </NarrowLayout>
  );
}
