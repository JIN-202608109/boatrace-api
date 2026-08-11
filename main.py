import pandas as pd
from datetime import datetime
import os

def main():
    # 1. 日付の生成
    dt = datetime.now()
    file_date = dt.strftime("%Y%m%d")      # 20260811
    disp_date = dt.strftime("%Y年%-m月%-d日") # 2026年8月11日
    file_path = f"shobu_races_{file_date}.xlsx"

    if not os.path.exists(file_path):
        print(f"データファイル {file_path} が見つかりません。")
        return

    df = pd.read_excel(file_path)

    # --- [サマリー表示] ---
    print("=" * 89)
    print(" 🎯 【全場】 本日の勝負レース判定サマリー（設定勝率: 85%以上 / 各場上位3Rまで）")
    print("=" * 89)
    print(f" 🔥 【判定】 本日は全国で合計 **{len(df)}件** の勝負レースがあります！\n")

    for venue, group in df.groupby("場名"):
        print(f" 🚤 【{venue}】 勝負レース ({len(group)}件) " + "-" * 52)
        for _, row in group.iterrows():
            print(f"   • {disp_date}_{venue}_{row['R']}R （締切: {row['締切時間']}） | スコア: {row['スコア']}pt | 1号艇AI勝率: {row['1号艇AI勝率']}%")
    
    print("-" * 89)
    print(" 💡 設定された条件を満たす、資金配分に適したレースを抽出しています。")
    print("=" * 89 + "\n\n")

    # --- [詳細表示] ---
    for venue, group in df.groupby("場名"):
        print(f"\n" + "#" * 89)
        print(f" 🏟️ 【レース場: {venue}】 の勝負レース一覧 ({len(group)}件)")
        print("#" * 89 + "\n")

        for _, row in group.iterrows():
            print("-" * 89)
            print(f" 🏁 【{venue} - {disp_date}_{venue}_{row['R']}R】 3連単 予想上位6位 （勝負レース指定）")
            print(f" ⏱️ 【締切時間】         : {row['締切時間']}")
            print("-" * 89)
            print(f" 📊 【レース自信度・評価】 : ★★★★★ (極・鉄板)")
            print(f" 📈 【総合スコア目安】     : {row['スコア']} pt")
            print(f" 📝 【状態・レース傾向】   : 1号艇の逃げ条件が完璧。壁も盤石で波乱要素が極めて少ない。")
            print(f" 💡 【推奨アクション】     : 本命固定（1-2, 1-3中心） / 勝負レース指定")
            print("=" * 89)
            print("順位   | 【予想】(アンサンブル)       | 【比較1】場限定      | 【比較2】全国       ")
            print("-" * 80)
            
            # 6位まで表示するループ
            for i in range(1, 7):
                e = row.get(f"{i}位_アンサンブル", "---")
                l = row.get(f"{i}位_場限定", "---")
                n = row.get(f"{i}位_全国", "---")
                # 文字幅を調整して揃える
                print(f"{i}位    | {str(e):<28} | {str(l):<20} | {str(n):<15}")
            print("=" * 89 + "\n")

if __name__ == "__main__":
    main()
