import base64
import requests

with open("11.pdf", "rb") as pdf_file:
    encoded_string = base64.b64decode(pdf_file.read())
    # encoded_string = pdf_file.read()
    print(str(encoded_string))
    # print(bytearray(encoded_string))
    # print(base64.b64decode(encoded_string))
    # print(str(encoded_string, encoding='utf-8'))
    payload = {
        "app_id": 1,
        "tasks": [
            {
                "account_id": "800",
                "task_type": "amazon:upload_invoice",
                "task_info": {"OrderId": "408-4453378-7649135", "InvoiceNumber": "INV-IT-408-4453378-7649135",
                              "pdf_byte": str(encoded_string, encoding='utf-8'), "TotalAmount": 4.29, "VATAmount": 0,
                              "DocumentType": "Invoice"}
            }
        ]
    }
    r = requests.post("http://192.168.6.20:18321/outer/addtask", data=payload)
    print(r.text)
