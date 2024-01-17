#!/bin/bash

# Define host entries
HOST_ENTRIES=(
    "# MUSCLE"
    "127.0.0.1 muscle.local"
    "127.0.0.1 backend.muscle.local"
    "# END MUSCLE"
)

# Path to the hosts file
HOSTS_FILE="/etc/hosts"

# Function to add an entry if it doesn't exist
add_host_entry() {
    local entry=$1
    if ! grep -q "$entry" "$HOSTS_FILE"; then
        echo "$entry" | sudo tee -a "$HOSTS_FILE"
    else
        echo "Entry already exists: $entry"
    fi
}

# Add each host entry
for entry in "${HOST_ENTRIES[@]}"; do
    add_host_entry "$entry"
done
