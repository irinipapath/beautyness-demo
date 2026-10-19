# BEAUTYNESS — Beyond the Surface

A standalone Streamlit demonstration with **entirely fictional** Milan-based data. It is separate from your existing app and does not require APIs or accounts.

## Mac installation

1. Unzip `beautyness-demo-dashboard.zip` and open Terminal.
2. Type `cd ` (with a trailing space), drag the extracted `beautyness-demo` folder from Finder into Terminal, and press Return.
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If Streamlit says port 8501 is busy, use `python -m streamlit run app.py --server.port 8502`.

The app is accessible at `http://localhost:8501` (or 8502). Stop with Control+C.

## Included sections

- Beauty ID: personal home, weather/cycle/sleep contextual notes, editable goals
- Your Data: daily skin chart, period overlays, correlations, weekly check-in form
- My Routine: checklist and fictional product catalogue
- Inside Out: cycle, wearable-style sleep, Milan weather and example biomarkers
- Let's Chat: guided sample questions and expert consultation concept

## Safety and limitations

All data are invented. The supplied screenshots inspired the interface and sample period starts, but no personal photo or skin scan is incorporated, and the app does not perform actual AI analysis. The check-in form only previews a new entry in the current session and does not persist health or image data. Cycle observations are not fertility predictions. The bloodwork section is not clinical advice. This is for classroom demonstration only.
