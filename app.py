from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

def load_beans():
    return pd.read_csv("beans.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    beans = load_beans()
    best_bean = None
    chart_data = None
    results = []  # カード表示用リストの初期化

    # デフォルトスライダー値
    acidity    = float(request.form.get("acidity",    5.0))
    bitterness = float(request.form.get("bitterness", 5.0))
    body       = float(request.form.get("body",       5.0))
    flavor     = float(request.form.get("flavor",     5.0))
    aftertaste = float(request.form.get("aftertaste", 5.0))

    if request.method == "POST":
        # スコア差を計算
        beans["スコア差"] = (
            (beans["酸味"] - acidity)**2 +
            (beans["苦味"] - bitterness)**2 +
            (beans["コク"]   - body)**2 +
            (beans["風味"]  - flavor)**2 +
            (beans["後味"]  - aftertaste)**2
        )**0.5

        # 小数点第2位までに丸める
        beans["スコア差"] = beans["スコア差"].round(2)

        # スコア順にソート
        beans_scored = beans.sort_values("スコア差")
        # ベストの豆取得
        best = beans_scored.iloc[0]
        best_bean = best.to_dict()

        # レーダーチャート用データ準備
        chart_data = {
            "categories": ["酸味","苦味","コク","風味","後味"],
            "values": [
                best_bean["酸味"], best_bean["苦味"], best_bean["コク"],
                best_bean["風味"], best_bean["後味"]
            ]
        }

        # 全ての豆を抽出
        results = beans_scored.to_dict(orient="records")

    return render_template(
        "index.html",
        best_bean=best_bean,
        chart_data=chart_data,
        beans=beans.to_dict(orient="records"),
        results=results,
        slider_values={
            "acidity": acidity,
            "bitterness": bitterness,
            "body": body,
            "flavor": flavor,
            "aftertaste": aftertaste
        }
    )

if __name__ == "__main__":
    app.run(debug=True)
