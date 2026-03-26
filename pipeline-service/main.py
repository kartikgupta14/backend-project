from fastapi import FastAPI, HTTPException
from database import engine, Base, SessionLocal
from models.customer import Customer
from services.ingestion import fetch_and_store_customers

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "FastAPI is working"}

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/ingest")
def ingest_data():
    count = fetch_and_store_customers()
    return {
        "status": "success",
        "records_processed": count
    }


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()

    try:
        start = (page - 1) * limit

        customers = db.query(Customer).offset(start).limit(limit).all()

        data = []
        for c in customers:
            data.append({
                "customer_id": c.customer_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "account_balance": c.account_balance
            })

        return {
            "data": data,
            "page": page,
            "limit": limit
        }

    finally:
        db.close()


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    try:
        customer = db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "account_balance": customer.account_balance
        }

    finally:
        db.close()
