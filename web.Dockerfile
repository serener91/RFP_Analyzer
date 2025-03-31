FROM python:3.10-slim
LABEL authors="gukhwan"
LABEL build_date="2025-03"

EXPOSE 10080

WORKDIR /app

# Copy web server
COPY web/rfp.py .

# Copy utility functions
COPY common/ /app/common/
COPY monitoring/.env /app/common/

# Copy env files
COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .

# Create env
RUN apt-get update && apt install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENTRYPOINT ["bash", "-c", "source $HOME/.local/bin/env && uv sync"]

# RUN uv init .
# RUN uv pip install --system --no-cache-dir -r requirements.txt

#RUN pip install --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt

# WORKDIR /
