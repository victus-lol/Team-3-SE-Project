name: Feature Request
description: Propose a new feature for the Task Manager Application
title: "[FEAT]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for proposing a new feature! Please fill in all required details.
  - type: input
    id: sprint
    attributes:
      label: Sprint
      description: Target sprint (e.g. Sprint 1, Sprint 2)
    validations:
      required: true
  - type: input
    id: owner
    attributes:
      label: Assigned Developer
      description: Assigned team member (Balaji, Aaryan, Aadi, Akash)
    validations:
      required: true
  - type: input
    id: req_id
    attributes:
      label: Requirement IDs
      description: Traceable requirement IDs (e.g. TMA-F-010)
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: Clear and concise description of the feature
    validations:
      required: true
  - type: textarea
    id: acceptance_criteria
    attributes:
      label: Acceptance Criteria
      description: Given-When-Then or itemized list of criteria
    validations:
      required: true

