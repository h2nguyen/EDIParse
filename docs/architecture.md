# EDIParse Architecture Documentation

## Table of Contents
<!-- TOC -->
* [EDIParse Architecture Documentation](#ediparse-architecture-documentation)
  * [Table of Contents](#table-of-contents)
  * [1. Introduction and Goals](#1-introduction-and-goals)
    * [1.1 Requirements Overview](#11-requirements-overview)
    * [1.2 Quality Goals](#12-quality-goals)
    * [1.3 Stakeholders](#13-stakeholders)
  * [2. Constraints](#2-constraints)
    * [2.1 Technical Constraints](#21-technical-constraints)
    * [2.2 Organizational Constraints](#22-organizational-constraints)
  * [3. Context and Scope](#3-context-and-scope)
    * [3.1 Business Context](#31-business-context)
    * [3.2 Technical Context](#32-technical-context)
    * [3.3 Use Case Diagram](#33-use-case-diagram)
  * [4. Solution Strategy](#4-solution-strategy)
    * [4.1 Hexagonal Architecture Diagram](#41-hexagonal-architecture-diagram)
  * [5. Building Block View](#5-building-block-view)
    * [5.1 Level 1 - White Box Overall System](#51-level-1---white-box-overall-system)
      * [5.1.1 REST API Adapter](#511-rest-api-adapter)
      * [5.1.2 Application Services](#512-application-services)
      * [5.1.3 Domain](#513-domain)
      * [5.1.4 EDIFACT MSCONS Parser Library](#514-edifact-mscons-parser-library)
  * [6. Runtime View](#6-runtime-view)
    * [6.1 Sequence Diagrams](#61-sequence-diagrams)
  * [7. Deployment View](#7-deployment-view)
    * [7.1 Development Environment](#71-development-environment)
    * [7.2 Testing Environment](#72-testing-environment)
    * [7.3 Production Environment](#73-production-environment)
  * [8. Cross-cutting Concepts](#8-cross-cutting-concepts)
    * [8.1 Domain Models](#81-domain-models)
    * [8.2 Exception Handling](#82-exception-handling)
    * [8.3 Handlers and Converters](#83-handlers-and-converters)
    * [8.4 Logging](#84-logging)
  * [9. Architecture Decisions](#9-architecture-decisions)
    * [9.1 Architecture Decision Records (ADRs) Overview](#91-architecture-decision-records-adrs-overview)
  * [10. Quality Requirements](#10-quality-requirements)
    * [10.1 Performance](#101-performance)
    * [10.2 Usability](#102-usability)
    * [10.3 Maintainability](#103-maintainability)
    * [10.4 Reliability](#104-reliability)
  * [11. Risks and Technical Debt](#11-risks-and-technical-debt)
    * [11.1 Extending the Parser Library](#111-extending-the-parser-library)
    * [11.2 Extending with New Message Types](#112-extending-with-new-message-types)
      * [11.2.1 Design Patterns for Message Type Extension](#1121-design-patterns-for-message-type-extension)
      * [11.2.2 The 'mods' Folder Structure](#1122-the-mods-folder-structure)
      * [11.2.3 Adding a New Message Type](#1123-adding-a-new-message-type)
  * [12. Glossary](#12-glossary)
<!-- TOC -->

## 1. Introduction and Goals

### 1.1 Requirements Overview

**EDIParse** is a lightweight and extensible REST-API service that parses **EDIFACT message** text inputs or files
(e.g. MSCONS) and returns structured JSON output. The EDIFACT specific messages are used in the energy sector (DE/AT/CH).
The application provides following REST-API endpoints for: 

- Parsing MSCONS messages from text input
- Parsing MSCONS messages from file input
- Downloading parsed MSCONS results as JSON text string
- Downloading parsed MSCONS results as JSON files

### 1.2 Quality Goals

| Priority | Quality Goal    | Scenario                                                                      |
|----------|-----------------|-------------------------------------------------------------------------------|
| 1        | Performance     | The system should parse MSCONS messages efficiently, even for large files     |
| 2        | Usability       | The API should be easy to use with clear documentation                        |
| 3        | Maintainability | The code should follow hexagonal architecture principles for easy maintenance |
| 4        | Reliability     | The system should handle malformed MSCONS messages gracefully                 |

### 1.3 Stakeholders

| Role                    | Expectations                                                                      |
|-------------------------|-----------------------------------------------------------------------------------|
| API Users               | Reliable and fast parsing of MSCONS messages                                      |
| Developers              | Clear documentation and maintainable codebase                                     |
| Energy Sector Companies | Compliance with EDIFACT MSCONS [2.4c](https://bdew-mako.de/linkPdf/9645) standard |

## 2. Constraints

### 2.1 Technical Constraints

- Python 3.9 or higher is required
- FastAPI is used as the web framework
- Docker is used for containerization

### 2.2 Organizational Constraints

- The application must comply with the EDIFACT MSCONS 2.4c standard
- The API must be RESTful

## 3. Context and Scope

### 3.1 Business Context

EDIParse serves as a parser for EDIFACT MSCONS messages, which are used in the energy sector for exchanging metered services consumption reports. The application provides a RESTful API for parsing these messages and returning structured JSON results.

### 3.2 Technical Context

The application is built using Python and FastAPI, with Docker for containerization. It exposes HTTP endpoints for parsing MSCONS messages and returning structured results.

### 3.3 Use Case Diagram

The following diagram shows the main use cases of the application:

```plantuml
@startuml "EDIParse Use Case Diagram"

!define RECTANGLE class

' Set vertical layout direction
top to bottom direction

skinparam actorStyle awesome
skinparam packageStyle rectangle
skinparam usecaseBackgroundColor #FEFECE
skinparam usecaseBorderColor #000000
skinparam usecaseFontColor #000000
skinparam actorBackgroundColor #FEFECE
skinparam actorBorderColor #000000
skinparam actorFontColor #000000

actor "API User" as user

rectangle "EDIParse" {
  usecase "Parse MSCONS Message from Text" as UC1
  usecase "Parse MSCONS Message from File" as UC2
  usecase "Download Parsed MSCONS Result as JSON Text String" as UC3
  usecase "Download Parsed MSCONS Result as JSON File" as UC4

  ' Arrange use cases vertically
  UC1 -[hidden]-> UC2
  UC2 -[hidden]-> UC3
  UC3 -[hidden]-> UC4
}

user --> UC1
user --> UC2
user --> UC3
user --> UC4

note right of UC1
  Parse raw MSCONS message provided as text
  and return structured JSON result
end note

note right of UC2
  Parse MSCONS message from uploaded file
  and return structured JSON result
end note

note right of UC3
  Parse MSCONS message and return result
  as JSON text string
end note

note right of UC4
  Parse MSCONS message and return result
  as downloadable JSON file
end note

@enduml
```

## 4. Solution Strategy

The application follows a hexagonal architecture (also known as ports and adapters architecture), which is very similar to clean architecture. This architectural style organizes the application around the domain, with clear boundaries between the domain and external concerns.

The application is structured with the following layers:

- **Domain Layer (Core)**: Contains domain models, business rules, and ports (interfaces)
  - Defines the core business logic and rules
  - Contains interfaces (ports) that define how the domain interacts with the outside world
  - Has no dependencies on other layers or external frameworks

- **Application Layer**: Implements application use cases
  - Orchestrates the flow of data to and from the domain
  - Implements the use cases of the application
  - Depends only on the domain layer

- **Adapters Layer (Infrastructure)**: Contains inbound and outbound adapters
  - **Inbound Adapters**: Implement interfaces defined by the domain to drive the application (e.g., REST API)
  - **Outbound Adapters**: Implement interfaces defined by the domain to interact with external systems

- **Library Layer**: Contains reusable libraries that can be used by other projects
  - **EDIFACT MSCONS Parser**: Implements the parsing functionality as a reusable library

The application uses dependency injection to ensure loose coupling between components and to facilitate testing. This approach allows the domain to remain isolated from external concerns, making it easier to test and maintain.

### 4.1 Hexagonal Architecture Diagram

The following PlantUML diagram illustrates the hexagonal architecture of the application:

```plantuml
@startuml "EDIParse Hexagonal Architecture"

skinparam backgroundColor white
skinparam packageStyle rectangle

' External World
package "External World" {
  [API Client] as Client
  [External Systems] as ExternalSystems
}

' Core Layers
package "Domain Layer (Core)" #ffe6cc {
  component "Domain Models & Ports" as Domain
}

package "Application Layer" #d5e8d4 {
  component "Use Cases & Services" as Application
}

' Adapters
package "Adapters Layer" #d4f1f9 {
  component "Inbound Adapters (REST API)" as AdaptersIn
  component "Outbound Adapters" as AdaptersOut
}

' Supporting Layers
package "Library Layer" #e1d5e7 {
  component "EDIFACT MSCONS Parser" as Library
}

' External connections
Client --> AdaptersIn : HTTP Requests
AdaptersIn --> Client : HTTP Responses
AdaptersOut --> ExternalSystems : Calls
ExternalSystems --> AdaptersOut : Responses

' Internal connections
AdaptersIn --> Application : Calls
Application --> Domain : Uses
AdaptersOut --> Domain : Implements
Domain --> AdaptersOut : Defines Ports
Application --> Library : Uses

@enduml
```

This diagram shows how the different layers interact with each other and with the external world. The Domain Layer is at the core, surrounded by the Application Layer, which implements the use cases. The Adapters Layer provides the interfaces to the external world, and the Library Layer contains reusable components like the EDIFACT MSCONS Parser.

## 5. Building Block View

### 5.1 Level 1 - White Box Overall System

The following diagram shows the overall system architecture:

```plantuml
@startuml "EDIParse Component Diagram"

skinparam packageStyle rectangle
skinparam componentStyle rectangle
skinparam backgroundColor white
skinparam packageBackgroundColor white
skinparam interfaceBackgroundColor #FEFECE
skinparam interfaceBorderColor #000000

' External World
package "External World" #f9f9f9 {
  [API Client] as Client
}

' EDIParse
package "EDIParse" {
  ' Adapters Layer
  package "Adapters Layer" #d4f1f9 {
    [REST API Adapter] as RestAdapter
    interface "HTTP API" as HttpApi
  }

  ' Application Layer
  package "Application Layer" #d5e8d4 {
    [Application Services] as AppServices
  }

  ' Domain Layer
  package "Domain Layer" #ffe6cc {
    [Domain Models & Business Rules] as Domain
    interface "MessageParserPort" as ParserPort
  }

  ' Library Layer
  package "Library Layer" #e1d5e7 {
    [EDIFACT MSCONS Parser Library] as Parser
  }
}

' External connections
Client --> HttpApi : HTTP Requests
HttpApi - RestAdapter : exposes
RestAdapter --> Client : HTTP Responses

' Internal connections
RestAdapter --> AppServices : calls
AppServices --> Domain : uses
Domain --> ParserPort : defines
ParserPort - Parser : implements
AppServices --> Parser : uses directly

note right of RestAdapter
  Handles HTTP requests and responses
  Implements FastAPI endpoints
  Converts between HTTP and domain models
end note

note right of AppServices
  Implements application use cases
  Coordinates domain operations
  Manages transaction boundaries
end note

note right of Domain
  Contains domain models and business rules
  Defines ports for external interactions
  Pure business logic without dependencies
end note

note right of Parser
  Reusable library for parsing EDIFACT MSCONS messages
  Implements segment handlers
  Converts raw text to structured data
  Can be used independently in other projects
end note

note bottom of HttpApi
  REST API for parsing MSCONS messages
  Endpoints for text and file input
  Returns JSON text strings or downloadable JSON files
end note

note bottom of ParserPort
  Interface for parsing MSCONS messages
  Abstracts the actual parser implementation
  Allows for different parser implementations
end note

@enduml
```

#### 5.1.1 REST API Adapter

The REST API Adapter is responsible for handling HTTP requests and responses. It uses FastAPI to expose endpoints for parsing MSCONS messages and returning structured results, either as JSON text strings or as downloadable JSON files.

#### 5.1.2 Application Services

The Application Services layer implements the application use cases. It coordinates domain operations and manages transaction boundaries.

#### 5.1.3 Domain

The Domain layer contains domain models and business rules. It defines ports for external interactions and contains pure business logic without dependencies.

#### 5.1.4 EDIFACT MSCONS Parser Library

The EDIFACT MSCONS Parser is implemented as a reusable library that can be used by other projects. It is responsible for parsing EDIFACT MSCONS messages, implementing segment handlers, and converting raw text to structured data.

The parser library consists of several key components:
- **Parser**: The main entry point that orchestrates the parsing process
- **Handlers**: Process specific segment types and update the parsing context
- **Converters**: Transform raw segment data into structured context objects
- **Wrappers**: Define the structure of the parsed data (context models)
- **Context**: Maintains state during the parsing process

This library is designed to be independent of the application's use cases, allowing it to be reused in different contexts and projects.

For detailed information about the parsing process, segment types, handlers, converters, and how to extend the parser, see the [MSCONS Parsing Process Documentation](mscons-parsing-process.md).

## 6. Runtime View

### 6.1 Sequence Diagrams

The following diagram shows the interaction between components when parsing MSCONS messages:

```plantuml
@startuml "EDIParse Sequence Diagram"

actor "API User" as User
participant "REST API\n(FastAPI)" as API
participant "ParseMSCONSRouter" as Router
participant "ParserService" as Service
participant "ParseMessageUseCase" as UseCase
participant "EdifactMSCONSParser" as Parser
participant "SegmentHandlerFactory" as Factory
participant "SegmentHandlers" as Handlers

== Parse MSCONS Message from Text ==

User -> API: POST /parse-raw-format
activate API

API -> Router: parse_mscons_raw_format(body, limit_mode)
activate Router

Router -> Service: parse_message(message_content, max_lines_to_parse)
activate Service

Service -> UseCase: execute(edifact_mscons_message_content, max_lines_to_parse)
activate UseCase

UseCase -> Parser: parse(edifact_text, max_lines_to_parse)
activate Parser

Parser -> Parser: __initialize_una_segment_logic_return_if_has_una_segment()
Parser -> Parser: split_segments()

loop for each segment
    Parser -> Parser: increment segment_count
    Parser -> Parser: remove_invalid_prefix_from_segment_data()
    Parser -> Parser: split_elements()
    Parser -> Parser: get_segment_group()
    Parser -> Factory: get_handler(segment_type)
    activate Factory
    Factory --> Parser: segment_handler
    deactivate Factory

    Parser -> Handlers: handle(line_number, element_components, ...)
    activate Handlers
    Handlers --> Parser: (updates context)
    deactivate Handlers
end

Parser --> UseCase: EdifactInterchange
deactivate Parser

UseCase --> Service: EdifactInterchange
deactivate UseCase

Service --> Router: EdifactInterchange
deactivate Service

Router --> API: JSONResponse(EdifactInterchange)
deactivate Router

API --> User: JSON Response
deactivate API

== Parse MSCONS Message from File ==

User -> API: POST /parse-raw-file
activate API

API -> Router: parse_mscons_file(body, limit_mode)
activate Router

Router -> Router: get_file_content(body)
Router -> Service: parse_message(file_content, max_lines_to_parse)
activate Service

Service -> UseCase: execute(edifact_mscons_message_content, max_lines_to_parse)
activate UseCase

UseCase -> Parser: parse(edifact_text, max_lines_to_parse)
activate Parser

note right: Same parsing process as above

Parser --> UseCase: EdifactInterchange
deactivate Parser

UseCase --> Service: EdifactInterchange
deactivate UseCase

Service --> Router: EdifactInterchange
deactivate Service

Router --> API: JSONResponse(EdifactInterchange)
deactivate Router

API --> User: JSON Response
deactivate API

== Download Parsed MSCONS Result as JSON File (from Text) ==

User -> API: POST /download-parsed-raw-format
activate API

API -> Router: download_parsed_result(body)
activate Router

Router -> Service: parse_message(body, unlimited)
activate Service

note right: Same parsing process as above

Service --> Router: EdifactInterchange
deactivate Service

Router -> Router: Add Content-Disposition header
Router --> API: JSONResponse with attachment
deactivate Router

API --> User: Downloadable JSON file
deactivate API

== Download Parsed MSCONS Result as JSON File (from File) ==

User -> API: POST /download-parsed-raw-file
activate API

API -> Router: download_parsed_file_result(body)
activate Router

Router -> Router: get_file_content(body)
Router -> Service: parse_message(file_content, unlimited)
activate Service

note right: Same parsing process as above

Service --> Router: EdifactInterchange
deactivate Service

Router -> Router: Add Content-Disposition header
Router --> API: JSONResponse with attachment
deactivate Router

API --> User: Downloadable JSON file
deactivate API

@enduml
```

## 7. Deployment View

The application is containerized using Docker and can be deployed in various environments:

- Development: Local Docker container
- Testing: CI/CD pipeline with automated tests
- Production: Docker container in a cloud environment

The following diagram illustrates the deployment architecture of the application:

```plantuml
@startuml "EDIParse Deployment View"

skinparam node {
  BackgroundColor #FEFECE
  BorderColor #000000
  FontColor #000000
}

skinparam database {
  BackgroundColor #EEEEEE
  BorderColor #000000
  FontColor #000000
}

skinparam cloud {
  BackgroundColor #F0F0F0
  BorderColor #000000
  FontColor #000000
}

skinparam rectangle {
  BackgroundColor #FFFFFF
  BorderColor #000000
  FontColor #000000
}

' Development Environment
node "Development Environment" as DevEnv {
  node "Developer Workstation" as DevWS {
    rectangle "Docker Engine" as DevDocker {
      rectangle "Docker Compose" as DevCompose {
        node "EDIParse Container" as DevContainer {
          rectangle "FastAPI Application" as DevApp {
            rectangle "EDIFACT MSCONS Parser Library" as DevLib
          }
        }
      }
    }
  }
}

' Testing Environment
node "Testing Environment" as TestEnv {
  node "CI/CD Pipeline" as CICD {
    rectangle "Build Stage" as BuildStage {
      rectangle "Docker Build" as TestDockerBuild
    }
    rectangle "Test Stage" as TestStage {
      rectangle "Unit Tests" as UnitTests
      rectangle "Integration Tests" as IntegrationTests
    }
    rectangle "Artifact Stage" as ArtifactStage {
      rectangle "Docker Image" as TestDockerImage
    }
  }
}

' Production Environment
node "Production Environment" as ProdEnv {
  cloud "Cloud Platform" as CloudPlatform {
    node "Container Orchestration" as ContainerOrch {
      node "EDIParse Container" as ProdContainer {
        rectangle "FastAPI Application" as ProdApp {
          rectangle "EDIFACT MSCONS Parser Library" as ProdLib
        }
      }
    }
  }

  node "Client Systems" as ClientSystems {
    rectangle "API Clients" as APIClients
  }
}

' Relationships
DevWS --> DevContainer : deploys
CICD --> TestDockerImage : produces
CloudPlatform --> ProdContainer : hosts
APIClients --> ProdContainer : HTTP requests
ProdContainer --> APIClients : HTTP responses

@enduml
```

### 7.1 Development Environment

In the development environment, the application is run using Docker Compose on the developer's workstation. The Docker Compose file defines a single service that builds from the Dockerfile using the "service" target. The service exposes port 8000 and runs the application using uvicorn.

### 7.2 Testing Environment

The testing environment is part of a CI/CD pipeline that builds the Docker image, runs tests, and produces an artifact (Docker image) that can be deployed to production. The Dockerfile includes a dedicated test stage that runs the tests using pytest.

### 7.3 Production Environment

In the production environment, the application is deployed as a Docker container in a cloud platform with container orchestration capabilities. The container runs the FastAPI application with the EDIFACT MSCONS Parser library. Clients interact with the application through HTTP requests to the exposed API endpoints.

## 8. Cross-cutting Concepts

### 8.1 Domain Models

The application uses domain models to represent EDIFACT MSCONS messages and their components. These models are defined in the Domain layer and are used throughout the application.

The domain models include representations of MSCONS message structures, segment types, segment groups, and context models. These models are essential for the parsing process and for representing the parsed data in a structured format.

For detailed information about MSCONS message structure, segment types, segment groups, and context models, see the [MSCONS Parsing Process Documentation](mscons-parsing-process.md).

### 8.2 Exception Handling

The application uses custom exceptions to handle errors during parsing. These exceptions are caught and converted to appropriate HTTP responses.

### 8.3 Handlers and Converters

The EDIFACT MSCONS Parser Library uses a system of handlers and converters to process MSCONS messages:

- **Segment Handlers**: Process specific segment types and update the parsing context
- **Segment Converters**: Transform raw segment data into structured context objects
- **Parsing Context**: Maintains state during the parsing process

This approach allows for a modular and extensible parsing system where each segment type is handled by a dedicated handler and converter.

For detailed information about segment handlers, converters, and the parsing context, see the [MSCONS Parsing Process Documentation](mscons-parsing-process.md).

### 8.4 Logging

The application uses Python's logging module to log events and errors. The logging configuration is defined in the infrastructure layer.

## 9. Architecture Decisions

This section documents the key architectural decisions made for the EDIParse project using the Architecture Decision Record (ADR) format. Each decision is presented in a structured format for better readability and maintainability.

### 9.1 Architecture Decision Records (ADRs) Overview

Architecture Decision Records (ADRs) are documents that capture important architectural decisions made along with their context and consequences. The ADR format used in this document includes the following elements:

- **Title/ID**: A unique identifier and descriptive title for the decision
- **Status**: The current status of the decision (proposed, accepted, deprecated, etc.)
- **Date**: When the decision was made
- **Context**: The issue or background that the decision is addressing
- **Decision**: The change being proposed or implemented
- **Rationale**: The reasons behind the decision
- **Implementation**: How the decision was or will be implemented
- **Consequences**: The resulting context after applying the decision (both positive and negative)
- **Alternatives Considered**: Other options that were evaluated
- **Related Decisions**: Links to other ADRs that are related to this decision

| ADR-001: Hexagonal Architecture                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Status:** Accepted                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Date:** 2025-07-02                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Context:** <br>The application needs an architecture that promotes separation of concerns, testability, and maintainability. The business logic should be isolated from external dependencies to ensure it remains focused on domain concerns.                                                                                                                                                                                                                                                                                                                               |
| **Decision:** <br>Adopt hexagonal architecture (also known as ports and adapters architecture) for the EDIParse application.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Rationale:** <br>1. **Domain-Centric Design**: Places the domain at the center, ensuring business logic is not contaminated by external concerns.<br>2. **Clear Boundaries**: Defines clear boundaries between domain and external systems through ports and adapters.<br>3. **Testability**: Isolates domain from external dependencies, making it easier to test business logic.<br>4. **Flexibility**: Allows easy replacement of adapters without affecting the domain.<br>5. **Maintainability**: Clear separation of concerns makes the codebase easier to understand. |
| **Implementation:** <br>- **Domain Layer** (`src/ediparse/domain`): Contains models, business rules, and ports with no external dependencies<br>- **Application Layer** (`src/ediparse/application`): Implements use cases and services, depends only on domain<br>- **Adapters Layer**: Includes inbound adapters (`adapters/inbound/rest`), infrastructure components, and the EDIFACT parser                                                                                                                                                                                |
| **Consequences:** <br>- Positive: Improved maintainability, testability, and adaptability to change<br>- Positive: Clear separation between business logic and technical concerns<br>- Negative: Slightly more complex initial setup compared to monolithic approaches<br>- Negative: Requires discipline to maintain the architectural boundaries                                                                                                                                                                                                                             |
| **Alternatives Considered:** <br>1. **Layered Architecture**: Simpler but less flexible and more prone to coupling<br>2. **Microservices**: Too complex for the current scope and requirements<br>3. **Event-Driven Architecture**: Not necessary for the primarily request-response nature of the application                                                                                                                                                                                                                                                                 |
| **Related Decisions:** <br>- ADR-002: FastAPI as Web Framework<br>- ADR-003: Docker for Containerization                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

| ADR-002: FastAPI as Web Framework                                                                                                                                                                                                                                                                                                                                                                                           |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Status:** Accepted                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Date:** 2025-07-02                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Context:** <br>The application requires a web framework that is performant, supports modern Python features, and provides good developer experience.                                                                                                                                                                                                                                                                      |
| **Decision:** <br>Use FastAPI as the web framework for the REST API implementation.                                                                                                                                                                                                                                                                                                                                         |
| **Rationale:** <br>1. **Performance**: Built on Starlette and Pydantic, FastAPI offers high performance<br>2. **OpenAPI Integration**: Automatic generation of OpenAPI documentation<br>3. **Type Checking**: Leverages Python type hints for validation and editor support<br>4. **Async Support**: First-class support for asynchronous request handling<br>5. **Modern Python**: Takes advantage of Python 3.6+ features |
| **Implementation:** <br>- FastAPI is used in the inbound adapters layer to expose REST endpoints<br>- Pydantic models are used for request/response validation<br>- Automatic OpenAPI documentation is generated for API exploration                                                                                                                                                                                        |
| **Consequences:** <br>- Positive: Improved developer productivity with automatic documentation<br>- Positive: Better runtime validation through Pydantic<br>- Positive: Good performance characteristics<br>- Negative: Requires Python 3.6+ which may limit deployment options in some environments                                                                                                                        |
| **Alternatives Considered:** <br>1. **Flask**: Simpler but less performant and lacks built-in async support<br>2. **Django**: Too heavyweight for the application's needs<br>3. **Starlette**: Lower-level framework that FastAPI builds upon                                                                                                                                                                               |
| **Related Decisions:** <br>- ADR-001: Hexagonal Architecture<br>- ADR-003: Docker for Containerization                                                                                                                                                                                                                                                                                                                      |

| ADR-003: Docker for Containerization                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Status:** Accepted                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Date:** 2025-07-02                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Context:** <br>The application needs to be deployed consistently across different environments with minimal configuration differences.                                                                                                                                                                                                                                                                                  |
| **Decision:** <br>Use Docker for containerization of the EDIParse application.                                                                                                                                                                                                                                                                                                                                            |
| **Rationale:** <br>1. **Consistency**: Ensures the application runs the same way in all environments<br>2. **Isolation**: Provides isolation from the host system and other applications<br>3. **Portability**: Makes it easy to deploy in different environments<br>4. **Scalability**: Facilitates horizontal scaling when needed<br>5. **DevOps Integration**: Works well with CI/CD pipelines and orchestration tools |
| **Implementation:** <br>- A Dockerfile defines the application container<br>- Docker Compose is used for local development and testing<br>- Environment variables are used for configuration                                                                                                                                                                                                                              |
| **Consequences:** <br>- Positive: Consistent deployment across environments<br>- Positive: Simplified dependency management<br>- Positive: Easier integration with cloud platforms<br>- Negative: Additional complexity in the build and deployment process<br>- Negative: Requires Docker knowledge for development and operations                                                                                       |
| **Alternatives Considered:** <br>1. **Virtual Environments**: Less isolation and consistency<br>2. **System Packages**: More difficult to manage across different platforms<br>3. **Serverless Deployment**: Not suitable for the application's continuous operation model                                                                                                                                                |
| **Related Decisions:** <br>- ADR-001: Hexagonal Architecture<br>- ADR-002: FastAPI as Web Framework                                                                                                                                                                                                                                                                                                                       |

## 10. Quality Requirements

### 10.1 Performance

The application should be able to parse MSCONS messages efficiently, even for large files. The parsing process is optimized to handle large messages with minimal memory usage.

### 10.2 Usability

The API is designed to be easy to use with clear documentation. The OpenAPI specification provides detailed information about the endpoints and their parameters.

### 10.3 Maintainability

The codebase follows hexagonal architecture principles and is well-documented to ensure easy maintenance.

### 10.4 Reliability

The application handles malformed MSCONS messages gracefully and provides clear error messages.

## 11. Risks and Technical Debt

- The application currently has a limit on the number of lines it can parse (2442 lines by default). This may need to be increased for larger messages. However, this limit was introduced because the Swagger-UI crashed when trying to load large response payloads, particularly for endpoints that return JSON text strings for display in the UI.
- The application does not currently support all EDIFACT message types. Additional segment handlers may need to be implemented.

### 11.1 Extending the Parser Library

The EDIFACT Parser is implemented as a reusable library that can be used by other projects. The library is designed to be extensible, allowing developers to add support for new segment types or modify existing behavior.

The parser can be extended to support new segment types by implementing new handlers and converters, creating context models for the new segments, and registering the handlers with the `SegmentHandlerFactory`.

Some segments, like UNA (Service String Advice), require special handling due to their role in defining the syntax of the EDIFACT message.

For detailed information about how to extend the parser and handle special segments, see the [MSCONS Parsing Process Documentation](mscons-parsing-process.md) and [APERAK Parsing Process Documentation](aperak-parsing-process.md).

### 11.2 Extending with New Message Types

The application is designed to support multiple EDIFACT message types (currently MSCONS and APERAK) through a flexible architecture that uses composition, inheritance, and Pydantic v2's Discriminated Unions feature.

#### 11.2.1 Design Patterns for Message Type Extension

The application uses several design patterns to facilitate the extension with new message types:

1. **Inheritance Pattern**: All message types inherit from an abstract base class `AbstractEdifactMessage` that defines the common structure and interface.

2. **Composition Pattern**: The `EdifactInterchange` class uses composition to combine different types of EDIFACT messages within a single interchange.

3. **Discriminated Unions**: Pydantic v2's Discriminated Unions feature is used to automatically determine the correct message type during deserialization based on a 'message_type' field.

Here's a class diagram illustrating these patterns:

```plantuml
@startuml "EDIFACT Message Type Extension Architecture"

skinparam packageStyle rectangle
skinparam classBackgroundColor #FEFECE
skinparam classBorderColor #000000
skinparam classArrowColor #000000
skinparam classFontColor #000000

abstract class "AbstractEdifactMessage" {
  +unh_nachrichtenkopfsegment: SegmentUNH
  +bgm_beginn_der_nachricht: SegmentBGM
  +dtm_nachrichtendatum: list[SegmentDTM]
  +unt_nachrichtenendsegment: SegmentUNT
}

class "EdifactMSconsMessage" {
  +message_type: Literal["MSCONS"]
  +sg1_referenzen: List[SegmentGroup1]
  +sg2_marktpartnern: List[SegmentGroup2]
  +uns_abschnitts_kontrollsegment: SegmentUNS
  +sg5_liefer_bzw_bezugsorte: List[SegmentGroup5]
}

class "EdifactAperakMessage" {
  +message_type: Literal["APERAK"]
  +sg2_referenzen: list[SegmentGroup2]
  +sg3_marktpartnern: list[SegmentGroup3]
  +sg4_fehler_beschreibung: list[SegmentGroup4]
}

class "EdifactMessageUnion" {
  <<Discriminated Union>>
  discriminator="message_type"
}

class "EdifactInterchange" {
  +una_service_string_advice: SegmentUNA
  +unb_nutzdaten_kopfsegment: SegmentUNB
  +unh_unt_nachrichten: list[EdifactMessageUnion]
  +unz_nutzdaten_endsegment: SegmentUNZ
  +to_json(): str
}

AbstractEdifactMessage <|-- EdifactMSconsMessage
AbstractEdifactMessage <|-- EdifactAperakMessage
EdifactMessageUnion ..> EdifactMSconsMessage
EdifactMessageUnion ..> EdifactAperakMessage
EdifactInterchange o--> "0..*" EdifactMessageUnion : contains

note right of EdifactMessageUnion
  Discriminated Union using Pydantic v2
  Automatically determines message type
  based on the 'message_type' field
end note

note right of AbstractEdifactMessage
  Abstract base class defining
  common structure for all
  EDIFACT message types
end note

note bottom of EdifactInterchange
  Uses composition to combine
  different message types in
  a single interchange
end note

@enduml
```

#### 11.2.2 The 'mods' Folder Structure

The application uses a modular folder structure to organize message type-specific code:

```
src/ediparse/infrastructure/libs/edifactparser/
├── mods/
│   ├── aperak/
│   │   ├── group_state_resolver.py
│   │   ├── segments/
│   │   │   ├── message_structure.py
│   │   │   ├── segment_group.py
│   │   │   └── ...
│   │   └── ...
│   ├── mscons/
│   │   ├── group_state_resolver.py
│   │   ├── segments/
│   │   │   ├── message_structure.py
│   │   │   ├── segment_group.py
│   │   │   └── ...
│   │   └── ...
│   └── ...
└── wrappers/
    ├── segments/
    │   ├── base.py (AbstractEdifactMessage)
    │   ├── message_structure.py (EdifactInterchange, EdifactMessageUnion)
    │   └── ...
    └── ...
```

This structure allows new message types to be added without modifying existing code, by creating a new directory under the 'mods' folder.

#### 11.2.3 Adding a New Message Type

To add support for a new EDIFACT message type (e.g., ORDERS), follow these steps:

1. **Create a new module in the 'mods' folder**:
   ```
   src/ediparse/infrastructure/libs/edifactparser/mods/orders/
   ```

2. **Create message-specific models**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/mods/orders/segments/message_structure.py
   from typing import Literal
   from pydantic import Field

   from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
   from ediparse.infrastructure.libs.edifactparser.wrappers.segments.base import AbstractEdifactMessage

   class EdifactOrdersMessage(AbstractEdifactMessage):
       """
       Represents an ORDERS message within an interchange.
       """
       message_type: Literal[EdifactMessageType.ORDERS] = Field(
           default=EdifactMessageType.ORDERS,
           exclude=True
       )

       # ORDERS-specific fields
       # ...
   ```

3. **Create segment groups for the message type**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/mods/orders/segments/segment_group.py
   from pydantic import BaseModel

   class SegmentGroup1(BaseModel):
       """
       Segment Group 1 for ORDERS messages.
       """
       # SG1-specific fields
       # ...
   ```

4. **Create a group state resolver**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/mods/orders/group_state_resolver.py
   from typing import Optional

   from ediparse.infrastructure.libs.edifactparser.resolvers import GroupStateResolver
   from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
   from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext

   class OrdersGroupStateResolver(GroupStateResolver):
       @staticmethod
       def resolve_and_get_segment_group(
               current_segment_type: str,
               current_segment_group: Optional[SegmentGroup],
               context: Optional[ParsingContext],
       ) -> Optional[SegmentGroup]:
            # ORDERS-specific segment group determination logic
            # ...
            pass
   ```

5. **Add the message type to the constants**:
   ```python
   from ediparse.infrastructure.libs.edifactparser.wrappers.constants import StrEnum
   # src/ediparse/infrastructure/libs/edifactparser/wrappers/constants.py
   class EdifactMessageType(StrEnum):
       """
       The EDIFACT message types supported by the parser.
       """
       APERAK = "APERAK"
       MSCONS = "MSCONS"
       ORDERS = "ORDERS"  # Add the new message type
   ```

6. **Update the EdifactMessageUnion**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/wrappers/segments/message_structure.py
   from typing import Union, Annotated
   from pydantic import Field
   from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments.message_structure import EdifactAperakMessage
   from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.message_structure import EdifactMSconsMessage
   from ediparse.infrastructure.libs.edifactparser.mods.orders.segments.message_structure import EdifactOrdersMessage

   EdifactMessageUnion = Annotated[
       Union[
           EdifactAperakMessage,
           EdifactMSconsMessage,
           EdifactOrdersMessage,  # Add the new message type
       ],
       Field(discriminator="message_type")
   ]
   ```

7. **Register the group state resolver**:
   ```python
   from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
   from ediparse.infrastructure.libs.edifactparser.mods.aperak.group_state_resolver import AperakGroupStateResolver
   from ediparse.infrastructure.libs.edifactparser.mods.mscons.group_state_resolver import MsconsGroupStateResolver
   from ediparse.infrastructure.libs.edifactparser.mods.orders.group_state_resolver import OrdersGroupStateResolver

   def __register_resolvers(self) -> None:
       self.__handlers = {
           EdifactMessageType.APERAK: AperakGroupStateResolver(),
           EdifactMessageType.MSCONS: MsconsGroupStateResolver(),
           EdifactMessageType.ORDERS: OrdersGroupStateResolver(),  # Add the new resolver
       }
   ```

8. **Create a parsing context for the message type**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/mods/orders/context.py
   from typing import Optional

   from ediparse.infrastructure.libs.edifactparser.wrappers.segments import EdifactInterchange
   from ediparse.infrastructure.libs.edifactparser.mods.orders.segments import EdifactOrdersMessage
   from ediparse.infrastructure.libs.edifactparser.mods.orders.segments import SegmentGroup1, SegmentGroup2  # etc.

   class OrdersParsingContext:
       def __init__(self):
           self.interchange = EdifactInterchange()
           self.current_message: Optional[EdifactOrdersMessage] = None
           self.current_sg1: Optional[SegmentGroup1] = None
           self.current_sg2: Optional[SegmentGroup2] = None
           # etc.
           self.segment_count = 0
   ```

9. **Register the parsing context factory**:
   ```python
   # src/ediparse/infrastructure/libs/edifactparser/wrappers/context_factory.py
   from ediparse.infrastructure.libs.edifactparser.wrappers.constants import EdifactMessageType
   from ediparse.infrastructure.libs.edifactparser.wrappers.context import ParsingContext
   from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
   from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
   from ediparse.infrastructure.libs.edifactparser.mods.orders.context import OrdersParsingContext

   def create_context(self, message_type: EdifactMessageType) -> ParsingContext:
       if message_type == EdifactMessageType.APERAK:
           return APERAKParsingContext()
       elif message_type == EdifactMessageType.MSCONS:
           return MSCONSParsingContext()
       elif message_type == EdifactMessageType.ORDERS:
           return OrdersParsingContext()
       else:
           raise ValueError(f"Unsupported message type: {message_type}")
   ```

10. **Add segment handlers and converters** for any message-specific segments.

11. **Add tests** for the new message type.

This modular approach allows the application to be extended with new message types without modifying existing code, following the Open/Closed Principle of SOLID design.

## 12. Glossary

| Term    | Definition                                                             |
|---------|------------------------------------------------------------------------|
| APERAK  | Application Error and Acknowledgement message                          |
| EDIFACT | Electronic Data Interchange for Administration, Commerce and Transport |
| MSCONS  | Metered Services Consumption Report                                    |
| UNA     | EDIFACT service string advice                                          |
| UNB     | EDIFACT interchange header                                             |
| UNH     | EDIFACT message header                                                 |
| UNT     | EDIFACT message trailer                                                |
| UNZ     | EDIFACT interchange trailer                                            |
