import requests
from database import SessionLocal
from models.customer import Customer
from datetime import datetime

def fetch_and_store_customers():
    db = SessionLocal()
    total = 0

    try:
        page = 1
        while True:
            url = f"http://localhost:5000/api/customers?page={page}&limit=5"
            res = requests.get(url)

            if res.status_code != 200:
                break

            data = res.json().get("data", [])
            if not data:
                break

            for cust in data:
                existing = db.query(Customer).filter(
                    Customer.customer_id == cust["customer_id"]
                ).first()

                dob = None
                if cust.get("date_of_birth"):
                    dob = datetime.strptime(cust["date_of_birth"], "%Y-%m-%d")

                if existing:
                    existing.first_name = cust["first_name"]
                    existing.last_name = cust["last_name"]
                    existing.email = cust["email"]
                    existing.phone = cust["phone"]
                    existing.address = cust["address"]
                    existing.account_balance = cust["account_balance"]
                    existing.date_of_birth = dob
                else:
                    new = Customer(
                        customer_id=cust["customer_id"],
                        first_name=cust["first_name"],
                        last_name=cust["last_name"],
                        email=cust["email"],
                        phone=cust["phone"],
                        address=cust["address"],
                        account_balance=cust["account_balance"],
                        date_of_birth=dob,
                        created_at=datetime.now()
                    )
                    db.add(new)

                total += 1

            db.commit()
            page += 1

    except Exception as e:
        print("ERROR:", e)
        db.rollback()
        raise e

    finally:
        db.close()

    return total