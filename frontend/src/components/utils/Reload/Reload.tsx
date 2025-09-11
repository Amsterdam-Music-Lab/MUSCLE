/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { API_BASE_URL } from "@/config";

export default function Reload() {
  const location = useLocation();
  useEffect(() => {
    window.location.href = API_BASE_URL + location.pathname;
  });
  return <div data-testid="reload" />;
}
