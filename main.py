import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import json

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
def get_results(limit: int = 1000):
    """
    shobu_races_prediction テーブルからデータを取得し、
    各レースの上位予想を6件に制限して返すAPI
    """
    try:
        query = f"SELECT * FROM shobu_races_prediction LIMIT {limit}"
        df = pd.read_sql(query, engine)
        
        # データフレームから辞書リストへ変換
        records = df.to_dict(orient="records")
        
        # 各レコードの予想データを処理
        processed_data = []
        for record in records:
            # もし「上位予想」のようなリストデータが含まれるキーがあればここでスライスする
            # ※お使いのDBの実際のカラム名に合わせて'top_predictions'を書き換えてください
            if 'top_predictions' in record and isinstance(record['top_predictions'], list):
                record['top_predictions'] = record['top_predictions'][:6]
            
            processed_data.append(record)
            
        return {"status": "success", "count": len(processed_data), "data": processed_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
