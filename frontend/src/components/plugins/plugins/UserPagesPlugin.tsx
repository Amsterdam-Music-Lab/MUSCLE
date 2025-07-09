/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import { InputGroup, InputLabel } from "@/components/forms";
import { LinkButton } from "@/components/buttons";

export interface UserPagesPluginArgs {
  links: Array<{ link: string; text: string }>;
  label?: string;
}

export interface UserPagesPluginMeta extends PluginMeta<UserPagesPluginArgs> {
  name: "userPages";
}

export interface UserPagesPluginSpec extends PluginSpec<UserPagesPluginArgs> {
  name: "userPages";
}

function UserPagesPlugin({ links, label = "User pages" }: UserPagesPluginArgs) {
  return (
    <InputGroup stretch={true}>
      <InputLabel style={{ flexGrow: 1 }}>{label}</InputLabel>
      {links.map(({ link, text }, index) => (
        <LinkButton link={link} key={index} outline={false}>
          {text}
        </LinkButton>
      ))}
    </InputGroup>
  );
}

export const userPagesPlugin: UserPagesPluginMeta = {
  name: "userPages",
  component: UserPagesPlugin,
  description: "Displays links to user pages",
};
