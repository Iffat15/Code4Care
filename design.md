# Agentic Emergency Care System

## System Design Document

## 1. Design Philosophy

The system uses a multi-agent architecture with clear separation between
decision-making (AI layer) and execution (transactional systems).

AI is applied only where: - Uncertainty exists - Trade-offs must be
evaluated - Context changes dynamically

## 2. High-Level Flow

User → SOS Agent → Triage Agent → Hospital Orchestration Agent →
Ambulance Agent (if required) → Form Agent → Deterministic System →
Billing Agent

## 3. Architectural Layers

### 3.1 Presentation Layer

-   Mobile/Web App
-   Admin Dashboard
-   Ambulance Console

### 3.2 Agentic Decision Layer

Agents: - SOS Agent (intent detection) - Triage Agent (medical
reasoning) - Orchestration Agent (hospital selection) - Ambulance Agent
(fleet coordination) - Form Agent (dynamic admission handling) - Billing
Agent (post-care reasoning)

Characteristics: - Stateless services - JSON-based structured
communication - Confidence scoring

### 3.3 Deterministic Execution Layer

Handles: - Bed locking - Ambulance dispatch confirmation -
Notifications - Data persistence - Audit logs

This layer executes but does not reason.

## 4. Human-in-the-Loop

Checkpoints: 1. Admin reviews triage reasoning 2. Confirmation call
before booking 3. Billing approval before discharge

## 5. Scalability Strategy

-   Microservices per agent
-   Horizontal scaling
-   API Gateway routing
-   Centralized monitoring

## 6. Security Design

-   Token-based authentication
-   Role-based authorization
-   Encryption in transit and at rest
-   Immutable audit logs

## 7. Future Enhancements

-   Predictive ICU demand modeling
-   Multi-city ambulance optimization
-   Insurance pre-authorization agent
