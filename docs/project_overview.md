# Project Overview

## Purpose

The Student Placement Management System (SPMS) is intended to organize common campus recruitment activities in one web application. It provides student-facing pages for viewing opportunities and tracking applications, and administrator-facing pages for maintaining recruitment information.

## Problem statement

Placement information is often distributed across notices, spreadsheets and separate communication channels. This can make it difficult for students to track opportunities and for placement coordinators to maintain consistent records. SPMS demonstrates a centralized workflow for those activities.

## Objectives

1. Maintain a structured student profile and academic information.
2. Store company and job information in a relational database.
3. Compare student profile fields against job eligibility criteria.
4. Record applications and their status changes.
5. Give administrators a single view of placement activity.

## Scope of the starter implementation

Included: student registration/login, profile editing, company creation, job posting, basic eligibility check, application submission, application status changes and a simple dashboard.

Not yet included: resume upload, email/SMS notifications, placement-record management screens, bulk import/export, advanced reporting, multi-factor authentication and production deployment.

## Main user roles

- **Student:** registers, edits profile, browses jobs, applies and views application status.
- **Administrator:** manages company/job information and updates application status.

## High-level workflow

1. Administrator creates a company record.
2. Administrator posts a job with eligibility criteria.
3. Student maintains department, graduation year and CGPA in their profile.
4. Student browses active jobs and submits an application when the configured eligibility check passes.
5. Administrator reviews applications and updates their status.
