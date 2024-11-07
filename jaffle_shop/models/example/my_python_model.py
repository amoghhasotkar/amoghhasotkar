import json, pandas
import vertexai
from vertexai.generative_models import GenerativeModel

region = "us-central1"
model_name = "gemini-1.5-flash-001"
prompt = """Here is a list of names.
I want you to check if the names correspond to real airports. For each real airport, return its name along with 
its icao code, iata code, city, state or province, and country.
Return the results as json.
For example:
{"name": "Los Angeles International Airport": "icao": "KLAX", "iata": "LAX", "city": "Los Angelos", "state": "CA", "co
untry": "United States"},
{"name": "Adak Airport": "icao": "PADK", "iata": "ADK", "city": "Adak Island", "state": "AK", "country": "United State
s"}
Don't return the records which are not valid airports.

Below is the list of names:
"Los Angeles International Airport, United States"
"Adak Airport, United States"
"""

def model(dbt, session):
    dbt.config(materialized="table")
    vertexai.init(location=region)
    model = GenerativeModel(model_name)
    resp = model.generate_content([prompt])
    resp_text = resp.text.replace("```json", "").replace("```", "").replace("\n", "")
    print(resp_text)

    json_obj = json.loads(resp_text)
    df_airports = session.createDataFrame(json_obj) 
    return df_airports
