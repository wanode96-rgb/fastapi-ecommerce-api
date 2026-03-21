# FastAPI E-Commerce API

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker)
![Railway](https://img.shields.io/badge/Deployed-Railway-6200EE?style=flat)

A high-performance, asynchronous REST API built with FastAPI, SQLModel, and PostgreSQL. Designed with a focus on scalability, security, and clean architecture.

🔗 **Live Demo:** [https://fastapi-ecommerce-api-production-9cf0.up.railway.app/docs](https://fastapi-ecommerce-api-production-9cf0.up.railway.app/docs)

---

## Screenshots

> Swagger UI — Live & Interactive

![Swagger UI](screenshots/swagger1.png)
![API Endpoints](screenshots/swagger2.png)

---

## Technical Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Async) |
| ORM | SQLModel (SQLAlchemy 2.0) |
| Database | PostgreSQL |
| Migrations | Alembic |
| Security | JWT (OAuth2) + Bcrypt |
| Validation | Pydantic v2 |
| Deployment | Docker + Railway |

---

## Key Features

- **JWT Authentication:** Secure login with OAuth2 password flow and access tokens.
- **Role-Based Access Control (RBAC):** Distinct permissions for Admins and Customers using FastAPI Dependency Injection.
- **Optimized Queries:** Implements SQLAlchemy `selectinload` to prevent N+1 query problems.
- **Order Management:** Checkout process that snapshots product prices at the time of purchase.
- **Async Database Sessions:** Fully non-blocking I/O for high concurrency.
- **Auto-generated Docs:** Interactive Swagger UI available at `/docs`.

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/login` | Login and get access token | ❌ |

### Users
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/users/register` | Register new user | ❌ |
| GET | `/users/me` | Get current user profile | ✅ |
| GET | `/users/admin` | Admin only route | ✅ Admin |

### Products
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/products/` | List all products | ❌ |
| GET | `/products/{product_id}` | Get single product | ❌ |
| POST | `/products/` | Create new product | ✅ Admin |
| PUT | `/products/{product_id}` | Update product | ✅ Admin |
| DELETE | `/products/{product_id}` | Delete product | ✅ Admin |

### Cart
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/cart/` | View cart | ✅ |
| POST | `/cart/` | Add item to cart | ✅ |
| DELETE | `/cart/{cart_id}` | Remove item from cart | ✅ |

### Orders
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/orders/checkout` | Place order | ✅ |
| GET | `/orders/history` | Get order history | ✅ |

### Categories
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/categories/` | List categories | ❌ |
| POST | `/categories/` | Add category | ✅ Admin |

### Reviews
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/reviews/{product_id}` | Post a review | ✅ |

---

## Local Setup
```bash
# 1. Clone the repo
git clone https://github.com/wanode96-rgb/fastapi-ecommerce-api.git
cd fastapi-ecommerce-api

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY

# 5. Run migrations
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload
```

## Run with Docker
```bash
docker build -t fastapi-ecommerce .
docker run -p 8000:8000 --env-file .env fastapi-ecommerce
```

---

## Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Project Structure
```
fastapi-ecommerce-api/
├── app/
│   ├── api/          # Route handlers
│   ├── core/         # Config, DB, security
│   ├── crud/         # Database operations
│   ├── models/       # SQLModel table models
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # App entry point
├── alembic/          # Database migrations
├── Dockerfile
├── requirements.txt
└── .env.example
```
