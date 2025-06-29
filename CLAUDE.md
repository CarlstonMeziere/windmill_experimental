# Felix/Felicia Platform - Technical Context

## Platform Overview

Felicia is a universal work management platform built on a revolutionary concept: **everything is a work item**. The platform transforms how organizations handle any type of work - from processing invoices to fixing bugs, from insurance claims to employee onboarding. This is achieved through a highly flexible, type-safe system where work items move through customizable stage-based workflows with embedded AI assistance.

### Core Philosophy
- **Unified Work Model**: All business activities are work items with stages, not disparate task types
- **Type-Safe Flexibility**: Strong typing with customizable schemas, not rigid predefined structures
- **AI-Native Design**: Specialized agents per work item type, not generic automation
- **Hierarchical by Design**: Up to 4-level deep hierarchies with custom terminology per workspace folder
- **Integration-First**: Built to connect with existing systems, not replace them

## Technical Architecture

### Architectural Patterns

1. **Entity Inheritance Model**
   - Base `Asset` entity with polymorphic relationships to `File`, `Document`, and `Client`
   - Allows flexible content management with type-specific metadata schemas
   - AssetType defines validation rules and extraction patterns

2. **Three-Tier Security Model**
   - **Instance Level**: Platform-wide roles (superadmin, devops, user)
   - **Workspace Level**: Functional roles (admin, developer, operator, advanced_operator)
   - **Folder Level**: Data access permissions (viewer, writer, admin)
   - Permissions cascade and combine: workspace role capabilities are gated by folder permissions

3. **Stage-Based Workflow Engine**
   - Work items progress through named stages defined per type
   - Stage transitions can require HITL approval or automated validation
   - Form templates are stage-specific for progressive data collection

4. **Specialized AI Agent Architecture**
   - One agent per work item type (not general-purpose)
   - Stage-specific contexts with different prompts and rules
   - Learning feedback weighted by user expertise level
   - Confidence-based HITL triggers for exception handling

5. **Event-Driven Processing**
   - Queue-based async architecture for reliability
   - Dead letter queues for failure handling
   - Webhook receivers for real-time external events
   - Scheduled jobs for recurring processes

## Domain Model Overview

### Implementation Waves (13 waves, 52 entities)

**Wave 1: Infrastructure (10-50)**
- Cache, RateLimiter, Queue, QueueDeadLetter, AuditLog
- Must exist before all other entities for performance and compliance

**Wave 2: User System (60-90)**
- User, Configuration, Secret, FeatureFlag
- Foundation for all ownership and access control

**Wave 3: Workspace (100-150)**
- Workspace, WorkspaceRole, Permission, WorkspaceAccess, UserGroup
- Top-level multi-tenancy with complete isolation

**Wave 4: Organization (160-170)**
- Folder, FolderPermission
- Hierarchical structure with inheritance

**Wave 5: Assets (180-220)**
- AssetType, AssetTaxonomy, Asset, Client
- Flexible content model with metadata schemas

**Wave 6: Type System (230-240)**
- WorkItemType, RelationshipTemplate
- Defines structure before instances

**Wave 7: Files (250-260)**
- File, Document
- Specialized asset types for content

**Wave 8: Work Items (270-280)**
- WorkItem, WorkItemRelationship
- Core business entities

**Wave 9: Forms (290-330)**
- FormTemplate, FormField, FormSubmission, ApprovalRule, Task
- Dynamic data capture

**Wave 10: Automation (340-390)**
- Script, Agent, AgentContext, Flow, FlowNode, Tool
- AI and workflow engine

**Wave 11: Execution (400-410)**
- AgentSuggestion, ExecutionHistory
- Runtime tracking

**Wave 12: Integration (420-470)**
- Integration, Webhook, Schedule
- External connectivity

**Wave 13: Analytics (480-520)**
- Template, Metric, Analytics, Notification
- Insights and communication

## Core Architectural Decisions

1. **Hierarchical Depth Limit**: Maximum 4 levels in work item hierarchies for complexity management
2. **JSON Fields**: Extensive use for flexible schemas with validation at application layer
3. **Self-Referential Entities**: Folder, WorkItemType, AssetTaxonomy, Flow support hierarchies
4. **Audit-First Design**: AuditLog in Wave 1, tracks all entity operations with impersonation support
5. **Asset-Based Architecture**: All content (files, documents, clients) extends Asset base type
6. **Stage-Gate Logic**: Parent work items blocked by child states via RelationshipTemplate rules
7. **Workspace Isolation**: Complete data separation, no cross-workspace queries
8. **Type Before Instance**: WorkItemType must exist before WorkItem, enforcing schema
9. **Progressive Disclosure**: Stage-specific forms show only relevant fields
10. **Weighted Learning**: Agent feedback weighted by user expertise level

