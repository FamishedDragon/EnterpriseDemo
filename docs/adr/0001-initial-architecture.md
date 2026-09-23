# ADR-0001: Initial Application Architecture

* **Status:** Accepted
* **Date:** 2026-09-22
* **Decision Owners:** Solo Developer
* **Project:** Enterprise Work Management Platform

## 1. Context

We are building an enterprise-style work management application as a full-stack interview preparation project.

The application will support user authentication, project management, work items, project membership, role-based access control, comments, and activity history.

The project has the following constraints:

* One developer.
* Approximately 20 hours per week for 30 days.
* Backend development is intended to improve knowledge of APIs, databases, security, testing, and deployment.
* The application should demonstrate enterprise-minded development practices without unnecessary architectural complexity.
* The application should be easy to run locally and straightforward to test.

The architecture should support a clear separation of responsibilities, secure backend access controls, database persistence, and future expansion.

## 2. Decision

We will use a modular monolith architecture.

### Frontend

* React
* TypeScript
* Vite
* React Router
* TanStack Query for server state
* Typed API client

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* pytest

### Database

* PostgreSQL
* Docker Compose for local development
* SQLAlchemy for database access
* Alembic for database migrations

### Infrastructure

* Docker for local supporting services
* Git for version control
* CI for automated testing and quality checks

The frontend and backend will be maintained as separate application components, while the backend will initially run as a single deployable service.

Backend functionality will be organized into modules for authentication, projects, work items, and related business logic.

## 3. Alternatives Considered

### Alternative A: Microservices

Separate services for authentication, projects, work items, and other domains.

**Advantages:**

* Independent deployment and scaling.
* Explicit service boundaries.
* Potentially useful for large teams and independently evolving systems.

**Disadvantages:**

* Increased operational complexity.
* Network communication and service-to-service authentication.
* More complex local development and testing.
* Additional deployment and monitoring requirements.

**Reason for not choosing:**

The project's current scope and single-developer constraint do not justify the additional complexity. The application can establish modular boundaries within a monolith and revisit service separation if real requirements emerge.

### Alternative B: Serverless Backend

Use managed functions and serverless database integrations.

**Advantages:**

* Potentially less infrastructure to manage.
* Managed deployment and scaling options.

**Disadvantages:**

* Platform-specific constraints.
* Additional architectural considerations for local development and debugging.
* Not as directly aligned with the intended practice of building and operating a conventional backend service.

**Reason for not choosing:**

A conventional FastAPI service provides a direct opportunity to practice API architecture, dependency management, application configuration, and deployment.

### Alternative C: Node.js / TypeScript Backend

Use TypeScript for both frontend and backend.

**Advantages:**

* Shared language across the stack.
* Strong ecosystem and type-sharing opportunities.
* Familiar development experience for a frontend-focused developer.

**Disadvantages:**

* Would provide less exposure to Python backend development.
* Framework and runtime choices would shift the focus of the learning project.

**Reason for not choosing:**

Python and FastAPI were selected to broaden backend experience. This decision is not a statement that TypeScript is unsuitable for enterprise backend development.

## 4. Consequences

### Positive consequences

* Clear separation between frontend and backend responsibilities.
* Reduced operational complexity compared with microservices.
* PostgreSQL provides experience with relational data modeling and SQL.
* The backend can be tested independently of the frontend.
* The architecture can evolve as requirements become more complex.
* The project provides concrete material for full-stack interview discussions.

### Negative consequences

* The monolith may require additional refactoring if independent deployment of modules becomes necessary.
* The developer must maintain both frontend and backend environments.
* Database schema changes require migration management.
* Some enterprise-scale concerns will be simulated rather than fully implemented.

## 5. Security Considerations

* Backend authorization will be enforced independently of frontend controls.
* Passwords will be stored using an appropriate password hashing algorithm.
* Sensitive configuration will not be committed to source control.
* Database access will use parameterized queries through SQLAlchemy.
* API inputs will be validated.
* Authentication and session/token management will follow the selected security model.
* Logs will avoid exposing passwords, credentials, and sensitive user data.

## 6. Review Criteria

Revisit this decision if:

* The application requires independently deployed services.
* The team grows beyond a single developer.
* Specific modules have substantially different scaling or reliability requirements.
* Operational complexity becomes a measurable limitation.
* The interview or project requirements change significantly.

## 7. Related Decisions

Future ADRs may cover:

* Authentication and session management.
* API versioning.
* Database migration strategy.
* Authorization model.
* Sensitive data handling and tokenization.
* Deployment architecture.
