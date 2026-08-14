# JudgeJudy

LLM jailbreak testing via LLM-as-a-judge. utilizes Gemini API to test open-source susceptibility to attacks

## launch (quick n dirty)

backend:
```
cd myproject/back-end
# make a .env with FLASK_ENV=development and Gemini=<your key>
uv sync
uv run python app.py
```

frontend:
```
cd myproject/front-end/react_landing_page
npm install
npm run dev
```

backend on :5000, frontend on :5173, just run both
