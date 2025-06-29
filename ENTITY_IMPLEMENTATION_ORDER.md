# Entity Implementation Order

This document defines the order in which entities should be implemented, considering both technical dependencies and business requirements. Entities are numbered in increments of 10 to allow for future additions.

## Implementation Waves

### Wave 1: Core Infrastructure & Audit (10-50)
These entities form the absolute foundation and must exist before anything else.

- **10 - Cache** - Infrastructure caching layer, no dependencies
- **20 - RateLimiter** - API protection, no dependencies  
- **30 - Queue** - Async processing infrastructure, needed by many systems
- **40 - QueueDeadLetter** - Queue error handling (depends on Queue)
- **50 - AuditLog** - Must exist early to audit all other entity operations

### Wave 2: User & Authentication (60-90)
Core user system required for all ownership and access control.

- **60 - User** - Foundation for all user references
- **70 - Configuration** - System configuration storage
- **80 - Secret** - Credential management (references User for ownership)
- **90 - FeatureFlag** - Feature control system

### Wave 3: Workspace Foundation (100-150)
Top-level organization container and core RBAC.

- **100 - Workspace** - Top-level container (references User for creator)
- **110 - WorkspaceRole** - Role definitions within workspaces
- **120 - Permission** - Granular permissions for roles
- **130 - WorkspaceAccess** - User-Workspace-Role associations
- **140 - UserGroup** - Group management within workspaces
- **150 - UserGroupMembership** - User-Group associations

### Wave 4: Folder Organization (160-170)
Hierarchical organization within workspaces.

- **160 - Folder** - Hierarchical organization (self-referential)
- **170 - FolderPermission** - Folder-level access control

### Wave 5: Asset Foundation (180-220)
Core content management framework.

- **180 - AssetType** - Defines types of assets (must exist before Asset)
- **190 - AssetTaxonomy** - Classification system (self-referential)
- **200 - Asset** - Base entity for all content
- **210 - AssetTaxonomyMapping** - Asset classification associations
- **220 - Client** - Specialized asset type for external entities

### Wave 6: Work Item Type System (230-240)
Defines the structure of work before instances.

- **230 - WorkItemType** - Defines work item structures (self-referential)
- **240 - RelationshipTemplate** - Defines hierarchical relationships

### Wave 7: File & Document Processing (250-260)
Specialized asset types for file handling.

- **250 - File** - File storage entity (extends Asset)
- **260 - Document** - Document processing (extends Asset, references File)

### Wave 8: Work Item Runtime (270-280)
Actual work item instances.

- **270 - WorkItem** - Core work instances (depends on WorkItemType, Folder, Client)
- **280 - WorkItemRelationship** - Hierarchical relationships between work items

### Wave 9: Form System (290-330)
Data capture and validation framework.

- **290 - FormTemplate** - Form definitions per work item type
- **300 - FormField** - Field definitions within forms
- **310 - FormSubmission** - Captured form data
- **320 - ApprovalRule** - Approval workflow rules
- **330 - Task** - Human tasks including HITL

### Wave 10: Agent & Automation Foundation (340-390)
AI and automation infrastructure.

- **340 - Script** - Reusable code units (minimal dependencies)
- **350 - Agent** - AI agents per work item type
- **360 - AgentContext** - Agent configuration per stage
- **370 - Flow** - Workflow automation (self-referential)
- **380 - FlowNode** - Flow step definitions
- **390 - Tool** - Packaged flows/agents

### Wave 11: Agent Runtime (400-410)
Agent execution and feedback.

- **400 - AgentSuggestion** - AI suggestions with feedback loop
- **410 - ExecutionHistory** - Tracks all executions

### Wave 12: External Integration (420-470)
External system connectivity.

- **420 - Integration** - External system connections
- **430 - IntegrationLog** - Integration activity tracking
- **440 - Webhook** - Inbound event receivers
- **450 - WebhookEvent** - Webhook event storage
- **460 - Schedule** - Scheduled job definitions
- **470 - ScheduleExecution** - Schedule run history

### Wave 13: Templates & Analytics (480-520)
Reusability and insights.

- **480 - Template** - Reusable configurations
- **490 - TemplateInstance** - Template usage tracking
- **500 - Metric** - Performance and business metrics
- **510 - Analytics** - Analytical reports and dashboards
- **520 - Notification** - User notifications

## Implementation Notes

### Critical Dependencies
1. **User** must exist before any entity with createdBy/updatedBy fields
2. **Workspace** must exist before any workspace-scoped entity
3. **AssetType** must exist before Asset
4. **Asset** must exist before File, Document, or Client
5. **WorkItemType** must exist before WorkItem
6. **Queue** should be early as many systems use it for async processing
7. **AuditLog** should be very early to capture all entity operations

### Entities That Must Be Implemented Together
1. **WorkspaceRole + Permission** - Roles are meaningless without permissions
2. **UserGroup + UserGroupMembership** - Groups need membership tracking
3. **Asset + AssetType** - Assets require types for validation
4. **WorkItem + WorkItemType** - Work items are instances of types
5. **FormTemplate + FormField** - Forms need fields to be useful
6. **Flow + FlowNode** - Flows are composed of nodes
7. **Agent + AgentContext** - Agents need context for different stages

### Special Considerations
1. **Self-referential entities** (Folder, WorkItemType, AssetTaxonomy) need special handling for hierarchies
2. **Polymorphic relationships** (Asset → File/Document/Client) require careful ORM configuration
3. **JSON fields** throughout the system need schema validation
4. **Audit logging** should be aspect-oriented to automatically capture all changes
5. **Queue processing** is critical infrastructure that many features depend on

### Recommended Development Approach
1. Implement each wave completely before moving to the next
2. Build comprehensive tests for each wave
3. Validate foreign key relationships are properly enforced
4. Ensure audit logging captures all operations from the start
5. Plan for data migration strategies early, especially for self-referential entities