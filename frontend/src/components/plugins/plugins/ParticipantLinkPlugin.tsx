/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { ParticipantLinkProps } from "@/components/modules/ParticipantLink/ParticipantLink";
import ParticipantLink from "@/components/modules/ParticipantLink/ParticipantLink";

export interface ParticipantLinkPluginArgs extends ParticipantLinkProps {}

export interface ParticipantLinkPluginMeta
  extends PluginMeta<ParticipantLinkPluginArgs> {
  name: "participantLink";
}

export interface ParticipantLinkPluginSpec
  extends PluginSpec<ParticipantLinkPluginArgs> {
  name: "participantLink";
}

export const participantLinkPlugin: ParticipantLinkPluginMeta = {
  name: "participantLink",
  component: ParticipantLink,
  description: "Displays a participant link",
};
