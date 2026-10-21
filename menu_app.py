"""献立スライド画面。
準備: python -m pip install nicegui
起動: python menu_app_recipes.py
ブラウザで http://localhost:8081 を開く。
画像未登録時は仮のイラストを表示します。栄養値・価格は未登録です。
画像とURLはRECIPESで管理します。未登録のままでも起動できます。
筋トレおかず候補の資料に載っている11品だけを登録しています。
例: imageを images/chicken_keema.jpg にすると、その画像を使用します。
"""
import base64
from pathlib import Path
from nicegui import ui
# ===== 編集する場所1：料理ごとの画像とレシピURL =====
# image: このファイルと同じフォルダーにある images 内の画像を指定。
# url: その料理の実際のレシピページURLを指定。未登録は空文字のまま。
# 外部サイトの画像は利用許可のあるものを使ってください。
BASE_DIR = Path(__file__).resolve().parent

RECIPES = {'protein_rice_bowl': {'name': 'たんぱくぱくドン',
                       'image': 'tanpakudon.png',
                       'url': 'https://park.ajinomoto.co.jp/recipe/card/802622/',
                       'source': '味の素パーク公式'},
 'chicken_dressing': {'name': 'キャベツと鶏むね肉のドレッシング炒め',
                      'image': 'torimune.png',
                      'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10005358/',
                      'source': 'キユーピー公式'},
 'chicken_keema': {'name': '鶏ひき肉のキーマカレー',
                   'image': 'ki-makare-.png',
                   'url': 'https://www.sbfoods.co.jp/recipe/detail/10317.html',
                   'source': 'エスビー食品公式'},
 'chicken_garlic_mayo': {'name': 'キャベツと鶏もも肉のガーリックマヨネーズ炒め',
                         'image': None,
                         'url': 'https://www.kewpie.co.jp/recipes/recipe/QP00012673/',
                         'source': 'キユーピー公式'},
 'mackerel_sesame': {'name': 'ドレッシングで！さばの深煎りごま煮',
                     'image': 'saba.png',
                     'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10004933/',
                     'source': 'キユーピー公式'},
 'pork_pepper_onion': {'name': 'ピーマン・玉ねぎ・豚こま肉の炒め物',
                       'image': None,
                       'url': 'https://park.ajinomoto.co.jp/recipe/card/805819/',
                       'source': '味の素パーク公式'},
 'chicken_broccoli_mayo': {'name': '鶏むね肉とブロッコリーのマヨネーズ炒め',
                           'image': None,
                           'url': 'https://park.ajinomoto.co.jp/recipe/card/803248/',
                           'source': '味の素パーク公式'},
 'cabbage_nori_salad': {'name': '春キャベツと焼きのりのちぎりサラダ',
                        'image': None,
                        'url': 'https://park.ajinomoto.co.jp/recipe/card/803142/',
                        'source': '味の素パーク公式'},
 'konjac_steak': {'name': '丸ごと！こんにゃくステーキ',
                  'image': None,
                  'url': 'https://park.ajinomoto.co.jp/recipe/card/803241/',
                  'source': '味の素パーク公式'},
 'mock_eel_bowl': {'name': 'なんちゃってうなぎの蒲焼丼',
                   'image': None,
                   'url': 'https://park.ajinomoto.co.jp/recipe/card/708973/',
                   'source': '味の素パーク公式'},
 'chicken_vinegar': {'name': '鶏胸肉のうま酢煮',
                     'image': None,
                     'url': 'https://park.ajinomoto.co.jp/recipe/card/708962/',
                     'source': '味の素パーク公式'}}

