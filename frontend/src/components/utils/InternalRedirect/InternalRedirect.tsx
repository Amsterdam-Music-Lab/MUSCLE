/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import { useLocation } from "react-router-dom";
import { Redirect } from "../Redirect";

export default function InternalRedirect() {
  const location = useLocation();
  const { pathname, search } = location;
  const path = pathname.replace(/^\/redirect\/?/, "");

  // Redirect to the experiment path
  return <Redirect to={`/${path}${search}`} />;
}
