"""献立スライド画面。
準備: python -m pip install nicegui
起動: python menu_app_recipes.py
ブラウザで http://localhost:8081 を開く。
画像未登録時は仮のイラストを表示します。栄養値・価格・検索タグは添付資料の記載に基づきます。
画像とURLはRECIPESで管理します。未登録のままでも起動できます。
合計44品（ダイエット系12品を含む）を登録しています。
例: imageを images/chicken_keema.jpg にすると、その画像を使用します。
"""
import base64
import os
import json
import random
from datetime import date, datetime, timedelta, timezone
from uuid import uuid4
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
                     'source': '味の素パーク公式'},
 'karaage': {'name': '唐揚げ',
             'image': 'karaage.png',
             'url': 'https://www.sbfoods.co.jp/recipe/detail/10842.html',
             'source': 'エスビー食品公式'},
 'oyakodon': {'name': '親子丼',
              'image': 'oyakodon.png',
              'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10012245/',
              'source': 'キユーピー公式'},
 'chicken_soboro_bowl': {'name': '鳥そぼろ丼',
                         'image': 'sorobo.png',
                         'url': 'https://www.sbfoods.co.jp/recipe/detail/11515.html',
                         'source': 'エスビー食品公式'},
 'hamburg': {'name': 'ハンバーグ',
             'image': 'hanba-gu.png',
             'url': 'https://park.ajinomoto.co.jp/recipe/card/805126/',
             'source': '味の素パーク公式'},
 'gyoza': {'name': '餃子',
           'image': 'gyouza.png',
           'url': 'https://park.ajinomoto.co.jp/recipe/card/707175/',
           'source': '味の素パーク公式'},
 'pork_vegetable_stir_fry': {'name': '肉野菜炒め',
                             'image': 'yasaiitame.png',
                             'url': 'https://park.ajinomoto.co.jp/recipe/card/706807/',
                             'source': '味の素パーク公式'},
 'tonjiru': {'name': '豚汁',
             'image': 'tonjiru.png',
             'url': 'https://park.ajinomoto.co.jp/recipe/card/705648/',
             'source': '味の素パーク公式'},
 'salmon_meuniere': {'name': '鮭のムニエル',
                     'image': 'sakenomunieru.png',
                     'url': 'https://www.sbfoods.co.jp/recipe/detail/08212.html',
                     'source': 'エスビー食品公式'},
 'mackerel_miso': {'name': 'サバの味噌煮',
                   'image': 'sabamiso.png',
                   'url': 'https://park.ajinomoto.co.jp/recipe/card/705926/',
                   'source': '味の素パーク公式'},
 'bonito_bowl': {'name': 'カツオの漬け丼',
                 'image': 'katuo.png',
                 'url': 'https://www.sbfoods.co.jp/recipe/detail/09605.html',
                 'source': 'エスビー食品公式'},
 'stuffed_pepper': {'name': 'ピーマンの肉詰め',
                    'image': 'pi-man_niku.png',
                    'url': 'https://park.ajinomoto.co.jp/recipe/card/805553/',
                    'source': '味の素パーク公式'},
 'chinjao_rosu': {'name': '青椒肉絲',
                  'image': 'tinjaoro-su.png',
                  'url': 'https://park.ajinomoto.co.jp/recipe/card/706052/',
                  'source': '味の素パーク公式'},
 'napolitan': {'name': 'ナポリタン',
               'image': 'naporitan.png',
               'url': 'https://park.ajinomoto.co.jp/recipe/card/706281/',
               'source': '味の素パーク公式'},
 'broccoli_peperoncino': {'name': 'ペペロンチーノ',
                          'image': 'peperonti-no.png',
                          'url': 'https://park.ajinomoto.co.jp/recipe/card/705551/',
                          'source': '味の素パーク公式'},
 'yakisoba': {'name': '焼きそば',
              'image': 'yakisoba.png',
              'url': 'https://park.ajinomoto.co.jp/recipe/card/701165/',
              'source': '味の素パーク公式'},
 'kamatama_udon': {'name': 'うどん',
                   'image': 'udon.png',
                   'url': 'https://park.ajinomoto.co.jp/recipe/card/804273/',
                   'source': '味の素パーク公式'},
 'asian_chicken_noodles': {'name': '糖質0g麺のアジアンチキンヌードル風',
                           'image': '2_0men.png',
                           'url': 'https://park.ajinomoto.co.jp/recipe/card/801070/',
                           'source': '味の素パーク公式'},
 'vegetable_stick_marinade': {'name': '彩り野菜のスティックマリネ',
                              'image': '2_yasai.jpg',
                              'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10006655/',
                              'source': 'キユーピー公式'},
 'bean_sprout_namul': {'name': 'もやしナムル',
                       'image': '2_namuru.jpg',
                       'url': 'https://park.ajinomoto.co.jp/recipe/card/800324/',
                       'source': '味の素パーク公式'},
 'salmon_garlic_butter': {'name': 'さけのガーリックバター炒め',
                          'image': '2_sake2.jpg',
                          'url': 'https://park.ajinomoto.co.jp/recipe/card/708893/',
                          'source': '味の素パーク公式'},
 'microwave_niratama': {'name': 'レンジでにら玉風',
                        'image': '2_kakitama.png',
                        'url': 'https://www.kewpie.co.jp/recipes/recipe/QP00012599/',
                        'source': 'キユーピー公式'},
 'pork_warm_vegetables': {'name': '豚しゃぶ温野菜のオイスターソースかけ',
                          'image': '2_butaniku.png',
                          'url': 'https://park.ajinomoto.co.jp/recipe/card/800390/',
                          'source': '味の素パーク公式'},
 'mushroom_yaki_udon': {'name': 'きのこたっぷり焼うどん',
                        'image': '2_yakiudon.png',
                        'url': 'https://www.kewpie.co.jp/recipes/recipe/QP00013732/',
                        'source': 'キユーピー公式'},
 'sasami_ume_shiso': {'name': 'ささ身の梅じそレンジ焼き',
                      'image': '2_umesasami.png',
                      'url': 'https://park.ajinomoto.co.jp/recipe/card/702187/',
                      'source': '味の素パーク公式'},
 'broccoli_egg_sesame_udon': {'name': 'ブロッコリーとゆで卵の深ごまうどん',
                              'image': '2_udon.png',
                              'url': 'https://www.kewpie.co.jp/recipes/recipe/QP10011545/',
                              'source': 'キユーピー公式'},
 'tofu_egg_ankake': {'name': '豆腐のかきたまあんかけ',
                     'image': '2_kakitama.png',
                     'url': 'https://park.ajinomoto.co.jp/recipe/card/801153/',
                     'source': '味の素パーク公式'},
 'salmon_teriyaki': {'name': '鮭の照り焼き',
                     'image': '2_sake.png',
                     'url': 'https://park.ajinomoto.co.jp/recipe/card/706774/',
                     'source': '味の素パーク公式'},
 'salad_chicken': {'name': '極上のサラダチキン',
                   'image': '2_saradatikin.png',
                   'url': 'https://www.ajinomoto.co.jp/company/umami/lowsaltclub/recipes/86.html',
                   'source': '味の素公式'},
 'yaki_udon': {'name': '焼きうどん',
               'image': '2_yakiudon.png',
               'url': 'https://park.ajinomoto.co.jp/recipe/card/706043/',
               'source': '味の素パーク公式'},
 'curry_udon': {'name': 'カレーうどん',
                'image': '2_kare-.png',
                'url': 'https://park.ajinomoto.co.jp/recipe/card/700787/',
                'source': '味の素パーク公式'},
 'bonito_tatsuta': {'name': 'かつおの竜田焼き',
                    'image': '2_tatuta.png',
                    'url': 'https://park.ajinomoto.co.jp/recipe/card/709236/',
                    'source': '味の素パーク公式'},
 'bonito_spicy': {'name': 'かつおのスパイシー揚げ',
                  'image': '2_katuo.png',
                  'url': 'https://www.sbfoods.co.jp/recipe/detail/03922.html',
                  'source': 'エスビー食品公式'},
 'salmon_daikon': {'name': '鮭大根',
                   'image': '2_daikon.png',
                   'url': 'https://park.ajinomoto.co.jp/recipe/card/706461/',
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
  'tags': ['ブロッコリー', '鶏むね肉'],
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
  'tags': ['鶏むね肉'],
  'salt': 2.7,
  'salt_label': '塩分',
  'vegetables': 120.0},
 {'id': 16,
  'name': '唐揚げ',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 467,
  'protein': 25.9,
  'fat': 32.7,
  'carbs': 18.9,
  'salt': None,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約222円（資料のAI推定）',
  'tags': ['鶏もも肉'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['karaage'],
  'cover_recipe_id': 'karaage'},
 {'id': 17,
  'name': '親子丼',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 698,
  'protein': 26.8,
  'fat': 26.6,
  'carbs': 82.8,
  'salt': 2.8,
  'salt_label': '食塩相当量',
  'vegetables': 48,
  'cost_est': '約370円（資料のAI推定）',
  'tags': ['鶏もも肉', '卵', '玉ねぎ'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['oyakodon'],
  'cover_recipe_id': 'oyakodon'},
 {'id': 18,
  'name': '鳥そぼろ丼',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 550,
  'protein': 25.7,
  'fat': 15.2,
  'carbs': 81.3,
  'salt': 2.0,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約211円（資料のAI推定）',
  'tags': ['ひき肉', '卵'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chicken_soboro_bowl'],
  'cover_recipe_id': 'chicken_soboro_bowl'},
 {'id': 19,
  'name': 'ハンバーグ',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 434,
  'protein': 21.8,
  'fat': 28,
  'carbs': None,
  'salt': 0.8,
  'salt_label': '食塩相当量',
  'vegetables': 69,
  'cost_est': '約256円（資料のAI推定）',
  'tags': ['ひき肉', '玉ねぎ', '牛乳'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['hamburg'],
  'cover_recipe_id': 'hamburg'},
 {'id': 20,
  'name': '餃子',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 222,
  'protein': 10.2,
  'fat': 9.5,
  'carbs': None,
  'salt': 1.1,
  'salt_label': '食塩相当量',
  'vegetables': 52,
  'cost_est': '約109円（資料のAI推定）',
  'tags': ['ひき肉', 'キャベツ'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['gyoza'],
  'cover_recipe_id': 'gyoza'},
 {'id': 21,
  'name': '肉野菜炒め',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 220,
  'protein': 15.3,
  'fat': 10.4,
  'carbs': None,
  'salt': 2.7,
  'salt_label': '食塩相当量',
  'vegetables': 232,
  'cost_est': '約215円（資料のAI推定）',
  'tags': ['豚肉', 'キャベツ', '玉ねぎ', 'にんじん'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['pork_vegetable_stir_fry'],
  'cover_recipe_id': 'pork_vegetable_stir_fry'},
 {'id': 22,
  'name': '豚汁',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 158,
  'protein': 5.8,
  'fat': 9.6,
  'carbs': None,
  'salt': 1.6,
  'salt_label': '食塩相当量',
  'vegetables': 67,
  'cost_est': '約99円（資料のAI推定）',
  'tags': ['豚肉', 'じゃがいも', '大根', 'にんじん', 'こんにゃく'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['tonjiru'],
  'cover_recipe_id': 'tonjiru'},
 {'id': 23,
  'name': '鮭のムニエル',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 250,
  'protein': 22.9,
  'fat': 16.4,
  'carbs': 4.7,
  'salt': 1.1,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約368円（資料のAI推定）',
  'tags': ['鮭', 'バター'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['salmon_meuniere'],
  'cover_recipe_id': 'salmon_meuniere'},
 {'id': 24,
  'name': 'サバの味噌煮',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 291,
  'protein': 22.8,
  'fat': 17.5,
  'carbs': None,
  'salt': 2.3,
  'salt_label': '食塩相当量',
  'vegetables': 32,
  'cost_est': '約272円（資料のAI推定）',
  'tags': ['さば'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['mackerel_miso'],
  'cover_recipe_id': 'mackerel_miso'},
 {'id': 25,
  'name': 'カツオの漬け丼',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 580,
  'protein': 34.1,
  'fat': 12.9,
  'carbs': 85,
  'salt': 1.5,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約399円（資料のAI推定）',
  'tags': ['かつお', '卵'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['bonito_bowl'],
  'cover_recipe_id': 'bonito_bowl'},
 {'id': 26,
  'name': 'ピーマンの肉詰め',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 258,
  'protein': 14.5,
  'fat': 17.1,
  'carbs': None,
  'salt': 1,
  'salt_label': '食塩相当量',
  'vegetables': 45,
  'cost_est': '約190円（資料のAI推定）',
  'tags': ['ピーマン', 'ひき肉'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['stuffed_pepper'],
  'cover_recipe_id': 'stuffed_pepper'},
 {'id': 27,
  'name': '青椒肉絲',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 286,
  'protein': 19.6,
  'fat': 16.3,
  'carbs': None,
  'salt': 2.1,
  'salt_label': '食塩相当量',
  'vegetables': 114,
  'cost_est': '約379円（資料のAI推定）',
  'tags': ['ピーマン', '豚肉'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['chinjao_rosu'],
  'cover_recipe_id': 'chinjao_rosu'},
 {'id': 28,
  'name': 'ナポリタン',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 768,
  'protein': 23,
  'fat': 34.9,
  'carbs': None,
  'salt': 6.7,
  'salt_label': '食塩相当量',
  'vegetables': 86,
  'cost_est': '約230円（資料のAI推定）',
  'tags': ['パスタ', '玉ねぎ', 'ピーマン'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['napolitan'],
  'cover_recipe_id': 'napolitan'},
 {'id': 29,
  'name': 'ペペロンチーノ',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 581,
  'protein': 16.5,
  'fat': 31.6,
  'carbs': None,
  'salt': 3.7,
  'salt_label': '食塩相当量',
  'vegetables': 25,
  'cost_est': '約188円（資料のAI推定）',
  'tags': ['パスタ', 'ブロッコリー'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['broccoli_peperoncino'],
  'cover_recipe_id': 'broccoli_peperoncino'},
 {'id': 30,
  'name': '焼きそば',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 536,
  'protein': 16.1,
  'fat': 29.1,
  'carbs': None,
  'salt': 2.4,
  'salt_label': '食塩相当量',
  'vegetables': 161,
  'cost_est': None,
  'tags': ['焼きそば麺', '玉ねぎ', 'にんじん', 'キャベツ', '豚肉'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['yakisoba'],
  'cover_recipe_id': 'yakisoba'},
 {'id': 31,
  'name': 'うどん',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 292,
  'protein': 14.5,
  'fat': 6.1,
  'carbs': None,
  'salt': 6.2,
  'salt_label': '食塩相当量',
  'vegetables': 0,
  'cost_est': None,
  'tags': ['うどん', '卵'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['kamatama_udon'],
  'cover_recipe_id': 'kamatama_udon'},
 {'id': 32,
  'name': '糖質0g麺のアジアンチキンヌードル風',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 71,
  'protein': 10.8,
  'fat': 0.3,
  'carbs': None,
  'salt': 3,
  'salt_label': '食塩相当量',
  'vegetables': 23,
  'cost_est': '約263円（資料のAI推定）',
  'tags': [],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['asian_chicken_noodles'],
  'cover_recipe_id': 'asian_chicken_noodles'},
 {'id': 33,
  'name': '彩り野菜のスティックマリネ',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 20,
  'protein': 0.5,
  'fat': 0.6,
  'carbs': 3.4,
  'salt': 0.3,
  'salt_label': '食塩相当量',
  'vegetables': 58,
  'cost_est': '約58円（資料のAI推定）',
  'tags': ['きゅうり', 'にんじん', '大根'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['vegetable_stick_marinade'],
  'cover_recipe_id': 'vegetable_stick_marinade'},
 {'id': 34,
  'name': 'もやしナムル',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 36,
  'protein': 1.4,
  'fat': 2.8,
  'carbs': None,
  'salt': 0.4,
  'salt_label': '食塩相当量',
  'vegetables': 50,
  'cost_est': '約15円（資料のAI推定）',
  'tags': ['もやし'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['bean_sprout_namul'],
  'cover_recipe_id': 'bean_sprout_namul'},
 {'id': 35,
  'name': 'さけのガーリックバター炒め',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 185,
  'protein': 15.7,
  'fat': 10,
  'carbs': None,
  'salt': 1.2,
  'salt_label': '食塩相当量',
  'vegetables': 15,
  'cost_est': '約296円（資料のAI推定）',
  'tags': ['鮭'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['salmon_garlic_butter'],
  'cover_recipe_id': 'salmon_garlic_butter'},
 {'id': 36,
  'name': 'レンジでにら玉風',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 112,
  'protein': 6.1,
  'fat': 8.3,
  'carbs': 4.1,
  'salt': 1.1,
  'salt_label': '食塩相当量',
  'vegetables': 141,
  'cost_est': '約62円（資料のAI推定）',
  'tags': ['もやし', 'ニラ'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['microwave_niratama'],
  'cover_recipe_id': 'microwave_niratama'},
 {'id': 37,
  'name': '豚しゃぶ温野菜のオイスターソースかけ',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 126,
  'protein': 12.5,
  'fat': 5.5,
  'carbs': None,
  'salt': 0.6,
  'salt_label': '食塩相当量',
  'vegetables': 113,
  'cost_est': '約158円（資料のAI推定）',
  'tags': ['豚肉', 'キャベツ', 'にんじん', '玉ねぎ', 'もやし'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['pork_warm_vegetables'],
  'cover_recipe_id': 'pork_warm_vegetables'},
 {'id': 38,
  'name': 'きのこたっぷり焼うどん',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 314,
  'protein': 8.4,
  'fat': 6.8,
  'carbs': 55.9,
  'salt': 1.3,
  'salt_label': '食塩相当量',
  'vegetables': 60,
  'cost_est': '約145円（資料のAI推定）',
  'tags': ['うどん', 'きのこ'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['mushroom_yaki_udon'],
  'cover_recipe_id': 'mushroom_yaki_udon'},
 {'id': 39,
  'name': 'ささ身の梅じそレンジ焼き',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 86,
  'protein': 17,
  'fat': 0.6,
  'carbs': None,
  'salt': 0.8,
  'salt_label': '食塩相当量',
  'vegetables': 12,
  'cost_est': '約125円（資料のAI推定）',
  'tags': ['鶏のささみ'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['sasami_ume_shiso'],
  'cover_recipe_id': 'sasami_ume_shiso'},
 {'id': 40,
  'name': 'ブロッコリーとゆで卵の深ごまうどん',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 419,
  'protein': 16.4,
  'fat': 12.2,
  'carbs': 58.3,
  'salt': 3.3,
  'salt_label': '食塩相当量',
  'vegetables': 65,
  'cost_est': '約151円（資料のAI推定）',
  'tags': ['うどん', 'ブロッコリー', '卵'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['broccoli_egg_sesame_udon'],
  'cover_recipe_id': 'broccoli_egg_sesame_udon'},
 {'id': 41,
  'name': '豆腐のかきたまあんかけ',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 187,
  'protein': 16.2,
  'fat': 8.7,
  'carbs': None,
  'salt': 4.1,
  'salt_label': '食塩相当量',
  'vegetables': 5,
  'cost_est': '約115円（資料のAI推定）',
  'tags': ['豆腐', '卵'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['tofu_egg_ankake'],
  'cover_recipe_id': 'tofu_egg_ankake'},
 {'id': 42,
  'name': '鮭の照り焼き',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 148,
  'protein': 18.3,
  'fat': 8,
  'carbs': None,
  'salt': 1.2,
  'salt_label': '食塩相当量',
  'vegetables': 0,
  'cost_est': '約251円（資料のAI推定）',
  'tags': ['鮭'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['salmon_teriyaki'],
  'cover_recipe_id': 'salmon_teriyaki'},
 {'id': 43,
  'name': '極上のサラダチキン',
  'tag': 'ダイエット系',
  'category': 'diet',
  'kcal': 164,
  'protein': 29.3,
  'fat': 2.4,
  'carbs': 3,
  'salt': 1.8,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約113円（資料のAI推定）',
  'tags': ['鶏むね肉'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['salad_chicken'],
  'cover_recipe_id': 'salad_chicken',
  'sugars': 3},
 {'id': 44,
  'name': '焼きうどん',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 486,
  'protein': 21.2,
  'fat': 23.3,
  'carbs': None,
  'salt': 3.7,
  'salt_label': '食塩相当量',
  'vegetables': 138,
  'cost_est': '約260円（資料のAI推定）',
  'tags': ['うどん'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['yaki_udon'],
  'cover_recipe_id': 'yaki_udon'},
 {'id': 45,
  'name': 'カレーうどん',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 448,
  'protein': 16.7,
  'fat': 15.6,
  'carbs': None,
  'salt': 4.9,
  'salt_label': '食塩相当量',
  'vegetables': 48,
  'cost_est': '約233円（資料のAI推定）',
  'tags': ['うどん'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['curry_udon'],
  'cover_recipe_id': 'curry_udon'},
 {'id': 46,
  'name': 'かつおの竜田焼き',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 187,
  'protein': 18.6,
  'fat': 9.8,
  'carbs': None,
  'salt': 0.6,
  'salt_label': '食塩相当量',
  'vegetables': 46,
  'cost_est': '約173円（資料のAI推定）',
  'tags': ['かつお'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['bonito_tatsuta'],
  'cover_recipe_id': 'bonito_tatsuta'},
 {'id': 47,
  'name': 'かつおのスパイシー揚げ',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 265,
  'protein': 33.8,
  'fat': 7.9,
  'carbs': 12.2,
  'salt': 1.7,
  'salt_label': '食塩相当量',
  'vegetables': None,
  'cost_est': '約297円（資料のAI推定）',
  'tags': ['かつお'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['bonito_spicy'],
  'cover_recipe_id': 'bonito_spicy'},
 {'id': 48,
  'name': '鮭大根',
  'tag': '定番メニュー',
  'category': 'standard',
  'kcal': 175,
  'protein': 23.9,
  'fat': 4.6,
  'carbs': None,
  'salt': 1.3,
  'salt_label': '食塩相当量',
  'vegetables': 104,
  'cost_est': '約231円（資料のAI推定）',
  'tags': ['鮭', '大根'],
  'color': '#d4a06a',
  'background': '#f0e8dc',
  'image': None,
  'recipe_ids': ['salmon_daikon'],
  'cover_recipe_id': 'salmon_daikon'}]


# ユーザー提示の1食あたりの比較目安。個人別の必要量を判定するものではありません。
MEAL_TARGETS = {
    'male': {'label': '男性 18〜29歳', 'protein': 22, 'fat': 24, 'carbs': 140, 'salt': 2.5},
    'female': {'label': '女性 18〜29歳', 'protein': 17, 'fat': 18, 'carbs': 107, 'salt': 2.1},
    'female_diet': {'label': '女性用ダイエットモード', 'protein': 17, 'fat': 18, 'salt': 2.1},
}
NUTRITION_FIELDS = [
    ('タンパク質', 'protein', 'g'),
    ('脂質', 'fat', 'g'),
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
        if reference == 'female_diet':
            with ui.column().classes('w-full rounded-xl bg-amber-50 p-3 gap-1'):
                ui.label('この料理のエネルギー').classes('text-xs text-amber-900')
                ui.label(nutrient_text(menu, 'kcal', 'kcal')).classes('text-2xl font-bold text-amber-900')
                ui.label('参考：以前に指定した女性の1食の目安は約650 kcal。減量用の目標値ではありません。').classes('text-xs text-amber-900')
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


# 検索候補の表示順。使いたい食材をこのリストの上に移動できます。
# 利用統計ではなく、このアプリでの表示優先度です。
TAG_PRIORITY = [
    '鶏むね肉', '鶏むね', '鶏もも肉', '鶏のささみ', 'ひき肉', '豚肉',
    '玉ねぎ', 'キャベツ', 'ブロッコリー', 'ピーマン',
    '卵', 'パスタ', 'うどん', '焼きそば麺',
    'にんじん', 'じゃがいも', '大根',
    'ちくわ', 'こんにゃく', 'さば', '鮭', 'かつお', '牛乳', 'バター',
]


def tag_search_options():
    # 件数は全カテゴリーの料理数。重複したタグは1料理につき1回だけ数えます。
    counts = {}
    for menu in MENUS:
        for tag in set(menu.get('tags', [])):
            counts[tag] = counts.get(tag, 0) + 1
    priority = {tag: index for index, tag in enumerate(TAG_PRIORITY)}
    tags = sorted(counts, key=lambda tag: (priority.get(tag, len(priority)), tag))
    return {tag: f'{tag}（{counts[tag]}品）' for tag in tags}


INGREDIENT_GROUPS = {
    '肉類': ['鶏むね肉', '鶏むね', '鶏もも肉', '鶏のささみ', '鶏肉', 'ひき肉', '豚肉', '牛肉'],
    '野菜類': ['玉ねぎ', 'キャベツ', 'ブロッコリー', 'ピーマン', 'にんじん', 'じゃがいも', '大根', 'きゅうり', 'もやし', 'ニラ', 'きのこ'],
    '麺類': ['パスタ', 'うどん', '焼きそば麺'],
    '魚類': ['さば', '鮭', 'かつお', 'ちくわ'],
    'その他': ['豆腐', '卵', '牛乳', 'バター', 'こんにゃく'],
}


def grouped_tag_options():
    """全タグを一つの分類に割り当てる。未分類の新しいタグはその他へ。"""
    options = tag_search_options()
    grouped = {group: {} for group in INGREDIENT_GROUPS}
    assigned = set()
    for group, tags in INGREDIENT_GROUPS.items():
        for tag in tags:
            if tag in options and tag not in assigned:
                grouped[group][tag] = options[tag]
                assigned.add(tag)
    for tag, label in options.items():
        if tag not in assigned:
            grouped['その他'][tag] = label
    return grouped


def filter_menus(category='all', tags=None, *, diet=False):
    required = set(tags or [])
    result = [menu for menu in MENUS
              if (category == 'all' or menu['category'] == category)
              and required.issubset(menu.get('tags', []))]
    if diet:
        # 記載量あたりのカロリーで並べ替え。未記載・単位不明は末尾。
        result.sort(key=lambda menu: menu['kcal']
                    if menu.get('kcal') is not None and not menu.get('kcal_unit_missing')
                    else float('inf'))
    return result



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
HISTORY_KEY = 'menu_days_meal_history_v1'
MEAL_TIMES = ['朝食', '昼食', '夕食', '間食']


def today_japan():
    return datetime.now(timezone(timedelta(hours=9))).date().isoformat()


def history_script(action='read', payload=None):
    """読み取りと変更をブラウザ内で一度に実行し、別タブの記録を上書きしない。"""
    return """(() => {
        const key = __KEY__;
        const action = __ACTION__;
        const payload = __PAYLOAD__;
        const raw = localStorage.getItem(key);
        let records = raw === null ? [] : JSON.parse(raw);
        if (!Array.isArray(records) || records.some(r => !r ||
            typeof r.id !== 'string' || typeof r.date !== 'string' ||
            typeof r.meal_time !== 'string' || typeof r.name !== 'string')) {
            throw new Error('Invalid meal history');
        }
        let duplicate = false;
        if (action === 'add') {
            duplicate = records.some(r => r.date === payload.date &&
                r.meal_time === payload.meal_time && r.menu_id === payload.menu_id);
            if (!duplicate) {
                records.push(payload);
                localStorage.setItem(key, JSON.stringify(records));
            }
        } else if (action === 'delete') {
            records = records.filter(r => r.id !== payload);
            localStorage.setItem(key, JSON.stringify(records));
        }
        return {records, duplicate};
    })()""".replace('__KEY__', json.dumps(HISTORY_KEY)).replace(
        '__ACTION__', json.dumps(action)).replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=True))


@ui.page("/")
def main_page():
    # 選んだ献立と、表示するカテゴリーを管理
    selected = {"menu": None}
    history_state = {"records": [], "loaded": False, "error": False, "date": ""}
    page_client = ui.context.client
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

    async def update_history(action='read', payload=None):
        try:
            await page_client.connected(timeout=10)
            result = await ui.run_javascript(history_script(action, payload), timeout=10)
            history_state.update(records=result['records'], loaded=True, error=False)
            history_panel.refresh()
            return result
        except Exception:
            history_state['error'] = True
            history_panel.refresh()
            ui.notify('履歴を読み書きできません。ブラウザの保存設定や接続を確認してください。', type='negative')
            return None

    def open_record_dialog(menu):
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-md gap-3'):
            ui.label('食べた記録を追加').classes('text-lg font-bold')
            ui.label(menu['name']).classes('font-bold')
            eaten_date = ui.input('食べた日', value=today_japan()).props('type=date').classes('w-full')
            meal_time = ui.select(MEAL_TIMES, label='食事の区分', value='夕食').classes('w-full')
            ui.label('レシピ記載の分量を1回分として記録します。').classes('muted text-xs')

            async def save_record():
                try:
                    day = date.fromisoformat(eaten_date.value or '')
                    if day > date.fromisoformat(today_japan()):
                        raise ValueError
                    if meal_time.value not in MEAL_TIMES:
                        raise ValueError
                except (ValueError, TypeError):
                    ui.notify('今日以前の正しい日付と食事の区分を選んでください。', type='warning')
                    return
                save_button.disable()
                # 名前と栄養値は登録時点の値を残す。
                record = {
                    'id': str(uuid4()), 'date': day.isoformat(), 'meal_time': meal_time.value,
                    'menu_id': menu['id'], 'name': menu['name'],
                    'kcal': menu.get('kcal'), 'protein': menu.get('protein'),
                    'fat': menu.get('fat'), 'salt': menu.get('salt'),
                    'fat_unit_missing': menu.get('fat_unit_missing', False),
                    'cost_est': menu.get('cost_est'),
                }
                result = await update_history('add', record)
                save_button.enable()
                if result is not None:
                    dialog.close()
                    if result['duplicate']:
                        ui.notify('同じ日・食事区分にこの料理は記録済みです。', type='info')
                    else:
                        ui.notify('食事履歴に保存しました。', type='positive')

            with ui.row().classes('w-full justify-end'):
                ui.button('キャンセル', on_click=dialog.close).props('flat')
                save_button = ui.button('履歴に保存', icon='save', on_click=save_record)
        dialog.open()

    def confirm_delete(record):
        with ui.dialog() as dialog, ui.card().classes('gap-3'):
            ui.label('この記録を削除しますか？').classes('font-bold')
            ui.label(f"{record['date']}・{record['meal_time']}：{record['name']}")
            async def delete_record():
                delete_button.disable()
                result = await update_history('delete', record['id'])
                delete_button.enable()
                if result is not None:
                    dialog.close()
                    ui.notify('記録を削除しました。')
            with ui.row().classes('justify-end w-full'):
                ui.button('キャンセル', on_click=dialog.close).props('flat')
                delete_button = ui.button('削除する', color='negative', on_click=delete_record)
        dialog.open()

    @ui.refreshable
    def history_panel():
        if history_state['error']:
            ui.label('履歴を取得できませんでした。保存済みのデータは消していません。更新を押して再試行してください。').classes('text-red-700 text-sm')
            return
        if not history_state['loaded']:
            ui.label('履歴を読み込んでいます…').classes('muted text-sm')
            return
        records = [r for r in history_state['records']
                   if not history_state['date'] or r['date'] == history_state['date']]
        records.sort(key=lambda r: (r['date'], MEAL_TIMES.index(r['meal_time'])
                                   if r['meal_time'] in MEAL_TIMES else -1), reverse=True)
        ui.label(f'{len(records)}件の記録').classes('muted text-sm')
        if not records:
            ui.label('まだ記録がありません。献立を選んで「食べた記録を追加」から保存できます。').classes('muted text-sm')
            return
        previous_day = None
        for record in records:
            if record['date'] != previous_day:
                ui.label(record['date']).classes('text-lg font-bold mt-3')
                previous_day = record['date']
            with ui.card().classes('w-full shadow-none border rounded-xl gap-2'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label(record['meal_time']).classes('text-sm text-green-800 font-bold')
                    ui.button(icon='delete_outline', on_click=lambda r=record: confirm_delete(r)).props('flat round aria-label=記録を削除')
                ui.label(record['name']).classes('font-bold')
                for label, key, unit in NUTRITION_FIELDS:
                    ui.label(f'{label}：{nutrient_text(record, key, unit)}').classes('text-xs')
                if target_state['reference'] == 'female_diet':
                    ui.label('エネルギー：' + nutrient_text(record, 'kcal', 'kcal')).classes('text-xs font-bold text-amber-900')

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
                ui.button('食べた記録を追加', icon='history', on_click=lambda: open_record_dialog(menu)).props('unelevated').classes('w-full rounded-xl')
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
        filtered_menus = filter_menus(cat, filter_state['tags'], diet=target_state['reference'] == 'female_diet')
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
            ui.button(
                "🍽️ 定番メニュー",
                on_click=lambda: set_filter("standard"),
            ).props(
                "unelevated" if cat == "standard" else "outline"
            ).classes("rounded-2xl text-lg px-8 py-3 font-bold shadow-sm")
            ui.button(
                "🥗 ダイエット系",
                on_click=lambda: set_filter("diet"),
            ).props(
                "unelevated" if cat == "diet" else "outline"
            ).classes("rounded-2xl text-lg px-8 py-3 font-bold shadow-sm")
        if target_state['reference'] == 'female_diet':
            ui.label('女性用ダイエットモード：カロリーが低い順').classes('font-bold text-amber-900')
            ui.label('料理ごとの記載量で比較しています。少ないカロリーだけで1食を選ばず、主食・主菜・副菜を組み合わせてください。').classes('muted text-xs')
        def choose_random_menu():
            if not filtered_menus:
                return
            current = int(carousel.value or 0)
            candidates = [i for i in range(len(filtered_menus)) if i != current]
            index = random.choice(candidates) if candidates else 0
            # 抽選した料理を読めるように自動スライドを停止します。
            autoplay_state['enabled'] = False
            autoplay_switch.set_value(False)
            carousel.props(remove='autoplay')
            carousel.set_value(str(index))
            menu_detail.refresh()
            message = f"今日はこれ！ {filtered_menus[index]['name']}"
            if len(filtered_menus) == 1:
                message = f"今の条件に合う料理はこの1品です：{filtered_menus[index]['name']}"
            ui.notify(message, type='positive')

        with ui.card().classes('w-full rounded-2xl bg-amber-50 shadow-none gap-2'):
            random_button = ui.button(
                '🎲 優柔不断モード：ランダムで選ぶ',
                on_click=choose_random_menu,
            ).classes('rounded-xl text-lg font-bold').props('unelevated')
            if not filtered_menus:
                random_button.disable()
            ui.label('今のカテゴリー・食材タグに合う料理から提案します。もう一度押すと選び直せます。').classes('text-xs muted')
            ui.label('提案後は自動スライドを停止します。気に入ったら「この献立にする」で決定してください。').classes('text-xs muted')
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

                autoplay_switch = ui.switch(
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
            was_diet = target_state['reference'] == 'female_diet'
            target_state['reference'] = event.value
            is_diet = event.value == 'female_diet'
            history_panel.refresh()
            if was_diet != is_diet:
                main_content.refresh()
            else:
                nutrition_panel.refresh()

        ui.label('栄養ゲージの比較目安・モード').classes('font-bold text-sm')
        ui.toggle(
            {'male': '男性 18〜29歳', 'female': '女性 18〜29歳',
             'female_diet': '女性用ダイエットモード'},
            value=target_state['reference'], on_change=change_reference,
        ).props('no-caps rounded unelevated').classes('flex-wrap')

        def toggle_tag(tag):
            if tag in filter_state['tags']:
                filter_state['tags'].remove(tag)
            else:
                filter_state['tags'].append(tag)
            # 再描画で食材一覧を閉じ、選んだタグと検索結果を表示。
            ingredient_search.refresh()
            main_content.refresh()

        def clear_tags():
            filter_state['tags'].clear()
            ingredient_search.refresh()
            main_content.refresh()

        @ui.refreshable
        def ingredient_search():
            ui.label('食材から探す').classes('font-bold text-base')
            ui.label('分類を開いて食材をクリック。複数選ぶと、すべての食材タグを含む料理を表示します。件数は全料理での登録数です。').classes('muted text-xs')
            if filter_state['tags']:
                with ui.row().classes('w-full gap-2 items-center flex-wrap'):
                    for tag in filter_state['tags']:
                        ui.button(tag, icon='close', on_click=lambda t=tag: toggle_tag(t)).props('unelevated no-caps').classes('rounded-full')
                    ui.button('選択をすべて解除', on_click=clear_tags).props('flat no-caps')
            icons = {'肉類': 'restaurant', '野菜類': 'eco', '麺類': 'ramen_dining',
                     '魚類': 'set_meal', 'その他': 'kitchen'}
            for group, options in grouped_tag_options().items():
                if not options:
                    continue
                with ui.expansion(group, icon=icons[group], value=False).props('group=ingredient-groups').classes('w-full rounded-xl border bg-white'):
                    with ui.row().classes('w-full gap-2 flex-wrap'):
                        for tag, label in options.items():
                            ui.button(label, on_click=lambda t=tag: toggle_tag(t)).props(
                                'unelevated no-caps' if tag in filter_state['tags'] else 'outline no-caps'
                            ).classes('rounded-full')
        ingredient_search()
        main_content()
        with ui.card().classes('panel w-full gap-3'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('食事履歴').classes('text-xl font-bold')
                ui.button('更新', icon='refresh', on_click=lambda: update_history()).props('flat')
            ui.label('このブラウザ・同じURLに保存します。別の端末やURLとは共有されず、ブラウザのサイトデータを消すと履歴も消えます。').classes('muted text-xs')
            def filter_history(event):
                history_state['date'] = event.value or ''
                history_panel.refresh()
            with ui.row().classes('items-center w-full'):
                history_date = ui.input('日付で絞り込み', on_change=filter_history).props('type=date clearable')
                ui.button('全期間', on_click=lambda: history_date.set_value('')).props('flat')
            history_panel()
        ui.timer(0.2, update_history, once=True)
if __name__ == "__main__":
    import os
    # クラウド環境が自動割り当てするポートを取得（ローカル時は8081）
    port = int(os.environ.get("PORT", 8081))
    ui.run(
        title="MENU DAYS | 献立とレシピリンク",
<<<<<<< HEAD
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8081")),
        reload=False,
        show=False,
=======
        host="0.0.0.0",  # 外部からのアクセスを許可
        port=port,
        reload=False,
        storage_secret="pass_menuapp_2134bvemomf2",  # 適当な秘密文字列に変更してください
>>>>>>> 58c4db4aad124a76e04261f495785bba8640fc94
    )