## Development Principles

1. **Dependency-Driven Implementation**: Entities implemented in waves based on foreign key dependencies
2. **Test-First for Each Wave**: Comprehensive testing before proceeding to next wave
3. **Schema Validation**: JSON fields require application-level validation
4. **Aspect-Oriented Auditing**: Automatic capture of all entity changes
5. **Performance by Design**: Cache and queue infrastructure in first wave
6. **Security by Default**: RBAC checks at every level
7. **API-First Development**: All features accessible via API
8. **Idempotent Operations**: All write operations should be safely retryable
9. **Event Sourcing Ready**: Audit log can reconstruct entity states
10. **Multi-Tenant Ready**: Workspace isolation from day one

## AI Integration Architecture

### Agent Design Pattern
```
WorkItemType 1:1 Agent 1:N AgentContext (per stage)
                   |
                   v
            AgentSuggestion (with feedback loop)
```

### Key Features
- **Specialized Training**: Each agent trained on its work item type's domain
- **Stage Awareness**: Different behavior per workflow stage
- **Confidence Scoring**: Automatic HITL triggers on low confidence
- **Feedback Loop**: User corrections improve future suggestions
- **Expertise Weighting**: Advanced operators' feedback valued higher
- **Extraction Rules**: Type-specific document processing

## Security Model Details

### Instance Roles
- **Superadmin**: Full platform access, impersonation, all workspaces
- **DevOps**: Technical operations, debugging, no business data access
- **User**: Standard user, workspace access controlled separately

### Workspace Roles
- **Admin**: User management, folder permissions, configuration
- **Developer**: Create types, write agents, build automation
- **Operator**: Execute work, limited to business UI
- **Advanced Operator**: Operator + agent training feedback

### Folder Permissions
- **Admin**: Full control including permission management
- **Writer**: Create/modify work items
- **Viewer**: Read-only access

### Permission Resolution
```
Effective Permission = Instance Role ∩ Workspace Role ∩ Folder Permission
```

## Key Technical Patterns

1. **Polymorphic Asset Model**
   - Base Asset with type-specific extensions
   - Metadata schemas defined in AssetType
   - Validation rules at type level

2. **Stage-Based Forms**
   - Different forms per stage
   - Progressive data collection
   - Conditional field visibility

3. **Queue-Driven Architecture**
   - Async processing for reliability
   - Retry logic with dead letters
   - Priority-based processing

4. **Template System**
   - Reusable configurations
   - Parameterized instantiation
   - Version tracking

5. **Integration Framework**
   - Configuration-driven mappings
   - Bi-directional sync
   - Transform functions

## Questions for Implementation Team

### Technology Stack
- **Backend Language**: ? (Node.js, Python, Go, Java, .NET?)
- **Backend Framework**: ? (Express, FastAPI, Gin, Spring, ASP.NET?)
- **Database**: ? (PostgreSQL, MySQL, MongoDB, DynamoDB?)
- **ORM/Query Builder**: ? (Prisma, SQLAlchemy, GORM, Hibernate?)
- **Cache Layer**: ? (Redis, Memcached, DynamoDB?)
- **Queue System**: ? (RabbitMQ, AWS SQS, Kafka, Redis?)
- **File Storage**: ? (S3, Azure Blob, GCS?)
- **Search Engine**: ? (Elasticsearch, Algolia, PostgreSQL FTS?)

### Frontend Architecture
- **Framework**: ? (React, Vue, Angular, Svelte?)
- **State Management**: ? (Redux, MobX, Zustand, Pinia?)
- **UI Component Library**: ? (Material-UI, Ant Design, Tailwind UI?)
- **Build System**: ? (Webpack, Vite, Parcel?)
- **Type System**: ? (TypeScript, Flow, PropTypes?)
- **Testing Framework**: ? (Jest, Vitest, Cypress?)

### API Design
- **Protocol**: ? (REST, GraphQL, gRPC, tRPC?)
- **Authentication**: ? (JWT, OAuth2, SAML?)
- **API Gateway**: ? (Kong, AWS API Gateway, Envoy?)
- **Versioning Strategy**: ? (URL path, headers, query params?)
- **Documentation**: ? (OpenAPI/Swagger, GraphQL Schema?)
- **Rate Limiting**: ? (Token bucket, sliding window?)

