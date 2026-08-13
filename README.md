# URL Shortener API

![Project Poster](screenshots/poster.png)

> Project poster placeholder — `screenshots/poster.png`

---

## 2. Project Badges

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)
![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-PASS-success)

---

## 3. Screenshots

### Frontend

![Frontend](screenshots/frontend.PNG)

Main URL Shortener frontend.

### Custom Alias

![Frontend Custom Alias](screenshots/frontend-new-alias.PNG)

Frontend displaying a custom alias URL.

### URL Analytics

![Frontend Analytics](screenshots/frontend-analytics.PNG)

Frontend analytics view showing click statistics.

### Record Created

![Record Created](screenshots/neon-record-created.PNG)

Database record creation verification.

### Click Count

![Click Count](screenshots/neon-alias-click-count.PNG)

Click analytics verification.

### Swagger API

![Swagger Home](screenshots/swagger-home.PNG)

FastAPI Swagger/OpenAPI interface.

### Custom Alias API Response

![Swagger Custom Alias](screenshots/swagger-custom-alias-response.PNG)

API response showing custom alias creation.

### Duplicate Alias Error

![Swagger Duplicate URL Error](screenshots/swagger-duplicate-url-error.PNG)

API validation/error handling for duplicate aliases.

---

## 4. Project Title

# URL Shortener API

**Project ID:** 018

A REST API and lightweight web frontend for creating, managing, redirecting, and analyzing shortened URLs.

---

## 5. Project Overview

### Purpose

The URL Shortener API converts long URLs into compact, shareable URLs that can be redirected to their original destinations.

The service also provides URL lifecycle management and click analytics.

### Problem Solved

Long URLs can be difficult to share, manage, and track.

This project provides a backend service that:

- Generates short URL identifiers.
- Supports user-defined custom aliases.
- Redirects users to the original destination.
- Records successful URL clicks.
- Provides click analytics.
- Supports URL expiration.
- Supports activation and deactivation.
- Retains historical URL records through soft deletion.

### Typical Use Cases

- Marketing campaign links
- Shareable application links
- Tracking links
- Internal enterprise tools
- SaaS applications
- API development demonstrations
- Backend engineering portfolios

---

## 6. Features

### URL Creation

- Create shortened URLs from long URLs.
- Automatically generate unique short codes.
- Support optional custom aliases.
- Support optional expiration timestamps.
- Return a complete public short URL.

### URL Redirect

- Resolve generated short codes.
- Resolve custom aliases.
- Redirect to the original destination.
- Record successful clicks.
- Prevent redirection of inactive or expired URLs.

### URL Analytics

- Total click count.
- First click timestamp.
- Last click timestamp.
- Analytics lookup using a short identifier.
- Refresh analytics from the frontend.

### URL Lifecycle Management

- Retrieve URL details.
- Activate URLs.
- Deactivate URLs.
- Soft-delete URLs.
- Detect expired URLs.
- Prevent invalid lifecycle transitions.

### Validation and Error Handling

- HTTP URL validation.
- Custom alias validation.
- Duplicate alias detection.
- Duplicate URL identifier protection.
- Appropriate HTTP status codes.
- API-level exception handling.

### API Documentation

FastAPI provides interactive Swagger/OpenAPI documentation through:

```text
http://localhost:8000/docs