# ===== 編集する場所2：献立の組み合わせ =====
# recipe_ids: 上のRECIPESのIDを並べます。
# cover_recipe_id: スライドの表紙に使う料理のID。
# image: 献立全体の写真を指定すると、表紙の料理画像より優先します。
MENUS = [{'id': 5,
  'name': 'たんぱくぱくドン',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['protein_rice_bowl'],
  'cover_recipe_id': 'protein_rice_bowl'},
 {'id': 6,
  'name': 'キャベツと鶏むね肉のドレッシング炒め',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_dressing'],
  'cover_recipe_id': 'chicken_dressing'},
 {'id': 7,
  'name': '鶏ひき肉のキーマカレー',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_keema'],
  'cover_recipe_id': 'chicken_keema'},
 {'id': 8,
  'name': 'キャベツと鶏もも肉のガーリックマヨネーズ炒め',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_garlic_mayo'],
  'cover_recipe_id': 'chicken_garlic_mayo'},
 {'id': 9,
  'name': 'ドレッシングで！さばの深煎りごま煮',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['mackerel_sesame'],
  'cover_recipe_id': 'mackerel_sesame'},
 {'id': 10,
  'name': 'ピーマン・玉ねぎ・豚こま肉の炒め物',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['pork_pepper_onion'],
  'cover_recipe_id': 'pork_pepper_onion'},
 {'id': 11,
  'name': '鶏むね肉とブロッコリーのマヨネーズ炒め',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['chicken_broccoli_mayo'],
  'cover_recipe_id': 'chicken_broccoli_mayo'},
 {'id': 12,
  'name': '春キャベツと焼きのりのちぎりサラダ',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['cabbage_nori_salad'],
  'cover_recipe_id': 'cabbage_nori_salad'},
 {'id': 13,
  'name': '丸ごと！こんにゃくステーキ',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['konjac_steak'],
  'cover_recipe_id': 'konjac_steak'},
 {'id': 14,
  'name': 'なんちゃってうなぎの蒲焼丼',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['mock_eel_bowl'],
  'cover_recipe_id': 'mock_eel_bowl'},
 {'id': 15,
  'name': '鶏胸肉のうま酢煮',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': None,
  'protein': None,
  'carbs': None,
  'fat': None,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['chicken_vinegar'],
  'cover_recipe_id': 'chicken_vinegar'}]


def nutrition_summary(menu):
    """資料にない栄養値を推測しない。"""
    if menu.get("kcal") is None:
        return "栄養値は未登録"
    return (f"{menu['kcal']} kcal / タンパク質 {menu['protein']} g / "
            f"脂質 {menu['fat']} g")


def cost_summary(menu):
    return f"目安: {menu['cost_est']}" if menu.get("cost_est") else "価格は未登録"


def image_source(image):
    """画像をプログラムの場所から探す。未登録・ファイル不在ならNone。"""
    if not image:
        return None
    path = Path(image)
    if not path.is_absolute():
        path = BASE_DIR / path
    return str(path) if path.is_file() else None


def menu_recipes(menu):
    """献立が参照する料理の情報を取得する。"""
    return [RECIPES[recipe_id] for recipe_id in menu['recipe_ids']]


# IDの入力ミスを、起動時に分かりやすく知らせる。
for menu in MENUS:
    for recipe_id in menu['recipe_ids']:
        if recipe_id not in RECIPES:
            raise ValueError(f"{menu['name']}: 未登録の料理ID {recipe_id}")
    if menu['cover_recipe_id'] not in menu['recipe_ids']:
        raise ValueError(f"{menu['name']}: 表紙の料理IDをrecipe_idsにも入れてください")