### Deployment Architecture
- **Cloud Provider**: ? (AWS, Azure, GCP, Hybrid?)
- **Container Orchestration**: ? (Kubernetes, ECS, Cloud Run?)
- **CI/CD Pipeline**: ? (GitHub Actions, GitLab CI, Jenkins?)
- **Infrastructure as Code**: ? (Terraform, CloudFormation, Pulumi?)
- **Monitoring**: ? (Datadog, New Relic, Prometheus?)
- **Log Aggregation**: ? (ELK Stack, Splunk, CloudWatch?)

### Development Workflow
- **Version Control**: Git (confirmed)
- **Branch Strategy**: ? (GitFlow, GitHub Flow, Trunk-based?)
- **Code Review Process**: ? (PR requirements, approval count?)
- **Testing Requirements**: ? (Coverage targets, test types?)
- **Documentation Standards**: ? (Code comments, API docs, ADRs?)
- **Development Environment**: ? (Docker, Vagrant, local setup?)

### Performance Requirements
- **Response Time SLA**: ? (p50, p95, p99 targets?)
- **Throughput**: ? (requests/second per workspace?)
- **Concurrent Users**: ? (per workspace, total platform?)
- **Data Retention**: ? (hot/cold storage tiers?)
- **Availability Target**: ? (99.9%, 99.99%?)
- **Disaster Recovery**: ? (RTO, RPO targets?)

### Integration Patterns
- **Event Bus**: ? (Internal events between services?)
- **API Standards**: ? (REST conventions, error formats?)
- **Webhook Delivery**: ? (Retry policy, signature verification?)
- **Batch Processing**: ? (ETL tools, scheduling?)
- **Data Sync**: ? (Real-time, near-real-time, batch?)
- **External Auth**: ? (Azure AD/Entra integration details?)

### Data Architecture
- **Multi-Tenancy**: ? (Schema per workspace, shared schema?)
- **Audit Storage**: ? (Same DB, separate service?)
- **File Processing**: ? (Sync, async, lambda?)
- **Full-Text Search**: ? (Which fields, languages?)
- **Data Archival**: ? (Strategy for old work items?)
- **Backup Strategy**: ? (Frequency, retention, testing?)

### AI/ML Infrastructure
- **LLM Provider**: ? (OpenAI, Anthropic, Azure OpenAI, self-hosted?)
- **Embedding Storage**: ? (Vector DB choice?)
- **Training Pipeline**: ? (How to update agents?)
- **Inference Caching**: ? (Cache AI responses?)
- **Cost Management**: ? (Token limits, monitoring?)
- **Fallback Strategy**: ? (When AI unavailable?)

### Security Considerations
- **Encryption**: ? (At rest, in transit requirements?)
- **Compliance**: ? (SOC2, HIPAA, GDPR needs?)
- **Pen Testing**: ? (Frequency, scope?)
- **Secret Management**: ? (Vault, KMS, environment vars?)
- **Session Management**: ? (Duration, refresh strategy?)
- **IP Restrictions**: ? (Workspace or instance level?)

## Implementation Priorities

Based on the implementation order document:

1. **Start with Infrastructure** (Wave 1)
   - Get caching, rate limiting, queuing, and auditing right first
   - These are much harder to retrofit later

2. **User System Before Workspaces** (Wave 2-3)
   - Authentication and authorization are foundational
   - Workspace isolation depends on solid user management

3. **Type Definitions Before Instances** (Wave 6 before 8)
   - WorkItemType must exist before WorkItem
   - AssetType must exist before Asset
   - Enforces schema-first development

4. **Keep Waves Small and Testable**
   - Each wave should be fully tested before proceeding
   - Dependencies between waves must be explicit

5. **Plan for Data Migration Early**
   - Self-referential entities need special handling
   - Hierarchical data requires careful migration strategies

## Common Workflows

### Creating a New Work Item Type
1. Define WorkItemType with hierarchy level and parent
2. Create RelationshipTemplate for parent-child rules
3. Design FormTemplates for each stage
4. Configure Agent with stage-specific contexts
5. Set up ApprovalRules for human review points
6. Create Flows for automation
7. Test with sample WorkItems

