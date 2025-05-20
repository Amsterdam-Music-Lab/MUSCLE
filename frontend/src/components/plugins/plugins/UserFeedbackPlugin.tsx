/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { UserFeedbackFormProps } from "@/components/user/UserFeedbackForm/UserFeedbackForm";
import UserFeedbackForm from "@/components/user/UserFeedbackForm/UserFeedbackForm";

export interface UserFeedbackPluginArgs extends UserFeedbackFormProps {}

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
  component: UserFeedbackForm,
  description: "Displays a user feedback form",
  defaultArgs: {},
};
