# Seatools API Documentation

## Overview

Seatools is a comprehensive Python toolkit (Python >= 3.9) inspired by Java Spring, providing IOC container management, file processing, encryption, notifications, and much more.

## Installation

```bash
pip install seatools --upgrade
```

## Table of Contents

1. [Core IOC Framework](#core-ioc-framework)
2. [File Processing](#file-processing)
3. [Data Models](#data-models)
4. [Builders](#builders)
5. [Cryptography](#cryptography)
6. [Notifications](#notifications)
7. [Logging](#logging)
8. [Caching](#caching)
9. [Database](#database)
10. [Utilities](#utilities)
11. [Environment Management](#environment-management)

---

## Core IOC Framework

### `seatools.ioc`

The IOC (Inversion of Control) framework provides dependency injection and AOP capabilities similar to Java Spring.

#### `run(scan_package_names, config_dir, enable_aspect=False)`

Starts the IOC container and scans packages for beans.

**Parameters:**
- `scan_package_names` (str|list): Package names to scan
- `config_dir` (str): Configuration directory path
- `enable_aspect` (bool): Enable AOP aspect support

**Example:**
```python
from seatools.ioc import run

# Start IOC container
run(scan_package_names='myapp', config_dir='./config')
```

#### `@Bean(name=None, primary=False)`

Decorator to register a class or function as a bean in the IOC container.

**Parameters:**
- `name` (str, optional): Bean name (defaults to camelCase class name)
- `primary` (bool): Whether this is the primary bean for the type

**Example:**
```python
from seatools.ioc import Bean

@Bean(primary=True)
class UserService:
    def get_user(self, user_id):
        return f"User {user_id}"

@Bean(name='special_service')
def create_special_service():
    return UserService()
```

#### `Autowired(value=None, cls=None, required=True)`

Auto-inject dependencies from the IOC container.

**Parameters:**
- `value` (str, optional): Bean name
- `cls` (type, optional): Bean type
- `required` (bool): Whether injection is required

**Example:**
```python
from seatools.ioc import Autowired, Bean

@Bean
class DatabaseService:
    def connect(self):
        return "Connected to database"

# Inject by type
db_service = Autowired(cls=DatabaseService)

# Inject by name
named_service = Autowired('special_service')
```

#### `Value(property_path, cls=None)`

Inject configuration values from application properties.

**Parameters:**
- `property_path` (str): Property path in ${} format
- `cls` (type, optional): Target model class

**Example:**
```python
from seatools.ioc import Value

# application.yml:
# database:
#   host: localhost
#   port: 3306

db_host = Value('${database.host}')
db_port = Value('${database.port}')

print(db_host.str)  # "localhost"
print(db_port.int)  # 3306
```

#### `@ConfigurationPropertiesBean(prop=None)`

Automatically bind configuration properties to a model class.

**Example:**
```python
from seatools.ioc import ConfigurationPropertiesBean
from seatools.models import BaseModel

@ConfigurationPropertiesBean(prop='database')
class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
```

### AOP (Aspect-Oriented Programming)

#### `@Aspect`

Mark a class as an aspect for cross-cutting concerns.

#### `AbstractAspect`

Base class for implementing aspects.

**Example:**
```python
from seatools.ioc import Aspect, AbstractAspect, JoinPoint

@Aspect
class LoggingAspect(AbstractAspect):
    pointcut = "execution(myapp.services.*.*)"
    
    def before(self, point: JoinPoint, **kwargs):
        print(f"Before executing {point.method_name}")
    
    def after(self, point: JoinPoint, **kwargs):
        print(f"After executing {point.method_name}")
    
    def around(self, point: JoinPoint, **kwargs):
        print("Around before")
        result = point.proceed()
        print("Around after")
        return result
```

---

## File Processing

### `seatools.files`

Unified file processing for multiple formats.

#### `AutoDataFileLoader`

Automatically detect and load various file formats.

**Methods:**
- `load(config_data, modelclass=dict, data_type=None, **kwargs)`: Load from string
- `load_file(file_path, encoding='utf-8', modelclass=dict, **kwargs)`: Load from file

**Example:**
```python
from seatools.files import AutoDataFileLoader
from seatools.models import BaseModel

class Config(BaseModel):
    name: str
    version: str

loader = AutoDataFileLoader()

# Load JSON string
config = loader.load('{"name": "myapp", "version": "1.0"}', modelclass=Config)

# Load YAML file
config = loader.load_file('config.yaml', modelclass=Config)
```

#### `DynamicDataFileExtractor`

Extract data to various file formats.

**Methods:**
- `extract(data, data_type=DataType.JSON, **kwargs)`: Extract to string
- `extract_file(file_path, data, encoding='utf-8', **kwargs)`: Extract to file

**Example:**
```python
from seatools.files import DynamicDataFileExtractor, DataType

extractor = DynamicDataFileExtractor()
data = {"name": "test", "value": 123}

# Extract to JSON
json_str = extractor.extract(data, DataType.JSON)

# Extract to YAML file
extractor.extract_file('output.yaml', data)
```

#### Supported File Types

- **JSON**: `.json`
- **YAML**: `.yaml`, `.yml`
- **CSV**: `.csv`
- **XML**: `.xml`, `.html`
- **Excel**: `.xls`, `.xlsx`
- **INI**: `.ini`, `.toml`, `.cfg`
- **Properties**: `.properties`
- **Python**: `.py`, `.pyi`, `.pyx`

---

## Data Models

### `seatools.models`

Enhanced Pydantic models for business scenarios.

#### `BaseModel`

Enhanced base model with automatic type conversion.

**Features:**
- Automatic string type enhancement
- JSON encoders for datetime
- Extensible type handlers

**Example:**
```python
from seatools.models import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    active: bool = True

user = User(id="123", name="John", active="true")
print(user.id)  # 123 (converted from string)
```

#### `R` - Response Model

Standard API response wrapper.

**Methods:**
- `R.ok(data=None, msg='请求成功', code=200)`: Success response
- `R.fail(msg='请求失败', code=500)`: Error response

**Example:**
```python
from seatools.models import R

# Success response
response = R.ok(data={"user_id": 123}, msg="User found")

# Error response
error = R.fail(msg="User not found", code=404)
```

#### `PageModel` & `PageR`

Pagination support for API responses.

**Example:**
```python
from seatools.models import PageModel, PageR

# Create paginated data
page_data = PageModel(
    rows=[{"id": 1}, {"id": 2}],
    page=1,
    page_size=10,
    total=100
)

response = PageR.ok(data=page_data)
```

---

## Builders

### `seatools.builders`

Build HTML and Markdown content programmatically.

#### `HtmlBuilder`

Build HTML elements with method chaining.

**Example:**
```python
from seatools.builders import HtmlBuilder, ATarget

html = HtmlBuilder()
content = (html
    .h1("Welcome")
    .p("This is a paragraph")
    .a("Click here", href="https://example.com", target=ATarget.BLANK)
    .div(
        html.ul(
            html.li("Item 1"),
            html.li("Item 2")
        )
    )
    .build())

print(content)
```

#### `MarkdownBuilder`

Build Markdown content with method chaining.

**Example:**
```python
from seatools.builders import MarkdownBuilder

md = MarkdownBuilder()
content = (md
    .h1("Title")
    .p("This is a paragraph")
    .code_block("print('Hello World')", language="python")
    .table([
        ["Name", "Age"],
        ["John", "30"],
        ["Jane", "25"]
    ])
    .build())

print(content)
```

---

## Cryptography

### `seatools.cryptography`

Common encryption and hashing utilities.

#### MD5 Hashing

**Example:**
```python
from seatools.cryptography import md5, Md5DigitEnum

# Generate MD5 hash
hash_32 = md5("hello world", Md5DigitEnum.DIGIT_32)
hash_16 = md5("hello world", Md5DigitEnum.DIGIT_16)
```

#### Base64 Encoding/Decoding

**Example:**
```python
from seatools.cryptography import (
    encode_base64, decode_base64,
    encode_base32, decode_base32,
    encode_base16, decode_base16
)

# Base64
encoded = encode_base64("hello world")
decoded = decode_base64(encoded)

# Base32
encoded32 = encode_base32("hello world")
decoded32 = decode_base32(encoded32)
```

#### HMAC

**Example:**
```python
from seatools.cryptography import md5_hmac, sha256_hmac

# HMAC with MD5
signature = md5_hmac("secret_key", "message")

# HMAC with SHA256
signature = sha256_hmac("secret_key", "message")
```

---

## Notifications

### `seatools.notices`

Send notifications via email and messaging platforms.

#### `SmtpEmailNotice`

Send emails via SMTP.

**Example:**
```python
from seatools.notices import SmtpEmailNotice

email_notice = SmtpEmailNotice(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="your_email@gmail.com",
    password="your_password"
)

email_notice.send(
    to=["recipient@example.com"],
    subject="Test Email",
    content="Hello from seatools!",
    content_type="text/html"
)
```

#### `FeishuRobotNotice`

Send messages to Feishu (Lark) via webhook.

**Example:**
```python
from seatools.notices import (
    FeishuRobotNotice, FeishuRobotTextMsg, 
    FeishuRobotPostMsg, FeishuRobotCardMsg
)

robot = FeishuRobotNotice(webhook_url="your_webhook_url")

# Send text message
text_msg = FeishuRobotTextMsg(text="Hello from robot!")
robot.send(text_msg)

# Send rich post message
post_msg = FeishuRobotPostMsg(title="Alert", content="System alert message")
robot.send(post_msg)
```

---

## Logging

### `seatools.logger`

Enhanced logging setup with Loguru.

#### `setup()`

Configure logging with file rotation and formatting.

**Example:**
```python
from seatools.logger import setup, PrefixLogger

# Setup logging
setup(
    log_file="app.log",
    level="INFO",
    rotation="100 MB",
    retention="30 days"
)

# Use prefix logger
logger = PrefixLogger("MyModule")
logger.info("This is an info message")
logger.error("This is an error message")
```

---

## Caching

### `seatools.cache`

Memory caching with TTL and various eviction policies.

#### `Cache`

Synchronous cache implementation.

**Example:**
```python
from seatools.cache import Cache
from cachetools import TTLCache

# Create cache with TTL
cache = Cache(TTLCache(maxsize=100, ttl=300))  # 5 minutes TTL

@cache.cached()
def expensive_operation(param):
    # Simulate expensive computation
    return f"Result for {param}"

# Function result will be cached
result = expensive_operation("test")
```

#### `AsyncCache`

Asynchronous cache implementation.

**Example:**
```python
from seatools.cache import AsyncCache
from cachetools import LRUCache

cache = AsyncCache(LRUCache(maxsize=100))

@cache.cached()
async def async_operation(param):
    # Simulate async operation
    return f"Async result for {param}"

# Usage
result = await async_operation("test")
```

---

## Database

### `seatools.sqlalchemy`

SQLAlchemy ORM utilities and database clients.

#### `SqlAlchemyClient`

Database client with connection management.

**Example:**
```python
from seatools.sqlalchemy import SqlAlchemyClient, Base

# Create client
client = SqlAlchemyClient(
    database_url="postgresql://user:pass@localhost/db"
)

# Define model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

# Use client
with client.session() as session:
    user = User(name="John")
    session.add(user)
    session.commit()
```

### `seatools.mysql`

MySQL database utilities.

**Example:**
```python
from seatools.mysql.pymysql import execute_sql, query_sql

# Execute query
results = query_sql(
    host="localhost",
    user="root",
    password="password",
    database="mydb",
    sql="SELECT * FROM users WHERE id = %s",
    params=(1,)
)
```

---

## Utilities

### `seatools.retry`

Retry mechanisms for unreliable operations.

#### `Retry`

Synchronous retry decorator.

**Example:**
```python
from seatools.retry import Retry

@Retry(max_attempts=3, delay=1.0, backoff=2.0)
def unreliable_operation():
    # Operation that might fail
    import random
    if random.random() < 0.5:
        raise Exception("Random failure")
    return "Success"

result = unreliable_operation()
```

#### `AsyncRetry`

Asynchronous retry decorator.

**Example:**
```python
from seatools.retry import AsyncRetry

@AsyncRetry(max_attempts=3, delay=1.0)
async def async_unreliable_operation():
    # Async operation that might fail
    return "Success"

result = await async_unreliable_operation()
```

### `seatools.task`

Task management utilities.

**Example:**
```python
from seatools.task import Task, AsyncTask

# Synchronous task
task = Task(target=lambda x: x * 2, args=(5,))
result = task.run()

# Asynchronous task
async_task = AsyncTask(target=lambda x: x * 2, args=(5,))
result = await async_task.run()
```

---

## Environment Management

### `seatools.env`

Multi-environment configuration management.

#### `EnvEnum`

Environment enumeration with helper methods.

**Example:**
```python
from seatools.env import get_env, EnvEnum
import os

# Set environment
os.environ['ENV'] = 'dev'

env = get_env()
if env.is_dev():
    print("Running in development mode")
elif env.is_pro():
    print("Running in production mode")
```

---

## Additional Modules

### FastAPI Extensions

```python
from seatools.fastapi import create_app

app = create_app()
```

### Redis Extensions

```python
from seatools.redis import RedisClient

client = RedisClient(host="localhost", port=6379)
```

### Algorithm Utilities

```python
from seatools.algorithm.similarity import cosine_similarity

similarity = cosine_similarity(vector1, vector2)
```

---

## Configuration

Seatools supports YAML configuration files:

```yaml
# application.yml
server:
  host: localhost
  port: 8080

database:
  host: localhost
  port: 3306
  username: user
  password: pass
```

Load configuration in your application:

```python
from seatools.ioc import run, Value

run(scan_package_names='myapp', config_dir='./config')

server_host = Value('${server.host}')
db_config = Value('${database}', cls=DatabaseConfig)
```

## Best Practices

1. **Use IOC for complex dependencies**: Leverage the IOC container for managing complex object graphs
2. **Type hints**: Always use type hints with Pydantic models
3. **Configuration externalization**: Keep configuration in YAML files
4. **Error handling**: Use the retry mechanisms for unreliable operations
5. **Logging**: Use the structured logging setup for better observability
6. **Caching**: Cache expensive operations to improve performance

## Contributing

1. Follow the existing code style
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Use type hints consistently

## License

MIT License - see LICENSE file for details.