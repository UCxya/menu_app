"""献立スライド画面。
準備: python -m pip install nicegui
起動: python menu_app_recipes.py
ブラウザで http://localhost:8081 を開く。
画像未登録時は仮のイラストを表示します。栄養値・価格・検索タグは添付資料の記載に基づきます。
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
                         'image': 'kyabetutorimomo.jpg',
                         'url': 'https://www.kewpie.co.jp/recipes/recipe/QP00012673/',
                         'source': 'キユーピー公式'},
 'mackerel_sesame': {'name': 'ドレッシングで！さばの深煎りごま煮',
                     'image': 'saba.png',
                     'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10004933/',
                     'source': 'キユーピー公式'},
 'pork_pepper_onion': {'name': 'ピーマン・玉ねぎ・豚こま肉の炒め物',
                       'image': 'pi-man.jpg',
                       'url': 'https://park.ajinomoto.co.jp/recipe/card/805819/',
                       'source': '味の素パーク公式'},
 'chicken_broccoli_mayo': {'name': '鶏むね肉とブロッコリーのマヨネーズ炒め',
                           'image': 'brokkori-.jpg',
                           'url': 'https://park.ajinomoto.co.jp/recipe/card/803248/',
                           'source': '味の素パーク公式'},
 'cabbage_nori_salad': {'name': '春キャベツと焼きのりのちぎりサラダ',
                        'image': 'retasu.jpg',
                        'url': 'https://park.ajinomoto.co.jp/recipe/card/803142/',
                        'source': '味の素パーク公式'},
 'konjac_steak': {'name': '丸ごと！こんにゃくステーキ',
                  'image': 'konnyaku.jpg',
                  'url': 'https://park.ajinomoto.co.jp/recipe/card/803241/',
                  'source': '味の素パーク公式'},
 'mock_eel_bowl': {'name': 'なんちゃってうなぎの蒲焼丼',
                   'image': 'unagi.png',
                   'url': 'https://park.ajinomoto.co.jp/recipe/card/708973/',
                   'source': '味の素パーク公式'},
 'chicken_vinegar': {'name': '鶏胸肉のうま酢煮',
                     'image': 'umasu.png',
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
  'kcal': 564.0,
  'protein': 37.7,
  'carbs': None,
  'fat': 18.6,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['protein_rice_bowl'],
  'cover_recipe_id': 'protein_rice_bowl',
  'tags': [],
  'salt': 1.3,
  'salt_label': '塩分',
  'vegetables': 0.0},
 {'id': 6,
  'name': 'キャベツと鶏むね肉のドレッシング炒め',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': 297.0,
  'protein': 28.8,
  'carbs': 9.2,
  'fat': 15.8,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_dressing'],
  'cover_recipe_id': 'chicken_dressing',
  'tags': ['キャベツ', '鶏むね肉'],
  'salt': 0.9,
  'salt_label': '食塩相当量',
  'vegetables': 101.0},
 {'id': 7,
  'name': '鶏ひき肉のキーマカレー',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': 602.0,
  'protein': 21.8,
  'carbs': 97.4,
  'fat': 16.8,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_keema'],
  'cover_recipe_id': 'chicken_keema',
  'tags': ['ひき肉', '玉ねぎ'],
  'sodium': 883.0,
  'salt': 2.2,
  'salt_label': '食塩相当量'},
 {'id': 8,
  'name': 'キャベツと鶏もも肉のガーリックマヨネーズ炒め',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': 418.0,
  'protein': 23.6,
  'carbs': 9.7,
  'fat': 31.0,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_garlic_mayo'],
  'cover_recipe_id': 'chicken_garlic_mayo',
  'tags': ['キャベツ', '鶏もも肉'],
  'salt': 1.8,
  'salt_label': '食塩相当量',
  'vegetables': 120.0},
 {'id': 9,
  'name': 'ドレッシングで！さばの深煎りごま煮',
  'tag': '資料の筋トレおかず候補',
  'category': 'muscle',
  'kcal': 303.0,
  'protein': 17.5,
  'carbs': 5.3,
  'fat': 22.5,
  'cost_est': None,
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['mackerel_sesame'],
  'cover_recipe_id': 'mackerel_sesame',
  'tags': ['さば'],
  'salt': 1.0,
  'salt_label': '食塩相当量',
  'vegetables': 20.0},
 {'id': 10,
  'name': 'ピーマン・玉ねぎ・豚こま肉の炒め物',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 168.0,
  'protein': 11.8,
  'carbs': None,
  'fat': 11.4,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['pork_pepper_onion'],
  'cover_recipe_id': 'pork_pepper_onion',
  'tags': ['ピーマン', '玉ねぎ', '豚肉'],
  'salt': 1.3,
  'salt_label': '塩分',
  'vegetables': 69.0},
 {'id': 11,
  'name': '鶏むね肉とブロッコリーのマヨネーズ炒め',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 396.0,
  'protein': 36.0,
  'carbs': None,
  'fat': 24.1,
  'cost_est': '約173円（資料のAI推定）',
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['chicken_broccoli_mayo'],
  'cover_recipe_id': 'chicken_broccoli_mayo',
  'tags': ['鶏肉', 'ブロッコリー', '鶏むね肉'],
  'salt': 1.6,
  'salt_label': '塩分',
  'vegetables': 65.0},
 {'id': 12,
  'name': '春キャベツと焼きのりのちぎりサラダ',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 61.0,
  'protein': 1.6,
  'carbs': None,
  'fat': 4.5,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['cabbage_nori_salad'],
  'cover_recipe_id': 'cabbage_nori_salad',
  'tags': ['キャベツ'],
  'salt': 0.3,
  'salt_label': '塩分',
  'vegetables': 75.0},
 {'id': 13,
  'name': '丸ごと！こんにゃくステーキ',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 114.0,
  'protein': 1.9,
  'carbs': None,
  'fat': 8.3,
  'cost_est': '約155円（資料のAI推定）',
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['konjac_steak'],
  'cover_recipe_id': 'konjac_steak',
  'tags': ['こんにゃく'],
  'salt': 3.1,
  'salt_label': '塩分',
  'fat_unit_missing': True},
 {'id': 14,
  'name': 'なんちゃってうなぎの蒲焼丼',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 526.0,
  'protein': 16.0,
  'carbs': None,
  'fat': 4.4,
  'cost_est': '約173円（資料のAI推定）',
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['mock_eel_bowl'],
  'cover_recipe_id': 'mock_eel_bowl',
  'tags': ['ちくわ'],
  'salt': 4.7,
  'salt_label': '塩分'},
 {'id': 15,
  'name': '鶏胸肉のうま酢煮',
  'tag': '資料の節約おかず候補',
  'category': 'saving',
  'kcal': 408.0,
  'protein': 35.8,
  'carbs': None,
  'fat': 16.2,
  'cost_est': None,
  'color': '#8a9a86',
  'background': '#e8ece6',
  'image': None,
  'recipe_ids': ['chicken_vinegar'],
  'cover_recipe_id': 'chicken_vinegar',
  'tags': [],
  'salt': 2.7,
  'salt_label': '塩分',
  'vegetables': 120.0}]


# ユーザー提示の1食あたりの比較目安。個人別の必要量を判定するものではありません。
MEAL_TARGETS = {
    'male': {'label': '男性 18〜29歳', 'protein': 22, 'fat': 24, 'carbs': 140, 'salt': 2.5},
    'female': {'label': '女性 18〜29歳', 'protein': 17, 'fat': 18, 'carbs': 107, 'salt': 2.1},
}
NUTRITION_FIELDS = [
    ('タンパク質', 'protein', 'g'),
    ('脂質', 'fat', 'g'),
    ('炭水化物', 'carbs', 'g'),
    ('食塩相当量', 'salt', 'g'),
]


def nutrient_text(menu, key, unit):
    value = menu.get(key)
    if value is None:
        return '資料に記載なし'
    suffix = '（単位は資料に記載なし）' if menu.get(key + '_unit_missing') else f' {unit}'
    return f'{value:g}{suffix}'


def cost_summary(menu):
    return f"推定材料費: {menu['cost_est']}" if menu.get('cost_est') else '価格は資料に記載なし'


def nutrient_ratio(menu, key, reference):
    if menu.get(key) is None or menu.get(key + '_unit_missing'):
        return None
    return menu[key] / MEAL_TARGETS[reference][key]


def show_nutrition(menu, reference='male'):
    targets = MEAL_TARGETS[reference]
    with ui.column().classes('w-full gap-3'):
        ui.label('1食の目安に対する割合').classes('font-bold text-base')
        ui.label(targets['label'] + '・3食均等割りの比較目安').classes('muted text-xs')
        for label, key, unit in NUTRITION_FIELDS:
            target = targets[key]
            ratio = nutrient_ratio(menu, key, reference)
            is_salt = key == 'salt'
            with ui.column().classes('w-full gap-1'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label(label).classes('font-bold text-sm')
                    ui.label(nutrient_text(menu, key, unit)).classes('text-sm')
                if ratio is None:
                    ui.label('数値または単位が未記載のため計算できません').classes('muted text-xs')
                    continue
                if is_salt:
                    color = '#dc7040' if ratio >= 1 else '#5286a0'
                    status = f'比較上限の {ratio:.0%}'
                    limit = f'{target:g} g未満' if reference == 'male' else f'約{target:g} g（比較上限）'
                    remaining = '比較上限に達しています' if ratio >= 1 else f'比較上限まで {target - menu[key]:.1f} g'
                else:
                    color = '#39705a' if ratio <= 1 else '#b57b30'
                    status = f'目安の {ratio:.0%}'
                    limit = f'目安 {target:g} g'
                    remaining = f'目安まで {target - menu[key]:.1f} g' if ratio < 1 else '目安以上'
                with ui.row().classes('w-full justify-between text-xs'):
                    ui.label(status).classes('font-bold')
                    ui.label(limit).classes('muted')
                ui.linear_progress(value=min(max(ratio, 0), 1), color=color, show_value=False).props('rounded size=12px')
                ui.label(remaining).classes('muted text-xs')
        ui.label('食塩は少なめに抑える項目です。100%を目指す必要はありません。').classes('muted text-xs')
        ui.label('この料理の記載量を1食の目安と比較しています。ほかに食べるご飯や副菜は含みません。資料の分量はレシピで確認してください。').classes('muted text-xs')


def filter_menus(category='all', tags=None):
    required = set(tags or [])
    return [menu for menu in MENUS
            if (category == 'all' or menu['category'] == category)
            and required.issubset(menu.get('tags', []))]


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
    filter_state = {"category": "all", "tags": []}
    autoplay_state = {"enabled": True}
    target_state = {"reference": "male"}
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

    @ui.refreshable
    def nutrition_panel(menu):
        show_nutrition(menu, target_state['reference'])

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
                    cost_summary(menu)
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
                            ui.label("画像はイメージです").classes("muted text-xs")
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
                nutrition_panel(menu)
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
        filtered_menus = filter_menus(cat, filter_state['tags'])
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
        ui.label(f'{len(filtered_menus)}件の料理').classes('muted text-sm')
        if not filtered_menus:
            ui.label(
                "該当する献立がありません。タグを減らすか、カテゴリーを変更してください。"
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
                ui.label("画像はイメージです").classes("muted text-xs")
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
                        with ui.row().classes('gap-2 flex-wrap'):
                            for tag in menu.get('tags', []):
                                ui.label('#' + tag).classes('text-xs bg-green-50 text-green-800 rounded-full px-3 py-1')
                            if not menu.get('tags'):
                                ui.label('資料に検索タグの記載なし').classes('muted text-xs')
                        nutrition_panel(menu)
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
        def change_reference(event):
            target_state['reference'] = event.value
            nutrition_panel.refresh()

        ui.label('栄養ゲージの比較目安').classes('font-bold text-sm')
        ui.toggle(
            {'male': '男性 18〜29歳', 'female': '女性 18〜29歳'},
            value=target_state['reference'], on_change=change_reference,
        ).props('no-caps rounded unelevated')
        def search_by_tags(event):
            filter_state['tags'] = list(event.value or [])
            tag_select.run_method('hidePopup')
            main_content.refresh()

        tag_select = ui.select(
            options=sorted({tag for menu in MENUS for tag in menu.get('tags', [])}),
            label='食材タグで検索',
            value=[], multiple=True, with_input=True,
            on_change=search_by_tags,
        ).props('outlined use-chips clearable').classes('w-full')
        ui.label('食材名を入力して候補を選択。複数選ぶと、すべてのタグを含む料理に絞ります。×で解除できます。').classes('muted text-xs')
        main_content()
if __name__ == "__main__":
    ui.run(
        title="MENU DAYS | 献立とレシピリンク",
        host="127.0.0.1",
        port=8081,
        reload=False,
    )
