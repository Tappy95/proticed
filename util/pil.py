import base64
import requests

with open("11.pdf", "rb") as pdf_file:
    encoded_string = pdf_file.read()
    # encoded_string = pdf_file.read()
    print(type(str(encoded_string)))
    print(type(encoded_string))
    print(encoded_string)
    print(type(eval(str(encoded_string))))

    # r = requests.post("http://192.168.6.20:18321/outer/addtask", data=payload)
    # print(r.text)
