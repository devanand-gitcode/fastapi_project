from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import StreamingResponse
# import  models for validation
from models import QueryRequest, QueryResponse
# import retrieve_response & retrieve
from rag_pipeline import retrieve, generate_response
# import logging module
import logging
from io import StringIO
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
app = FastAPI()


def log_request(query: str, top_k: int):
    logging.info(f"Received query: '{query}' with top_k: {top_k}")



@app.post("/query")
async def query(request: QueryRequest):
    query = request.query
    top_k = request.top_k

    log_request(query, top_k)


    # Retrieve relevant contexts
    contexts = retrieve(query, top_k)

    # If no contexts found, handle the error
    if not contexts:
        raise HTTPException(status_code=404, detail="No relevant contexts found.")

    # Generate the response based on retrieved contexts
    generated_response = generate_response(query, contexts)

    def stream_response():
        # Simulate a streaming response by chunking the generated response
        yield f"Generated Response:\n"
        time.sleep(1)
        for chunk in generated_response.splitlines():
            yield f"{chunk}\n"
            time.sleep(1)

    return StreamingResponse(stream_response(), media_type="text/plain")
