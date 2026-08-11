import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine

app = FastAPI(title="Boatrace API", version="1.0")

# 環境変数からSupabaseの接続URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Welcome to Boatrace API on Render & Supabase!"}

@app.get("/results")
def get_results(limit: int = 200):
    """
    shobu_races_prediction テーブルからデータを取得するAPI
    """
    try:
        # LIMITを増やし、必要に応じて並び順を指定（例ではそのまま全件取得または必要数）
        query = f"SELECT * FROM shobu_races_prediction LIMIT {limit}"
        df = pd.read_sql(query, engine)
        data = df.to_dict(orient="records")
        return {"status": "success", "count": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
