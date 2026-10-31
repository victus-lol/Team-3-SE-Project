name: Testing Task
description: Track testing coverage, regression tests, or QA work
title: "[TEST]: "
labels: ["testing", "qa"]
body:
  - type: input
    id: tc_id
    attributes:
      label: Test Case ID
      description: Formal test case ID (e.g. TC-Task-01, TC-Perf-01)
    validations:
      required: true
  - type: input
    id: req_id
    attributes:
      label: Requirement IDs
      description: Associated requirement IDs
    validations:
      required: true
  - type: textarea
    id: scope
    attributes:
      label: Test Scope & Procedure
      description: Specific scenarios tested
    validations:
      required: true

