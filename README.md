# StockLoop V1

StockLoop is a polished Streamlit prototype for simulated hospital stock redistribution across three fictional sites. It includes a dashboard, searchable inventory (20 medicines and 30 consumables), transparent AI-style predictions, cross-site matching, and an approval workflow.

## Important scope

All data, sites, predictions and outcomes are simulated. This prototype is not NHS-endorsed, does not claim validated model accuracy or real savings, and must not be used for clinical decisions or real transfer authorisation. Medicine and consumable checks are intentionally separate. Medicine transfers require batch, expiry, storage, traceability and eligibility checks and can never be automatically approved.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -q
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Deployment options

- Streamlit Community Cloud: push this folder to a Git repository, choose `app.py` as the entrypoint, and use `requirements.txt` for dependencies.
- Docker or a managed container service: install the requirements and run `streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT`.
- Internal hosting: place behind your organisation's authentication, network controls and audit logging before any non-simulated use.

