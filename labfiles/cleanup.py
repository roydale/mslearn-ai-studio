import os
import openai
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai_client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=token_provider,
)

try:
    for vs in openai_client.vector_stores.list():
        print(f"Deleting vector store {vs.name} ({vs.id})")
        openai_client.vector_stores.delete(vs.id)

    for f in openai_client.files.list():
        print(f"Deleting file {f.filename} ({f.id})")
        openai_client.files.delete(f.id)

except openai.APIConnectionError:
    raise SystemExit("Can't reach the endpoint in .env. If the resource was purged, its vector stores and files are gone with it.")

except openai.NotFoundError:
    raise SystemExit("The resource behind the endpoint was deleted. Its vector stores and files go with it when it's purged.")