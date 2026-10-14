GOVERNMENT SCHEME INFORMATION CHATBOT — VS CODE PROJECT
======================================================

FILES
-----
app.py              Streamlit chatbot interface
nlp_engine.py       Offline keyword search for English, common Tanglish and Tamil keywords
eligibility.py      Simple profile-based keyword filtering (demo only)
database.py         SQLite search-history logging
schemes.csv         100 scheme starter dataset
requirements.txt    Required Python packages

RUN ON WINDOWS
--------------
1. Download and unzip this folder.
2. Open the unzipped folder in VS Code.
3. Open Terminal > New Terminal.
4. Run:
   python -m pip install -r requirements.txt
5. Start the app:
   python -m streamlit run app.py
6. A local browser page will open. Keep the terminal running while using it.

IMPORTANT
---------
- No paid API key or external AI API is required.
- Tamil/Tanglish support is a small offline keyword dictionary, not full natural-language understanding or automatic translation.
- Eligibility results are only keyword-based suggestions and are NOT official eligibility decisions.
- The dataset is a starter educational dataset. It includes a mixture of schemes, services and programmes. Verify scheme status, benefits, dates, eligibility and URLs from official portals before real-world use.
- Some records may be legacy, notification-dependent, or not direct cash-benefit schemes. Check each record before presenting it as currently open.
- Do not collect sensitive personal data for a demo. Avoid storing names, Aadhaar numbers, bank details or documents.