def meal_image(menu):
    """写真が未登録の場合は、仮の献立イラストを表示します。"""
    source = image_source(menu.get("image"))
    if not source:
        source = image_source(RECIPES[menu["cover_recipe_id"]].get("image"))
    if source:
        return source
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
    autoplay_state = {"enabled": True}
    ui.colors(primary="#39705a")
    ui.add_css('''
        body {
            background: #f6f7f3;
            color: #263c32;
            font-family: sans-serif;
        }
        .page {
            position: relative;
            z-index: 1;
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
        /* 炎は背面に配置し、クリックやスクロールを妨げない。 */
        .fire-background {
            position: fixed;
            inset: 0;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
            opacity: 0;
            transition: opacity .7s ease;
            background: linear-gradient(0deg, #ff863b66, #fff1dd55 55%, transparent);
        }
        .fire-background.is-burning { opacity: 1; }
        .flame {
            position: absolute;
            bottom: -110px;
            left: var(--x);
            width: clamp(75px, 12vw, 180px);
            height: var(--height);
            border-radius: 80% 20% 60% 40% / 65% 35% 65% 35%;
            background: radial-gradient(ellipse at 50% 90%,
                #fff8ad 0%, #ffc33c 28%, #ff742a 55%, #ef431c99 72%, transparent 78%);
            filter: blur(5px);
            transform-origin: center bottom;
            animation: flame-sway var(--duration) ease-in-out infinite alternate;
            animation-delay: var(--delay);
            animation-play-state: paused;
        }
        .is-burning .flame { animation-play-state: running; }
        @keyframes flame-sway {
            0% { transform: translateX(-12px) rotate(-9deg) scaleY(.8); }
            50% { transform: translateX(7px) rotate(4deg) scaleY(1.08); }
            100% { transform: translateX(15px) rotate(11deg) scaleY(.92); }
        }
        @media (prefers-reduced-motion: reduce) {
            .fire-background { transition: none; }
            .fire-background .flame { animation: none; }
        }
        @media (max-width: 900px) {
            .layout {
                grid-template-columns: minmax(0, 1fr);
            }
        }
    ''')
    # 画像ファイル不要のCSSアニメーション。ページごとに独立して管理。
    with ui.element('div').classes('fire-background').props('aria-hidden=true') as fire_background:
        for i in range(14):
            ui.element('div').classes('flame').style(
                f'--x: {i * 8 - 6}%; --height: {240 + (i % 4) * 55}px; '
                f'--duration: {1.8 + (i % 5) * .3}s; --delay: {-i * .37}s;'
            )

    def set_fire(enabled):
        if enabled:
            fire_background.classes(add='is-burning')
        else:
            fire_background.classes(remove='is-burning')

    def select_menu(menu):
        """献立を選び、決定した献立のパネルを更新します。"""
        selected["menu"] = menu
        set_fire(menu['category'] == 'muscle')
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
                    nutrition_summary(menu) + " ・ " + cost_summary(menu)
                ).classes(
                    "text-sm font-bold text-amber-800"
                )
                ui.separator()
                # 料理ごとに、その料理の画像とリンクを表示します。
                ui.label("料理ごとのレシピ").classes("text-base font-bold")
                for recipe in menu_recipes(menu):
                    with ui.card().classes("w-full shadow-none border rounded-xl p-3 gap-2"):
                        ui.label(recipe["name"]).classes("font-bold")
                        source = image_source(recipe.get("image"))
                        url = recipe.get("url", "").strip()
                        valid_url = url.startswith(("https://", "http://"))
                        if source:
                            if valid_url:
                                with ui.link(target=url, new_tab=True).classes("w-full"):
                                    ui.image(source).classes("w-full rounded-lg").props("height=140px fit=cover")
                            else:
                                ui.image(source).classes("w-full rounded-lg").props("height=140px fit=cover")
                        else:
                            ui.label("画像は未登録、またはファイルが見つかりません").classes("muted text-xs")
                        if valid_url:
                            ui.link(
                                text=f"{recipe.get('source', '外部サイト')}でレシピを見る",
                                target=url,
                                new_tab=True,
                            ).classes("recipe-link")
                        else:
                            ui.label("レシピURLは未登録です" if not url else "URLはhttps://から入力してください").classes("muted text-xs")
                ui.separator()
                for label, key, target, color in [
                    ("タンパク質", "protein", 40, "#39705a"),
                    ("炭水化物", "carbs", 80, "#d6ab61"),
                    ("脂質", "fat", 20, "#a789aa"),
                ]:
                    amount = menu.get(key)
                    if amount is None:
                        with ui.row().classes("w-full justify-between text-xs"):
                            ui.label(label)
                            ui.label("未登録").classes("muted")
                        continue
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
                    "栄養値・価格は未登録です。バーの基準は表示用のサンプルです。"
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
            set_fire(category == 'muscle')
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
                "💪 筋トレ向け",
                on_click=lambda: set_filter("muscle"),
            ).props(
                "unelevated" if cat == "muscle" else "outline"
            ).classes(
                "rounded-2xl text-lg px-8 py-3 font-bold shadow-sm"
            )
            ui.button(
                "👛 節約向け",
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
                def set_autoplay(event):
                    autoplay_state["enabled"] = event.value
                    if event.value:
                        carousel.props("autoplay")  # 標準の間隔は5秒
                    else:
                        carousel.props(remove="autoplay")

                if autoplay_state["enabled"]:
                    carousel.props("autoplay")  # 標準の間隔は5秒

                ui.switch(
                    "5秒ごとに自動切り替え",
                    value=autoplay_state["enabled"],
                    on_change=set_autoplay,
                )
                ui.label(
                    "左右の矢印やスワイプでも切り替えられます。じっくり見るときは自動切り替えをOFFにしてください。"
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
                                cost_summary(menu)
                            ).classes(
                                "text-xs font-bold text-amber-900 "
                                "bg-amber-100 px-3 py-1 rounded-full"
                            )
                        ui.label(
                            menu["name"]
                        ).classes("text-2xl font-bold")
                        with ui.row().classes("gap-1.5"):
                            for recipe in menu_recipes(menu):
                                ui.label(recipe["name"]).classes(
                                    "bg-gray-100 rounded-lg "
                                    "px-2.5 py-1 text-xs text-gray-700"
                                )
                        ui.label(
                            nutrition_summary(menu)
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
