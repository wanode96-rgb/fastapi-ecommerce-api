# FastAPI E-Commerce API 

A high-performance, asynchronous REST API built with FastAPI, SQLModel, and PostgreSQL. Designed with a focus on scalability and clean architecture.

##  Technical Stack
- **Framework:** FastAPI (Asynchronous)
- **Database/ORM:** PostgreSQL with SQLModel (SQLAlchemy 2.0 based)
- **Security:** JWT Authentication (OAuth2), Password Hashing with Bcrypt
- **Validation:** Pydantic v2

##  Key Features
- **Role-Based Access Control (RBAC):** Distinct permissions for Admins and Customers.
- **Optimized Cart System:** Implements "Upsert" logic and SQLAlchemy `selectinload` to prevent N+1 query problems.
- **Order Management:** Secure checkout process that snapshots product prices at the time of purchase.
- **Async Database Sessions:** Fully non-blocking I/O operations for high concurrency.

##  How to Run
1. Clone the repo.
2. Create a `.env` file with your `DATABASE_URL` and `SECRET_KEY`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the server: `uvicorn app.main:app --reload`.

##  Future Roadmap
- [ ] Integration with Payment Gateways (Stripe/Razorpay)
- [ ] Redis caching for product catalog
- [ ] Dockerization for easy deployment