/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export interface RedirectProps {
  to: string;
}

// TODO This is redundant and can be replaced by <Navigate> from ReactRouter
export default function Redirect({ to }: RedirectProps) {
  let navigate = useNavigate();
  useEffect(() => navigate(to));
  return null;
}
