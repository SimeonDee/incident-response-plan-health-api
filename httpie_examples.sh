#!/usr/bin/env bash
# Example HTTPie commands for CRUD operations

BASE=http://localhost:8000/api/v1

# Create
http --json POST $BASE/incidents/ \
  incident_type="Test" \
  description="HTTPie test" \
  location="CLI" \
  date_time="2025-11-08T12:00:00Z" \
  severity_level="low" \
  contact_information="cli@example.org"

# List
http GET $BASE/incidents/

# Get (replace {id})
# http GET $BASE/incidents/{id}

# Update
# http PUT $BASE/incidents/{id} severity_level="high"

# Delete
# http DELETE $BASE/incidents/{id}
