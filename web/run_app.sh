#! /bin/bash

# 175.196.78.7 30010
# nohup uv run python -m streamlit run main.py --server.headless true &> log.out &

uv run python -m streamlit run rfp.py --server.headless true