/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { LinkButton } from "@/components/buttons";
import { Card } from "@/components/ui";
import { routes } from "@/config";

export default function ConsentDeniedView() {
  return (
    <>
      <Card>
        <Card.Header title={"No consent was given"} />
        <Card.Section>
          Unfortunately, you cannot participate in this experiment if you do not
          want to provide consent.
        </Card.Section>
      </Card>
      <LinkButton
        link={routes.home()}
        variant="secondary"
        rounded={false}
        size="lg"
      >
        Go back to the homepage
      </LinkButton>
    </>
  );
}

ConsentDeniedView.viewName = "consentDenied";
ConsentDeniedView.usesOwnLayout = false;
