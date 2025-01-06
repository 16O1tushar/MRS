import requests

url = "https://drive.google.com/file/d/19U23aQ947aR_8pljX09aZ8T-N_DkCJMx/view?usp=sharing"
response = requests.get(url)
with open("similarity.pkl", "wb") as f:
    f.write(response.content)
