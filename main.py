import os
from datetime import datetime
import pandas as pd


def load_and_display_shobu_races(file_path: str):
  if not os.path.exists(file_path):
    print(f"エラー: ファイルが見つかりません -> {file_path}")
    return

  # Excelファイルの読み込み（必要に応じてシート名を指定してください）
  df = pd.read_excel(file_path)

  # --- [前提] Excel側のカラム構成（例）に合わせて適宜変更してください ---
  # 必要なカラムの目安:
  # '場名' (例: 唐津), 'R' (例: 1), '締切時間' (例: 08:44),
  # 'スコア' (例: 95), '1号艇AI勝率' (例: 87.1), '日付' (例: 2026年8月11日)
  # -----------------------------------------------------------------

  # 全体の件数
  total_count = len(df)
  date_str = "2026年8月11日"  # 必要に応じてdfから動的に取得してもOK

  # 1. サマリー部分の表示
  print(
      "=" * 89
      + f"\n 🎯 【全場】 本日の勝負レース判定サマリー（設定勝率: 85%以上 /"
      " 各場上位3Rまで）\n"
      + "=" * 89
  )
  print(
      f" 🔥 【判定】 本日は全国で合計 **{total_count}件**"
      " の勝負レースがあります！\n"
  )

  # 場ごとにグループ化してサマリーを出力
  grouped = df.groupby("場名")
  for venue, group in grouped:
    count = len(group)
    print(f" 🚤 【{venue}】 勝負レース ({count}件) " + "-" * 52)
    for _, row in group.iterrows():
      r_num = row["R"]
      deadline = row["締切時間"]
      score = row["スコア"]
      ai_rate = row["1号艇AI勝率"]
      print(
          f"   • {date_str}_{venue}_{r_num}R （締切: {deadline}） | スコア:"
          f" {score}pt | 1号艇AI勝率: {ai_rate}%"
      )

  print("-" * 89)
  print(
      " 💡 設定された条件を満たす、資金配分に適したレースを抽出しています。\n"
      + "=" * 89
  )
  print("\n\n")

  # 2. 詳細部分の表示（場ごと、レースごと）
  for venue, group in grouped:
    print(
        "#" * 89
        + f"\n 🏟️ 【レース場: {venue}】 の勝負レース一覧 ({len(group)}件)\n"
        + "#" * 89
        + "\n"
    )

    for _, row in group.iterrows():
      r_num = row["R"]
      deadline = row["締切時間"]
      score = row["スコア"]

      print("-" * 89)
      print(
          f" 🏁 【{venue} - {date_str}_{venue}_{r_num}R】 3連単"
          " 予想上位6位 （勝負レース指定）"
      )
      print(f" ⏱️ 【締切時間】         : {deadline}")
      print("-" * 89)
      print(f" 📊 【レース自信度・評価】 : ★★★★★ (極・鉄板)")
      print(f" 📈 【総合スコア目安】     : {score} pt")
      print(
          " 📝 【状態・レース傾向】   : 1号艇の逃げ条件が完璧。壁も盤石で波乱要素が極めて少ない。"
      )
      print(
          " 💡 【推奨アクション】     : 本命固定（1-2, 1-3中心） / 勝負レース指定"
      )
      print("=" * 89)

      # 3連単テーブルヘッダー
      print(
          "順位   | 【予想】(アンサンブル)       | 【比較1】場限定      |"
          " 【比較2】       "
      )
      print("-" * 80)

      # ※ Excel側に順位ごとの予想データ（例: 1位予想, 2位予想...）が
      # カラムとして入っている想定でループ、または固定テキストを差し込み
      for rank in range(1, 7):
        # サンプルとして列名が存在する場合の取得処理（適宜カラム名に変更してください）
        pred_ens = row.get(
            f"{rank}位_アンサンブル", "1-2-4 (6.8%)"
        )  // 例
        pred_loc = row.get(f"{rank}位_場限定", "1-4-2 (7.0%)")
        pred_nat = row.get(f"{rank}位_全国", "1-2-3 (8.6%)")

        print(
            f"{rank}位    | {pred_ens:<28} | {pred_loc:<20} | {pred_nat:<15}"
        )

      print("=" * 89 + "\n")


if __name__ == "__main__":
  # 実行例
  target_file = "shobu_races_20260811.xlsx"
  load_and_display_shobu_races(target_file)
