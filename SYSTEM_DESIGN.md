# System Design Principles Applied

## 🏗️ Architecture Overview

This document outlines the system design principles and patterns applied to make ResumeOS production-ready and maintainable.

## ✅ Design Principles Implemented

### 1. **Separation of Concerns (SoC)**

**Before**: Business logic mixed with API layer  
**After**: Clear separation into layers

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │  ← HTTP endpoints, request/response
├─────────────────────────────────────┤
│        Service Layer                │  ← Business logic, orchestration
├─────────────────────────────────────┤
│      Domain Layer                   │  ← Core business entities
│  (Compiler, Parser, Renderer)      │
├─────────────────────────────────────┤
│      Infrastructure Layer           │  ← File I/O, AI, Config
└─────────────────────────────────────┘
```

**Files**:
- `api_example.py` - API layer only
- `services.py` - Business logic service layer
- `resume_compiler.py` - Domain logic
- `config.py` - Infrastructure

### 2. **Dependency Injection**

**Before**: Direct instantiation, hardcoded dependencies  
**After**: Services injected, configurable

```python
# Services are created once and injected
resume_service = ResumeService()
file_service = FileService()

# Configuration is injected
config = get_config()
```

**Benefits**:
- Testable (can mock dependencies)
- Flexible (easy to swap implementations)
- Maintainable (clear dependencies)

### 3. **Configuration Management (12-Factor App)**

**Before**: `os.getenv()` scattered throughout code  
**After**: Centralized configuration class

```python
# Single source of truth
config = get_config()

# Type-safe access
api_port = config.api_port
ai_provider = config.ai_provider
```

**Features**:
- Environment-based configuration
- Sensible defaults
- Type safety
- Easy to test (can override)

### 4. **Custom Exception Hierarchy**

**Before**: Generic exceptions, unclear error handling  
**After**: Domain-specific exceptions

```python
# Clear error types
try:
    resume = service.parse_latex_resume(latex)
except ParsingError:
    # Handle parsing errors
except ValidationError:
    # Handle validation errors
```

**Exception Types**:
- `ResumeOSError` - Base exception
- `CompilationError` - Compilation failures
- `ParsingError` - Input parsing failures
- `RenderingError` - Output rendering failures
- `ValidationError` - Input validation failures
- `AIError` - AI-related errors
- `ConfigurationError` - Config errors

### 5. **Service Layer Pattern**

**Before**: Direct calls to compiler from API  
**After**: Service layer abstracts business logic

```python
# Service encapsulates complexity
class ResumeService:
    def compile_resume(self, master_resume, job_description, enable_ai):
        # Handles AI agent creation
        # Handles error recovery
        # Handles validation
        # Returns structured result
```

**Benefits**:
- Single responsibility
- Reusable business logic
- Easier to test
- Clear API boundaries

### 6. **Repository Pattern (File Operations)**

**Before**: Direct file I/O in API layer  
**After**: FileService abstracts file operations

```python
# Abstracted file operations
file_service.save_latex(content, filename)
file_service.read_latex(file_path)
file_service.file_exists(filename)
```

**Benefits**:
- Testable (can mock file operations)
- Consistent error handling
- Easy to swap storage (local → S3)

### 7. **Error Handling Strategy**

**Before**: Inconsistent error handling  
**After**: Consistent error mapping

```python
# API layer maps domain exceptions to HTTP
try:
    result = service.compile_resume(...)
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
except CompilationError as e:
    raise HTTPException(status_code=500, detail=str(e))
```

**Benefits**:
- Consistent API responses
- Proper HTTP status codes
- Clear error messages
- Logging at appropriate levels

### 8. **Single Responsibility Principle (SRP)**

Each module has one clear purpose:

- `config.py` - Configuration management only
- `exceptions.py` - Exception definitions only
- `services.py` - Business logic orchestration
- `api_example.py` - HTTP endpoints only
- `resume_compiler.py` - Compilation logic only

### 9. **Open/Closed Principle**

**Extensible without modification**:

```python
# Easy to add new AI providers
class ResumeService:
    def _create_ai_agent(self):
        # Can extend without modifying service
        if config.ai_provider == "openai":
            return create_openai_agent()
        elif config.ai_provider == "anthropic":
            return create_anthropic_agent()
        # Easy to add new providers
```

### 10. **Dependency Inversion Principle**

**Depend on abstractions, not concretions**:

```python
# Service depends on AI agent interface, not implementation
class ResumeService:
    def __init__(self, ai_agent: Optional[AIAgent] = None):
        # Can work with any AI agent implementation
        self.compiler = ResumeCompiler(ai_agent=ai_agent)
```

## 📊 Architecture Layers

### Layer 1: API Layer (`api_example.py`)
- **Responsibility**: HTTP endpoints, request/response handling
- **Dependencies**: Services, exceptions
- **No business logic**

### Layer 2: Service Layer (`services.py`)
- **Responsibility**: Business logic orchestration
- **Dependencies**: Domain layer, infrastructure
- **Coordinates**: Compiler, parser, renderer, AI agent

### Layer 3: Domain Layer
- **Responsibility**: Core business logic
- **Files**: `resume_compiler.py`, `latex_parser.py`, `latex_renderer.py`
- **No dependencies on infrastructure**

### Layer 4: Infrastructure Layer
- **Responsibility**: External concerns
- **Files**: `config.py`, `ai_agent.py`, `services.py` (file operations)
- **Handles**: Configuration, AI APIs, file I/O

## 🔄 Data Flow

```
HTTP Request
    ↓
API Layer (validation, error mapping)
    ↓
Service Layer (orchestration, business logic)
    ↓
Domain Layer (compilation, parsing, rendering)
    ↓
Infrastructure Layer (file I/O, AI calls)
    ↓
Response
```

## 🧪 Testability Improvements

### Before
- Hard to test (tightly coupled)
- Can't mock dependencies
- Configuration scattered

### After
- Easy to test (dependency injection)
- Can mock services
- Configuration can be overridden

```python
# Example test
def test_compile_resume():
    mock_ai_agent = MockAIAgent()
    service = ResumeService(ai_agent=mock_ai_agent)
    result = service.compile_resume(master_resume, jd)
    assert result is not None
```

## 🚀 Scalability Considerations

1. **Stateless Services**: Services are stateless, can scale horizontally
2. **Configuration**: Environment-based, easy to deploy
3. **Error Recovery**: Graceful fallbacks (AI → rule-based)
4. **Logging**: Structured logging for monitoring
5. **CORS**: Configured for production use

## 📝 Best Practices Applied

1. ✅ **12-Factor App**: Configuration via environment
2. ✅ **SOLID Principles**: All five principles applied
3. ✅ **Clean Architecture**: Clear layer separation
4. ✅ **Error Handling**: Consistent, domain-specific exceptions
5. ✅ **Logging**: Structured, appropriate levels
6. ✅ **Type Hints**: Better IDE support, documentation
7. ✅ **Documentation**: Clear docstrings, architecture docs

## 🔮 Future Improvements

1. **Caching Layer**: Add Redis for expensive operations
2. **Rate Limiting**: Add rate limiting middleware
3. **Database Layer**: Add repository pattern for persistence
4. **Event Bus**: For async processing
5. **Monitoring**: Add metrics and health checks
6. **API Versioning**: Support multiple API versions

---

**Status**: ✅ Production-ready architecture with best practices applied