### Processing a Work Item
1. User creates WorkItem of specific type
2. Initial FormTemplate captures required data
3. Agent analyzes and suggests field values
4. User reviews/corrects suggestions (training feedback)
5. Work item progresses through stages
6. Each stage may trigger Flows or require approvals
7. HITL tasks created for exceptions
8. Notifications sent on status changes
9. Metrics captured throughout

### Setting Up an Integration
1. Create Integration configuration
2. Map external schemas to AssetTypes
3. Configure transform functions
4. Set up Webhooks for real-time updates
5. Create Schedule for batch sync
6. Test with sample data
7. Monitor IntegrationLogs
8. Handle failures via dead letter queue

## Project File Map

### Vision & Documentation Files
- **DOMAIN_UI_IMPLEMENTATION.md** - Comprehensive UI vision document describing all domains and their user interfaces
- **ENTITY_IMPLEMENTATION_ORDER.md** - Technical implementation order for 52 entities in 13 waves
- **entities.mermaid** - Complete ER diagram showing all entities and relationships
- **claude.md** - This file - technical context and memory for future development sessions

### UI Mockup Task Management
- **UI_MOCKUP_TASKS.md** - Hierarchical task list with 985 tasks including review checkpoints
  - Uses 10-increment numbering (10, 20, 30...) at all levels
  - Includes 76 human review checkpoints (numbered with +5 offset)
  - 4-level hierarchy matching Felicia's work item concept
  
- **task_tracker.py** - Python script for task management and progress tracking
- **UI_MOCKUP_README.md** - Documentation for the task management system
- **REVIEW_CHECKLIST_TEMPLATE.md** - Standardized template for conducting component reviews
- **UI_REVIEW_PROCESS.md** - Detailed guide for the human review process

### Git-Ignored Files
- **UI_IMPLEMENTATION.md** - Previous UI ideas (deprecated, replaced by DOMAIN_UI_IMPLEMENTATION.md)
- Python/TypeScript implementation attempts from earlier iterations

## Using task_tracker.py

### Installation
No installation needed - just Python 3.6+ required. The script parses UI_MOCKUP_TASKS.md directly.

### Command Line Usage

#### View Overall Progress
```bash
python3 task_tracker.py summary
```
**Returns**: 
- Total tasks and completion percentage
- Progress breakdown by level (1, 2, 3)
- Progress by domain with task counts
- Last updated timestamp

#### Find Next Actionable Tasks
```bash
python3 task_tracker.py next --limit 10
```
**Returns**: List of incomplete leaf tasks (tasks with no children) that can be worked on immediately, showing:
- Task ID and line number
- Parent context
- Task description

#### Mark Task Complete
```bash
python3 task_tracker.py complete --task-id 10.10.10
```
**Returns**: Success/failure message. Will fail if:
- Task has incomplete children
- Task ID doesn't exist

#### Validate Completion Rules
```bash
python3 task_tracker.py validate
```
**Returns**: List of any parent tasks incorrectly marked complete while having incomplete children

#### Export Task Data
```bash
python3 task_tracker.py export --output task_status.json
```
**Returns**: JSON file with complete task hierarchy and status

### Progress Interpretation

When running `summary`, key metrics to watch:
- **Overall %**: Total project completion (0-100%)
- **Level 1 Progress**: Domain completion (16 major domains)
- **Level 2 Progress**: Feature completion within domains
- **Level 3 Progress**: Individual component/task completion

Example output interpretation:
```
Total Tasks: 985
Completed: 492
Overall Progress: 49.95%
```
This would mean the UI mockup is roughly halfway complete.

### Development Workflow with task_tracker.py

1. **Start of Day**: Run `summary` to see overall status
2. **Find Work**: Run `next` to get actionable tasks
3. **During Work**: Complete tasks, focusing on leaf nodes
4. **Mark Complete**: Use `complete --task-id X` as you finish
5. **Review Points**: When you see .X5 tasks, schedule human review
6. **End of Day**: Run `summary` again to see progress

### Review Checkpoint Handling

Review tasks (numbered .15, .25, .35, etc.) require special handling:
1. Complete all sibling component tasks first
2. Prepare demo/screenshots
3. Conduct review using REVIEW_CHECKLIST_TEMPLATE.md
4. Only mark review task complete after approval
5. Fix any issues before proceeding to next section

### Tips for AI Agents

When working on the UI mockup:
1. Always check parent task context: `next` command shows parent description
2. Follow existing patterns from completed components
3. Create all subtasks before marking parent complete
4. Review tasks block progress - schedule human reviews promptly
5. Use `validate` periodically to ensure hierarchy integrity