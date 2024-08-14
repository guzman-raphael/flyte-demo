# task image
FROM python:3.11-slim
RUN pip install --no-cache-dir datajoint flytekit
COPY ./src/workflow_v4.py ./src/pipeline_v4.py ./src/utils_v4.py /usr/local/lib/python3.11/site-packages/
