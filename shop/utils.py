import uuid

# Generates order reference code
def refCodeGenereator():
    ref_code = uuid.uuid4().hex[:32].upper()
    return ref_code