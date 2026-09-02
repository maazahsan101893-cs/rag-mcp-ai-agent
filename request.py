import requests

response = requests.post(
    "http://127.0.0.1:8000/query",
    json={"query": "What is covered in Week 1 of the HEC Generative AI course?"}
)

print(response.json())