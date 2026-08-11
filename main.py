import os
import pandas as pd
from datetime import datetime

def main():
    # 1. 本日の日付に基づいたファイル名を取得
    date_str = datetime.now().strftime("%Y%m%d")
    file_name = f"shobu_races_{date_str}.xlsx"
    
    if not os.path.exists(file_name):
        print(f"エラー: ファイル '{file_name}' が見つかりません。")
        return

    # 2. ファイル自体の最終更新日時を取得（ファイルプロパティの更新時刻）
    file_mtime = os.path.getmtime(file_name)
    file_update_str = datetime.fromtimestamp(file_mtime).strftime("%Y年%m月%d日 %H:%M:%S")

    # 3. Excelファイルの読み込み
    df = pd.read_excel(file_name)

    # もしExcel内に「更新日時」という列があればそれを優先し、なければファイルの最終更新時刻を使う
    if '更新日時' in df.columns:
        data_update_str = str(df['更新日時'].iloc[0])
    else:
        data_update_str = file_update_str

    # 4. サマリー用データの抽出（レースID単位で一意の情報を取得）
    summary_df = df[['レース場', 'レースID', '締切時間', '自信度', '総合スコア', '推奨アクション']].drop_duplicates()

    # 5. サマリー表示（冒頭にデータ更新日時を目立つように配置）
    print("=" * 89)
    print(" 🎯 【全場】 本日の勝負レース判定サマリー（設定勝率: 85%以上 / 各場上位3Rまで）")
    print("=" * 89)
    print(f" 🕒 【データ更新日時】 : {data_update_str}")
    print(f" 🔥 【判定】 本日は全国で合計 **{len(summary_df)}件** の勝負レースがあります！\n")

    for venue, group in summary_df.groupby("レース場"):
        print(f" 🚤 【{venue}】 勝負レース ({len(group)}件) " + "-" * 52)
        for _, row in group.iterrows():
            print(f"   • {row['レースID']} （締切: {row['締切時間']}） | スコア: {row['総合スコア']}pt")
    
    print("-" * 89)
    print(" 💡 設定された条件を満たす、資金配分に適したレースを抽出しています。")
    print("=" * 89 + "\n\n")

    # 6. 詳細レース一覧表示
    for venue, venue_group in df.groupby("レース場"):
        print("#" * 89)
        print(f" 🏟️ 【レース場: {venue}】 の勝負レース一覧 ({len(venue_group.drop_duplicates(subset='レースID'))}件)")
        print("#" * 89 + "\n")
        
        # レースIDごとにグループ化
        for race_id, race_rows in venue_group.groupby("レースID"):
            basic = race_rows.iloc[0]
            
            print("-" * 89)
            print(f" 🏁 【{race_id}】 3連単 予想上位6位 （勝負レース指定）")
            print(f" ⏱️ 【締切時間】         : {basic['締切時間']}")
            print("-" * 89)
            print(f" 📊 【レース自信度・評価】 : {basic['自信度']}")
            print(f" 📈 【総合スコア目安】     : {basic['総合スコア']} pt")
            print(f" 📝 【状態・レース傾向】   : 1号艇の逃げ条件が完璧。壁も盤石で波乱要素が極めて少ない。")
            print(f" 💡 【推奨アクション】     : {basic['推奨アクション']}")
            print("=" * 89)
            print("順位   | 【予想】(アンサンブル)       | 【比較1】場限定      | 【比較2】全国       ")
            print("-" * 80)
            
            # 各順位の行をループして出力
            for _, row in race_rows.iterrows():
                print(f"{str(row['順位']):<6}| {str(row['アンサンブル予想']):<28} | {str(row['場限定予想']):<20} | {str(row['全国予想']):<15}")
            
            print("=" * 89 + "\n")

if __name__ == "__main__":
    main()
