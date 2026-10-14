"""献立スライド画面。

準備: python -m pip install nicegui
起動: python menu_app.py
ブラウザで http://localhost:8081 を開く。

画像・栄養値・価格は表示用のサンプルです。
"""

import base64
from nicegui import ui


# 献立の情報
# linksには、献立ごとのレシピリンクを1〜2個登録します。
# 現在のURLはレシピ一覧ページです。
MENUS = [
    {
        "id": 1,
        "name": "鶏むね肉の彩り定食",
        "tag": "高タンパク・低脂質",
        "category": "muscle",
        "foods": [
            "ご飯",
            "鶏むね肉のソテー",
            "ブロッコリー",
            "みそ汁",
        ],
        "kcal": 520,
        "protein": 42,
        "carbs": 65,
        "fat": 8,
        "cost_est": "約250円",
        "color": "#d4a06a",
        "background": "#f0e8dc",
        "image": None,
        "links": [
            {
                "title": "エスビー食品で主菜を探す",
                "url": "https://www.sbfoods.co.jp/recipe/",
            },
            {
                "title": "キユーピーで副菜を探す",
                "url": "https://www.kewpie.co.jp/recipes/",
            },
        ],
    },
    {
        "id": 2,
        "name": "焼き鮭と豆腐の定食",
        "tag": "バランス良好・高タンパク",
        "category": "muscle",
        "foods": [
            "ご飯",
            "焼き鮭",
            "冷ややっこ",
            "小松菜のおひたし",
        ],
        "kcal": 480,
        "protein": 35,
        "carbs": 60,
        "fat": 10,
        "cost_est": "約320円",
        "color": "#ed987e",
        "background": "#e4ece8",
        "image": None,
        "links": [
            {
                "title": "ミツカンでレシピを探す",
                "url": "https://www.mizkan.co.jp/ouchirecipe/",
            },
            {
                "title": "キユーピーで副菜を探す",
                "url": "https://www.kewpie.co.jp/recipes/",
            },
        ],
    },
    {
        "id": 3,
        "name": "モヤシと豆腐の節約炒め定食",
        "tag": "コスパ抜群・ヘルシー",
        "category": "saving",
        "foods": [
            "ご飯",
            "豆腐ともやしの卵炒め",
            "きゅうりの浅漬け",
            "わかめスープ",
        ],
        "kcal": 450,
        "protein": 22,
        "carbs": 68,
        "fat": 12,
        "cost_est": "約130円",
        "color": "#9c674b",
        "background": "#eee5de",
        "image": None,
        "links": [
            {
                "title": "ミツカンでレシピを探す",
                "url": "https://www.mizkan.co.jp/ouchirecipe/",
            },
        ],
    },
    {
        "id": 4,
        "name": "豆と鶏そぼろの節約丼定食",
        "tag": "安くて満足感たっぷり",
        "category": "saving",
        "foods": [
            "鶏そぼろと豆のどんぶり",
            "キャベツの塩昆布和え",
            "みそ汁",
        ],
        "kcal": 510,
        "protein": 28,
        "carbs": 72,
        "fat": 11,
        "cost_est": "約160円",
        "color": "#8a9a86",
        "background": "#e8ece6",
        "image": None,
        "links": [
            {
                "title": "エスビー食品で主菜を探す",
                "url": "https://www.sbfoods.co.jp/recipe/",
            },
            {
                "title": "キユーピーで副菜を探す",
                "url": "https://www.kewpie.co.jp/recipes/",
            },
        ],
    },
]


