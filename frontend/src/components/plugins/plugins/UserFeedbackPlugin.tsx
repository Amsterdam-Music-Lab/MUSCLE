/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { FeedbackFormProps } from "@/components/modules";
import { FeedbackForm } from "@/components/modules";

export interface UserFeedbackPluginArgs extends FeedbackFormProps {}

export interface UserFeedbackPluginMeta
  extends PluginMeta<UserFeedbackPluginArgs> {
  name: "userFeedback";
}

export interface UserFeedbackPluginSpec
  extends PluginSpec<UserFeedbackPluginArgs> {
  name: "userFeedback";
}

export const userFeedbackPlugin: UserFeedbackPluginMeta = {
  name: "userFeedback",
  component: FeedbackForm,
  description: "Displays a user feedback form",
  defaultArgs: {},
};
