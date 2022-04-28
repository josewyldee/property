import uuid

def generate_transaction_id():
    transaction_id=str(uuid.uuid4()).replace("-","").upper()[:8]
    return transaction_id