def meal_image(menu):
    """写真が未登録の場合は、仮の献立イラストを表示します。"""

    if menu["image"]:
        return menu["image"]

    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg"
         width="900" height="600" viewBox="0 0 900 600">

      <rect width="900" height="600"
            fill="{menu['background']}"/>

      <rect x="100" y="50" width="700" height="500"
            rx="35" fill="#b18b66"/>

      <rect x="115" y="65" width="670" height="470"
            rx="28" fill="#c9a57e"/>

      <ellipse cx="450" cy="290" rx="240" ry="160"
               fill="#000" opacity=".09"/>

      <ellipse cx="440" cy="275" rx="240" ry="160"
               fill="#fbfaf5"/>

      <ellipse cx="440" cy="275" rx="210" ry="135"
               fill="#f1efe7"/>

      <g transform="rotate(-10 430 260)">
        <rect x="290" y="190" width="260" height="130"
              rx="45" fill="{menu['color']}"/>

        <path d="M330 205l-12 90
                 M380 200l-12 100
                 M430 200l-12 100
                 M480 205l-12 90"
              stroke="#78452e" stroke-width="7"
              opacity=".45"/>
      </g>

      <g fill="#638a46">
        <circle cx="570" cy="230" r="30"/>
        <circle cx="600" cy="265" r="32"/>
        <circle cx="560" cy="295" r="28"/>
      </g>

      <g fill="#d65f46">
        <circle cx="530" cy="325" r="18"/>
        <circle cx="575" cy="330" r="16"/>
      </g>

      <ellipse cx="220" cy="420" rx="125" ry="85"
               fill="#203b44"/>

      <ellipse cx="220" cy="405" rx="110" ry="68"
               fill="#f6f2df"/>

      <g fill="#fffdf0">
        <circle cx="175" cy="395" r="26"/>
        <circle cx="220" cy="380" r="32"/>
        <circle cx="260" cy="398" r="28"/>
        <circle cx="218" cy="418" r="34"/>
      </g>

      <ellipse cx="670" cy="425" rx="100" ry="72"
               fill="#653e31"/>

      <ellipse cx="670" cy="415" rx="85" ry="53"
               fill="#b78b52"/>

      <g fill="#e8d9af">
        <rect x="640" y="390" width="22" height="18" rx="4"/>
        <rect x="675" y="420" width="24" height="18" rx="4"/>
      </g>

      <g fill="#496a3e">
        <ellipse cx="695" cy="400" rx="12" ry="5"/>
        <ellipse cx="638" cy="432" rx="11" ry="5"/>
      </g>

      <path d="M780 120v310 M796 120v310"
            stroke="#654735" stroke-width="9"
            stroke-linecap="round"/>
    </svg>
    '''

    encoded = base64.b64encode(svg.encode()).decode()
    return "data:image/svg+xml;base64," + encoded


@ui.page("/")
def main_page():
    # 選んだ献立と、表示するカテゴリーを管理
    selected = {"menu": None}
    filter_state = {"category": "all"}

    ui.colors(primary="#39705a")

    ui.add_css('''
        body {
            background: #f6f7f3;
            color: #263c32;
            font-family: sans-serif;
        }

        .page {
            width: 100%;
            max-width: 1200px;
            margin: auto;
            padding: 28px 16px;
        }

        .layout {
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
            gap: 24px;
            width: 100%;
        }

        .panel {
            border: 1px solid #e1e7df;
            border-radius: 22px;
            box-shadow: none;
            padding: 24px;
            background: white;
        }

        .muted {
            color: #78877d;
        }

        .q-carousel {
            border-radius: 22px;
            background: #eef2eb;
        }

        .q-carousel__slide {
            padding: 0;
        }

        .recipe-link {
            display: block;
            width: 100%;
            padding: 14px 16px;
            background: #edf5ef;
            color: #28533f;
            border-radius: 12px;
            font-weight: bold;
            text-decoration: none;
            overflow-wrap: anywhere;
        }

        .recipe-link:hover {
            background: #dcecdf;
        }

        @media (max-width: 900px) {
            .layout {
                grid-template-columns: minmax(0, 1fr);
            }
        }
    ''')

    def select_menu(menu):
        """献立を選び、決定した献立のパネルを更新します。"""

        selected["menu"] = menu
        selection.refresh()
        ui.notify(
            f"{menu['name']}を決定しました！",
            type="positive",
        )

    @ui.refreshable
    def selection():
        """選んだ献立、レシピリンク、栄養素を表示します。"""

        menu = selected["menu"]

        with ui.column().classes("w-full gap-3"):
            ui.label("決定した献立").classes(
                "text-xs font-bold text-gray-400 tracking-wider"
            )

            if menu:
                ui.label(menu["name"]).classes(
                    "text-xl font-bold text-green-900"
                )

                ui.label(
                    f"{menu['kcal']} kcal ・ 目安: {menu['cost_est']}"
                ).classes(
                    "text-sm font-bold text-amber-800"
                )

                ui.separator()

                # 献立に登録されているリンクを最大2個表示
                links = menu.get("links", [])

                if links:
                    ui.label("レシピへのリンク").classes(
                        "text-base font-bold"
                    )

                    for link in links[:2]:
                        ui.link(
                            text=link["title"],
                            target=link["url"],
                            new_tab=True,
                        ).classes("recipe-link")

                else:
                    ui.label(
                        "レシピのリンクは未登録です"
                    ).classes("muted text-xs")

                ui.separator()

                for label, key, target, color in [
                    ("タンパク質", "protein", 40, "#39705a"),
                    ("炭水化物", "carbs", 80, "#d6ab61"),
                    ("脂質", "fat", 20, "#a789aa"),
                ]:
                    amount = menu[key]

                    with ui.row().classes(
                        "w-full justify-between text-xs"
                    ):
                        ui.label(label)

                        ui.label(
                            f"{amount} / {target} g"
                        ).classes("font-bold")

                    ui.linear_progress(
                        value=min(amount / target, 1),
                        color=color,
                        show_value=False,
                    ).props("rounded size=8px")

                ui.label(
                    "栄養値・価格・バーの基準はサンプルです。"
                ).classes("muted text-xs")

            else:
                ui.label("未選択").classes(
                    "text-lg font-bold text-gray-400"
                )

                ui.label(
                    "上の「この献立にする」ボタンを押すと、"
                    "ここにレシピリンクが表示されます。"
                ).classes("muted text-xs")

    @ui.refreshable
    def main_content():
        """カテゴリーに合う献立のスライドと詳細を表示します。"""

        cat = filter_state["category"]

        if cat == "all":
            filtered_menus = MENUS
        else:
            filtered_menus = [
                menu
                for menu in MENUS
                if menu["category"] == cat
            ]

        def set_filter(category):
            filter_state["category"] = category
            main_content.refresh()

        # 大きなカテゴリー切り替えボタン
        with ui.row().classes(
            "gap-4 mb-4 w-full flex-wrap"
        ):
            ui.button(
                "すべて",
                on_click=lambda: set_filter("all"),
            ).props(
                "unelevated" if cat == "all" else "outline"
            ).classes(
                "rounded-2xl text-lg px-8 py-3 font-bold shadow-sm"
            )

            ui.button(
                "💪 筋トレ向け（高タンパク）",
                on_click=lambda: set_filter("muscle"),
            ).props(
                "unelevated" if cat == "muscle" else "outline"
            ).classes(
                "rounded-2xl text-lg px-8 py-3 font-bold shadow-sm"
            )

            ui.button(
                "👛 節約向け（低コスト）",
                on_click=lambda: set_filter("saving"),
            ).props(
                "unelevated" if cat == "saving" else "outline"
            ).classes(
                "rounded-2xl text-lg px-8 py-3 font-bold shadow-sm"
            )

        if not filtered_menus:
            ui.label(
                "該当する献立がありません"
            ).classes("muted p-4")
            return

        with ui.element("div").classes("layout"):

            # 左側：献立画像のスライド
            with ui.column().classes("w-full gap-2"):
                with ui.carousel(
                    value="0",
                    animated=True,
                    arrows=True,
                    navigation=True,
                ).props(
                    "height=420px infinite swipeable "
                    "control-color=primary"
                ).classes("w-full shadow-sm") as carousel:

                    for i, menu in enumerate(filtered_menus):
                        with ui.carousel_slide(name=str(i)):
                            ui.image(
                                meal_image(menu)
                            ).classes(
                                "w-full h-full"
                            ).props(
                                "fit=cover no-spinner"
                            )

                ui.label(
                    "左右の矢印やスワイプで献立を切り替えられます。"
                ).classes("muted text-xs")

            # 右側：表示中の献立と、決定した献立
            with ui.column().classes("w-full gap-4"):

                @ui.refreshable
                def menu_detail():
                    idx = int(carousel.value or 0)

                    if not 0 <= idx < len(filtered_menus):
                        idx = 0

                    menu = filtered_menus[idx]

                    with ui.card().classes(
                        "panel w-full gap-3"
                    ):
                        with ui.row().classes(
                            "items-center justify-between w-full"
                        ):
                            ui.label(
                                menu["tag"]
                            ).classes(
                                "text-xs font-bold text-green-700 "
                                "bg-green-50 px-3 py-1 rounded-full"
                            )

                            ui.label(
                                f"目安: {menu['cost_est']}"
                            ).classes(
                                "text-xs font-bold text-amber-900 "
                                "bg-amber-100 px-3 py-1 rounded-full"
                            )

                        ui.label(
                            menu["name"]
                        ).classes("text-2xl font-bold")

                        with ui.row().classes("gap-1.5"):
                            for food in menu["foods"]:
                                ui.label(food).classes(
                                    "bg-gray-100 rounded-lg "
                                    "px-2.5 py-1 text-xs text-gray-700"
                                )

                        ui.label(
                            f"{menu['kcal']} kcal / "
                            f"タンパク質 {menu['protein']} g / "
                            f"脂質 {menu['fat']} g"
                        ).classes(
                            "muted text-xs font-bold mt-1"
                        )

                        ui.button(
                            "この献立にする",
                            icon="check",
                            on_click=lambda: select_menu(menu),
                        ).classes(
                            "w-full rounded-xl mt-2"
                        ).props(
                            "unelevated size=lg"
                        )

                menu_detail()
                carousel.on_value_change(menu_detail.refresh)

                with ui.card().classes("panel w-full"):
                    selection()

    # ヘッダー
    with ui.column().classes("page gap-4"):
        with ui.row().classes(
            "w-full items-center justify-between"
        ):
            with ui.column().classes("gap-0.5"):
                ui.label("MENU DAYS").classes(
                    "text-xs font-bold tracking-widest muted"
                )

                ui.label(
                    "今日、何を食べよう？"
                ).classes("text-2xl font-bold")

            ui.label(
                "目的別献立セレクター"
            ).classes("muted text-xs")

        main_content()


if __name__ == "__main__":
    ui.run(
        title="MENU DAYS | 献立とレシピリンク",
        host="127.0.0.1",
        port=8081,
        reload=False,
    )