# ---------------------------------------------------------------------------
# Bakery recipes (ingredient dict → output)
# ---------------------------------------------------------------------------

BAKERY_RECIPES = [
    {"name": "Bread",          "ingredients": {"wheat": 3},                   "output_id": "bread",          "output_count": 1},
    {"name": "Strawberry Jam", "ingredients": {"strawberry": 3},              "output_id": "strawberry_jam", "output_count": 1},
    {"name": "Cheese",      "ingredients": {"milk": 3},                    "output_id": "cheese",      "output_count": 1},
    {"name": "Tomato Soup", "ingredients": {"tomato": 3},                  "output_id": "tomato_soup", "output_count": 1},
    {"name": "Corn Bread",  "ingredients": {"corn": 2, "wheat": 1},        "output_id": "corn_bread",  "output_count": 1},
    {"name": "Pumpkin Pie", "ingredients": {"pumpkin": 1, "wheat": 2},     "output_id": "pumpkin_pie", "output_count": 1},
    {"name": "Apple Pie",   "ingredients": {"apple": 2, "wheat": 2},       "output_id": "apple_pie",   "output_count": 1},
    {"name": "Carrot Cake",    "ingredients": {"carrot": 2, "wheat": 2},                  "output_id": "carrot_cake",    "output_count": 1},
    {"name": "Cheese Bread",   "ingredients": {"bread": 1, "cheese": 1},                  "output_id": "cheese_bread",   "output_count": 1},
    # --- Chinese cuisine ---
    {"name": "Tofu",           "ingredients": {"corn": 3},                                 "output_id": "tofu",           "output_count": 1},
    {"name": "Steamed Rice",   "ingredients": {"rice": 2},                                 "output_id": "steamed_rice",   "output_count": 1},
    {"name": "Egg Fried Rice", "ingredients": {"rice": 1, "egg": 1, "carrot": 1},          "output_id": "egg_fried_rice", "output_count": 1},
    {"name": "Congee",         "ingredients": {"rice": 2, "milk": 1},                      "output_id": "congee",         "output_count": 1},
    {"name": "Mapo Tofu",      "ingredients": {"tofu": 1, "tomato": 1, "ginger": 1},       "output_id": "mapo_tofu",      "output_count": 1},
    {"name": "Dumplings",      "ingredients": {"wheat": 1, "carrot": 1, "ginger": 1},      "output_id": "dumplings",      "output_count": 2},
    {"name": "Wonton Soup",    "ingredients": {"wheat": 1, "mushroom": 1, "ginger": 1},    "output_id": "wonton_soup",    "output_count": 1},
    {"name": "Kung Pao",       "ingredients": {"corn": 1, "pumpkin": 1, "ginger": 1},      "output_id": "kung_pao",       "output_count": 1},
    {"name": "Moon Cake",      "ingredients": {"wheat": 1, "pumpkin": 1, "egg": 1},        "output_id": "moon_cake",      "output_count": 2},
    {"name": "Hot & Sour Soup","ingredients": {"mushroom": 1, "tomato": 1, "egg": 1},      "output_id": "hot_sour_soup",  "output_count": 1},
    {"name": "Sweet Rice Ball","ingredients": {"rice": 1, "pumpkin": 1},                   "output_id": "sweet_rice_ball","output_count": 2},
    {"name": "Sweet Potato Pie",   "ingredients": {"sweet_potato": 2, "wheat": 1},         "output_id": "sweet_potato_pie",   "output_count": 1},
    # --- Desert bakery ---
    {"name": "Date Cake",     "ingredients": {"date_palm_fruit": 2, "wheat": 1},             "output_id": "date_cake",     "output_count": 1},
    {"name": "Cactus Candy",  "ingredients": {"cactus_fruit": 2, "agave_syrup": 1},          "output_id": "cactus_candy",  "output_count": 2},
    # --- Italian ---
    {"name": "Bruschetta",    "ingredients": {"bread": 1, "tomato": 1, "garlic": 1},           "output_id": "bruschetta",    "output_count": 2},
    {"name": "Pasta al Forno","ingredients": {"noodles": 1, "tomato": 1, "cheese": 1},         "output_id": "pasta_al_forno","output_count": 1},
    {"name": "Polenta",       "ingredients": {"corn": 2, "milk": 1},                           "output_id": "polenta",       "output_count": 1},
    # --- Middle Eastern ---
    {"name": "Flatbread",    "ingredients": {"wheat": 2},                                      "output_id": "flatbread",    "output_count": 2},
    {"name": "Tahini",       "ingredients": {"sesame_seeds": 3},                               "output_id": "tahini",       "output_count": 1},
    {"name": "Bulgur",       "ingredients": {"wheat": 2},                                      "output_id": "bulgur",       "output_count": 2},
    {"name": "Labneh",       "ingredients": {"milk": 3},                                       "output_id": "labneh",       "output_count": 1},
    {"name": "Couscous",     "ingredients": {"wheat": 2},                                      "output_id": "couscous",     "output_count": 2},
    {"name": "Halva",        "ingredients": {"tahini": 2, "date_palm_fruit": 1},               "output_id": "halva",        "output_count": 2},
    {"name": "Baklava",      "ingredients": {"wheat": 1, "date_palm_fruit": 2},                "output_id": "baklava",      "output_count": 2},
    {"name": "Pide",         "ingredients": {"wheat": 2, "egg": 1},                            "output_id": "pide",         "output_count": 2},
    {"name": "Borek",        "ingredients": {"wheat": 1, "egg": 1, "cheese": 1},               "output_id": "borek",        "output_count": 2},
    {"name": "Kunafa",       "ingredients": {"wheat": 1, "cheese": 1},                         "output_id": "kunafa",       "output_count": 1},
    {"name": "Sfeeha",       "ingredients": {"wheat": 1, "raw_beef": 1, "onion": 1},           "output_id": "sfeeha",       "output_count": 2},
    {"name": "Lahmacun",     "ingredients": {"flatbread": 1, "raw_beef": 1, "tomato": 1},      "output_id": "lahmacun",     "output_count": 1},
    {"name": "Manakish",    "ingredients": {"flatbread": 1, "sesame_seeds": 1, "onion": 1},    "output_id": "manakish",     "output_count": 1},
    {"name": "Ka'ak",       "ingredients": {"wheat": 2, "sesame_seeds": 1},                    "output_id": "ka_ak",        "output_count": 2},
    {"name": "Ma'amoul",    "ingredients": {"wheat": 1, "date_palm_fruit": 2},                 "output_id": "maamoul",      "output_count": 2},
    {"name": "Basbousa",    "ingredients": {"wheat": 1, "milk": 1, "agave": 1},                "output_id": "basbousa",     "output_count": 1},
    {"name": "Qatayef",     "ingredients": {"wheat": 1, "milk": 1, "egg": 1},                  "output_id": "qatayef",      "output_count": 2},
    {"name": "Arayes",      "ingredients": {"flatbread": 1, "raw_beef": 1, "onion": 1},        "output_id": "arayes",       "output_count": 1},
    # --- Spanish ---
    {"name": "Pan Tostado", "ingredients": {"bread": 1, "tomato": 1, "olive_oil": 1},          "output_id": "pan_tostado",  "output_count": 2},
    {"name": "Empanada",    "ingredients": {"wheat": 1, "cooked_beef": 1, "onion": 1},          "output_id": "empanada",     "output_count": 1},
    {"name": "Churros",     "ingredients": {"wheat": 2, "egg": 1},                              "output_id": "churros",      "output_count": 3},
    {"name": "Torrija",     "ingredients": {"wheat": 1, "milk": 1, "egg": 1},                   "output_id": "torrija",      "output_count": 2},
    {"name": "Polvoron",    "ingredients": {"wheat": 1, "milk": 1, "agave": 1},                 "output_id": "polvoron",     "output_count": 3},
    # --- Wild game pies & pasties ---
    {"name": "Game Pasty",    "ingredients": {"cooked_venison": 1, "wheat": 2, "onion": 1},        "output_id": "game_pasty",    "output_count": 2},
    {"name": "Rabbit Pie",    "ingredients": {"raw_rabbit": 1, "wheat": 2, "potato": 1},           "output_id": "rabbit_pie",    "output_count": 1},
    {"name": "Venison Pasty", "ingredients": {"raw_venison": 1, "wheat": 2, "mushroom": 1},        "output_id": "venison_pasty", "output_count": 2},
    {"name": "Pheasant Pie",  "ingredients": {"raw_pheasant": 1, "wheat": 2, "onion": 1},          "output_id": "pheasant_pie",  "output_count": 1},
    # --- Typed cheese dishes ---
    {"name": "Fondue",            "ingredients": {"cheese_alpine": 1, "milk": 1, "wheat": 1},      "output_id": "fondue",            "output_count": 1},
    {"name": "Cheesecake",        "ingredients": {"cheese_double_cream": 1, "egg": 1, "wheat": 1}, "output_id": "cheesecake",        "output_count": 1},
    {"name": "Cheese Tart",       "ingredients": {"cheese_fresh": 1, "wheat": 1, "egg": 1},        "output_id": "cheese_tart",       "output_count": 2},
    {"name": "Gratin",            "ingredients": {"cheese_pressed": 1, "potato": 2},               "output_id": "gratin",            "output_count": 1},
    {"name": "Blue Cheese Toast", "ingredients": {"cheese_blue": 1, "bread": 1},                   "output_id": "blue_cheese_toast", "output_count": 1},
    {"name": "Herb Cheese Bread", "ingredients": {"cheese_herb_crusted": 1, "bread": 1},           "output_id": "herb_cheese_bread", "output_count": 1},
    {"name": "Ash Flatbread",     "ingredients": {"cheese_ash_coated": 1, "wheat": 2},             "output_id": "ash_flatbread",     "output_count": 2},
    # --- Salt seasoned ---
    {"name": "Focaccia",       "ingredients": {"wheat": 2, "olive_oil": 1, "fleur_de_sel": 1},   "output_id": "focaccia",       "output_count": 1},
    {"name": "Salted Pretzel", "ingredients": {"wheat": 2, "coarse_salt": 1},                     "output_id": "salted_pretzel", "output_count": 3},
    # --- Fruit baked goods ---
    {"name": "Apple Tart",          "ingredients": {"apple": 2, "wheat": 1},                          "output_id": "apple_tart",          "output_count": 1},
    {"name": "Pear Tart",           "ingredients": {"pear": 2, "wheat": 1},                           "output_id": "pear_tart",           "output_count": 1},
    {"name": "Lemon Tart",          "ingredients": {"lemon": 2, "wheat": 1, "egg": 1},                "output_id": "lemon_tart",          "output_count": 1},
    {"name": "Apple Crumble",       "ingredients": {"apple": 2, "wheat": 2},                          "output_id": "apple_crumble",       "output_count": 1},
    {"name": "Fig Roll",            "ingredients": {"fig": 2, "wheat": 1},                            "output_id": "fig_roll",            "output_count": 2},
    {"name": "Lemon Drizzle Cake",  "ingredients": {"lemon": 1, "wheat": 2, "egg": 1},               "output_id": "lemon_drizzle",       "output_count": 1},
    {"name": "Pear & Ginger Cake",  "ingredients": {"pear": 1, "ginger": 1, "wheat": 2},             "output_id": "pear_ginger_cake",    "output_count": 1},
    {"name": "Pomegranate Cake",    "ingredients": {"pomegranate": 1, "wheat": 2, "egg": 1},          "output_id": "pomegranate_cake",    "output_count": 1},
    {"name": "Fig Jam",             "ingredients": {"fig": 3},                                        "output_id": "fig_jam",             "output_count": 2},
    {"name": "Apple Cinnamon Roll", "ingredients": {"apple": 1, "wheat": 2},                          "output_id": "apple_cinnamon_roll", "output_count": 2},
    {"name": "Strawberry Tart",     "ingredients": {"strawberry": 2, "wheat": 1, "egg": 1},          "output_id": "strawberry_tart",     "output_count": 1},
    {"name": "Fruit Cake",          "ingredients": {"apple": 1, "pear": 1, "wheat": 2, "egg": 1},    "output_id": "fruit_cake",          "output_count": 1},
    # --- Fruit baked goods batch 2 ---
    {"name": "Fig Tart",              "ingredients": {"fig": 2, "wheat": 1, "egg": 1},                "output_id": "fig_tart",              "output_count": 1},
    {"name": "Pomegranate Jam",       "ingredients": {"pomegranate": 3},                              "output_id": "pomegranate_jam",       "output_count": 2},
    {"name": "Lemon Shortbread",      "ingredients": {"lemon": 1, "wheat": 2},                        "output_id": "lemon_shortbread",      "output_count": 3},
    {"name": "Pear Upside-Down Cake", "ingredients": {"pear": 2, "wheat": 2, "egg": 1},              "output_id": "pear_upside_down_cake", "output_count": 1},
    {"name": "Strawberry Shortcake",  "ingredients": {"strawberry": 2, "wheat": 1, "milk": 1},       "output_id": "strawberry_shortcake",  "output_count": 1},
    {"name": "Lemon Meringue Pie",    "ingredients": {"lemon": 2, "wheat": 1, "egg": 2},              "output_id": "lemon_meringue_pie",    "output_count": 1},
    {"name": "Apple Strudel",         "ingredients": {"apple": 2, "wheat": 2},                        "output_id": "apple_strudel",         "output_count": 1},
    {"name": "Apple & Pear Pie",      "ingredients": {"apple": 1, "pear": 1, "wheat": 2},             "output_id": "apple_pear_pie",        "output_count": 1},
    {"name": "Pear Almond Cake",      "ingredients": {"pear": 1, "wheat": 2, "milk": 1},              "output_id": "pear_almond_cake",      "output_count": 1},
    {"name": "Fig Cake",              "ingredients": {"fig": 2, "wheat": 1, "milk": 1},               "output_id": "fig_cake",              "output_count": 1},
    # --- Fruit baked goods batch 3 ---
    {"name": "Lemon Curd",            "ingredients": {"lemon": 3, "egg": 1},                          "output_id": "lemon_curd",            "output_count": 2},
    {"name": "Apple Butter",          "ingredients": {"apple": 3},                                    "output_id": "apple_butter",          "output_count": 2},
    {"name": "Pear Frangipane",       "ingredients": {"pear": 1, "wheat": 2, "egg": 2},               "output_id": "pear_frangipane",       "output_count": 1},
    {"name": "Fig Brioche",           "ingredients": {"fig": 2, "wheat": 2, "egg": 1},                "output_id": "fig_brioche",           "output_count": 2},
    {"name": "Lemon Poppy Muffin",    "ingredients": {"lemon": 1, "wheat": 1, "milk": 1},             "output_id": "lemon_poppy_muffin",    "output_count": 2},
    {"name": "Pomegranate Danish",    "ingredients": {"pomegranate": 1, "wheat": 2},                  "output_id": "pomegranate_danish",    "output_count": 2},
    {"name": "Watermelon Cake",       "ingredients": {"watermelon": 1, "wheat": 2, "egg": 1},         "output_id": "watermelon_cake",       "output_count": 1},
    {"name": "Apple Loaf",            "ingredients": {"apple": 1, "wheat": 2, "egg": 1},              "output_id": "apple_loaf",            "output_count": 1},
    # --- Desserts: Cakes ---
    {"name": "Honey Cake",            "ingredients": {"agave_syrup": 2, "wheat": 2, "egg": 1},        "output_id": "honey_cake",            "output_count": 1},
    {"name": "Black Forest Cake",     "ingredients": {"wheat": 2, "egg": 2, "milk": 2},               "output_id": "black_forest_cake",     "output_count": 1},
    {"name": "Victoria Sponge",       "ingredients": {"strawberry": 2, "wheat": 2, "egg": 1},         "output_id": "victoria_sponge",       "output_count": 1},
    {"name": "Tres Leches Cake",      "ingredients": {"milk": 3, "wheat": 2, "egg": 2},               "output_id": "tres_leches",           "output_count": 1},
    {"name": "Matcha Roll Cake",      "ingredients": {"taro": 1, "wheat": 2, "egg": 2},               "output_id": "matcha_roll",           "output_count": 1},
    {"name": "Stollen",               "ingredients": {"wheat": 2, "date_palm_fruit": 2, "sesame_seeds": 1}, "output_id": "stollen",          "output_count": 1},
    {"name": "Orange Cake",           "ingredients": {"lemon": 1, "wheat": 2, "egg": 1},              "output_id": "orange_cake",           "output_count": 1},
    {"name": "Chestnut Cake",         "ingredients": {"pumpkin": 1, "wheat": 2, "egg": 1},            "output_id": "chestnut_cake",         "output_count": 1},
    # --- Desserts: Cookies ---
    {"name": "Ginger Snap",           "ingredients": {"ginger": 1, "wheat": 2},                       "output_id": "ginger_snap",           "output_count": 4},
    {"name": "Biscotti",              "ingredients": {"wheat": 1, "sesame_seeds": 1, "egg": 1},       "output_id": "biscotti",              "output_count": 4},
    {"name": "Almond Cookie",         "ingredients": {"wheat": 1, "egg": 1},                          "output_id": "almond_cookie",         "output_count": 4},
    {"name": "Shortbread",            "ingredients": {"wheat": 2, "milk": 1},                         "output_id": "shortbread",            "output_count": 4},
    {"name": "Lebkuchen",             "ingredients": {"ginger": 1, "wheat": 1, "sesame_seeds": 1},    "output_id": "lebkuchen",             "output_count": 4},
    {"name": "Macaron",               "ingredients": {"sesame_seeds": 1, "egg": 2, "milk": 1},        "output_id": "macaron",               "output_count": 4},
    {"name": "Alfajor",               "ingredients": {"wheat": 2, "milk": 1, "egg": 1},               "output_id": "alfajor",               "output_count": 4},
    {"name": "Spekulatius",           "ingredients": {"ginger": 1, "wheat": 2, "agave_syrup": 1},     "output_id": "spekulatius",           "output_count": 4},
    # --- Desserts: Pies & Tarts ---
    {"name": "Berry Pie",             "ingredients": {"strawberry": 2, "wheat": 2, "egg": 1},         "output_id": "berry_pie",             "output_count": 1},
    {"name": "Honey Tart",            "ingredients": {"agave_syrup": 2, "wheat": 1, "egg": 1},        "output_id": "honey_tart",            "output_count": 1},
    {"name": "Almond Tart",           "ingredients": {"sesame_seeds": 1, "wheat": 1, "egg": 1},       "output_id": "almond_tart",           "output_count": 1},
    {"name": "Key Lime Tart",         "ingredients": {"lemon": 2, "wheat": 1, "milk": 1},             "output_id": "key_lime_tart",         "output_count": 1},
    {"name": "Date Tart",             "ingredients": {"date_palm_fruit": 2, "wheat": 1, "egg": 1},    "output_id": "date_tart",             "output_count": 1},
    # --- Desserts: Japanese ---
    {"name": "Mochi",                 "ingredients": {"rice": 2, "agave_syrup": 1},                   "output_id": "mochi",                 "output_count": 4},
    {"name": "Dorayaki",              "ingredients": {"wheat": 1, "egg": 1, "date_palm_fruit": 1},    "output_id": "dorayaki",              "output_count": 2},
    {"name": "Daifuku",               "ingredients": {"rice": 2, "milk": 1, "strawberry": 1},         "output_id": "daifuku",               "output_count": 4},
    {"name": "Yokan",                 "ingredients": {"date_palm_fruit": 2, "rice": 1},               "output_id": "yokan",                 "output_count": 2},
    {"name": "Taiyaki",               "ingredients": {"wheat": 1, "egg": 1, "pumpkin": 1},            "output_id": "taiyaki",               "output_count": 2},
    # --- Desserts: Indian ---
    {"name": "Gulab Jamun",           "ingredients": {"milk": 2, "wheat": 1, "agave_syrup": 1},       "output_id": "gulab_jamun",           "output_count": 4},
    {"name": "Kheer",                 "ingredients": {"rice": 2, "milk": 2, "date_palm_fruit": 1},    "output_id": "kheer",                 "output_count": 2},
    {"name": "Ladoo",                 "ingredients": {"sesame_seeds": 1, "agave_syrup": 1, "milk": 1}, "output_id": "ladoo",                "output_count": 4},
    {"name": "Barfi",                 "ingredients": {"milk": 2, "agave_syrup": 1, "carrot": 1},      "output_id": "barfi",                 "output_count": 4},
    {"name": "Rasgulla",              "ingredients": {"milk": 3, "egg": 1},                           "output_id": "rasgulla",              "output_count": 4},
    # --- Desserts: French ---
    {"name": "Eclair",                "ingredients": {"wheat": 1, "egg": 2, "milk": 1},               "output_id": "eclair",                "output_count": 2},
    {"name": "Creme Brulee",          "ingredients": {"egg": 2, "milk": 2, "agave_syrup": 1},         "output_id": "creme_brulee",          "output_count": 2},
    {"name": "Mille-Feuille",         "ingredients": {"wheat": 2, "egg": 1, "milk": 2},               "output_id": "mille_feuille",         "output_count": 1},
    {"name": "Clafoutis",             "ingredients": {"strawberry": 2, "egg": 2, "milk": 1},          "output_id": "clafoutis",             "output_count": 1},
    {"name": "Profiteroles",          "ingredients": {"wheat": 1, "egg": 2, "milk": 1},               "output_id": "profiteroles",          "output_count": 4},
    # --- Desserts: Italian ---
    {"name": "Tiramisu",              "ingredients": {"egg": 2, "milk": 2, "wheat": 1},               "output_id": "tiramisu",              "output_count": 1},
    {"name": "Panna Cotta",           "ingredients": {"milk": 3, "agave_syrup": 1},                   "output_id": "panna_cotta",           "output_count": 2},
    {"name": "Cannoli",               "ingredients": {"wheat": 2, "milk": 2, "egg": 1},               "output_id": "cannoli",               "output_count": 2},
    {"name": "Zeppole",               "ingredients": {"wheat": 1, "egg": 2, "agave_syrup": 1},        "output_id": "zeppole",               "output_count": 4},
    # --- Desserts: British ---
    {"name": "Sticky Toffee Pudding", "ingredients": {"date_palm_fruit": 2, "wheat": 1, "egg": 2},    "output_id": "sticky_toffee_pudding", "output_count": 1},
    {"name": "Eton Mess",             "ingredients": {"strawberry": 2, "egg": 2, "milk": 1},          "output_id": "eton_mess",             "output_count": 2},
    {"name": "Trifle",                "ingredients": {"strawberry": 2, "pear": 1, "milk": 2},         "output_id": "trifle",                "output_count": 1},
    {"name": "Jam Roly-Poly",         "ingredients": {"strawberry": 2, "wheat": 2, "milk": 1},        "output_id": "jam_roly_poly",         "output_count": 1},
    # --- Desserts: Mexican & Latin American ---
    {"name": "Flan",                  "ingredients": {"egg": 3, "milk": 2, "agave_syrup": 1},         "output_id": "flan",                  "output_count": 2},
    {"name": "Bunuelos",              "ingredients": {"wheat": 2, "egg": 1, "agave_syrup": 1},        "output_id": "bunuelos",              "output_count": 4},
    {"name": "Arroz con Leche",       "ingredients": {"rice": 2, "milk": 2, "lemon": 1},              "output_id": "arroz_con_leche",       "output_count": 2},
    # --- Desserts: American ---
    {"name": "Brownie",               "ingredients": {"wheat": 1, "egg": 2, "milk": 1},               "output_id": "brownie",               "output_count": 4},
    {"name": "Bread Pudding",         "ingredients": {"wheat": 2, "milk": 2, "egg": 2},               "output_id": "bread_pudding",         "output_count": 1},
    {"name": "Rice Pudding",          "ingredients": {"rice": 2, "milk": 2, "agave_syrup": 1},        "output_id": "rice_pudding",          "output_count": 2},
]

# ---------------------------------------------------------------------------
# Wok recipes
# ---------------------------------------------------------------------------

WOK_RECIPES = [
    {"name": "Scallion Pancake", "ingredients": {"scallion": 2, "wheat": 1},                    "output_id": "scallion_pancake", "output_count": 2},
    {"name": "Chili Oil Tofu",   "ingredients": {"tofu": 1, "chili": 1, "ginger": 1},           "output_id": "chili_oil_tofu",   "output_count": 1},
    {"name": "Stir Fried Rice",  "ingredients": {"rice": 1, "scallion": 1, "egg": 1},           "output_id": "stir_fried_rice",  "output_count": 1},
    {"name": "Spicy Corn",       "ingredients": {"corn": 2, "chili": 1},                         "output_id": "spicy_corn",       "output_count": 2},
    {"name": "Chili Bok Choy",   "ingredients": {"bok_choy": 2, "chili": 1, "garlic": 1},       "output_id": "chili_bok_choy",   "output_count": 1},
    {"name": "Scallion Eggs",    "ingredients": {"egg": 2, "scallion": 1},                       "output_id": "scallion_eggs",    "output_count": 1},
    {"name": "Cooked Egg",       "ingredients": {"egg": 1},                                      "output_id": "cooked_egg",       "output_count": 1},
    {"name": "Omelette",         "ingredients": {"egg": 2},                                      "output_id": "omelette",         "output_count": 1},
    {"name": "Garlic Bok Choy",  "ingredients": {"bok_choy": 2, "garlic": 1},                   "output_id": "garlic_bok_choy",  "output_count": 1},
    {"name": "Turnip Mash",      "ingredients": {"turnip": 2, "ginger": 1},                      "output_id": "turnip_mash",      "output_count": 1},
    {"name": "Zucchini Stir Fry","ingredients": {"zucchini": 2, "garlic": 1},                    "output_id": "zucchini_stir_fry","output_count": 1},
    {"name": "Celery Stir Fry",  "ingredients": {"celery": 2, "scallion": 1},                    "output_id": "celery_stir_fry",  "output_count": 1},
    {"name": "Broccoli Stir Fry","ingredients": {"broccoli": 2, "garlic": 1},                    "output_id": "broccoli_stir_fry","output_count": 1},
    # --- Meat ---
    {"name": "Beef & Broccoli",   "ingredients": {"cooked_beef": 1, "broccoli": 1, "garlic": 1},  "output_id": "beef_broccoli",      "output_count": 1},
    {"name": "Chili Chicken",     "ingredients": {"cooked_chicken": 1, "chili": 1, "garlic": 1},  "output_id": "chili_chicken",      "output_count": 1},
    {"name": "Ginger Beef",       "ingredients": {"cooked_beef": 1, "ginger": 1, "scallion": 1},  "output_id": "ginger_beef",        "output_count": 1},
    {"name": "Sesame Chicken",    "ingredients": {"cooked_chicken": 1, "mushroom": 1, "scallion": 1}, "output_id": "sesame_chicken", "output_count": 1},
    {"name": "Mutton Stir Fry",   "ingredients": {"cooked_mutton": 1, "pepper": 1, "onion": 1},   "output_id": "mutton_stir_fry",    "output_count": 1},
    # --- Fish ---
    {"name": "Sweet & Sour Fish", "ingredients": {"fish": 1, "tomato": 1, "pumpkin": 1},          "output_id": "sweet_sour_fish",    "output_count": 1},
    {"name": "Fish & Tofu",       "ingredients": {"fish": 1, "tofu": 1, "scallion": 1},           "output_id": "fish_tofu",          "output_count": 1},
    # --- Desert wok ---
    {"name": "Desert Salad",     "ingredients": {"cactus_fruit": 1, "watermelon": 1, "chili": 1}, "output_id": "desert_salad",     "output_count": 1},
    # --- Italian ---
    {"name": "Caponata",         "ingredients": {"eggplant": 1, "tomato": 1, "onion": 1},         "output_id": "caponata",         "output_count": 1},
    {"name": "Frittata",         "ingredients": {"egg": 2, "zucchini": 1, "onion": 1},             "output_id": "frittata",         "output_count": 1},
    {"name": "Peperonata",       "ingredients": {"pepper": 1, "onion": 1, "tomato": 1},            "output_id": "peperonata",       "output_count": 1},
    {"name": "Zucchini Fritters","ingredients": {"zucchini": 1, "egg": 1, "wheat": 1},             "output_id": "zucchini_fritters","output_count": 2},
    # --- Middle Eastern ---
    {"name": "Falafel",         "ingredients": {"chickpea": 2, "onion": 1, "garlic": 1},          "output_id": "falafel",         "output_count": 3},
    {"name": "Fattoush",        "ingredients": {"tomato": 2, "flatbread": 1, "onion": 1},          "output_id": "fattoush",        "output_count": 1},
    {"name": "Tabbouleh",       "ingredients": {"bulgur": 1, "tomato": 2, "onion": 1},             "output_id": "tabbouleh",       "output_count": 1},
    {"name": "Muhammara",       "ingredients": {"pepper": 2, "wheat": 1, "onion": 1},              "output_id": "muhammara",       "output_count": 1},
    {"name": "Samboosa",        "ingredients": {"wheat": 1, "lentil": 1, "onion": 1},              "output_id": "samboosa",        "output_count": 3},
    {"name": "Kibbeh",          "ingredients": {"raw_beef": 1, "onion": 1, "wheat": 1},            "output_id": "kibbeh",          "output_count": 2},
    {"name": "Pomegranate Salad","ingredients": {"pomegranate": 2, "onion": 1},                    "output_id": "pomegranate_salad","output_count": 1},
    {"name": "Musakhan",       "ingredients": {"cooked_chicken": 1, "onion": 2, "flatbread": 1},  "output_id": "musakhan",        "output_count": 1},
    {"name": "Fattet Hummus",  "ingredients": {"hummus": 1, "flatbread": 1, "egg": 1},             "output_id": "fattet_hummus",   "output_count": 1},
    {"name": "Fatayer",        "ingredients": {"wheat": 1, "cabbage": 1, "onion": 1},              "output_id": "spinach_fatayer", "output_count": 2},
    {"name": "Byesar",         "ingredients": {"chickpea": 2, "garlic": 2},                        "output_id": "byesar",          "output_count": 1},
    {"name": "White Shakshuka","ingredients": {"egg": 2, "onion": 1, "garlic": 1},                 "output_id": "white_shakshuka", "output_count": 1},
    # --- Spanish ---
    {"name": "Olive Oil",       "ingredients": {"olive": 3},                                       "output_id": "olive_oil",        "output_count": 1},
    {"name": "Patatas Bravas",  "ingredients": {"potato": 3, "tomato": 1},                          "output_id": "patatas_bravas",   "output_count": 1},
    {"name": "Tortilla Española","ingredients": {"potato": 2, "egg": 2, "onion": 1},               "output_id": "tortilla_espanola","output_count": 1},
    {"name": "Pimientos Padrón","ingredients": {"pepper": 3, "olive_oil": 1},                      "output_id": "pimientos_padron", "output_count": 1},
    {"name": "Croquetas",       "ingredients": {"potato": 1, "wheat": 1, "cheese": 1},              "output_id": "croquetas",        "output_count": 2},
    {"name": "Gambas al Ajillo","ingredients": {"fish": 1, "garlic": 3, "olive_oil": 1},            "output_id": "gambas_al_ajillo", "output_count": 1},
    # --- Wild game ---
    {"name": "Wild Game Stir Fry","ingredients": {"cooked_venison": 1, "bok_choy": 1, "garlic": 1},"output_id": "wild_game_stir_fry","output_count": 1},
    {"name": "Duck Fried Rice",  "ingredients": {"cooked_duck": 1, "rice": 1, "scallion": 1},       "output_id": "duck_fried_rice",   "output_count": 1},
    # --- Fruit wok dishes batch 3 ---
    {"name": "Pear & Ginger Stir-Fry",   "ingredients": {"pear": 1, "ginger": 1, "bok_choy": 1},   "output_id": "pear_ginger_stir_fry",   "output_count": 1},
    {"name": "Lemon Tofu Stir-Fry",      "ingredients": {"lemon": 1, "tofu": 1, "scallion": 1},    "output_id": "lemon_tofu_stir_fry",    "output_count": 1},
    {"name": "Sweet Pomegranate Rice",   "ingredients": {"pomegranate": 1, "rice": 2},              "output_id": "sweet_pomegranate_rice", "output_count": 1},
    {"name": "Apple & Mushroom Stir-Fry","ingredients": {"apple": 1, "mushroom": 2, "garlic": 1},  "output_id": "apple_mushroom_stir_fry","output_count": 1},
    # --- Fruit wok dishes ---
    {"name": "Lemon Garlic Stir-Fry", "ingredients": {"lemon": 1, "garlic": 2, "bok_choy": 1},     "output_id": "lemon_garlic_stir_fry", "output_count": 1},
    {"name": "Citrus Fried Rice",     "ingredients": {"lemon": 1, "rice": 2, "egg": 1},             "output_id": "citrus_fried_rice",     "output_count": 1},
    {"name": "Tangy Apple Stir-Fry",  "ingredients": {"apple": 1, "ginger": 1, "garlic": 1},        "output_id": "tangy_apple_stir_fry",  "output_count": 1},
    {"name": "Fig Glazed Tofu",       "ingredients": {"fig": 1, "tofu": 1, "ginger": 1},            "output_id": "fig_glazed_tofu",       "output_count": 1},
    {"name": "Pomegranate Stir-Fry",  "ingredients": {"pomegranate": 1, "bok_choy": 1, "garlic": 1},"output_id": "pomegranate_stir_fry",  "output_count": 1},
    # --- Pacific ---
    {"name": "Coconut Rice",    "ingredients": {"rice": 2, "coconut": 1},                           "output_id": "coconut_rice",    "output_count": 2},
    {"name": "Poke Bowl",       "ingredients": {"fish": 1, "rice": 1, "scallion": 1},               "output_id": "poke_bowl",       "output_count": 1},
]

# ---------------------------------------------------------------------------
# Steamer recipes
# ---------------------------------------------------------------------------

STEAMER_RECIPES = [
    {"name": "Steamed Bun",    "ingredients": {"wheat": 2},                                      "output_id": "steamed_bun",    "output_count": 2},
    {"name": "Lotus Rice",     "ingredients": {"rice": 2, "mushroom": 1},                        "output_id": "lotus_rice",     "output_count": 1},
    {"name": "Crystal Rolls",  "ingredients": {"wheat": 1, "bok_choy": 1, "scallion": 1},       "output_id": "crystal_rolls",  "output_count": 2},
    {"name": "Steamed Egg",    "ingredients": {"egg": 2, "milk": 1},                             "output_id": "steamed_egg",    "output_count": 1},
    {"name": "Pumpkin Cake",        "ingredients": {"pumpkin": 1, "rice": 1},                    "output_id": "pumpkin_cake",        "output_count": 2},
    {"name": "Steamed Ginger Fish",   "ingredients": {"fish": 1, "ginger": 1, "scallion": 1},           "output_id": "steamed_ginger_fish",   "output_count": 1},
    {"name": "Meat Bun",             "ingredients": {"cooked_mutton": 1, "wheat": 2},                   "output_id": "meat_bun",              "output_count": 2},
    {"name": "Steamed Chicken",      "ingredients": {"raw_chicken": 1, "ginger": 1, "scallion": 1},     "output_id": "steamed_chicken",       "output_count": 1},
    {"name": "Steamed Tofu",         "ingredients": {"tofu": 1, "soy_sauce": 1, "scallion": 1},         "output_id": "steamed_tofu",          "output_count": 1},
    {"name": "Sticky Rice",          "ingredients": {"rice": 3},                                        "output_id": "sticky_rice",           "output_count": 2},
    {"name": "Veggie Dumplings",     "ingredients": {"wheat": 1, "cabbage": 1, "carrot": 1},            "output_id": "veggie_dumplings",      "output_count": 3},
    {"name": "Chicken Bun",          "ingredients": {"cooked_chicken": 1, "wheat": 2},                  "output_id": "chicken_bun",           "output_count": 2},
    {"name": "Steamed Corn",         "ingredients": {"corn": 2},                                        "output_id": "steamed_corn",          "output_count": 2},
    {"name": "Steamed Sweet Potato", "ingredients": {"sweet_potato": 2},                                "output_id": "steamed_sweet_potato",  "output_count": 2},
    {"name": "Taro Cake",            "ingredients": {"potato": 2, "rice": 1},                           "output_id": "taro_cake",             "output_count": 2},
    {"name": "Steamed Broccoli",     "ingredients": {"broccoli": 2, "garlic": 1},                       "output_id": "steamed_broccoli",      "output_count": 1},
    {"name": "Rice Noodle Roll",     "ingredients": {"wheat": 1, "scallion": 1},                        "output_id": "rice_noodle_roll",      "output_count": 2},
    {"name": "Steamed Cabbage Rolls","ingredients": {"cabbage": 1, "rice": 1, "egg": 1},                "output_id": "steamed_cabbage_rolls", "output_count": 1},
    {"name": "Pea Rice Cake",        "ingredients": {"pea": 2, "rice": 1},                              "output_id": "pea_rice_cake",         "output_count": 2},
    {"name": "Steamed Carrots",      "ingredients": {"carrot": 2, "ginger": 1},                         "output_id": "steamed_carrots",       "output_count": 1},
    {"name": "Veggie Bao",           "ingredients": {"wheat": 1, "bok_choy": 1, "mushroom": 1},         "output_id": "veggie_bao",            "output_count": 2},
    {"name": "Steamed Custard",      "ingredients": {"egg": 2, "pumpkin": 1},                           "output_id": "steamed_custard",       "output_count": 1},
    # --- Fruit steamer dishes ---
    {"name": "Lemon Steamed Fish",   "ingredients": {"lemon": 1, "fish": 1, "ginger": 1},             "output_id": "lemon_steamed_fish",    "output_count": 1},
    {"name": "Fig Sticky Rice",      "ingredients": {"fig": 2, "rice": 2},                            "output_id": "fig_sticky_rice",       "output_count": 2},
    {"name": "Pear Custard",         "ingredients": {"pear": 1, "milk": 2, "egg": 1},                 "output_id": "pear_custard",          "output_count": 1},
    # --- Pacific ---
    {"name": "Poi",                 "ingredients": {"taro": 2},                                      "output_id": "poi",                   "output_count": 1},
]

# ---------------------------------------------------------------------------
# Noodle Pot recipes
# ---------------------------------------------------------------------------

NOODLE_POT_RECIPES = [
    {"name": "Soy Sauce",     "ingredients": {"wheat": 3},                                       "output_id": "soy_sauce",     "output_count": 1},
    {"name": "Noodles",       "ingredients": {"wheat": 2},                                       "output_id": "noodles",       "output_count": 2},
    {"name": "Ramen",         "ingredients": {"noodles": 1, "soy_sauce": 1, "scallion": 1},     "output_id": "ramen",         "output_count": 1},
    {"name": "Chili Noodles", "ingredients": {"noodles": 1, "chili": 1, "garlic": 1},           "output_id": "chili_noodles", "output_count": 1},
    {"name": "Noodle Soup",   "ingredients": {"noodles": 1, "bok_choy": 1, "mushroom": 1},      "output_id": "noodle_soup",   "output_count": 1},
    {"name": "Sesame Noodles","ingredients": {"noodles": 1, "ginger": 1},                        "output_id": "sesame_noodles","output_count": 1},
    {"name": "Hot Pot Broth", "ingredients": {"mushroom": 2, "ginger": 1, "chili": 1},          "output_id": "hot_pot_broth", "output_count": 1},
    {"name": "Scallion Soup",     "ingredients": {"scallion": 2, "tofu": 1},                    "output_id": "scallion_soup",    "output_count": 1},
    {"name": "Leek & Potato Soup","ingredients": {"leek": 1, "potato": 2},                       "output_id": "leek_potato_soup", "output_count": 1},
    {"name": "Pea Soup",          "ingredients": {"pea": 2, "onion": 1},                         "output_id": "pea_soup",         "output_count": 1},
    {"name": "Fish Congee",        "ingredients": {"fish": 1, "rice": 2},                        "output_id": "fish_congee",       "output_count": 1},
    {"name": "Fish Noodle Soup",   "ingredients": {"fish": 1, "noodles": 1, "ginger": 1},       "output_id": "fish_noodle_soup",  "output_count": 1},
    {"name": "Beef Noodle Soup",   "ingredients": {"cooked_beef": 1, "noodles": 1, "scallion": 1}, "output_id": "beef_noodle_soup",  "output_count": 1},
    {"name": "Chicken Noodle Soup","ingredients": {"cooked_chicken": 1, "noodles": 1, "ginger": 1},"output_id": "chicken_noodle_soup","output_count": 1},
    # --- Italian ---
    {"name": "Spaghetti Pomodoro","ingredients": {"noodles": 1, "tomato": 1, "garlic": 1},         "output_id": "spaghetti_pomodoro","output_count": 1},
    {"name": "Pesto Gnocchi",     "ingredients": {"potato": 1, "wheat": 1, "broccoli": 1},         "output_id": "pesto_gnocchi",     "output_count": 1},
    {"name": "Puttanesca",        "ingredients": {"noodles": 1, "tomato": 1, "chili": 1},           "output_id": "puttanesca",        "output_count": 1},
    {"name": "Cacio e Pepe",      "ingredients": {"noodles": 1, "cheese": 1, "pepper": 1},          "output_id": "cacio_e_pepe",      "output_count": 1},
    {"name": "Pasta e Fagioli",   "ingredients": {"noodles": 1, "pea": 1, "carrot": 1},             "output_id": "pasta_e_fagioli",   "output_count": 1},
    # --- Middle Eastern ---
    {"name": "Lentil Vermicelli","ingredients": {"lentil": 2, "wheat": 1, "onion": 1},             "output_id": "lentil_vermicelli", "output_count": 1},
    {"name": "Chorba Frik",      "ingredients": {"bulgur": 1, "cooked_mutton": 1, "tomato": 1},    "output_id": "chorba_frik",       "output_count": 1},
    # --- Spanish ---
    {"name": "Fideos",           "ingredients": {"noodles": 1, "fish": 1, "tomato": 1},            "output_id": "fideos",            "output_count": 1},
    # --- Wild game ---
    {"name": "Venison Noodle Soup","ingredients": {"cooked_venison": 1, "noodles": 1, "scallion": 1},"output_id": "venison_noodle_soup","output_count": 1},
    # --- Salt breads ---
    {"name": "Salted Bread",   "ingredients": {"wheat": 3, "fine_salt": 1},                          "output_id": "salted_bread",   "output_count": 1},
    {"name": "Artisan Loaf",   "ingredients": {"wheat": 3, "fleur_de_sel": 1},                       "output_id": "artisan_loaf",   "output_count": 1},
    # --- Salt seasoned ---
    {"name": "Seasoned Ramen", "ingredients": {"noodles": 1, "soy_sauce": 1, "fine_salt": 1},        "output_id": "seasoned_ramen", "output_count": 1},
]

# ---------------------------------------------------------------------------
# BBQ Grill recipes
# ---------------------------------------------------------------------------

BBQ_GRILL_RECIPES = [
    {"name": "Grilled Corn",     "ingredients": {"corn": 2},                                    "output_id": "grilled_corn",     "output_count": 2},
    {"name": "Potato Wedges",    "ingredients": {"potato": 2},                                  "output_id": "potato_wedges",    "output_count": 2},
    {"name": "BBQ Eggplant",     "ingredients": {"eggplant": 1, "scallion": 1},                 "output_id": "bbq_eggplant",     "output_count": 1},
    {"name": "Grilled Mushroom", "ingredients": {"mushroom": 2, "garlic": 1},                   "output_id": "grilled_mushroom", "output_count": 2},
    {"name": "Stuffed Pepper",   "ingredients": {"pepper": 1, "rice": 1, "egg": 1},             "output_id": "stuffed_pepper",   "output_count": 1},
    {"name": "Eggplant Skewer",  "ingredients": {"eggplant": 2, "chili": 1, "scallion": 1},    "output_id": "eggplant_skewer",  "output_count": 2},
    {"name": "Corn Ribs",        "ingredients": {"corn": 1, "chili": 1, "garlic": 1},           "output_id": "corn_ribs",        "output_count": 2},
    {"name": "BBQ Tofu",         "ingredients": {"tofu": 1, "pepper": 1, "scallion": 1},        "output_id": "bbq_tofu",         "output_count": 1},
    {"name": "Roast Onion",      "ingredients": {"onion": 2, "garlic": 1},                      "output_id": "roast_onion",      "output_count": 2},
    {"name": "Grilled Cabbage",   "ingredients": {"cabbage": 2, "garlic": 1},                   "output_id": "grilled_cabbage",   "output_count": 1},
    {"name": "Sweet Potato Wedges","ingredients": {"sweet_potato": 2},                            "output_id": "sweet_potato_wedges","output_count": 2},
    {"name": "Grilled Leek",      "ingredients": {"leek": 3},                                    "output_id": "grilled_leek",      "output_count": 2},
    {"name": "Watermelon Salad",  "ingredients": {"watermelon": 2},                              "output_id": "watermelon_salad",  "output_count": 1},
    # --- Desert BBQ ---
    {"name": "Grilled Cactus",   "ingredients": {"cactus_fruit": 2},                             "output_id": "grilled_cactus",    "output_count": 2},
    # --- Meat ---
    {"name": "Cooked Mutton",    "ingredients": {"raw_mutton": 1},                                "output_id": "cooked_mutton",     "output_count": 1},
    {"name": "Cooked Beef",      "ingredients": {"raw_beef": 1},                                  "output_id": "cooked_beef",       "output_count": 1},
    {"name": "Cooked Chicken",   "ingredients": {"raw_chicken": 1},                               "output_id": "cooked_chicken",    "output_count": 1},
    # --- Meat ---
    {"name": "Mutton Skewer",    "ingredients": {"raw_mutton": 1, "chili": 1, "scallion": 1},    "output_id": "mutton_skewer",     "output_count": 2},
    {"name": "Herb Chicken",     "ingredients": {"raw_chicken": 1, "garlic": 1, "leek": 1},      "output_id": "herb_chicken",      "output_count": 1},
    {"name": "BBQ Beef Ribs",    "ingredients": {"raw_beef": 1, "pepper": 1, "garlic": 1},       "output_id": "bbq_beef_ribs",     "output_count": 1},
    # --- Fish ---
    {"name": "Grilled Fish",     "ingredients": {"fish": 1, "chili": 1, "scallion": 1},          "output_id": "grilled_fish",      "output_count": 1},
    # --- Italian ---
    {"name": "Saltimbocca",      "ingredients": {"raw_chicken": 1, "mushroom": 1, "garlic": 1},   "output_id": "saltimbocca",       "output_count": 1},
    {"name": "Bistecca",         "ingredients": {"raw_beef": 1, "garlic": 1, "pepper": 1},        "output_id": "bistecca",          "output_count": 1},
    # --- Middle Eastern ---
    {"name": "Shawarma",      "ingredients": {"cooked_chicken": 1, "flatbread": 1, "onion": 1},  "output_id": "shawarma",      "output_count": 1},
    {"name": "Kofte",         "ingredients": {"raw_beef": 1, "onion": 1, "pepper": 1},           "output_id": "kofte",         "output_count": 2},
    {"name": "Shish Tawook",  "ingredients": {"raw_chicken": 1, "garlic": 1, "onion": 1},        "output_id": "shish_tawook",  "output_count": 1},
    {"name": "Lamb Chops",    "ingredients": {"raw_mutton": 1, "garlic": 1, "rosemary": 1},       "output_id": "lamb_chops",    "output_count": 1},
    {"name": "Grld. Halloumi","ingredients": {"cheese": 2, "onion": 1},                            "output_id": "grilled_halloumi","output_count": 1},
    {"name": "Chicken Shish", "ingredients": {"raw_chicken": 2, "onion": 1},                       "output_id": "chicken_shish", "output_count": 1},
    {"name": "Lahem Mishwe",  "ingredients": {"raw_beef": 1, "pomegranate": 1, "garlic": 1},       "output_id": "lahem_mishwe",  "output_count": 1},
    # --- Spanish ---
    {"name": "Chorizo",          "ingredients": {"raw_beef": 1, "pepper": 1, "chili": 1},             "output_id": "chorizo",          "output_count": 2},
    {"name": "Pollo al Ajillo",  "ingredients": {"raw_chicken": 1, "garlic": 3},                      "output_id": "pollo_al_ajillo",  "output_count": 1},
    {"name": "Cordero Asado",    "ingredients": {"raw_mutton": 1, "garlic": 1, "rosemary": 1},         "output_id": "cordero_asado",    "output_count": 1},
    {"name": "Espetos",          "ingredients": {"fish": 2, "olive_oil": 1},                           "output_id": "espetos",          "output_count": 1},
    {"name": "Berenjena Rellena","ingredients": {"eggplant": 2, "rice": 1, "tomato": 1},               "output_id": "berenjena_rellena","output_count": 1},
    # --- Wild game ---
    {"name": "Cooked Venison",    "ingredients": {"raw_venison": 1},                                       "output_id": "cooked_venison",    "output_count": 1},
    {"name": "Cooked Boar",       "ingredients": {"raw_boar_meat": 1},                                     "output_id": "cooked_boar",       "output_count": 1},
    {"name": "Cooked Rabbit",     "ingredients": {"raw_rabbit": 1},                                        "output_id": "cooked_rabbit",     "output_count": 1},
    {"name": "Cooked Turkey",     "ingredients": {"raw_turkey": 1},                                        "output_id": "cooked_turkey",     "output_count": 1},
    {"name": "Cooked Bear",       "ingredients": {"raw_bear_meat": 1},                                     "output_id": "cooked_bear",       "output_count": 1},
    {"name": "Cooked Duck",       "ingredients": {"raw_duck": 1},                                          "output_id": "cooked_duck",       "output_count": 1},
    {"name": "Cooked Bison",      "ingredients": {"raw_bison_meat": 1},                                    "output_id": "cooked_bison",      "output_count": 1},
    {"name": "Venison Steak",     "ingredients": {"raw_venison": 1, "garlic": 1, "rosemary": 1},           "output_id": "venison_steak",     "output_count": 1},
    {"name": "Wild Boar Chop",    "ingredients": {"raw_boar_meat": 1, "chili": 1, "pepper": 1},            "output_id": "wild_boar_chop",    "output_count": 1},
    {"name": "Duck Roast",        "ingredients": {"raw_duck": 1, "garlic": 1, "onion": 1},                 "output_id": "duck_roast",        "output_count": 1},
    {"name": "Bison Steak",       "ingredients": {"raw_bison_meat": 1, "garlic": 1, "pepper": 1},          "output_id": "bison_steak",       "output_count": 1},
    {"name": "Bear Roast",        "ingredients": {"raw_bear_meat": 1, "garlic": 1, "mushroom": 1},         "output_id": "bear_roast",        "output_count": 1},
    {"name": "Game Skewers",      "ingredients": {"raw_venison": 1, "raw_rabbit": 1, "chili": 1},          "output_id": "game_skewers",      "output_count": 2},
    {"name": "Elk Medallion",     "ingredients": {"raw_venison": 1, "mushroom": 1, "garlic": 1},           "output_id": "elk_medallion",     "output_count": 1},
    {"name": "Cooked Pheasant",   "ingredients": {"raw_pheasant": 1},                                       "output_id": "cooked_pheasant",   "output_count": 1},
    {"name": "Cooked Goose",      "ingredients": {"raw_goose": 1},                                          "output_id": "cooked_goose",      "output_count": 1},
    {"name": "Cooked Crocodile",  "ingredients": {"raw_crocodile": 1},                                      "output_id": "cooked_crocodile",  "output_count": 1},
    {"name": "Roast Pheasant",    "ingredients": {"raw_pheasant": 1, "garlic": 1, "mushroom": 1},           "output_id": "roast_pheasant",    "output_count": 1},
    {"name": "Goose Confit",      "ingredients": {"raw_goose": 1, "garlic": 2, "onion": 1},                 "output_id": "goose_confit",      "output_count": 1},
    {"name": "Bighorn Roast",     "ingredients": {"raw_mutton": 1, "rosemary": 1, "garlic": 1},             "output_id": "bighorn_roast",     "output_count": 1},
    {"name": "Warthog Skewer",    "ingredients": {"raw_boar_meat": 1, "chili": 1, "scallion": 1},           "output_id": "warthog_skewer",    "output_count": 2},
    # --- Typed cheese dishes ---
    {"name": "Smoked Cheese Melt","ingredients": {"cheese_smoked": 1, "bread": 1, "tomato": 1},            "output_id": "smoked_cheese_melt","output_count": 1},
    {"name": "Grilled Cured",     "ingredients": {"cheese_cured": 1, "pepper": 1},                         "output_id": "grilled_cured_cheese","output_count": 1},
    {"name": "Stretched Caprese", "ingredients": {"cheese_stretched": 1, "tomato": 1},                      "output_id": "stretched_caprese", "output_count": 1},
    # --- Salt cured / seasoned ---
    {"name": "Salt-Cured Mutton",  "ingredients": {"raw_mutton": 1, "coarse_salt": 2},                      "output_id": "salt_cured_mutton",  "output_count": 1},
    {"name": "Salted Fish",        "ingredients": {"fish": 1, "coarse_salt": 1},                             "output_id": "salted_fish",        "output_count": 1},
    {"name": "Salt-Cured Venison", "ingredients": {"raw_venison": 1, "coarse_salt": 2},                      "output_id": "salt_cured_venison", "output_count": 1},
    # --- Grilled fruit ---
    {"name": "Grilled Figs",            "ingredients": {"fig": 2},                                          "output_id": "grilled_figs",            "output_count": 2},
    {"name": "Caramelized Pears",       "ingredients": {"pear": 2},                                         "output_id": "caramelized_pears",       "output_count": 1},
    {"name": "Glazed Apple",            "ingredients": {"apple": 2},                                        "output_id": "glazed_apple",            "output_count": 2},
    {"name": "Grilled Pear & Cheese",   "ingredients": {"pear": 1, "cheese": 1},                            "output_id": "grilled_pear_cheese",     "output_count": 1},
    {"name": "Citrus Glazed Chicken",   "ingredients": {"lemon": 1, "raw_chicken": 1, "garlic": 1},         "output_id": "citrus_glazed_chicken",   "output_count": 1},
    {"name": "Fig & Mutton Skewer",     "ingredients": {"fig": 2, "raw_mutton": 1},                         "output_id": "fig_meat_skewer",         "output_count": 2},
    {"name": "Pomegranate Chicken",     "ingredients": {"pomegranate": 1, "raw_chicken": 1},                "output_id": "pomegranate_chicken",     "output_count": 1},
    {"name": "Grilled Watermelon",          "ingredients": {"watermelon": 2},                                     "output_id": "grilled_watermelon",          "output_count": 2},
    # --- Grilled batch 3 ---
    {"name": "Apple & Pork Skewer",         "ingredients": {"apple": 1, "raw_boar_meat": 1},                         "output_id": "apple_pork_skewer",           "output_count": 2},
    {"name": "Lemon Herb Fish",             "ingredients": {"lemon": 1, "fish": 1, "rosemary": 1},                   "output_id": "lemon_herb_fish",             "output_count": 1},
    {"name": "Fig Glazed Pheasant",         "ingredients": {"fig": 1, "raw_pheasant": 1},                            "output_id": "fig_glazed_pheasant",         "output_count": 1},
    {"name": "Pomegranate Venison Steak",   "ingredients": {"pomegranate": 1, "raw_venison": 1, "onion": 1},         "output_id": "pomegranate_venison_steak",   "output_count": 1},
    {"name": "Grilled Lemon Corn",          "ingredients": {"lemon": 1, "corn": 2},                                  "output_id": "grilled_lemon_corn",          "output_count": 2},
    # --- Pacific ---
    {"name": "Roasted Breadfruit",         "ingredients": {"breadfruit": 2},                                         "output_id": "roasted_breadfruit",          "output_count": 2},
]

# ---------------------------------------------------------------------------
# Clay Pot recipes
# ---------------------------------------------------------------------------

CLAY_POT_RECIPES = [
    {"name": "Potato Stew",          "ingredients": {"potato": 2, "carrot": 1},                      "output_id": "potato_stew",          "output_count": 1},
    {"name": "Cabbage Soup",         "ingredients": {"cabbage": 2, "onion": 1},                       "output_id": "cabbage_soup",         "output_count": 1},
    {"name": "Braised Eggplant",     "ingredients": {"eggplant": 1, "garlic": 1, "soy_sauce": 1},    "output_id": "braised_eggplant",     "output_count": 1},
    {"name": "Pepper Soup",          "ingredients": {"pepper": 1, "mushroom": 1, "tofu": 1},          "output_id": "pepper_soup",          "output_count": 1},
    {"name": "Onion Broth",          "ingredients": {"onion": 2, "ginger": 1},                        "output_id": "onion_broth",          "output_count": 1},
    {"name": "Potato Mushroom Stew", "ingredients": {"potato": 1, "mushroom": 2, "onion": 1},         "output_id": "potato_mushroom_stew", "output_count": 1},
    {"name": "Stuffed Cabbage",      "ingredients": {"cabbage": 1, "rice": 1, "egg": 1},              "output_id": "stuffed_cabbage",      "output_count": 1},
    {"name": "Braised Tofu",         "ingredients": {"tofu": 1, "bok_choy": 1, "soy_sauce": 1},       "output_id": "braised_tofu",         "output_count": 1},
    {"name": "Pepper Pot",           "ingredients": {"pepper": 2, "chili": 1, "garlic": 1},           "output_id": "pepper_pot",           "output_count": 1},
    {"name": "Harvest Stew",      "ingredients": {"carrot": 1, "potato": 1, "cabbage": 1},          "output_id": "harvest_stew",     "output_count": 1},
    {"name": "Beet Soup",         "ingredients": {"beet": 2, "onion": 1},                            "output_id": "beet_soup",        "output_count": 1},
    {"name": "Root Medley",       "ingredients": {"beet": 1, "turnip": 1, "carrot": 1},              "output_id": "root_medley",      "output_count": 1},
    {"name": "Radish Kimchi",     "ingredients": {"radish": 2, "chili": 1, "garlic": 1},             "output_id": "radish_kimchi",    "output_count": 1},
    {"name": "Stuffed Zucchini",  "ingredients": {"zucchini": 2, "rice": 1},                         "output_id": "stuffed_zucchini", "output_count": 1},
    {"name": "Garden Soup",       "ingredients": {"broccoli": 1, "pea": 1, "celery": 1},             "output_id": "garden_soup",      "output_count": 1},
    # --- Meat ---
    {"name": "Beef Stew",           "ingredients": {"cooked_beef": 1, "potato": 1, "carrot": 1},  "output_id": "beef_stew",           "output_count": 1},
    {"name": "Chicken Mushroom Pot","ingredients": {"cooked_chicken": 1, "mushroom": 1, "onion": 1},"output_id": "chicken_mushroom_pot","output_count": 1},
    {"name": "Mutton Hotpot",       "ingredients": {"raw_mutton": 1, "chili": 1, "tomato": 1},    "output_id": "mutton_hotpot",       "output_count": 1},
    {"name": "Braised Chicken",     "ingredients": {"raw_chicken": 1, "soy_sauce": 1, "ginger": 1},"output_id": "braised_chicken",    "output_count": 1},
    # --- Fish ---
    {"name": "Sichuan Boiled Fish", "ingredients": {"fish": 1, "chili": 2, "bok_choy": 1},        "output_id": "sichuan_boiled_fish", "output_count": 1},
    {"name": "West Lake Fish",      "ingredients": {"fish": 1, "ginger": 1, "mushroom": 1},       "output_id": "west_lake_fish",      "output_count": 1},
    # --- Desert clay pot ---
    {"name": "Date Palm Broth",  "ingredients": {"date_palm_fruit": 2, "onion": 1},                "output_id": "date_palm_broth",  "output_count": 1},
    # --- Italian ---
    {"name": "Minestrone",       "ingredients": {"tomato": 1, "carrot": 1, "onion": 1},            "output_id": "minestrone",       "output_count": 1},
    {"name": "Ossobuco",         "ingredients": {"cooked_beef": 1, "onion": 1, "carrot": 1},       "output_id": "ossobuco",         "output_count": 1},
    {"name": "Ribollita",        "ingredients": {"cabbage": 1, "potato": 1, "tomato": 1},          "output_id": "ribollita",        "output_count": 1},
    {"name": "Cacciatore",       "ingredients": {"raw_chicken": 1, "tomato": 1, "mushroom": 1},    "output_id": "cacciatore",       "output_count": 1},
    {"name": "Zuppa di Pesce",   "ingredients": {"fish": 1, "tomato": 1, "onion": 1},              "output_id": "zuppa_di_pesce",   "output_count": 1},
    {"name": "Acquacotta",       "ingredients": {"celery": 1, "onion": 1, "egg": 1},               "output_id": "acquacotta",       "output_count": 1},
    # --- Middle Eastern ---
    {"name": "Hummus",           "ingredients": {"chickpea": 3, "tahini": 1, "garlic": 1},                    "output_id": "hummus",           "output_count": 1},
    {"name": "Lentil Soup",      "ingredients": {"lentil": 3, "onion": 1, "tomato": 1},                       "output_id": "lentil_soup",      "output_count": 1},
    {"name": "Baba Ghanoush",    "ingredients": {"eggplant": 2, "tahini": 1, "garlic": 1},                    "output_id": "baba_ghanoush",    "output_count": 1},
    {"name": "Shakshuka",        "ingredients": {"tomato": 3, "egg": 2, "onion": 1},                          "output_id": "shakshuka",        "output_count": 1},
    {"name": "Mansaf",           "ingredients": {"cooked_mutton": 1, "rice": 2, "onion": 1},                  "output_id": "mansaf",           "output_count": 1},
    {"name": "Mujaddara",        "ingredients": {"lentil": 2, "rice": 1, "onion": 2},                         "output_id": "mujaddara",        "output_count": 1},
    {"name": "Ful Medames",      "ingredients": {"chickpea": 2, "tomato": 1, "garlic": 2},                    "output_id": "ful_medames",      "output_count": 1},
    {"name": "Harira",           "ingredients": {"lentil": 2, "tomato": 2, "onion": 1},                       "output_id": "harira",           "output_count": 1},
    {"name": "Tagine",           "ingredients": {"cooked_mutton": 1, "date_palm_fruit": 2, "onion": 1},       "output_id": "tagine",           "output_count": 1},
    {"name": "Maqluba",          "ingredients": {"cooked_chicken": 1, "eggplant": 1, "rice": 2},              "output_id": "maqluba",          "output_count": 1},
    {"name": "Couscous Royale",  "ingredients": {"couscous": 1, "cooked_mutton": 1, "carrot": 1},             "output_id": "couscous_royale",  "output_count": 1},
    {"name": "Fatteh",           "ingredients": {"chickpea": 2, "flatbread": 1, "egg": 1},                    "output_id": "fatteh",           "output_count": 1},
    {"name": "Fasolia",          "ingredients": {"chickpea": 2, "tomato": 1, "garlic": 1},                    "output_id": "fasolia",          "output_count": 1},
    {"name": "Bamia",            "ingredients": {"zucchini": 2, "tomato": 1, "garlic": 1},                    "output_id": "bamia",            "output_count": 1},
    {"name": "Tepsi",            "ingredients": {"eggplant": 2, "tomato": 2, "onion": 1},                     "output_id": "tepsi",            "output_count": 1},
    {"name": "Djej bil Lemon",   "ingredients": {"cooked_chicken": 1, "garlic": 2, "onion": 1},               "output_id": "djej_bil_lemon",   "output_count": 1},
    {"name": "Freekeh Soup",     "ingredients": {"bulgur": 1, "cooked_chicken": 1, "onion": 1},               "output_id": "freekeh_soup",     "output_count": 1},
    # --- Wild game ---
    {"name": "Venison Stew",       "ingredients": {"cooked_venison": 1, "potato": 1, "carrot": 1},          "output_id": "venison_stew",       "output_count": 1},
    {"name": "Wild Boar Casserole","ingredients": {"raw_boar_meat": 1, "onion": 1, "mushroom": 1},          "output_id": "wild_boar_casserole","output_count": 1},
    {"name": "Hunter's Pot",       "ingredients": {"cooked_venison": 1, "carrot": 1, "onion": 1},           "output_id": "hunters_pot",        "output_count": 1},
    {"name": "Duck Confit",        "ingredients": {"raw_duck": 1, "onion": 1, "garlic": 1},                 "output_id": "duck_confit",        "output_count": 1},
    {"name": "Bison Chili",        "ingredients": {"raw_bison_meat": 1, "chili": 1, "tomato": 1},           "output_id": "bison_chili",        "output_count": 1},
    {"name": "Bear Broth",         "ingredients": {"raw_bear_meat": 1, "onion": 1, "ginger": 1},            "output_id": "bear_broth",         "output_count": 1},
    {"name": "Rabbit Fricassee",   "ingredients": {"raw_rabbit": 1, "mushroom": 1, "garlic": 1},            "output_id": "rabbit_fricassee",   "output_count": 1},
    {"name": "Wild Turkey Soup",   "ingredients": {"raw_turkey": 1, "celery": 1, "onion": 1},               "output_id": "wild_turkey_soup",   "output_count": 1},
    {"name": "Moose Stew",         "ingredients": {"raw_venison": 2, "potato": 1, "carrot": 1},             "output_id": "moose_stew",         "output_count": 1},
    {"name": "Crocodile Stew",     "ingredients": {"raw_crocodile": 1, "tomato": 1, "onion": 1},            "output_id": "croc_stew",          "output_count": 1},
    {"name": "Goose Soup",         "ingredients": {"raw_goose": 1, "onion": 1, "carrot": 1},                "output_id": "goose_soup",         "output_count": 1},
    {"name": "Keshkek",          "ingredients": {"cooked_mutton": 1, "bulgur": 2},                            "output_id": "keshkek",          "output_count": 1},
    {"name": "Thareed",          "ingredients": {"cooked_mutton": 1, "flatbread": 1, "tomato": 1},            "output_id": "thareed",          "output_count": 1},
    {"name": "Kofta bil Tahini", "ingredients": {"kofte": 1, "tahini": 1},                                    "output_id": "kofta_bil_tahini", "output_count": 1},
    # --- Spanish ---
    {"name": "Paella",           "ingredients": {"rice": 2, "fish": 1, "saffron": 1},                        "output_id": "paella",           "output_count": 1},
    {"name": "Cocido Madrileño", "ingredients": {"cooked_beef": 1, "potato": 1, "cabbage": 1},               "output_id": "cocido_madrileno", "output_count": 1},
    {"name": "Puchero",          "ingredients": {"cooked_chicken": 1, "potato": 2, "carrot": 1},             "output_id": "puchero",          "output_count": 1},
    {"name": "Potaje",           "ingredients": {"chickpea": 2, "cabbage": 1, "onion": 1},                   "output_id": "potaje",           "output_count": 1},
    {"name": "Rabo de Toro",     "ingredients": {"cooked_beef": 1, "onion": 1, "tomato": 1},                 "output_id": "rabo_de_toro",     "output_count": 1},
    {"name": "Fabada",           "ingredients": {"chickpea": 2, "chorizo": 1, "onion": 1},                   "output_id": "fabada",           "output_count": 1},
    # --- Typed cheese dishes ---
    {"name": "Cheese Soup",      "ingredients": {"cheese_washed_rind": 1, "onion": 2, "carrot": 1},         "output_id": "cheese_soup",      "output_count": 1},
    {"name": "Monastic Stew",    "ingredients": {"cheese_monastery": 1, "potato": 2, "onion": 1},           "output_id": "monastic_stew",    "output_count": 1},
    {"name": "Truffle Bisque",   "ingredients": {"cheese_truffled": 1, "potato": 1, "onion": 1},            "output_id": "truffle_bisque",   "output_count": 1},
    # --- Salt cured / seasoned ---
    {"name": "Salt-Cured Beef",    "ingredients": {"cooked_beef": 1, "coarse_salt": 2},                     "output_id": "salt_cured_beef",     "output_count": 1},
    {"name": "Salted Lentil Soup", "ingredients": {"lentil": 3, "onion": 1, "tomato": 1, "fine_salt": 1},  "output_id": "salted_lentil_soup",  "output_count": 1},
    {"name": "Salted Potato Soup", "ingredients": {"potato": 2, "onion": 1, "fine_salt": 1},                "output_id": "salted_potato_soup",  "output_count": 1},
    {"name": "Brined Cabbage",       "ingredients": {"cabbage": 2, "coarse_salt": 1},                      "output_id": "brined_cabbage",       "output_count": 2},
    # --- Fruit compotes & stews ---
    {"name": "Lemon Posset",            "ingredients": {"lemon": 2, "milk": 2},                             "output_id": "lemon_posset",            "output_count": 1},
    {"name": "Watermelon Sorbet",       "ingredients": {"watermelon": 2, "lemon": 1},                       "output_id": "watermelon_sorbet",       "output_count": 2},
    {"name": "Apple Cider Stew",        "ingredients": {"apple": 2, "potato": 1, "onion": 1},               "output_id": "apple_cider_stew",        "output_count": 1},
    {"name": "Lemon Herb Broth",        "ingredients": {"lemon": 1, "onion": 1, "garlic": 1},               "output_id": "lemon_herb_broth",        "output_count": 2},
    {"name": "Fig & Lamb Tagine",       "ingredients": {"fig": 1, "raw_mutton": 1, "onion": 1},             "output_id": "fig_lamb_tagine",         "output_count": 1},
    {"name": "Pomegranate Chicken Stew","ingredients": {"pomegranate": 1, "raw_chicken": 1, "onion": 1},    "output_id": "pomegranate_chicken_stew","output_count": 1},
    {"name": "Pear & Ginger Soup",      "ingredients": {"pear": 2, "ginger": 1},                            "output_id": "pear_ginger_soup",        "output_count": 1},
    # --- Fruit clay pot batch 3 ---
    {"name": "Apple & Onion Soup",      "ingredients": {"apple": 1, "onion": 2},                            "output_id": "apple_onion_soup",        "output_count": 1},
    {"name": "Fig & Chickpea Stew",     "ingredients": {"fig": 1, "chickpea": 2, "onion": 1},               "output_id": "fig_chickpea_stew",       "output_count": 1},
    {"name": "Lemon Lentil Soup",       "ingredients": {"lemon": 1, "lentil": 3},                           "output_id": "lemon_lentil_soup",       "output_count": 1},
    {"name": "Pear & Pumpkin Soup",     "ingredients": {"pear": 1, "pumpkin": 2},                           "output_id": "pear_pumpkin_soup",       "output_count": 1},
    {"name": "Watermelon Gazpacho",     "ingredients": {"watermelon": 2, "tomato": 1},                      "output_id": "watermelon_gazpacho",     "output_count": 1},
    {"name": "Spiced Pear Compote",  "ingredients": {"pear": 2, "ginger": 1},                               "output_id": "spiced_pear_compote",  "output_count": 1},
    {"name": "Fig & Date Pudding",   "ingredients": {"fig": 2, "date_palm_fruit": 1},                       "output_id": "fig_date_pudding",     "output_count": 1},
    {"name": "Pomegranate Stew",     "ingredients": {"pomegranate": 1, "onion": 1, "tomato": 1},            "output_id": "pomegranate_stew",     "output_count": 1},
    # --- Pacific ---
    {"name": "Laplap",               "ingredients": {"taro": 2, "fish": 1},                                 "output_id": "laplap",               "output_count": 1},
    {"name": "Coconut Fish Curry",   "ingredients": {"fish": 1, "coconut": 1, "ginger": 1},                "output_id": "coconut_fish_curry",   "output_count": 1},
]

# ---------------------------------------------------------------------------
# Desert Forge recipes (ingredient dict → output, same pattern as cooking stations)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Glass Kiln recipes (sand + dye extracts → glass blocks)
# ---------------------------------------------------------------------------

GLASS_KILN_RECIPES = [
    {"name": "Clear Glass",             "ingredients": {"sand_grain": 3},                                         "output_id": "clear_glass",           "output_count": 2},
    {"name": "Stained Glass (Golden)",  "ingredients": {"sand_grain": 2, "dye_extract_golden": 1},               "output_id": "stained_glass_golden",  "output_count": 2},
    {"name": "Stained Glass (Crimson)", "ingredients": {"sand_grain": 2, "dye_extract_crimson": 1},              "output_id": "stained_glass_crimson", "output_count": 2},
    {"name": "Stained Glass (Rose)",    "ingredients": {"sand_grain": 2, "dye_extract_rose": 1},                 "output_id": "stained_glass_rose",    "output_count": 2},
    {"name": "Stained Glass (Cobalt)",  "ingredients": {"sand_grain": 2, "dye_extract_cobalt": 1},               "output_id": "stained_glass_cobalt",  "output_count": 2},
    {"name": "Stained Glass (Violet)",  "ingredients": {"sand_grain": 2, "dye_extract_violet": 1},               "output_id": "stained_glass_violet",  "output_count": 2},
    {"name": "Stained Glass (Verdant)", "ingredients": {"sand_grain": 2, "dye_extract_verdant": 1},              "output_id": "stained_glass_verdant", "output_count": 2},
    {"name": "Stained Glass (Amber)",   "ingredients": {"sand_grain": 2, "dye_extract_amber": 1},                "output_id": "stained_glass_amber",   "output_count": 2},
    {"name": "Stained Glass (Ivory)",   "ingredients": {"sand_grain": 2, "dye_extract_ivory": 1},                "output_id": "stained_glass_ivory",   "output_count": 2},
    {"name": "Cathedral Window",        "ingredients": {"sand_grain": 2, "crystal_shard": 1, "dye_extract_cobalt": 1}, "output_id": "cathedral_window", "output_count": 1},
    {"name": "Mosaic Glass",            "ingredients": {"sand_grain": 1, "dye_extract_golden": 1, "dye_extract_cobalt": 1}, "output_id": "mosaic_glass", "output_count": 2},
    {"name": "Smoked Glass",            "ingredients": {"sand_grain": 2, "coal": 2},                              "output_id": "smoked_glass",          "output_count": 2},
    # --- Additional glass varieties ---
    {"name": "Ribbed Glass",            "ingredients": {"sand_grain": 3, "iron_chunk": 1},                         "output_id": "ribbed_glass",          "output_count": 2},
    {"name": "Hammered Glass",          "ingredients": {"sand_grain": 3, "stone_chip": 1},                        "output_id": "hammered_glass",        "output_count": 2},
    {"name": "Crackled Glass",          "ingredients": {"sand_grain": 2, "crystal_shard": 1, "coal": 1},          "output_id": "crackled_glass",        "output_count": 2},
    {"name": "Oculus Window",           "ingredients": {"sand_grain": 2, "crystal_shard": 2},                     "output_id": "oculus_window",         "output_count": 1},
    {"name": "Lancet Window",           "ingredients": {"sand_grain": 2, "dye_extract_cobalt": 1, "iron_chunk": 1}, "output_id": "lancet_window",       "output_count": 1},
    {"name": "Diamond Pane",            "ingredients": {"sand_grain": 3, "iron_chunk": 1, "coal": 1},             "output_id": "diamond_pane",          "output_count": 2},
    {"name": "Sea Glass",               "ingredients": {"sand_grain": 2, "dye_extract_verdant": 1, "crystal_shard": 1}, "output_id": "sea_glass",       "output_count": 2},
    {"name": "Mirror Glass",            "ingredients": {"sand_grain": 2, "iron_chunk": 2, "gold_nugget": 1},      "output_id": "mirror_glass",          "output_count": 1},
    {"name": "Iridescent Glass",        "ingredients": {"sand_grain": 1, "dye_extract_violet": 1, "dye_extract_amber": 1, "crystal_shard": 1}, "output_id": "iridescent_glass", "output_count": 2},
    {"name": "Sunset Glass",            "ingredients": {"sand_grain": 2, "dye_extract_amber": 1, "dye_extract_crimson": 1}, "output_id": "sunset_glass", "output_count": 2},
    {"name": "Obsidian Glass",          "ingredients": {"sand_grain": 1, "obsidian_slab": 2},                     "output_id": "obsidian_glass",        "output_count": 2},
    {"name": "Crystal Glass",           "ingredients": {"sand_grain": 1, "crystal_shard": 3},                     "output_id": "crystal_glass",         "output_count": 2},
]

# ---------------------------------------------------------------------------
FORGE_RECIPES = [
    {"name": "Desert Glass",  "ingredients": {"sand_grain": 3},                              "output_id": "desert_glass",  "output_count": 1},
    {"name": "Sandstone",     "ingredients": {"sand_grain": 4, "stone_chip": 1},             "output_id": "sandstone",     "output_count": 2},
    {"name": "Tempered Iron", "ingredients": {"iron_chunk": 2, "coal": 3},                   "output_id": "tempered_iron", "output_count": 1},
    {"name": "Cactus Fiber",     "ingredients": {"cactus_spine": 3},                         "output_id": "cactus_fiber",     "output_count": 2},
    {"name": "Agave Syrup",      "ingredients": {"agave": 3},                                "output_id": "agave_syrup",      "output_count": 1},
    # --- Sonoran plant processing ---
    {"name": "Prickly Pear Dye", "ingredients": {"prickly_pear_fruit": 3},                  "output_id": "prickly_pear_dye", "output_count": 2},
    {"name": "Saguaro Nectar",   "ingredients": {"saguaro_fruit": 2, "agave": 1},           "output_id": "saguaro_nectar",   "output_count": 1},
    {"name": "Ocotillo Wax",     "ingredients": {"ocotillo_flower": 3},                     "output_id": "ocotillo_wax",     "output_count": 2},
    {"name": "Cholla Needle",    "ingredients": {"cholla_joint": 3},                        "output_id": "cholla_needle",    "output_count": 2},
    {"name": "Desert Mortar",    "ingredients": {"sandstone": 2, "agave_syrup": 1},         "output_id": "desert_mortar",    "output_count": 2},
    {"name": "Desert Pitch",     "ingredients": {"cholla_joint": 1, "agave_syrup": 1},      "output_id": "desert_pitch",     "output_count": 2},
]

# ---------------------------------------------------------------------------
# Smithing Forge recipes — available at FORGE_BLOCK
# ---------------------------------------------------------------------------

SMITHING_FORGE_RECIPES = [
    {"name": "Steel Ingot", "ingredients": {"iron_bar": 2, "coal": 1}, "output_id": "steel_ingot", "output_count": 1},
]

# ---------------------------------------------------------------------------
# Artisan Bench recipes — refine raw materials into decorative building blocks
# ---------------------------------------------------------------------------

ARTISAN_RECIPES = [
    {"name": "Acanthus Panel",       "ingredients": {"limestone_block": 1, "stone_chip": 2},              "output_id": "acanthus_panel",          "output_count": 2},
    {"name": "Adobe Brick",          "ingredients": {"clay": 2, "sand_grain": 1},                         "output_id": "adobe_brick",             "output_count": 2},
    {"name": "African Mud Brick",    "ingredients": {"clay": 2, "lumber": 1},                             "output_id": "african_mud_brick",       "output_count": 2},
    {"name": "Amber Tile",           "ingredients": {"sand_grain": 2, "gold_nugget": 1},                  "output_id": "amber_tile",              "output_count": 2},
    {"name": "Amethyst Block",       "ingredients": {"stone_chip": 1, "crystal_shard": 2},                "output_id": "amethyst_block",          "output_count": 2},
    {"name": "Andean Textile",       "ingredients": {"lumber": 1, "ruby": 1, "gold_nugget": 1},           "output_id": "andean_textile",          "output_count": 2},
    {"name": "Arabesque Panel",      "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "arabesque_panel",         "output_count": 2},
    {"name": "Armenian Khachkar",    "ingredients": {"stone_chip": 2, "ruby": 1},                         "output_id": "armenian_khachkar",       "output_count": 2},
    {"name": "Art Deco Panel",       "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "art_deco_panel",          "output_count": 2},
    {"name": "Art Nouveau Panel",    "ingredients": {"limestone_block": 1, "crystal_shard": 1},           "output_id": "art_nouveau_panel",       "output_count": 2},
    {"name": "Ash Plank",            "ingredients": {"lumber": 2, "sand_grain": 1},                       "output_id": "ash_plank",               "output_count": 2},
    {"name": "Ashlar Block",         "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "ashlar_block",            "output_count": 2},
    {"name": "Aztec Sunstone",       "ingredients": {"basalt_shard": 1, "stone_chip": 1, "obsidian_slab": 1}, "output_id": "aztec_sunstone",       "output_count": 2},
    {"name": "Azulejo Tile",         "ingredients": {"clay": 1, "crystal_shard": 1},                      "output_id": "azulejo_tile",            "output_count": 2},
    {"name": "Bamboo Panel",         "ingredients": {"lumber": 1, "sand_grain": 1},                       "output_id": "bamboo_panel",            "output_count": 2},
    {"name": "Bamboo Screen",        "ingredients": {"lumber": 2, "sand_grain": 1},                       "output_id": "bamboo_screen",           "output_count": 2},
    {"name": "Baroque Ornament",     "ingredients": {"limestone_block": 1, "gold_nugget": 2},             "output_id": "baroque_ornament",        "output_count": 2},
    {"name": "Baroque Trim",         "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "baroque_trim",            "output_count": 2},
    {"name": "Barrel Vault",         "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "barrel_vault",            "output_count": 2},
    {"name": "Basalt Column",        "ingredients": {"basalt_shard": 2, "coal": 1},                       "output_id": "basalt_column",           "output_count": 2},
    {"name": "Benin Relief",         "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "benin_relief",            "output_count": 2},
    {"name": "Blue & White Tile",    "ingredients": {"clay": 1, "crystal_shard": 1, "sand_grain": 1},     "output_id": "blue_white_tile",         "output_count": 2},
    {"name": "Brick Nogging",        "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "brick_nogging",           "output_count": 2},
    {"name": "Bronze Door",          "ingredients": {"iron_chunk": 2, "gold_nugget": 1},                  "output_id": "bronze_door",             "output_count": 1},
    {"name": "Brutalist Panel",      "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "brutalist_panel",         "output_count": 2},
    {"name": "Byzantine Mosaic",     "ingredients": {"sand_grain": 1, "gold_nugget": 2},                  "output_id": "byzantine_mosaic",        "output_count": 2},
    {"name": "Carved Plaster",       "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "carved_plaster",          "output_count": 2},
    {"name": "Cedar Panel",          "ingredients": {"lumber": 2, "iron_chunk": 1},                       "output_id": "cedar_panel",             "output_count": 2},
    {"name": "Celtic Knotwork",      "ingredients": {"basalt_shard": 1, "stone_chip": 1, "obsidian_slab": 1}, "output_id": "celtic_knotwork",      "output_count": 2},
    {"name": "Ceramic Planter",      "ingredients": {"clay": 2, "crystal_shard": 1},                      "output_id": "ceramic_planter",         "output_count": 2},
    {"name": "Charcoal Plank",       "ingredients": {"lumber": 1, "coal": 1},                             "output_id": "charcoal_plank",          "output_count": 2},
    {"name": "Chequerboard Marble",  "ingredients": {"stone_chip": 1, "crystal_shard": 1},                "output_id": "chequerboard_marble",     "output_count": 2},
    {"name": "Chevron Stone",        "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "chevron_stone",           "output_count": 2},
    {"name": "Cinnabar Wall",        "ingredients": {"limestone_block": 2, "ruby": 1},                    "output_id": "cinnabar_wall",           "output_count": 2},
    {"name": "Cloud Motif",          "ingredients": {"limestone_block": 1, "stone_chip": 1},              "output_id": "cloud_motif",             "output_count": 2},
    {"name": "Cobalt Door",          "ingredients": {"lumber": 2, "crystal_shard": 1, "gold_nugget": 1},  "output_id": "cobalt_door",             "output_count": 1},
    {"name": "Cobblestone",          "ingredients": {"stone_chip": 3},                                    "output_id": "cobblestone",             "output_count": 3},
    {"name": "Coffered Ceiling",     "ingredients": {"limestone_block": 3},                               "output_id": "coffered_ceiling",        "output_count": 2},
    {"name": "Coin Tile",            "ingredients": {"stone_chip": 1, "sand_grain": 1},                   "output_id": "coin_tile",               "output_count": 2},
    {"name": "Copper Tile",          "ingredients": {"stone_chip": 1, "iron_chunk": 1},                   "output_id": "copper_tile",             "output_count": 2},
    {"name": "Cornice",              "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "cornice_block",           "output_count": 2},
    {"name": "Craftsman Panel",      "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "craftsman_panel",         "output_count": 2},
    {"name": "Cream Brick",          "ingredients": {"sand_grain": 3},                                    "output_id": "cream_brick",             "output_count": 2},
    {"name": "Crenellation",         "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "crenellation",            "output_count": 2},
    {"name": "Crimson Brick",        "ingredients": {"dirt_clump": 2, "ruby": 1},                         "output_id": "crimson_brick",           "output_count": 2},
    {"name": "Crimson Cedar Door",   "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "crimson_cedar_door",      "output_count": 1},
    {"name": "Dancheong",            "ingredients": {"lumber": 1, "ruby": 1, "crystal_shard": 1},         "output_id": "dancheong",               "output_count": 2},
    {"name": "Dark Slate Roof",      "ingredients": {"magmatic_shard": 1, "coal": 1},                     "output_id": "dark_slate_roof",         "output_count": 2},
    {"name": "Dentil Trim",          "ingredients": {"limestone_block": 2},                               "output_id": "dentil_trim",             "output_count": 2},
    {"name": "Diagonal Tile",        "ingredients": {"clay": 1, "sand_grain": 2},                         "output_id": "diagonal_tile",           "output_count": 2},
    {"name": "Dougong",              "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "dougong",                 "output_count": 2},
    {"name": "Dragon Tile",          "ingredients": {"magmatic_shard": 1, "stone_chip": 1, "crystal_shard": 1}, "output_id": "dragon_tile",         "output_count": 2},
    {"name": "Driftwood Plank",      "ingredients": {"lumber": 1, "sand_grain": 2},                       "output_id": "driftwood_plank",         "output_count": 2},
    {"name": "Dutch Gable",          "ingredients": {"stone_chip": 1, "dirt_clump": 2},                   "output_id": "dutch_gable",             "output_count": 2},
    {"name": "Ebony Plank",          "ingredients": {"lumber": 2, "obsidian_slab": 1},                    "output_id": "ebony_plank",             "output_count": 2},
    {"name": "Egyptian Frieze",      "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "egyptian_frieze",         "output_count": 2},
    {"name": "Encaustic Tile",       "ingredients": {"clay": 1, "sand_grain": 1},                         "output_id": "encaustic_tile",          "output_count": 2},
    {"name": "English Bond",         "ingredients": {"stone_chip": 1, "dirt_clump": 2},                   "output_id": "english_bond",            "output_count": 2},
    {"name": "Fan Vault",            "ingredients": {"limestone_block": 2, "crystal_shard": 1},           "output_id": "fan_vault",               "output_count": 2},
    {"name": "Flemish Brick",        "ingredients": {"stone_chip": 2, "ruby": 1},                         "output_id": "flemish_brick",           "output_count": 2},
    {"name": "Fluted Column",        "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "fluted_column",           "output_count": 2},
    {"name": "Frosted Glass",        "ingredients": {"sand_grain": 2, "crystal_shard": 1},                "output_id": "frosted_glass",           "output_count": 2},
    {"name": "Garden Rock",          "ingredients": {"basalt_shard": 1, "stone_chip": 1, "obsidian_slab": 1}, "output_id": "garden_rock_block",    "output_count": 2},
    {"name": "Gargoyle Block",       "ingredients": {"basalt_shard": 1, "stone_chip": 1, "obsidian_slab": 1}, "output_id": "gargoyle_block",       "output_count": 2},
    {"name": "Georgian Fanlight",    "ingredients": {"sand_grain": 2, "iron_chunk": 1},                   "output_id": "georgian_fanlight",       "output_count": 2},
    {"name": "Gilded Brick",         "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "gilded_brick",            "output_count": 2},
    {"name": "Gilded Door",          "ingredients": {"lumber": 2, "gold_nugget": 2},                      "output_id": "gilded_door",             "output_count": 1},
    {"name": "Glazed Roof Tile",     "ingredients": {"clay": 1, "crystal_shard": 1},                      "output_id": "glazed_roof_tile",        "output_count": 2},
    {"name": "Gold Leaf Trim",       "ingredients": {"gold_nugget": 2, "lumber": 1},                      "output_id": "gold_leaf_trim",          "output_count": 2},
    {"name": "Gothic Tracery",       "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "gothic_tracery",          "output_count": 2},
    {"name": "Greek Key",            "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "greek_key",               "output_count": 2},
    {"name": "Grotesque Frieze",     "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "grotesque_frieze",        "output_count": 2},
    {"name": "Half-Timber Wall",     "ingredients": {"lumber": 1, "limestone_block": 1},                  "output_id": "half_timber_wall",        "output_count": 2},
    {"name": "Han Brick",            "ingredients": {"clay": 2, "coal": 1},                               "output_id": "han_brick",               "output_count": 2},
    {"name": "Hanji Screen",         "ingredients": {"lumber": 2, "crystal_shard": 1},                    "output_id": "hanji_screen",            "output_count": 2},
    {"name": "Hearth Stone",         "ingredients": {"stone_chip": 2, "coal": 1},                         "output_id": "hearth_stone",            "output_count": 2},
    {"name": "Herringbone Brick",    "ingredients": {"stone_chip": 1, "dirt_clump": 2},                   "output_id": "herringbone_brick",       "output_count": 2},
    {"name": "Inca Ashlar",          "ingredients": {"granite_slab": 2, "stone_chip": 1},                 "output_id": "inca_ashlar",             "output_count": 2},
    {"name": "Ionic Capital",        "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "ionic_capital",           "output_count": 2},
    {"name": "Iron Balustrade",      "ingredients": {"iron_chunk": 2, "coal": 1},                         "output_id": "wrought_iron_balustrade", "output_count": 2},
    {"name": "Iron Lantern",         "ingredients": {"iron_chunk": 2, "gold_nugget": 1},                  "output_id": "iron_lantern",            "output_count": 2},
    {"name": "Ivory Brick",          "ingredients": {"stone_chip": 1, "sand_grain": 1, "gold_nugget": 1}, "output_id": "ivory_brick",             "output_count": 2},
    {"name": "Jade Panel",           "ingredients": {"stone_chip": 1, "crystal_shard": 1, "lumber": 1},   "output_id": "jade_panel",              "output_count": 2},
    {"name": "Japanese Shoji",       "ingredients": {"lumber": 2, "crystal_shard": 1},                    "output_id": "japanese_shoji",          "output_count": 2},
    {"name": "Kente Panel",          "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "kente_panel",             "output_count": 2},
    {"name": "Keystone",             "ingredients": {"limestone_block": 1, "stone_chip": 1},              "output_id": "keystone",                "output_count": 2},
    {"name": "Khmer Stone",          "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "khmer_stone",             "output_count": 2},
    {"name": "Kilim Tile",           "ingredients": {"lumber": 1, "ruby": 1, "gold_nugget": 1},           "output_id": "kilim_tile",              "output_count": 2},
    {"name": "Lacquer Panel",        "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "lacquer_panel",           "output_count": 2},
    {"name": "Lapis Brick",          "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "lapis_brick",             "output_count": 2},
    {"name": "Lattice Screen",       "ingredients": {"lumber": 2, "stone_chip": 1},                       "output_id": "lattice_screen",          "output_count": 2},
    {"name": "Leadlight Window",     "ingredients": {"sand_grain": 2, "iron_chunk": 1},                   "output_id": "leadlight_window",        "output_count": 2},
    {"name": "Limestone",            "ingredients": {"limestone_chip": 3},                               "output_id": "limestone_block",         "output_count": 2},
    {"name": "Linen Fold",           "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "linen_fold",              "output_count": 2},
    {"name": "Lotus Capital",        "ingredients": {"limestone_block": 1, "stone_chip": 2},              "output_id": "lotus_capital",           "output_count": 2},
    {"name": "Mahogany Plank",       "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "mahogany_plank",          "output_count": 2},
    {"name": "Mansard Slate",        "ingredients": {"magmatic_shard": 1, "stone_chip": 1, "coal": 1},    "output_id": "mansard_slate",           "output_count": 2},
    {"name": "Manueline Panel",      "ingredients": {"limestone_block": 2, "iron_chunk": 1},              "output_id": "manueline_panel",         "output_count": 2},
    {"name": "Marble Inlay",         "ingredients": {"sand_grain": 1, "gold_nugget": 1, "crystal_shard": 1}, "output_id": "marble_inlay",         "output_count": 2},
    {"name": "Mashrabiya",           "ingredients": {"lumber": 2, "iron_chunk": 1},                       "output_id": "mashrabiya",              "output_count": 2},
    {"name": "Maya Relief",          "ingredients": {"stone_chip": 3},                                    "output_id": "maya_relief",             "output_count": 2},
    {"name": "Māori Carving",        "ingredients": {"lumber": 2, "obsidian_slab": 1},                    "output_id": "maori_carving",           "output_count": 2},
    {"name": "Metope",               "ingredients": {"limestone_block": 1, "stone_chip": 1},              "output_id": "metope",                  "output_count": 2},
    {"name": "Moon Gate",            "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "moon_gate",               "output_count": 2},
    {"name": "Moorish Column",       "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "moorish_column",          "output_count": 2},
    {"name": "Moorish Star Tile",    "ingredients": {"stone_chip": 1, "crystal_shard": 1},                "output_id": "moorish_star_tile",       "output_count": 2},
    {"name": "Mossy Brick",          "ingredients": {"stone_chip": 2, "dirt_clump": 1},                   "output_id": "mossy_brick",             "output_count": 2},
    {"name": "Mughal Arch",          "ingredients": {"limestone_block": 2, "crystal_shard": 1},           "output_id": "mughal_arch",             "output_count": 2},
    {"name": "Mughal Jali",          "ingredients": {"limestone_block": 2, "sand_grain": 1},              "output_id": "mughal_jali",             "output_count": 2},
    {"name": "Muqarnas",             "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "muqarnas_block",          "output_count": 2},
    {"name": "Nordic Plank",         "ingredients": {"lumber": 2, "coal": 2},                             "output_id": "nordic_plank",            "output_count": 2},
    {"name": "Oak Panel",            "ingredients": {"lumber": 2, "stone_chip": 1},                       "output_id": "oak_panel",               "output_count": 2},
    {"name": "Obsidian Cut",         "ingredients": {"obsidian_slab": 2, "stone_chip": 1},                "output_id": "obsidian_cut",            "output_count": 2},
    {"name": "Obsidian Tile",        "ingredients": {"obsidian_slab": 1, "stone_chip": 2},                "output_id": "obsidian_tile",           "output_count": 2},
    {"name": "Ogee Arch",            "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "ogee_arch",               "output_count": 2},
    {"name": "Onion Dome Tile",      "ingredients": {"clay": 1, "crystal_shard": 1, "gold_nugget": 1},    "output_id": "onion_dome_tile",         "output_count": 2},
    {"name": "Onyx Inlay",           "ingredients": {"obsidian_slab": 1, "coal": 1},                      "output_id": "onyx_inlay",              "output_count": 2},
    {"name": "Opus Incertum",        "ingredients": {"stone_chip": 2, "dirt_clump": 1},                   "output_id": "opus_incertum",           "output_count": 2},
    {"name": "Opus Signinum",        "ingredients": {"stone_chip": 1, "sand_grain": 1, "ruby": 1},        "output_id": "opus_signinum",           "output_count": 2},
    {"name": "Ottoman Arch",         "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "ottoman_arch",            "output_count": 2},
    {"name": "Ottoman Tile",         "ingredients": {"sand_grain": 2, "crystal_shard": 1},                "output_id": "ottoman_tile",            "output_count": 2},
    {"name": "Pagoda Eave",          "ingredients": {"lumber": 1, "ruby": 1, "crystal_shard": 1},         "output_id": "pagoda_eave",             "output_count": 2},
    {"name": "Painted Beam",         "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "painted_beam",            "output_count": 2},
    {"name": "Palladian Window",     "ingredients": {"limestone_block": 2, "crystal_shard": 1},           "output_id": "palladian_window",        "output_count": 2},
    {"name": "Paper Lantern",        "ingredients": {"lumber": 1, "crystal_shard": 1},                    "output_id": "paper_lantern",           "output_count": 2},
    {"name": "Parquet Floor",        "ingredients": {"lumber": 2, "sand_grain": 1},                       "output_id": "parquet_floor",           "output_count": 2},
    {"name": "Pavilion Floor",       "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "pavilion_floor",          "output_count": 2},
    {"name": "Pebble Dash",          "ingredients": {"stone_chip": 1, "sand_grain": 2},                   "output_id": "pebble_dash",             "output_count": 2},
    {"name": "Persian Iwan",         "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "persian_iwan",            "output_count": 2},
    {"name": "Persian Tile",         "ingredients": {"clay": 1, "crystal_shard": 2},                      "output_id": "persian_tile",            "output_count": 2},
    {"name": "Pietra Dura",          "ingredients": {"sand_grain": 1, "gold_nugget": 1, "ruby": 1},       "output_id": "pietra_dura",             "output_count": 2},
    {"name": "Pilaster",             "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "pilaster",                "output_count": 2},
    {"name": "Plinth Block",         "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "plinth_block",            "output_count": 2},
    {"name": "Pointed Arch",         "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "pointed_arch",            "output_count": 2},
    {"name": "Polished Granite",     "ingredients": {"granite_slab": 2},                                 "output_id": "polished_granite",        "output_count": 2},
    {"name": "Polished Marble",      "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "polished_marble",         "output_count": 2},
    {"name": "Polynesian Carved",    "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "polynesian_carved",       "output_count": 2},
    {"name": "Portuguese Cork",      "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "portuguese_cork",         "output_count": 2},
    {"name": "Quartz Pillar",        "ingredients": {"stone_chip": 3, "crystal_shard": 1},                "output_id": "quartz_pillar",           "output_count": 2},
    {"name": "Relief Panel",         "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "relief_panel",            "output_count": 2},
    {"name": "Roman Mosaic",         "ingredients": {"sand_grain": 1, "stone_chip": 1},                   "output_id": "roman_mosaic",            "output_count": 2},
    {"name": "Romanesque Arch",      "ingredients": {"stone_chip": 1, "sand_grain": 2},                   "output_id": "romanesque_arch",         "output_count": 2},
    {"name": "Rose Quartz",          "ingredients": {"stone_chip": 2, "ruby": 1},                         "output_id": "rose_quartz_block",       "output_count": 2},
    {"name": "Rose Window",          "ingredients": {"stone_chip": 1, "crystal_shard": 2},                "output_id": "rose_window",             "output_count": 2},
    {"name": "Rune Stone",           "ingredients": {"magmatic_shard": 1, "coal": 1},                     "output_id": "rune_stone",              "output_count": 2},
    {"name": "Rusticated Stone",     "ingredients": {"granite_slab": 2, "stone_chip": 1},                 "output_id": "rusticated_stone",        "output_count": 2},
    {"name": "Russian Kokoshnik",    "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "russian_kokoshnik",       "output_count": 2},
    {"name": "Saffron Door",         "ingredients": {"lumber": 2, "gold_nugget": 2},                      "output_id": "saffron_door",            "output_count": 1},
    {"name": "Saltillo Tile",        "ingredients": {"clay": 1, "sand_grain": 1},                         "output_id": "saltillo_tile",           "output_count": 2},
    {"name": "Sandalwood Door",      "ingredients": {"lumber": 2, "dirt_clump": 1, "ruby": 1},            "output_id": "sandalwood_door",         "output_count": 1},
    {"name": "Sandstone Ashlar",     "ingredients": {"sand_grain": 2, "stone_chip": 1},                   "output_id": "sandstone_ashlar",        "output_count": 2},
    {"name": "Sandstone Column",     "ingredients": {"sand_grain": 2, "limestone_block": 1},              "output_id": "sandstone_column",        "output_count": 2},
    {"name": "Scottish Rubble",      "ingredients": {"granite_slab": 2, "stone_chip": 1},                 "output_id": "scottish_rubble",         "output_count": 2},
    {"name": "Sett Stone",           "ingredients": {"granite_slab": 2, "stone_chip": 1},                 "output_id": "sett_stone",              "output_count": 3},
    {"name": "Shoji Door",           "ingredients": {"lumber": 2, "crystal_shard": 1},                    "output_id": "shoji_door",              "output_count": 1},
    {"name": "Silver Panel",         "ingredients": {"iron_chunk": 2, "crystal_shard": 1},                "output_id": "silver_panel",            "output_count": 2},
    {"name": "Slate Tile",           "ingredients": {"stone_chip": 2, "coal": 1},                         "output_id": "slate_tile",              "output_count": 2},
    {"name": "Spanish Roof Tile",    "ingredients": {"clay": 1, "dirt_clump": 1},                         "output_id": "spanish_roof_tile",       "output_count": 2},
    {"name": "Stained Glass (Blue)", "ingredients": {"sand_grain": 1, "crystal_shard": 2},                "output_id": "stained_glass_blue",      "output_count": 2},
    {"name": "Stained Glass (Green)","ingredients": {"sand_grain": 2, "crystal_shard": 1, "dirt_clump": 1}, "output_id": "stained_glass_green",  "output_count": 2},
    {"name": "Stained Glass (Red)",  "ingredients": {"sand_grain": 2, "ruby": 1},                         "output_id": "stained_glass_red",       "output_count": 2},
    {"name": "Stave Plank",          "ingredients": {"lumber": 2, "coal": 1},                             "output_id": "stave_plank",             "output_count": 2},
    {"name": "Stepped Wall",         "ingredients": {"clay": 2, "stone_chip": 1},                         "output_id": "stepped_wall",            "output_count": 2},
    {"name": "Stone Lantern",        "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "stone_lantern",           "output_count": 2},
    {"name": "Stone Slab Door",      "ingredients": {"stone_chip": 3, "granite_slab": 1},                 "output_id": "stone_slab_door",         "output_count": 1},
    {"name": "Striped Arch",         "ingredients": {"limestone_block": 1, "stone_chip": 1, "coal": 1},   "output_id": "striped_arch",            "output_count": 2},
    {"name": "Studded Oak Door",     "ingredients": {"lumber": 2, "iron_chunk": 1},                       "output_id": "studded_oak_door",        "output_count": 1},
    {"name": "Swahili Door",         "ingredients": {"lumber": 2, "gold_nugget": 1, "iron_chunk": 1},     "output_id": "swahili_door",            "output_count": 1},
    {"name": "Swiss Chalet Panel",   "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "swiss_chalet",            "output_count": 2},
    {"name": "Talavera Tile",        "ingredients": {"sand_grain": 1, "crystal_shard": 1},                "output_id": "talavera_tile",           "output_count": 2},
    {"name": "Tapestry",             "ingredients": {"lumber": 1, "ruby": 1},                             "output_id": "tapestry_block",          "output_count": 1},
    {"name": "Teak Plank",           "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "teak_plank",              "output_count": 2},
    {"name": "Teal Door",            "ingredients": {"lumber": 2, "crystal_shard": 2},                    "output_id": "teal_door",               "output_count": 1},
    {"name": "Terracotta",           "ingredients": {"clay": 2},                                          "output_id": "terracotta",              "output_count": 2},
    {"name": "Terracotta Shingle",   "ingredients": {"stone_chip": 1, "dirt_clump": 2},                   "output_id": "terracotta_shingle",      "output_count": 2},
    {"name": "Thatch Roof",          "ingredients": {"lumber": 2, "wheat": 1},                            "output_id": "thatch_roof",             "output_count": 2},
    {"name": "Timber Truss",         "ingredients": {"lumber": 3},                                        "output_id": "timber_truss",            "output_count": 2},
    {"name": "Torii Panel",          "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "torii_panel",             "output_count": 2},
    {"name": "Triglyph Panel",       "ingredients": {"limestone_block": 2, "limestone_chip": 1},          "output_id": "triglyph_panel",          "output_count": 2},
    {"name": "Tudor Beam",           "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "tudor_beam",              "output_count": 2},
    {"name": "Tudor Rose",           "ingredients": {"limestone_block": 1, "ruby": 1},                    "output_id": "tudor_rose",              "output_count": 2},
    {"name": "Venetian Floor",       "ingredients": {"sand_grain": 1, "gold_nugget": 1},                  "output_id": "venetian_floor",          "output_count": 2},
    {"name": "Venetian Plaster",     "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "venetian_plaster",        "output_count": 2},
    {"name": "Verdigris Copper",     "ingredients": {"iron_chunk": 1, "crystal_shard": 1},                "output_id": "verdigris_copper",        "output_count": 2},
    {"name": "Vermilion Door",       "ingredients": {"lumber": 2, "ruby": 1, "gold_nugget": 1},           "output_id": "vermilion_door",          "output_count": 1},
    {"name": "Viking Carving",       "ingredients": {"lumber": 2, "obsidian_slab": 1},                    "output_id": "viking_carving",          "output_count": 2},
    {"name": "Walnut Plank",         "ingredients": {"lumber": 2, "coal": 1},                             "output_id": "walnut_plank",            "output_count": 2},
    {"name": "Wat Finial",           "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "wat_finial",              "output_count": 2},
    {"name": "Wattle & Daub",        "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "wattle_daub",             "output_count": 2},
    {"name": "White Plaster Wall",   "ingredients": {"limestone_block": 2, "sand_grain": 1},              "output_id": "white_plaster_wall",      "output_count": 2},
    {"name": "Woven Rug",            "ingredients": {"lumber": 1, "dirt_clump": 1, "ruby": 1},            "output_id": "woven_rug",               "output_count": 1},
    {"name": "Wrought Iron Grille",  "ingredients": {"iron_chunk": 2, "coal": 1},                         "output_id": "wrought_iron_grille",     "output_count": 2},
    {"name": "Zellige Tile",         "ingredients": {"sand_grain": 2, "crystal_shard": 1},                "output_id": "zellige_tile",            "output_count": 2},
    # --- Renaissance palace blocks ---
    # Facade stonework
    {"name": "Pietra Serena",       "ingredients": {"limestone_block": 2, "coal": 1},             "output_id": "pietra_serena",        "output_count": 2},
    {"name": "Travertine Wall",     "ingredients": {"limestone_block": 2, "stone_chip": 1},       "output_id": "travertine_wall",      "output_count": 2},
    {"name": "Marble Facade",       "ingredients": {"polished_marble": 2, "stone_chip": 1},       "output_id": "marble_facade",        "output_count": 2},
    {"name": "Rusticated Quoin",    "ingredients": {"stone_chip": 3, "limestone_block": 1},       "output_id": "rusticated_quoin",     "output_count": 2},
    {"name": "Bicolor Marble",      "ingredients": {"polished_marble": 1, "verdite_slab": 1},     "output_id": "bicolor_marble",       "output_count": 2},
    {"name": "Pink Granite Base",   "ingredients": {"granite_slab": 3},                           "output_id": "pink_granite_base",    "output_count": 2},
    {"name": "Blind Arch",          "ingredients": {"limestone_block": 2, "stone_chip": 2},       "output_id": "blind_arch",           "output_count": 1},
    {"name": "Console Cornice",     "ingredients": {"limestone_block": 2, "stone_chip": 1},       "output_id": "console_cornice",      "output_count": 2},
    # Columns and pilasters
    {"name": "Corinthian Capital",  "ingredients": {"polished_marble": 2, "gold_nugget": 1},      "output_id": "corinthian_capital",   "output_count": 1},
    {"name": "Giant Pilaster",      "ingredients": {"limestone_block": 2, "stone_chip": 2},       "output_id": "giant_pilaster",       "output_count": 2},
    {"name": "Engaged Column",      "ingredients": {"polished_marble": 2, "limestone_chip": 1},   "output_id": "engaged_column",       "output_count": 1},
    {"name": "Atlas Figure",        "ingredients": {"polished_marble": 3, "iron_chunk": 1},       "output_id": "atlas_figure",         "output_count": 1},
    {"name": "Caryatid Column",     "ingredients": {"polished_marble": 3, "iron_chunk": 1},       "output_id": "caryatid_column",      "output_count": 1},
    {"name": "Composite Capital",   "ingredients": {"polished_marble": 2, "gold_nugget": 1},      "output_id": "composite_capital",    "output_count": 1},
    # Interior walls
    {"name": "Intarsia Panel",      "ingredients": {"lumber": 2, "gold_nugget": 1, "coal": 1},    "output_id": "intarsia_panel",       "output_count": 2},
    {"name": "Studiolo Wall",       "ingredients": {"lumber": 3, "iron_chunk": 1},                "output_id": "studiolo_wall",        "output_count": 2},
    {"name": "Gilt Leather Wall",   "ingredients": {"lumber": 1, "gold_nugget": 2},               "output_id": "gilt_leather",         "output_count": 2},
    {"name": "Fresco Lunette",      "ingredients": {"limestone_block": 1, "crystal_shard": 1},    "output_id": "fresco_lunette",       "output_count": 2},
    {"name": "Marble Wainscoting",  "ingredients": {"polished_marble": 2, "limestone_chip": 1},   "output_id": "wainscot_marble",      "output_count": 2},
    {"name": "Tapestry Frame",      "ingredients": {"lumber": 1, "gold_nugget": 2},               "output_id": "tapestry_frame",       "output_count": 1},
    # Ceilings
    {"name": "Lacunar Ceiling",     "ingredients": {"limestone_block": 3, "gold_nugget": 1},      "output_id": "lacunar_ceiling",      "output_count": 2},
    {"name": "Barrel Vault Fresco", "ingredients": {"limestone_block": 2, "crystal_shard": 2},    "output_id": "barrel_fresco",        "output_count": 2},
    {"name": "Golden Ceiling",      "ingredients": {"lumber": 1, "gold_nugget": 3},               "output_id": "golden_ceiling",       "output_count": 2},
    {"name": "Grotesque Vault",     "ingredients": {"limestone_block": 2, "stone_chip": 2},       "output_id": "grotesque_vault",      "output_count": 2},
    {"name": "Cupola Oculus",       "ingredients": {"polished_marble": 1, "crystal_shard": 2},    "output_id": "cupola_oculus",        "output_count": 1},
    # Floors
    {"name": "Cosmatesque Floor",   "ingredients": {"polished_marble": 1, "ruby": 1, "stone_chip": 1}, "output_id": "cosmatesque_floor", "output_count": 2},
    {"name": "Terrazzo Floor",      "ingredients": {"limestone_block": 1, "stone_chip": 2},       "output_id": "terrazzo_floor_ren",   "output_count": 2},
    {"name": "Opus Alexandrinum",   "ingredients": {"polished_marble": 1, "onyx_slab": 1, "ruby": 1}, "output_id": "opus_alexandrinum",  "output_count": 2},
    {"name": "Marble Medallion",    "ingredients": {"polished_marble": 3, "gold_nugget": 1},      "output_id": "marble_medallion_ren", "output_count": 1},
    {"name": "Palace Floor Tile",   "ingredients": {"polished_marble": 2, "limestone_chip": 1},   "output_id": "palace_floor_tile",    "output_count": 2},
    # Doorways and windows
    {"name": "Palace Portal",       "ingredients": {"limestone_block": 3, "stone_chip": 3},       "output_id": "palace_portal",        "output_count": 1},
    {"name": "Aedicule Frame",      "ingredients": {"limestone_block": 2, "gold_nugget": 1},      "output_id": "aedicule_frame",       "output_count": 1},
    {"name": "Thermal Window",      "ingredients": {"stone_chip": 2, "iron_chunk": 1},             "output_id": "thermal_window",       "output_count": 1},
    {"name": "Bifora Window",       "ingredients": {"limestone_block": 1, "iron_chunk": 1},        "output_id": "bifora_window",        "output_count": 1},
    {"name": "Serliana Window",     "ingredients": {"limestone_block": 2, "iron_chunk": 1},        "output_id": "serliana_window",      "output_count": 1},
    {"name": "Palazzo Balcony",     "ingredients": {"limestone_block": 2, "iron_chunk": 2},        "output_id": "palazzo_balcony",      "output_count": 1},
    # Arches and vaulting
    {"name": "Roman Arch",          "ingredients": {"limestone_block": 3, "stone_chip": 2},       "output_id": "roman_arch_ren",       "output_count": 1},
    {"name": "Coffered Barrel Vault","ingredients": {"limestone_block": 3, "gold_nugget": 1},      "output_id": "barrel_vault_coffer",  "output_count": 2},
    {"name": "Pendentive",          "ingredients": {"polished_marble": 2, "limestone_chip": 1},   "output_id": "pendentive_block",     "output_count": 2},
    {"name": "Groin Vault",         "ingredients": {"limestone_block": 3, "stone_chip": 1},       "output_id": "groin_vault",          "output_count": 2},
    # Fireplaces and niches
    {"name": "Renaissance Mantel",  "ingredients": {"polished_marble": 3, "iron_chunk": 1},       "output_id": "renaissance_mantel",   "output_count": 1},
    {"name": "Chimney Breast",      "ingredients": {"limestone_block": 2, "stone_chip": 2},       "output_id": "chimney_breast_ren",   "output_count": 1},
    {"name": "Pedimented Niche",    "ingredients": {"limestone_block": 2, "stone_chip": 1},       "output_id": "pedimented_niche",     "output_count": 1},
    {"name": "Shell Niche",         "ingredients": {"limestone_block": 1, "stone_chip": 2},       "output_id": "shell_niche_ren",      "output_count": 1},
    # Medieval Castle
    {"name": "Portcullis",          "ingredients": {"iron_chunk": 3, "lumber": 1},                "output_id": "portcullis_block",    "output_count": 1},
    {"name": "Arrow Loop",          "ingredients": {"stone_chip": 2, "limestone_block": 1},        "output_id": "arrow_loop",          "output_count": 2},
    {"name": "Machicolation",       "ingredients": {"stone_chip": 3, "limestone_chip": 1},         "output_id": "machicolation",       "output_count": 2},
    {"name": "Drawbridge Plank",    "ingredients": {"lumber": 3, "iron_chunk": 1},                 "output_id": "drawbridge_plank",    "output_count": 3},
    {"name": "Round Tower Wall",    "ingredients": {"stone_chip": 2, "limestone_block": 1},        "output_id": "round_tower_wall",    "output_count": 3},
    {"name": "Curtain Wall",        "ingredients": {"limestone_block": 2, "stone_chip": 1},        "output_id": "curtain_wall",        "output_count": 3},
    {"name": "Corbel Course",       "ingredients": {"stone_chip": 3},                              "output_id": "corbel_course",       "output_count": 3},
    {"name": "Tower Cap",           "ingredients": {"stone_chip": 2, "lumber": 1},                 "output_id": "tower_cap",           "output_count": 2},
    {"name": "Great Hall Floor",    "ingredients": {"limestone_block": 1, "stone_chip": 1},        "output_id": "great_hall_floor",    "output_count": 4},
    {"name": "Dungeon Wall",        "ingredients": {"stone_chip": 2, "iron_chunk": 1},             "output_id": "dungeon_wall",        "output_count": 3},
    {"name": "Castle Fireplace",    "ingredients": {"stone_chip": 3, "limestone_block": 1},        "output_id": "castle_fireplace",    "output_count": 1},
    {"name": "Heraldic Panel",      "ingredients": {"limestone_block": 1, "stone_chip": 2},        "output_id": "heraldic_panel",      "output_count": 2},
    {"name": "Wall-Walk Floor",     "ingredients": {"stone_chip": 2, "limestone_chip": 1},         "output_id": "wall_walk_floor",     "output_count": 4},
    {"name": "Castle Gate Arch",    "ingredients": {"stone_chip": 3, "iron_chunk": 1},             "output_id": "castle_gate_arch",    "output_count": 1},
    {"name": "Drawbridge Chain",    "ingredients": {"iron_chunk": 3},                              "output_id": "drawbridge_chain",    "output_count": 3},
    {"name": "Dungeon Grate",       "ingredients": {"iron_chunk": 2, "stone_chip": 1},             "output_id": "dungeon_grate",       "output_count": 2},
    {"name": "Moat Stone",          "ingredients": {"stone_chip": 2, "sand_grain": 1},             "output_id": "moat_stone",          "output_count": 4},
    {"name": "Chapel Stone",        "ingredients": {"limestone_block": 1, "crystal_shard": 1},     "output_id": "chapel_stone",        "output_count": 2},
    {"name": "Murder Hole",         "ingredients": {"stone_chip": 3},                              "output_id": "murder_hole",         "output_count": 2},
    {"name": "Garderobe Chute",     "ingredients": {"stone_chip": 2, "limestone_chip": 1},         "output_id": "garderobe_chute",     "output_count": 2},
    # --- Mid-Century Modern ---
    {"name": "Concrete Panel",      "ingredients": {"stone_chip": 2, "sand_grain": 1},              "output_id": "mcm_concrete_panel",   "output_count": 4},
    {"name": "Breeze Block",        "ingredients": {"stone_chip": 2, "sand_grain": 1},              "output_id": "mcm_breeze_block",     "output_count": 2},
    {"name": "Board and Batten",    "ingredients": {"lumber": 2},                                   "output_id": "mcm_board_batten",     "output_count": 4},
    {"name": "Walnut Panel",        "ingredients": {"lumber": 2},                                   "output_id": "mcm_walnut_panel",     "output_count": 4},
    {"name": "Teak Panel",          "ingredients": {"lumber": 2},                                   "output_id": "mcm_teak_panel",       "output_count": 4},
    {"name": "Roman Brick",         "ingredients": {"clay": 2, "sand_grain": 1},                    "output_id": "mcm_roman_brick",      "output_count": 4},
    {"name": "Terrazzo Floor",      "ingredients": {"stone_chip": 2, "crystal_shard": 1},           "output_id": "terrazzo_floor_mcm",   "output_count": 4},
    {"name": "Travertine Floor",    "ingredients": {"limestone_block": 1, "stone_chip": 1},         "output_id": "travertine_floor_mcm", "output_count": 4},
    {"name": "Quarry Tile",         "ingredients": {"clay": 2},                                     "output_id": "quarry_tile",          "output_count": 4},
    {"name": "Flagstone Patio",     "ingredients": {"stone_chip": 2, "sand_grain": 1},              "output_id": "flagstone_patio",      "output_count": 4},
    {"name": "Parquet Floor",       "ingredients": {"lumber": 2},                                   "output_id": "mcm_parquet",          "output_count": 4},
    {"name": "Cork Floor Tile",     "ingredients": {"lumber": 1},                                   "output_id": "cork_floor_tile",      "output_count": 4},
    {"name": "Avocado Tile",        "ingredients": {"clay": 1, "sand_grain": 1},                    "output_id": "avocado_tile",         "output_count": 4},
    {"name": "Harvest Gold Tile",   "ingredients": {"clay": 1, "sand_grain": 1},                    "output_id": "harvest_gold_tile",    "output_count": 4},
    {"name": "Burnt Orange Tile",   "ingredients": {"clay": 1, "sand_grain": 1},                    "output_id": "burnt_orange_tile",    "output_count": 4},
    {"name": "Turquoise Tile",      "ingredients": {"clay": 1, "crystal_shard": 1},                 "output_id": "turquoise_tile",       "output_count": 4},
    {"name": "Plate Glass Panel",   "ingredients": {"sand_grain": 3},                               "output_id": "plate_glass_panel",    "output_count": 2},
    {"name": "Tinted Glass Panel",  "ingredients": {"sand_grain": 2, "coal": 1},                    "output_id": "tinted_glass_panel",   "output_count": 2},
    {"name": "Ribbed Glass",        "ingredients": {"sand_grain": 2, "limestone_chip": 1},          "output_id": "ribbed_glass_mcm",     "output_count": 2},
    {"name": "Brass Trim Panel",    "ingredients": {"iron_chunk": 1, "gold_nugget": 1},             "output_id": "brass_trim_panel",     "output_count": 2},
    {"name": "Copper Screen",       "ingredients": {"iron_chunk": 2},                               "output_id": "copper_screen_mcm",    "output_count": 2},
    {"name": "Anodized Aluminum",   "ingredients": {"iron_chunk": 2, "sand_grain": 1},              "output_id": "anodized_aluminum",    "output_count": 3},
    {"name": "Rattan Screen",       "ingredients": {"lumber": 1, "wool": 1},                        "output_id": "rattan_screen_mcm",    "output_count": 2},
    {"name": "Split Bamboo Panel",  "ingredients": {"lumber": 2},                                   "output_id": "split_bamboo_panel",   "output_count": 4},
    {"name": "Lava Rock Wall",      "ingredients": {"basalt_shard": 2},                             "output_id": "lava_rock_wall",       "output_count": 3},
    {"name": "Tongue and Groove",   "ingredients": {"lumber": 2},                                   "output_id": "mcm_tongue_groove",    "output_count": 4},
    {"name": "Butterfly Beam",      "ingredients": {"lumber": 3},                                   "output_id": "butterfly_beam",       "output_count": 2},
    {"name": "Starburst Panel",     "ingredients": {"stone_chip": 2, "gold_nugget": 1},             "output_id": "starburst_panel",      "output_count": 2},
    {"name": "Stacked Stone Veneer","ingredients": {"stone_chip": 3},                               "output_id": "stacked_stone_veneer", "output_count": 4},
    {"name": "Fiberglass Shell",    "ingredients": {"sand_grain": 2, "iron_chunk": 1},              "output_id": "fiberglass_shell",     "output_count": 3},
    {"name": "Alpine Balcony Rail", "ingredients": {"walnut_plank": 3, "iron_chunk": 1},      "output_id": "alpine_balcony_rail", "output_count": 2},
    {"name": "Dark Timber Beam",    "ingredients": {"charcoal_plank": 2},                       "output_id": "dark_timber_beam",    "output_count": 2},
    {"name": "Rough Stone Wall",    "ingredients": {"stone_chip": 4},                           "output_id": "rough_stone_wall",    "output_count": 4},
    {"name": "Alpine Plaster",      "ingredients": {"limestone_block": 2, "stone_chip": 1},     "output_id": "alpine_plaster",      "output_count": 4},
    {"name": "Flower Box",          "ingredients": {"walnut_plank": 2, "wool": 1},              "output_id": "flower_box",          "output_count": 2},
    {"name": "Firewood Stack",      "ingredients": {"teak_plank": 3},                           "output_id": "firewood_stack",      "output_count": 2},
    {"name": "Slate Shingle",       "ingredients": {"slate_tile": 3},                           "output_id": "slate_shingle",       "output_count": 4},
    {"name": "Carved Shutter",      "ingredients": {"walnut_plank": 2, "iron_chunk": 1},        "output_id": "carved_shutter",      "output_count": 2},
    {"name": "Bear Hide",           "ingredients": {"wool": 3, "coal": 1},                      "output_id": "bear_hide",           "output_count": 1},
    {"name": "Alpine Herb Rack",    "ingredients": {"teak_plank": 2, "wool": 1},                "output_id": "alpine_herb_rack",    "output_count": 2},
    {"name": "Hay Bale",            "ingredients": {"wool": 4},                                 "output_id": "hay_bale",            "output_count": 2},
    {"name": "Pine Plank Wall",     "ingredients": {"walnut_plank": 2, "stone_chip": 1},        "output_id": "pine_plank_wall",     "output_count": 4},
    {"name": "Granite Ashlar",      "ingredients": {"granite_slab": 2},                         "output_id": "granite_ashlar",      "output_count": 2},
    {"name": "Cuckoo Clock",        "ingredients": {"walnut_plank": 3, "iron_chunk": 1},        "output_id": "cuckoo_clock",        "output_count": 1},
    {"name": "Geranium Box",        "ingredients": {"walnut_plank": 2, "wool": 1},              "output_id": "geranium_box",        "output_count": 2},
    {"name": "Arch Stone",          "ingredients": {"limestone_block": 2, "stone_chip": 2},     "output_id": "arch_stone",          "output_count": 2},
    {"name": "Swiss Panel",         "ingredients": {"oak_panel": 2, "wool": 1},                 "output_id": "swiss_panel",         "output_count": 2},
    {"name": "Copper Cowbell",      "ingredients": {"copper_tile": 2, "iron_chunk": 1},         "output_id": "copper_cowbell",      "output_count": 1},
    {"name": "Wooden Gear",         "ingredients": {"walnut_plank": 4},                         "output_id": "wooden_gear",         "output_count": 1},
    {"name": "Stone Basin",         "ingredients": {"stone_chip": 4, "iron_chunk": 1},          "output_id": "stone_basin",         "output_count": 1},
    {"name": "Milk Churn",          "ingredients": {"iron_chunk": 3, "stone_chip": 1},          "output_id": "milk_churn",          "output_count": 1},
    {"name": "Alpine Chest",        "ingredients": {"walnut_plank": 4, "iron_chunk": 2},        "output_id": "alpine_chest",        "output_count": 1},
    {"name": "Alpine Lantern",      "ingredients": {"iron_chunk": 3, "coal": 1},                "output_id": "alpine_lantern",      "output_count": 1},
    {"name": "Wrought Iron Rail",   "ingredients": {"iron_chunk": 3, "tempered_iron": 1},       "output_id": "wrought_iron_rail",   "output_count": 2},
    {"name": "Alpine Chandelier",   "ingredients": {"iron_chunk": 4, "tempered_iron": 1},       "output_id": "alpine_chandelier",   "output_count": 1},
    {"name": "Woven Textile",       "ingredients": {"wool": 4, "golden_wool": 1},               "output_id": "woven_textile",       "output_count": 1},
    {"name": "Cowbell Rack",        "ingredients": {"walnut_plank": 2, "copper_tile": 2},       "output_id": "cowbell_rack",        "output_count": 1},
    {"name": "Alpine Stucco",       "ingredients": {"limestone_block": 2, "clay": 1},           "output_id": "alpine_stucco",       "output_count": 4},
    {"name": "Carved Lintel",       "ingredients": {"limestone_block": 3, "stone_chip": 1},     "output_id": "carved_lintel",       "output_count": 1},
    {"name": "Chalet Door",         "ingredients": {"walnut_plank": 4, "iron_chunk": 2},        "output_id": "chalet_door",         "output_count": 1},
    {"name": "Ceramic Tile Stove", "ingredients": {"clay": 4, "limestone_block": 2},             "output_id": "ceramic_tile_stove", "output_count": 1},
    {"name": "Carved Bargeboard",  "ingredients": {"charcoal_plank": 2, "walnut_plank": 1},      "output_id": "carved_bargeboard",  "output_count": 2},
    {"name": "Dormer Window",      "ingredients": {"walnut_plank": 2, "iron_chunk": 1},           "output_id": "dormer_window",      "output_count": 1},
    {"name": "Wooden Shingle",     "ingredients": {"teak_plank": 3},                              "output_id": "wooden_shingle",     "output_count": 4},
    {"name": "Stone Step",         "ingredients": {"granite_slab": 2, "stone_chip": 1},           "output_id": "stone_step",         "output_count": 2},
    {"name": "Water Trough",       "ingredients": {"stone_chip": 4, "iron_chunk": 1},             "output_id": "water_trough",       "output_count": 1},
    {"name": "Carved Bench",       "ingredients": {"walnut_plank": 3, "stone_chip": 1},           "output_id": "carved_bench",       "output_count": 1},
    {"name": "Cheese Wheel",       "ingredients": {"limestone_block": 1, "wool": 1},              "output_id": "cheese_wheel",       "output_count": 1},
    {"name": "Antler Mount",       "ingredients": {"walnut_plank": 2, "iron_chunk": 1},           "output_id": "antler_mount",       "output_count": 1},
    {"name": "Edelweiss Wreath",   "ingredients": {"wool": 2, "stone_chip": 1},                   "output_id": "edelweiss_wreath",   "output_count": 1},
    {"name": "Boot Rack",          "ingredients": {"teak_plank": 2, "iron_chunk": 1},             "output_id": "boot_rack",          "output_count": 1},
    {"name": "Tallow Candle",      "ingredients": {"wool": 1, "stone_chip": 1},                   "output_id": "tallow_candle",      "output_count": 4},
    {"name": "Alpine Hearth",      "ingredients": {"granite_slab": 3, "stone_chip": 2},           "output_id": "alpine_hearth",      "output_count": 1},
    {"name": "Pine Cone Garland",  "ingredients": {"wool": 1, "teak_plank": 1},                   "output_id": "pine_cone_garland",  "output_count": 2},
    {"name": "Iron Hook Rack",     "ingredients": {"iron_chunk": 2, "walnut_plank": 1},           "output_id": "iron_hook_rack",     "output_count": 2},
    {"name": "Alpine Gate",        "ingredients": {"walnut_plank": 4, "iron_chunk": 2},           "output_id": "alpine_gate",        "output_count": 1},
    {"name": "Butter Churn",       "ingredients": {"walnut_plank": 3, "iron_chunk": 1},           "output_id": "butter_churn",       "output_count": 1},
    {"name": "Carved Wainscot",    "ingredients": {"charcoal_plank": 3, "walnut_plank": 1},       "output_id": "carved_wainscot",    "output_count": 4},
    {"name": "Chimney Cap",        "ingredients": {"cobblestone": 3, "iron_chunk": 1},            "output_id": "chimney_cap",        "output_count": 1},
    {"name": "Feather Duvet",      "ingredients": {"wool": 5, "golden_wool": 1},                  "output_id": "feather_duvet",      "output_count": 1},
    {"name": "Greek Amphora",       "ingredients": {"clay": 3},                               "output_id": "greek_amphora",       "output_count": 1},
    {"name": "Krater",              "ingredients": {"clay": 4, "stone_chip": 1},              "output_id": "krater",              "output_count": 1},
    {"name": "Hydria",              "ingredients": {"clay": 3, "iron_chunk": 1},              "output_id": "hydria",              "output_count": 1},
    {"name": "Lekythos",            "ingredients": {"clay": 2},                               "output_id": "lekythos",            "output_count": 2},
    {"name": "Storage Pithos",      "ingredients": {"clay": 5, "stone_chip": 1},              "output_id": "storage_pithos",      "output_count": 1},
    {"name": "Kline",               "ingredients": {"walnut_plank": 3, "wool": 2},            "output_id": "kline",               "output_count": 1},
    {"name": "Tripod Brazier",      "ingredients": {"iron_chunk": 3, "tempered_iron": 1},     "output_id": "tripod_brazier",      "output_count": 1},
    {"name": "Olive Press",         "ingredients": {"granite_slab": 3, "walnut_plank": 2},    "output_id": "olive_press",         "output_count": 1},
    {"name": "Loom Frame",          "ingredients": {"walnut_plank": 4, "wool": 1},            "output_id": "loom_frame",          "output_count": 1},
    {"name": "Meander Border",      "ingredients": {"limestone_block": 2, "stone_chip": 2},   "output_id": "meander_border",      "output_count": 4},
    {"name": "Symposium Table",     "ingredients": {"walnut_plank": 3, "iron_chunk": 1},      "output_id": "symposium_table",     "output_count": 1},
    {"name": "Votive Tablet",       "ingredients": {"limestone_block": 2, "stone_chip": 1},   "output_id": "votive_tablet",       "output_count": 1},
    {"name": "Bronze Cuirass Stand","ingredients": {"iron_chunk": 4, "tempered_iron": 2},     "output_id": "bronze_cuirass_stand","output_count": 1},
    {"name": "Chariot Wheel",       "ingredients": {"walnut_plank": 3, "iron_chunk": 2},      "output_id": "chariot_wheel",       "output_count": 1},
    {"name": "Terracotta Roof Tile","ingredients": {"clay": 3},                               "output_id": "terracotta_roof_tile","output_count": 4},
    {"name": "Attic Vase",          "ingredients": {"clay": 3, "coal": 1},                    "output_id": "attic_vase",          "output_count": 1},
    {"name": "Greek Stone Bench",   "ingredients": {"limestone_block": 3, "stone_chip": 1},   "output_id": "greek_stone_bench",   "output_count": 1},
    {"name": "Stone Altar",         "ingredients": {"granite_slab": 3, "limestone_block": 2}, "output_id": "stone_altar",         "output_count": 1},
    {"name": "Bronze Mirror",       "ingredients": {"copper_tile": 3, "tempered_iron": 1},    "output_id": "bronze_mirror",       "output_count": 1},
    {"name": "Clay Oil Lamp",       "ingredients": {"clay": 2},                               "output_id": "clay_oil_lamp",       "output_count": 2},
    {"name": "Agora Scale",         "ingredients": {"iron_chunk": 3, "tempered_iron": 1},     "output_id": "agora_scale",         "output_count": 1},
    {"name": "Laurel Wreath Mount", "ingredients": {"wool": 2, "limestone_block": 1},         "output_id": "laurel_wreath_mount", "output_count": 1},
    {"name": "Hermes Stele",        "ingredients": {"limestone_block": 3, "stone_chip": 2},   "output_id": "hermes_stele",        "output_count": 1},
    {"name": "Doric Capital",       "ingredients": {"limestone_block": 2, "stone_chip": 2},   "output_id": "doric_capital",       "output_count": 1},
    {"name": "Victory Stele",       "ingredients": {"limestone_block": 4, "stone_chip": 2},   "output_id": "victory_stele",       "output_count": 1},
    {"name": "Bronze Shield Mount", "ingredients": {"iron_chunk": 4, "tempered_iron": 2},     "output_id": "bronze_shield_mount", "output_count": 1},
    {"name": "Egg and Dart",        "ingredients": {"limestone_block": 2, "stone_chip": 1},   "output_id": "egg_and_dart",        "output_count": 4},
    {"name": "Olive Branch",        "ingredients": {"wool": 1, "stone_chip": 1},              "output_id": "olive_branch",        "output_count": 2},
    {"name": "Philosophers Scroll", "ingredients": {"wool": 2, "walnut_plank": 1},            "output_id": "philosophers_scroll", "output_count": 2},
    {"name": "Greek Theatre Mask",  "ingredients": {"clay": 3, "stone_chip": 1},              "output_id": "greek_theatre_mask",  "output_count": 1},
    # Light sources
    {"name": "Torch",         "ingredients": {"coal": 1, "lumber": 1},                    "output_id": "torch",         "output_count": 4},
    {"name": "Wall Sconce",   "ingredients": {"iron_chunk": 1, "coal": 1},                "output_id": "wall_sconce",   "output_count": 2},
    {"name": "Brazier",       "ingredients": {"iron_chunk": 2, "coal": 1},                "output_id": "brazier",       "output_count": 1},
    {"name": "Chandelier",    "ingredients": {"iron_chunk": 3, "crystal_shard": 1},       "output_id": "chandelier",    "output_count": 1},
    {"name": "Candelabra",    "ingredients": {"iron_chunk": 1, "gold_nugget": 1},         "output_id": "candelabra",    "output_count": 2},
    {"name": "Lantern Orb",   "ingredients": {"crystal_shard": 2, "gold_nugget": 1},      "output_id": "lantern_orb",   "output_count": 1},
    {"name": "Pendant Lamp",  "ingredients": {"iron_chunk": 2, "stone_chip": 1},          "output_id": "pendant_lamp",  "output_count": 2},
    {"name": "Fire Bowl",     "ingredients": {"stone_chip": 3, "coal": 1},                "output_id": "fire_bowl",     "output_count": 1},
    {"name": "Cross Lantern", "ingredients": {"iron_chunk": 2, "coal": 1},                "output_id": "cross_lantern", "output_count": 2},
    {"name": "Star Lamp",     "ingredients": {"crystal_shard": 1, "gold_nugget": 2},      "output_id": "star_lamp",     "output_count": 2},
    {"name": "Glow Vine",     "ingredients": {"lumber": 1, "crystal_shard": 1},           "output_id": "glow_vine",     "output_count": 4},
    {"name": "Ice Shard", "ingredients": {"stone_chip": 2}, "output_id": "ice_shard", "output_count": 2},
    {"name": "Frozen Bog", "ingredients": {"stone_chip": 2}, "output_id": "frozen_bog", "output_count": 2},
    {"name": "Weapon Assembler", "ingredients": {"lumber": 4, "iron_chunk": 2}, "output_id": "weapon_assembler", "output_count": 1},
]

WEAPON_ASSEMBLER_RECIPES = [
    {"name": "Sword Hilt",    "ingredients": {"lumber": 2},                    "output_id": "sword_hilt",    "output_count": 1},
    {"name": "Dagger Handle", "ingredients": {"lumber": 1},                    "output_id": "dagger_handle", "output_count": 1},
    {"name": "Spear Shaft",   "ingredients": {"lumber": 3},                    "output_id": "spear_shaft",   "output_count": 1},
    {"name": "Axe Haft",      "ingredients": {"lumber": 2},                    "output_id": "axe_haft",      "output_count": 1},
    {"name": "Mace Haft",     "ingredients": {"lumber": 2},                    "output_id": "mace_haft",     "output_count": 1},
    {"name": "Halberd Shaft", "ingredients": {"lumber": 4},                    "output_id": "halberd_shaft", "output_count": 1},
    {"name": "Glaive Pole",   "ingredients": {"lumber": 3},                    "output_id": "glaive_pole",   "output_count": 1},
    {"name": "Rapier Grip",   "ingredients": {"lumber": 1},                    "output_id": "rapier_grip",   "output_count": 1},
    {"name": "Trident Shaft", "ingredients": {"lumber": 3},                    "output_id": "trident_shaft", "output_count": 1},
    {"name": "Scythe Snath",  "ingredients": {"lumber": 4},                    "output_id": "scythe_snath",  "output_count": 1},
]

# ---------------------------------------------------------------------------
# Shaped 3x3 grid recipes
# ---------------------------------------------------------------------------

RECIPES = [
    # --- Utility ---
    {
        "name": "Wood Stairs",
        "pattern": [
            ["lumber",  None,    None   ],
            ["lumber",  "lumber", None   ],
            ["lumber",  "lumber", "lumber"],
        ],
        "output_id":    "wood_stairs",
        "output_count": 4,
    },
    {
        "name": "Ladder",
        "pattern": [
            ["lumber", None, None],
            [None,     None, None],
            [None,     None, None],
        ],
        "output_id":    "ladder_item",
        "output_count": 5,
    },
    {
        "name": "Diamond",
        "pattern": [
            [None,   "ruby", None],
            ["ruby",   None, "ruby"],
            [None,   "ruby", None],
        ],
        "output_id":    "diamond",
        "output_count": 1,
    },
    # --- Tools ---
    {
        "name": "Stone Pickaxe",
        "pattern": [
            ["stone_chip",  "stone_chip",  "stone_chip"],
            [None,          "lumber",      None        ],
            [None,          "lumber",      None        ],
        ],
        "output_id":    "stone_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Iron Pickaxe",
        "pattern": [
            ["iron_chunk",  "iron_chunk",  "iron_chunk"],
            [None,          "lumber",      None        ],
            [None,          "lumber",      None        ],
        ],
        "output_id":    "iron_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Gold Pickaxe",
        "pattern": [
            ["gold_nugget", "gold_nugget", "gold_nugget"],
            [None,          "lumber",      None         ],
            [None,          "lumber",      None         ],
        ],
        "output_id":    "gold_pickaxe",
        "output_count": 1,
    },
    # --- Axes ---
    {
        "name": "Stone Axe",
        "pattern": [
            ["stone_chip", "stone_chip", None],
            ["stone_chip", "lumber",     None],
            [None,         "lumber",     None],
        ],
        "output_id":    "stone_axe",
        "output_count": 1,
    },
    {
        "name": "Iron Axe",
        "pattern": [
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "lumber",     None],
            [None,         "lumber",     None],
        ],
        "output_id":    "iron_axe",
        "output_count": 1,
    },
    {
        "name": "Gold Axe",
        "pattern": [
            ["gold_nugget", "gold_nugget", None],
            ["gold_nugget", "lumber",      None],
            [None,          "lumber",      None],
        ],
        "output_id":    "gold_axe",
        "output_count": 1,
    },
    # --- Animal harvesting tools ---
    {
        "name": "Shears",
        "pattern": [
            [None,         "iron_chunk", None       ],
            ["iron_chunk", None,         None       ],
            [None,         None,         None       ],
        ],
        "output_id":    "shears",
        "output_count": 1,
    },
    {
        "name": "Bucket",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "iron_chunk", None        ],
            [None,         None,         None        ],
        ],
        "output_id":    "bucket",
        "output_count": 1,
    },
    # --- Farming tools ---
    {
        "name": "Hoe",
        "pattern": [
            ["stone_chip", "stone_chip", None],
            [None,         "lumber",     None],
            [None,         "lumber",     None],
        ],
        "output_id":    "hoe",
        "output_count": 1,
    },
    {
        "name": "Watering Can",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            [None,         None,         None        ],
        ],
        "output_id":    "watering_can",
        "output_count": 1,
    },
    # --- Farming structures ---
    {
        "name": "Compost Bin",
        "pattern": [
            ["lumber",     "lumber",     "lumber"],
            ["lumber",     None,         "lumber"],
            ["dirt_clump", "dirt_clump", "dirt_clump"],
        ],
        "output_id":    "compost_bin_item",
        "output_count": 1,
    },
    {
        "name": "Well",
        "pattern": [
            ["stone_chip", None,         "stone_chip"],
            ["stone_chip", "lumber",     "stone_chip"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "well_item",
        "output_count": 1,
    },
    # --- Refinery equipment ---
    {
        "name": "Rock Tumbler",
        "pattern": [
            ["iron_chunk",  "stone_chip", "iron_chunk"],
            ["stone_chip",  "stone_chip", "stone_chip"],
            ["iron_chunk",  None,         "iron_chunk"],
        ],
        "output_id":    "tumbler_item",
        "output_count": 1,
    },
    {
        "name": "Stone Crusher",
        "pattern": [
            ["gold_nugget", "iron_chunk",  "gold_nugget"],
            ["iron_chunk",  "iron_chunk",  "iron_chunk" ],
            ["gold_nugget", "iron_chunk",  "gold_nugget"],
        ],
        "output_id":    "crusher_item",
        "output_count": 1,
    },
    {
        "name": "Gem Cutter",
        "pattern": [
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
            ["gold_nugget",   "crystal_shard", "gold_nugget"  ],
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
        ],
        "output_id":    "gem_cutter_item",
        "output_count": 1,
    },
    {
        "name": "Alchemical Kiln",
        "pattern": [
            ["crystal_shard", "ruby",          "crystal_shard"],
            ["crystal_shard", "crystal_shard", "crystal_shard"],
            ["crystal_shard", "ruby",          "crystal_shard"],
        ],
        "output_id":    "kiln_item",
        "output_count": 1,
    },
    {
        "name": "Smelter",
        "pattern": [
            ["stone_chip",  "iron_chunk", "stone_chip"],
            ["iron_chunk",  "coal",       "iron_chunk"],
            ["stone_chip",  "coal",       "stone_chip"],
        ],
        "output_id":    "smelter_item",
        "output_count": 1,
    },
    {
        "name": "Resonance Chamber",
        "pattern": [
            ["obsidian_slab", "ruby",          "obsidian_slab"],
            ["ruby",          "obsidian_slab", "ruby"         ],
            ["obsidian_slab", "ruby",          "obsidian_slab"],
        ],
        "output_id":    "resonance_item",
        "output_count": 1,
    },
    {
        "name": "Bakery",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
            ["iron_chunk", "stone_chip", "iron_chunk"],
        ],
        "output_id":    "bakery_item",
        "output_count": 1,
    },
    {
        "name": "Wok",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "iron_chunk", None        ],
            ["stone_chip", "coal",       "stone_chip"],
        ],
        "output_id":    "wok_item",
        "output_count": 1,
    },
    {
        "name": "Steamer",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
        ],
        "output_id":    "steamer_item",
        "output_count": 1,
    },
    {
        "name": "Noodle Pot",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "stone_chip", None        ],
        ],
        "output_id":    "noodle_pot_item",
        "output_count": 1,
    },
    {
        "name": "BBQ Grill",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
            ["iron_chunk", None,         "iron_chunk"],
        ],
        "output_id":    "bbq_grill_item",
        "output_count": 1,
    },
    {
        "name": "Clay Pot",
        "pattern": [
            ["stone_chip", "coal",       "stone_chip"],
            ["stone_chip", None,         "stone_chip"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "clay_pot_item",
        "output_count": 1,
    },
    {
        "name": "Desert Forge",
        "pattern": [
            ["stone_chip",  "coal",       "stone_chip"],
            ["stone_chip",  "iron_chunk", "stone_chip"],
            ["stone_chip",  "coal",       "stone_chip"],
        ],
        "output_id":    "desert_forge_item",
        "output_count": 1,
    },
    {
        "name": "Forge",
        "pattern": [
            ["stone_chip", "coal",     "stone_chip"],
            ["iron_bar",   "iron_bar", "iron_bar"  ],
            ["stone_chip", "stone_chip","stone_chip"],
        ],
        "output_id":    "forge_item",
        "output_count": 1,
    },
    {
        "name": "Weapon Rack",
        "pattern": [
            [None,      "lumber", None     ],
            ["lumber",  "lumber", "lumber" ],
            ["lumber",  None,     "lumber" ],
        ],
        "output_id":    "weapon_rack_item",
        "output_count": 1,
    },
    # --- Tempered tools ---
    {
        "name": "Tempered Pickaxe",
        "pattern": [
            ["tempered_iron", "tempered_iron", "tempered_iron"],
            [None,            "lumber",        None           ],
            [None,            "lumber",        None           ],
        ],
        "output_id":    "tempered_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Tempered Axe",
        "pattern": [
            ["tempered_iron", "tempered_iron", None],
            ["tempered_iron", "lumber",        None],
            [None,            "lumber",        None],
        ],
        "output_id":    "tempered_axe",
        "output_count": 1,
    },
    # --- Fences & Doors ---
    {
        "name": "Wood Fence",
        "pattern": [
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
            [None,     None,     None],
        ],
        "output_id":    "wood_fence",
        "output_count": 4,
    },
    {
        "name": "Iron Fence",
        "pattern": [
            ["iron_bar", "iron_bar", None],
            ["iron_bar", "iron_bar", None],
            [None,       None,       None],
        ],
        "output_id":    "iron_fence",
        "output_count": 4,
    },
    {
        "name": "Wood Door",
        "pattern": [
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
        ],
        "output_id":    "wood_door",
        "output_count": 1,
    },
    {
        "name": "Iron Door",
        "pattern": [
            ["iron_bar", "iron_bar", None],
            ["iron_bar", "iron_bar", None],
            ["iron_bar", "iron_bar", None],
        ],
        "output_id":    "iron_door",
        "output_count": 1,
    },
    # --- Furniture ---
    {
        "name": "Bed",
        "pattern": [
            ["wool",   "wool",   "wool"  ],
            ["lumber", "lumber", "lumber"],
            [None,     None,     None   ],
        ],
        "output_id":    "bed",
        "output_count": 1,
    },
    # --- Automations ---
    {
        "name": "Coal Miner",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", "coal",       None        ],
            ["stone_chip", "stone_chip", None        ],
        ],
        "output_id":    "coal_miner_item",
        "output_count": 1,
    },
    {
        "name": "Iron Miner",
        "pattern": [
            ["steel_bar", "gold_nugget", "steel_bar"],
            ["steel_bar", "coal",        "steel_bar"],
            ["steel_bar", "gold_nugget", "steel_bar"],
        ],
        "output_id":    "iron_miner_item",
        "output_count": 1,
    },
    {
        "name": "Crystal Miner",
        "pattern": [
            ["crystal_shard", "iron_chunk",  "crystal_shard"],
            ["iron_chunk",    "gold_nugget", "iron_chunk"   ],
            ["crystal_shard", "iron_chunk",  "crystal_shard"],
        ],
        "output_id":    "crystal_miner_item",
        "output_count": 1,
    },
    {
        "name": "Chest",
        "pattern": [
            ["lumber", "lumber",     "lumber"],
            ["lumber", None,         "lumber"],
            ["lumber", "iron_chunk", "lumber"],
        ],
        "output_id":    "chest_item",
        "output_count": 1,
    },
    # --- Farm Bots ---
    {
        "name": "Farm Bot",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["iron_chunk", "coal",       "iron_chunk"],
            ["lumber",     "iron_chunk", "lumber"    ],
        ],
        "output_id":    "farm_bot_item",
        "output_count": 1,
    },
    {
        "name": "Iron Farm Bot",
        "pattern": [
            ["steel_bar",   "gold_nugget", "steel_bar"  ],
            ["gold_nugget", "steel_bar",   "gold_nugget"],
            ["steel_bar",   "gold_nugget", "steel_bar"  ],
        ],
        "output_id":    "iron_farm_bot_item",
        "output_count": 1,
    },
    {
        "name": "Crystal Farm Bot",
        "pattern": [
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
            ["gold_nugget",   "iron_chunk",     "gold_nugget"  ],
            ["crystal_shard", "gold_nugget",    "crystal_shard"],
        ],
        "output_id":    "crystal_farm_bot_item",
        "output_count": 1,
    },
    # --- Construction Equipment ---
    {
        "name": "Empty Barrel",
        "pattern": [
            ["iron_chunk", None,          "iron_chunk"],
            ["iron_chunk", None,          "iron_chunk"],
            ["iron_chunk", "iron_chunk",  "iron_chunk"],
        ],
        "output_id":    "empty_barrel",
        "output_count": 1,
    },
    {
        "name": "Backhoe",
        "pattern": [
            ["iron_chunk", "lumber",      "iron_chunk"],
            ["iron_chunk", "coal",        "iron_chunk"],
            ["iron_chunk", "iron_chunk",  "iron_chunk"],
        ],
        "output_id":    "backhoe_item",
        "output_count": 1,
    },
    {
        "name": "Hunting Knife",
        "pattern": [
            [None, "stone_chip", None],
            [None, "lumber",     None],
            [None, None,         None],
        ],
        "output_id":    "hunting_knife",
        "output_count": 1,
    },
    # --- Fishing ---
    {
        "name": "Fishing Pole",
        "pattern": [
            [None,     None,     "lumber"],
            [None,     "lumber", None    ],
            ["lumber", None,     None    ],
        ],
        "output_id":    "fishing_pole",
        "output_count": 1,
    },
    {
        "name": "Cane Rod",
        "pattern": [
            [None,           None,           "lumber"     ],
            [None,           "lumber",       None         ],
            ["iron_chunk",   "lumber",       None         ],
        ],
        "output_id":    "cane_rod",
        "output_count": 1,
    },
    {
        "name": "Composite Rod",
        "pattern": [
            [None,              None,           "lumber"     ],
            [None,              "lumber",       None         ],
            ["crystal_shard",   "lumber",       "iron_chunk" ],
        ],
        "output_id":    "composite_rod",
        "output_count": 1,
    },
    {
        "name": "Fish Trophy",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            [None,         None,         None        ],
        ],
        "output_id":    "fish_trophy_item",
        "output_count": 1,
    },
    # --- Bird furniture ---
    {
        "name": "Bird Feeder",
        "pattern": [
            ["lumber", "lumber", "lumber"],
            [None,     "lumber", None    ],
            ["lumber", "lumber", "lumber"],
        ],
        "output_id":    "bird_feeder",
        "output_count": 1,
    },
    {
        "name": "Bird Bath",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            [None,         "stone_chip", None        ],
            [None,         "stone_chip", None        ],
        ],
        "output_id":    "bird_bath",
        "output_count": 1,
    },
    {
        "name": "Binoculars",
        "pattern": [
            ["clear_glass", None,     "clear_glass"],
            ["iron_bar",    "lumber", "iron_bar"   ],
            ["clear_glass", None,     "clear_glass"],
        ],
        "output_id":    "binoculars",
        "output_count": 1,
    },
    # --- Insect collecting ---
    {
        "name": "Bug Net",
        "pattern": [
            [None,     "wool",   None  ],
            [None,     "wool",   None  ],
            [None,     "lumber", None  ],
        ],
        "output_id":    "bug_net",
        "output_count": 1,
    },
    {
        "name": "Insect Display Case",
        "pattern": [
            ["lumber",        "crystal_shard", "lumber"],
            [None,            None,            None    ],
            ["lumber",        "lumber",        "lumber"],
        ],
        "output_id":    "insect_display_case",
        "output_count": 1,
    },
    {
        "name": "Light Trap",
        "pattern": [
            ["clear_glass",   "iron_lantern",  "clear_glass"],
            [None,            "sugar_lump",    None         ],
            [None,            "lumber",        None         ],
        ],
        "output_id":    "light_trap",
        "output_count": 1,
    },
    {
        "name": "Garden Block",
        "pattern": [
            [None,          None,          None        ],
            ["lumber",      "dirt_clump",  "lumber"    ],
            ["lumber",      "stone_chip",  "lumber"    ],
        ],
        "output_id":    "garden_block",
        "output_count": 1,
    },
    {
        "name": "Wildflower Display",
        "pattern": [
            [None,          "glass_pane",  None        ],
            [None,          "glass_pane",  None        ],
            ["lumber",      "lumber",      "lumber"    ],
        ],
        "output_id":    "wildflower_display",
        "output_count": 1,
    },
    # --- Horse items ---
    {
        "name": "Saddle",
        "pattern": [
            ["wool",        "wool",        "wool"      ],
            ["wool",        "iron_chunk",  "wool"      ],
            [None,          "iron_chunk",  None        ],
        ],
        "output_id":    "saddle",
        "output_count": 1,
    },
    {
        "name": "Horse Brush",
        "pattern": [
            [None,          "wool",        None        ],
            ["lumber",      "wool",        "lumber"    ],
            [None,          "lumber",      None        ],
        ],
        "output_id":    "horse_brush",
        "output_count": 3,
    },
    {
        "name": "Horseshoe",
        "pattern": [
            [None,          None,          None        ],
            ["iron_chunk",  None,          "iron_chunk"],
            [None,          None,          None        ],
        ],
        "output_id":    "horseshoe",
        "output_count": 2,
    },
    {
        "name": "Sugar Lump",
        "pattern": [
            [None,          None,          None        ],
            [None,          "wheat",       None        ],
            ["wheat",       "wheat",       "wheat"     ],
        ],
        "output_id":    "sugar_lump",
        "output_count": 4,
    },
    {
        "name": "Stable",
        "pattern": [
            ["lumber",      "stone_chip",  "lumber"    ],
            ["lumber",      "stone_chip",  "lumber"    ],
            ["lumber",      "lumber",      "lumber"    ],
        ],
        "output_id":    "stable_item",
        "output_count": 1,
    },
    {
        "name": "Horse Trough",
        "pattern": [
            [None,          None,          None        ],
            ["stone_chip",  "lumber",      "stone_chip"],
            ["stone_chip",  "stone_chip",  "stone_chip"],
        ],
        "output_id":    "horse_trough_item",
        "output_count": 1,
    },
    # --- Dog items ---
    {
        "name": "Dog Collar",
        "pattern": [
            [None,       None,         None     ],
            ["leather",  "iron_chunk", "leather"],
            [None,       None,         None     ],
        ],
        "output_id":    "dog_collar",
        "output_count": 1,
    },
    {
        "name": "Dog Treat",
        "pattern": [
            [None,     None,    None ],
            ["carrot", "wheat", "bone"],
            [None,     None,    None ],
        ],
        "output_id":    "dog_treat",
        "output_count": 3,
    },
    {
        "name": "Dog Whistle",
        "pattern": [
            [None,         None,          None        ],
            ["lumber",     "iron_chunk",  None        ],
            [None,         None,          None        ],
        ],
        "output_id":    "dog_whistle",
        "output_count": 1,
    },
    {
        "name": "Kennel",
        "pattern": [
            ["lumber",      "lumber",      "lumber"    ],
            ["lumber",      "stone_chip",  "lumber"    ],
            ["stone_chip",  "stone_chip",  "stone_chip"],
        ],
        "output_id":    "kennel_item",
        "output_count": 1,
    },
    {
        "name": "Dog Bowl",
        "pattern": [
            [None,          None,          None        ],
            ["stone_chip",  None,          "stone_chip"],
            [None,          "stone_chip",  None        ],
        ],
        "output_id":    "dog_bowl_item",
        "output_count": 1,
    },
    # --- Coffee equipment ---
    {
        "name": "Coffee Roaster",
        "pattern": [
            ["stone_chip",  "iron_chunk",  "stone_chip"],
            ["iron_chunk",  "coal",        "iron_chunk"],
            ["stone_chip",  "lumber",      "stone_chip"],
        ],
        "output_id":    "roaster_item",
        "output_count": 1,
    },
    {
        "name": "Blend Station",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "blend_station_item",
        "output_count": 1,
    },
    {
        "name": "Brew Station",
        "pattern": [
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "iron_chunk", "stone_chip"],
        ],
        "output_id":    "brew_station_item",
        "output_count": 1,
    },
    {
        "name": "Anaerobic Tank",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "anaerobic_tank_item",
        "output_count": 1,
    },
    {
        "name": "Glass Kiln",
        "pattern": [
            ["stone_chip", "iron_chunk",  "stone_chip"],
            ["sand_grain", None,          "sand_grain"],
            ["coal",       "coal",        "coal"      ],
        ],
        "output_id":    "glass_kiln_item",
        "output_count": 1,
    },
    {
        "name": "Fossil Prep Table",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            ["lumber",     "lumber",     "lumber"    ],
            ["lumber",     "lumber",     "lumber"    ],
        ],
        "output_id":    "fossil_table_item",
        "output_count": 1,
    },
    {
        "name": "Artisan Bench",
        "pattern": [
            ["stone_chip", "lumber",     "stone_chip"],
            ["lumber",     "iron_chunk", "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "artisan_bench_item",
        "output_count": 1,
    },
    {
        "name": "City Block",
        "pattern": [
            ["gold_nugget", "stone_chip", "gold_nugget"],
            ["stone_chip",  "iron_chunk", "stone_chip" ],
            ["gold_nugget", "stone_chip", "gold_nugget"],
        ],
        "output_id":    "city_block_item",
        "output_count": 1,
    },
    {
        "name": "Mining Post",
        "pattern": [
            ["iron_chunk",  "stone_chip",  "iron_chunk" ],
            ["stone_chip",  "stone_chip",  "stone_chip" ],
            ["stone_chip",  "lumber",      "stone_chip" ],
        ],
        "output_id":    "mining_post_item",
        "output_count": 1,
    },
    {
        "name": "Banner",
        "pattern": [
            ["wool",    "wool",    "wool"  ],
            ["lumber",  "wool",    "lumber"],
            [None,      "lumber",  None    ],
        ],
        "output_id":    "banner_item",
        "output_count": 1,
    },
    # --- Wine equipment ---
    {
        "name": "Grape Press",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
            ["stone_chip", "lumber",     "stone_chip"],
        ],
        "output_id":    "grape_press_item",
        "output_count": 1,
    },
    {
        "name": "Fermentation Tank",
        "pattern": [
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["iron_chunk", "stone_chip", "iron_chunk"],
        ],
        "output_id":    "fermentation_item",
        "output_count": 1,
    },
    {
        "name": "Wine Cellar",
        "pattern": [
            ["stone_chip", "lumber",     "stone_chip"],
            ["stone_chip", "coal",       "stone_chip"],
            ["stone_chip", "lumber",     "stone_chip"],
        ],
        "output_id":    "wine_cellar_item",
        "output_count": 1,
    },
    # --- Distillery equipment ---
    {
        "name": "Copper Still",
        "pattern": [
            ["iron_chunk",  "gold_nugget", "iron_chunk"],
            ["coal",        "iron_chunk",  "coal"],
            ["stone_chip",  "iron_chunk",  "stone_chip"],
        ],
        "output_id":    "still_item",
        "output_count": 1,
    },
    {
        "name": "Barrel Room",
        "pattern": [
            ["lumber",     "coal",    "lumber"],
            ["iron_chunk", "lumber",  "iron_chunk"],
            ["lumber",     "lumber",  "lumber"],
        ],
        "output_id":    "barrel_room_item",
        "output_count": 1,
    },
    {
        "name": "Bottling Station",
        "pattern": [
            ["stone_chip", "iron_chunk", "stone_chip"],
            ["lumber",     "coal",       "lumber"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "bottling_item",
        "output_count": 1,
    },
    # --- Herbalism equipment ---
    {
        "name": "Drying Rack",
        "pattern": [
            ["lumber",  "lumber",  "lumber"],
            ["lumber",  None,      "lumber"],
            [None,      None,      None    ],
        ],
        "output_id":    "drying_rack_item",
        "output_count": 1,
    },
    # --- Tea equipment ---
    {
        "name": "Withering Rack",
        "pattern": [
            ["lumber",     "lumber",     "lumber"],
            ["lumber",     None,         "lumber"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "withering_rack_item",
        "output_count": 1,
    },
    {
        "name": "Oxidation Station",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["iron_chunk", "stone_chip", "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "oxidation_station_item",
        "output_count": 1,
    },
    {
        "name": "Tea Cellar",
        "pattern": [
            ["stone_chip", "lumber",  "stone_chip"],
            ["lumber",     "coal",    "lumber"],
            ["stone_chip", "lumber",  "stone_chip"],
        ],
        "output_id":    "tea_cellar_item",
        "output_count": 1,
    },
    {
        "name": "Roasting Kiln",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "roasting_kiln_item",
        "output_count": 1,
    },
    # --- Textile equipment ---
    {
        "name": "Spinning Wheel",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["iron_chunk", None,         "iron_chunk"],
            ["lumber",     "stone_chip", "lumber"    ],
        ],
        "output_id":    "spinning_wheel_item",
        "output_count": 1,
    },
    {
        "name": "Dye Vat",
        "pattern": [
            ["iron_chunk", "clay",       "iron_chunk"],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "dye_vat_item",
        "output_count": 1,
    },
    {
        "name": "Loom",
        "pattern": [
            ["lumber",  "lumber",  "lumber"],
            ["lumber",  None,      "lumber"],
            ["lumber",  "lumber",  "lumber"],
        ],
        "output_id":    "loom_item",
        "output_count": 1,
    },
    # --- Cheese supply chain ---
    {
        "name": "Dairy Vat",
        "pattern": [
            ["iron_chunk", "stone_chip", "iron_chunk"],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "dairy_vat_item",
        "output_count": 1,
    },
    {
        "name": "Cheese Press",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "lumber",     "stone_chip"],
        ],
        "output_id":    "cheese_press_item",
        "output_count": 1,
    },
    {
        "name": "Aging Cave",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            ["stone_chip", None,         "stone_chip"],
            ["stone_chip", "iron_chunk", "stone_chip"],
        ],
        "output_id":    "aging_cave_item",
        "output_count": 1,
    },
    # --- Salt supply chain ---
    {
        "name": "Evaporation Pan",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "evap_pan_item",
        "output_count": 1,
    },
    {
        "name": "Salt Grinder",
        "pattern": [
            ["stone_chip", "iron_chunk",  "stone_chip"],
            ["stone_chip", None,          "stone_chip"],
            ["lumber",     "lumber",      "lumber"    ],
        ],
        "output_id":    "salt_grinder_item",
        "output_count": 1,
    },
    # --- Premium seeds (selective_breeding research) ---
    {
        "name": "Premium Strawberry Seed",
        "pattern": [
            ["strawberry_seed", "strawberry_seed", None],
            ["strawberry_seed", "iron_chunk",       None],
            [None,              None,               None],
        ],
        "output_id":    "strawberry_seed_premium",
        "output_count": 1,
    },
    {
        "name": "Premium Tomato Seed",
        "pattern": [
            ["tomato_seed", "tomato_seed", None],
            ["tomato_seed", "iron_chunk",  None],
            [None,          None,          None],
        ],
        "output_id":    "tomato_seed_premium",
        "output_count": 1,
    },
    {
        "name": "Premium Watermelon Seed",
        "pattern": [
            ["watermelon_seed", "watermelon_seed", None],
            ["watermelon_seed", "iron_chunk",       None],
            [None,              None,               None],
        ],
        "output_id":    "watermelon_seed_premium",
        "output_count": 1,
    },
    {
        "name": "Premium Corn Seed",
        "pattern": [
            ["corn_seed", "corn_seed", None],
            ["corn_seed", "iron_chunk", None],
            [None,        None,         None],
        ],
        "output_id":    "corn_seed_premium",
        "output_count": 1,
    },
    {
        "name": "Premium Rice Seed",
        "pattern": [
            ["rice_seed", "rice_seed", None],
            ["rice_seed", "iron_chunk", None],
            [None,        None,         None],
        ],
        "output_id":    "rice_seed_premium",
        "output_count": 1,
    },
    # --- Fishing equipment ---
    {
        "name": "Bait Station",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "bait_station_item",
        "output_count": 1,
    },
    # --- Hunting ---
    {
        "name": "Fletching Table",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["stone_chip", None,         "stone_chip"],
            [None,         None,         None        ],
        ],
        "output_id":    "fletching_table_item",
        "output_count": 1,
    },
    # --- Elevator system ---
    {
        "name": "Elevator Stop",
        "pattern": [
            ["iron_chunk", "stone_chip", "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "elevator_stop",
        "output_count": 1,
    },
    {
        "name": "Elevator Cable (x4)",
        "pattern": [
            [None,         "iron_chunk", None],
            [None,         "iron_chunk", None],
            [None,         "iron_chunk", None],
        ],
        "output_id":    "elevator_cable",
        "output_count": 4,
    },
    {
        "name": "Elevator Car",
        "pattern": [
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
        ],
        "output_id":    "elevator_car",
        "output_count": 1,
    },
    # --- Minecart system ---
    {
        "name": "Mine Track (x4)",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "mine_track",
        "output_count": 4,
    },
    {
        "name": "Track Stop",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "mine_track_stop",
        "output_count": 1,
    },
    {
        "name": "Minecart",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
        ],
        "output_id":    "minecart",
        "output_count": 1,
    },
    {
        "name": "Cart",
        "pattern": [
            [None,         "lumber",     None        ],
            ["lumber",     "iron_chunk", "lumber"    ],
            ["iron_chunk", "lumber",     "iron_chunk"],
        ],
        "output_id":    "cart",
        "output_count": 1,
    },
    {
        "name": "Trade Post",
        "pattern": [
            ["stone_chip", "lumber",     "stone_chip"],
            ["lumber",     "iron_chunk", "lumber"    ],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "trade_block",
        "output_count": 1,
    },
    # --- Jewelry ---
    {
        "name": "Jewelry Workbench",
        "pattern": [
            ["iron_chunk",    "crystal_shard", "iron_chunk"   ],
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
            ["iron_chunk",    "iron_chunk",    "iron_chunk"   ],
        ],
        "output_id":    "jewelry_workbench_item",
        "output_count": 1,
    },
    # --- Garden Workshop ---
    {
        "name": "Garden Workshop",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "garden_workshop_item",
        "output_count": 1,
    },
    {
        "name": "Juicer",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["iron_chunk", None,         "iron_chunk"],
            ["lumber",     "stone_chip", "lumber"    ],
        ],
        "output_id":    "juicer_item",
        "output_count": 1,
    },
    # --- Brewery supply chain ---
    {
        "name": "Brew Kettle",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
        ],
        "output_id":    "brew_kettle_item",
        "output_count": 1,
    },
    {
        "name": "Fermentation Vessel",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
        ],
        "output_id":    "ferm_vessel_item",
        "output_count": 1,
    },
    {
        "name": "Taproom",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["stone_chip", "lumber",     "stone_chip"],
        ],
        "output_id":    "taproom_item",
        "output_count": 1,
    },
    # --- Automation Bench ---
    {
        "name": "Automation Bench",
        "pattern": [
            ["tempered_iron", "iron_chunk",    "tempered_iron"],
            ["iron_chunk",    "lumber",        "iron_chunk"   ],
            ["stone_chip",    "stone_chip",    "stone_chip"   ],
        ],
        "output_id":    "automation_bench_item",
        "output_count": 1,
    },
    # --- Sculpture system ---
    {
        "name":    "Stone Chisel",
        "pattern": [[None,          "stone_chip", None],
                    [None,          "stone_chip", None],
                    [None,          "lumber",     None]],
        "output_id":    "chisel",
        "output_count": 1,
    },
    {
        "name":    "Sculptor's Bench",
        "pattern": [["stone_chip",  "chisel",     "stone_chip"],
                    ["lumber",      "iron_bar",    "lumber"],
                    ["lumber",      None,           "lumber"]],
        "output_id":    "sculptors_bench_item",
        "output_count": 1,
    },
    # --- Custom Tapestry ---
    {
        "name":    "Weaving Needle",
        "pattern": [[None,       "iron_bar", None],
                    [None,       "iron_bar", None],
                    [None,       "wool",     None]],
        "output_id":    "weaving_needle",
        "output_count": 1,
    },
    {
        "name":    "Tapestry Frame",
        "pattern": [["lumber",   "wool",    "lumber"],
                    ["lumber",   "iron_bar", "lumber"],
                    ["lumber",   None,       "lumber"]],
        "output_id":    "tapestry_frame_item",
        "output_count": 1,
    },
    # --- Pottery & Ceramics ---
    {
        "name":    "Pottery Wheel",
        "pattern": [["lumber",     "clay",    "lumber"],
                    ["stone_chip", "clay",    "stone_chip"],
                    ["lumber",     "clay",    "lumber"]],
        "output_id":    "pottery_wheel_item",
        "output_count": 1,
    },
    {
        "name":    "Pottery Kiln",
        "pattern": [["stone_chip", "coal",    "stone_chip"],
                    ["clay",       None,       "clay"],
                    ["stone_chip", "clay",    "stone_chip"]],
        "output_id":    "pottery_kiln_item",
        "output_count": 1,
    },
    {
        "name":    "Pottery Display",
        "pattern": [[None,         "stone_chip", None],
                    ["stone_chip", "clay",       "stone_chip"],
                    ["stone_chip", "stone_chip", "stone_chip"]],
        "output_id":    "pottery_display",
        "output_count": 1,
    },
]

# ---------------------------------------------------------------------------
# Automation Bench recipes — logic components, sensors, and fluid infrastructure
# ---------------------------------------------------------------------------

AUTOMATION_RECIPES = [
    {"name": "Wire",              "ingredients": {"iron_chunk": 2, "tempered_iron": 1},              "output_id": "wire",                  "output_count": 16},
    {"name": "Switch",            "ingredients": {"iron_chunk": 2, "wire": 1},                       "output_id": "switch_item",           "output_count": 1},
    {"name": "Toggle Latch",      "ingredients": {"iron_chunk": 3, "wire": 2},                       "output_id": "latch_item",            "output_count": 1},
    {"name": "AND Gate",          "ingredients": {"tempered_iron": 2, "wire": 2},                    "output_id": "and_gate_item",         "output_count": 1},
    {"name": "OR Gate",           "ingredients": {"tempered_iron": 2, "wire": 1},                    "output_id": "or_gate_item",          "output_count": 1},
    {"name": "NOT Gate",          "ingredients": {"tempered_iron": 2, "iron_chunk": 1, "wire": 1},   "output_id": "not_gate_item",         "output_count": 1},
    {"name": "Dam",               "ingredients": {"stone_chip": 6, "iron_chunk": 2},                 "output_id": "dam_item",              "output_count": 1},
    {"name": "Pump",              "ingredients": {"iron_chunk": 4, "tempered_iron": 2, "wire": 2},   "output_id": "pump_item",             "output_count": 1},
    {"name": "Iron Gate",         "ingredients": {"iron_chunk": 6},                                  "output_id": "iron_gate_item",        "output_count": 1},
    {"name": "Pressure Plate",    "ingredients": {"stone_chip": 4, "wire": 1},                       "output_id": "pressure_plate_item",   "output_count": 1},
    {"name": "Day Sensor",        "ingredients": {"glass": 2, "wire": 2},                            "output_id": "day_sensor_item",       "output_count": 1},
    {"name": "Water Sensor",      "ingredients": {"iron_chunk": 2, "wire": 1},                       "output_id": "water_sensor_item",     "output_count": 1},
    {"name": "Crop Sensor",       "ingredients": {"iron_chunk": 1, "wire": 2},                       "output_id": "crop_sensor_item",      "output_count": 1},
    {"name": "Repeater",          "ingredients": {"iron_chunk": 2, "wire": 3},                       "output_id": "repeater_item",         "output_count": 1},
    {"name": "Pulse Gen",         "ingredients": {"tempered_iron": 2, "wire": 2},                    "output_id": "pulse_gen_item",        "output_count": 1},
    {"name": "RS Latch",          "ingredients": {"tempered_iron": 3, "wire": 2},                    "output_id": "rs_latch_item",         "output_count": 1},
    {"name": "Powered Lantern",   "ingredients": {"glass": 2, "iron_chunk": 2, "wire": 1},          "output_id": "powered_lantern_item",  "output_count": 1},
    {"name": "Alarm Bell",        "ingredients": {"iron_chunk": 4, "wire": 1},                       "output_id": "alarm_bell_item",       "output_count": 1},
    {"name": "Water Bucket",      "ingredients": {"iron_chunk": 2},                                  "output_id": "water_bucket",          "output_count": 1},
    {"name": "Irrigation Channel","ingredients": {"stone_chip": 3, "iron_chunk": 1},                 "output_id": "irrigation_channel_item","output_count": 4},
    {"name": "Grow Lamp",        "ingredients": {"glass": 3, "iron_chunk": 2, "coal": 2},            "output_id": "grow_lamp_item",         "output_count": 1},
    {"name": "Counter",           "ingredients": {"tempered_iron": 2, "wire": 2, "iron_chunk": 1},  "output_id": "counter_item",          "output_count": 1},
    {"name": "Comparator",        "ingredients": {"tempered_iron": 2, "wire": 1, "quartz": 1},      "output_id": "comparator_item",       "output_count": 1},
    {"name": "Observer",          "ingredients": {"tempered_iron": 1, "wire": 2, "quartz": 1},      "output_id": "observer_item",         "output_count": 1},
    {"name": "Sequencer",         "ingredients": {"tempered_iron": 3, "wire": 3},                   "output_id": "sequencer_item",        "output_count": 1},
    {"name": "T Flip-Flop",       "ingredients": {"tempered_iron": 2, "wire": 2},                   "output_id": "t_flipflop_item",       "output_count": 1},
    {"name": "Deposit Trigger",   "ingredients": {"tempered_iron": 3, "wire": 2, "chest_item": 1},  "output_id": "deposit_trigger_item",  "output_count": 1},
]

# ---------------------------------------------------------------------------
# Pottery Kiln recipes (gem dust, unlocked by glaze_arts research)
# ---------------------------------------------------------------------------

POTTERY_KILN_RECIPES = [
    {"name": "Ruby Dust",     "ingredients": {"ruby": 1},         "output_id": "ruby_dust",     "output_count": 3, "research_required": "glaze_arts"},
    {"name": "Amethyst Dust", "ingredients": {"amethyst_gem": 1}, "output_id": "amethyst_dust", "output_count": 3, "research_required": "glaze_arts"},
    {"name": "Emerald Dust",  "ingredients": {"quartz_gem": 1},   "output_id": "emerald_dust",  "output_count": 3, "research_required": "glaze_arts"},
    {"name": "Sapphire Dust", "ingredients": {"crystal_shard": 2},"output_id": "sapphire_dust", "output_count": 3, "research_required": "glaze_arts"},
    {"name": "Topaz Dust",    "ingredients": {"citrine_gem": 1},  "output_id": "topaz_dust",    "output_count": 3, "research_required": "glaze_arts"},
]

# ---------------------------------------------------------------------------
# Bait Station recipes
# ---------------------------------------------------------------------------

BAIT_STATION_RECIPES = [
    {"name": "Worm Bait",     "ingredients": {"wheat": 2},                                         "output_id": "worm_bait",     "output_count": 4},
    {"name": "Insect Bait",   "ingredients": {"mint": 1, "rosemary": 1},                           "output_id": "insect_bait",   "output_count": 4},
    {"name": "Grain Bait",    "ingredients": {"corn": 2, "wheat": 1},                              "output_id": "grain_bait",    "output_count": 4},
    {"name": "Berry Bait",    "ingredients": {"strawberry": 3},                                    "output_id": "berry_bait",    "output_count": 4},
    {"name": "Meat Bait",     "ingredients": {"fish": 2},                                          "output_id": "meat_bait",     "output_count": 4},
    # Cross-system baits — draw from wildflower / herbalism / cooking outputs
    {"name": "Floral Bait",   "ingredients": {"pressed_flower": 2, "dried_chamomile": 1},          "output_id": "floral_bait",   "output_count": 3},
    {"name": "Spiced Bait",   "ingredients": {"dried_ginger": 1, "olive_oil": 1, "wheat": 1},      "output_id": "spiced_bait",   "output_count": 3},
    {"name": "Aromatic Bait", "ingredients": {"dried_lavender": 1, "dried_mint": 1},               "output_id": "aromatic_bait", "output_count": 3},
    {"name": "Honeyed Bait",  "ingredients": {"pressed_flower": 1, "dried_rosemary": 1, "corn": 2},"output_id": "honeyed_bait",  "output_count": 3},
]

# ---------------------------------------------------------------------------
# Fletching Table recipes
# ---------------------------------------------------------------------------

SMELTER_RECIPES = [
    {"name": "Iron Bar",    "ingredients": {"iron_chunk": 1, "coal": 1}, "output_id": "iron_bar",    "output_count": 1},
    {"name": "Gold Ingot",  "ingredients": {"gold_nugget": 1, "coal": 1},"output_id": "gold_ingot",  "output_count": 1},
    {"name": "Steel Bar",   "ingredients": {"iron_bar": 1, "coal": 2},   "output_id": "steel_bar",   "output_count": 1},
    {"name": "Steel Ingot", "ingredients": {"iron_bar": 2, "coal": 1},   "output_id": "steel_ingot", "output_count": 1},
    {"name": "Cut Crystal", "ingredients": {"crystal_shard": 1, "coal": 1},"output_id": "cut_crystal","output_count": 1},
]

FLETCHING_RECIPES = [
    # Bows
    {"name": "Wood Bow",         "ingredients": {"lumber": 3, "wool": 2},                               "output_id": "wood_bow",        "output_count": 1},
    {"name": "Recurve Bow",      "ingredients": {"lumber": 3, "stone_chip": 2, "wool": 2},              "output_id": "recurve_bow",     "output_count": 1},
    {"name": "Composite Bow",    "ingredients": {"lumber": 4, "iron_chunk": 2, "wool": 2},              "output_id": "composite_bow",   "output_count": 1},
    {"name": "Longbow",          "ingredients": {"lumber": 6, "wool": 3, "deer_hide": 1},               "output_id": "longbow",         "output_count": 1},
    {"name": "Crossbow",         "ingredients": {"lumber": 4, "iron_chunk": 4, "stone_chip": 2},        "output_id": "crossbow",        "output_count": 1},
    # Arrows
    {"name": "Wood Arrows",      "ingredients": {"lumber": 2, "feather": 1, "stone_chip": 1},           "output_id": "wood_arrow",      "output_count": 8},
    {"name": "Bone Arrows",      "ingredients": {"bone": 2, "feather": 1},                              "output_id": "bone_arrow",      "output_count": 8},
    {"name": "Flint Arrows",     "ingredients": {"stone_chip": 2, "feather": 1},                        "output_id": "flint_arrow",     "output_count": 8},
    {"name": "Iron Arrows",      "ingredients": {"iron_chunk": 1, "feather": 1, "lumber": 1},           "output_id": "iron_arrow",      "output_count": 6},
    {"name": "Barbed Arrows",    "ingredients": {"iron_chunk": 1, "bone": 1, "feather": 1},             "output_id": "barbed_arrow",    "output_count": 6},
    {"name": "Broadhead Arrows", "ingredients": {"iron_chunk": 2, "feather": 1, "lumber": 1},           "output_id": "broadhead_arrow", "output_count": 4},
    {"name": "Poison Arrows",    "ingredients": {"bone": 1, "iron_chunk": 1, "feather": 2, "wool": 1},  "output_id": "poison_arrow",    "output_count": 4},
    {"name": "Gold Arrows",      "ingredients": {"gold_nugget": 1, "feather": 2},                       "output_id": "gold_arrow",      "output_count": 4},
]

# ---------------------------------------------------------------------------
# Garden Workshop recipes — Alhambra / Italian garden blocks
# ---------------------------------------------------------------------------

GARDEN_WORKSHOP_RECIPES = [
    # Zellige tiles
    # Portuguese / Spanish ceramic tiles
    {"name": "Calçada Portuguesa",   "ingredients": {"stone_chip": 2, "coal": 1},                                        "output_id": "calcada_portuguesa",  "output_count": 4},
    {"name": "Azulejo Geometric",    "ingredients": {"clay": 2, "dye_extract_cobalt": 1},                                "output_id": "azulejo_geometric",   "output_count": 4},
    {"name": "Painted Tile Border",  "ingredients": {"clay": 1, "dye_extract_cobalt": 1, "dye_extract_golden": 1},       "output_id": "painted_tile_border", "output_count": 6},
    {"name": "Spanish Majolica",     "ingredients": {"clay": 2, "dye_extract_verdant": 1, "dye_extract_amber": 1},       "output_id": "spanish_majolica",    "output_count": 3},
    {"name": "Azulejo Stair",        "ingredients": {"clay": 2, "dye_extract_cobalt": 1, "dye_extract_ivory": 1},        "output_id": "azulejo_stair",       "output_count": 4},
    {"name": "Portuguese Pink Marble", "ingredients": {"limestone_block": 1, "dye_extract_rose": 1},                    "output_id": "portuguese_pink_marble", "output_count": 4},
    {"name": "Spanish Hex Tile",     "ingredients": {"clay": 2, "coal": 1},                                             "output_id": "spanish_hex_tile",    "output_count": 4},
    {"name": "Mudéjar Star Tile",    "ingredients": {"clay": 2, "dye_extract_cobalt": 1, "dye_extract_amber": 1},       "output_id": "mudejar_star_tile",   "output_count": 3},
    {"name": "Albarrada Panel",      "ingredients": {"clay": 2, "dye_extract_cobalt": 1},                               "output_id": "albarrada_panel",     "output_count": 2},
    {"name": "Sgraffito Wall",       "ingredients": {"clay": 2, "limestone_chip": 1},                                   "output_id": "sgraffito_wall",      "output_count": 4},
    {"name": "Trencadís Panel",      "ingredients": {"clay": 1, "dye_extract_cobalt": 1, "dye_extract_crimson": 1},     "output_id": "trencadis_panel",     "output_count": 2},
    {"name": "Azulejo Navy",         "ingredients": {"clay": 2, "dye_extract_cobalt": 2},                               "output_id": "azulejo_navy",        "output_count": 4},
    {"name": "Azulejo Manganese",    "ingredients": {"clay": 2, "dye_extract_violet": 1},                               "output_id": "azulejo_manganese",   "output_count": 4},
    {"name": "Plateresque Panel",    "ingredients": {"stone_chip": 3},                                                  "output_id": "plateresque_panel",   "output_count": 2},
    {"name": "Azulejo Cornice",      "ingredients": {"clay": 1, "dye_extract_cobalt": 1},                               "output_id": "azulejo_cornice",     "output_count": 6},
    {"name": "Talavera Fountain",    "ingredients": {"clay": 3, "dye_extract_cobalt": 1},                               "output_id": "talavera_fountain",   "output_count": 1},
    {"name": "Barcelona Tile",       "ingredients": {"clay": 2, "dye_extract_rose": 1},                                 "output_id": "barcelona_tile",      "output_count": 4},
    {"name": "Moorish Archway Tile", "ingredients": {"stone_chip": 2, "clay": 1},                                       "output_id": "moorish_archway_tile","output_count": 2},
    {"name": "Portuguese Chimney",   "ingredients": {"clay": 3, "dye_extract_cobalt": 1},                               "output_id": "portuguese_chimney",  "output_count": 1},
    {"name": "Barcelos Tile",        "ingredients": {"clay": 2, "dye_extract_cobalt": 1},                               "output_id": "barcelos_tile",       "output_count": 3},
    {"name": "Reja Panel",           "ingredients": {"iron_chunk": 2, "clay": 1},                                       "output_id": "reja_panel",          "output_count": 2},
    {"name": "Orange Tree Planter",  "ingredients": {"clay": 3, "dye_extract_amber": 1},                                "output_id": "orange_tree_planter", "output_count": 1},
    {"name": "Wave Cobble",          "ingredients": {"stone_chip": 2},                                                  "output_id": "wave_cobble",         "output_count": 4},
    {"name": "Azulejo Facade Panel", "ingredients": {"clay": 3, "dye_extract_cobalt": 2},                               "output_id": "azulejo_facade_panel","output_count": 2},
    {"name": "Mudéjar Brick",        "ingredients": {"clay": 2, "stone_chip": 1},                                       "output_id": "mudejar_brick",       "output_count": 4},
    {"name": "Portuguese Bench",     "ingredients": {"stone_chip": 3, "dye_extract_cobalt": 1},                         "output_id": "portuguese_bench",    "output_count": 1},
    {"name": "Spanish Patio Floor",  "ingredients": {"clay": 2, "coal": 1},                                             "output_id": "spanish_patio_floor", "output_count": 4},
    {"name": "Arabic Roof Tile",     "ingredients": {"clay": 2},                                                        "output_id": "arabic_roof_tile",    "output_count": 4},
    {"name": "Moorish Column Tile",  "ingredients": {"clay": 2, "dye_extract_cobalt": 1, "dye_extract_verdant": 1},     "output_id": "moorish_column_tile", "output_count": 3},
    {"name": "Estremoz Marble",      "ingredients": {"limestone_block": 2},                                             "output_id": "estremoz_marble",     "output_count": 4},
    # Córdoba / Umayyad Architecture
    {"name": "Mezquita Arch",        "ingredients": {"clay": 2, "dye_extract_crimson": 1},                               "output_id": "mezquita_arch",       "output_count": 2},
    {"name": "Mihrab Tile",          "ingredients": {"clay": 2, "dye_extract_golden": 2},                                "output_id": "mihrab_tile",         "output_count": 1},
    {"name": "Medina Azahara Stone", "ingredients": {"limestone_block": 1, "stone_chip": 1},                             "output_id": "medina_azahara_stone","output_count": 3},
    {"name": "Córdoba Column",       "ingredients": {"limestone_block": 2},                                              "output_id": "cordoba_column",      "output_count": 2},
    {"name": "Orange Court Floor",   "ingredients": {"stone_chip": 2, "clay": 1},                                        "output_id": "orange_court_floor",  "output_count": 4},
    {"name": "Cordoban Leather",     "ingredients": {"clay": 1, "dye_extract_amber": 1, "dye_extract_golden": 1},        "output_id": "cordoban_leather",    "output_count": 2},
    {"name": "Umayyad Multilobed",   "ingredients": {"stone_chip": 3},                                                   "output_id": "umayyad_multilobed",  "output_count": 2},
    {"name": "Gold Tessera Panel",   "ingredients": {"clay": 1, "dye_extract_golden": 2},                                "output_id": "gold_tessera_panel",  "output_count": 2},
    {"name": "Umayyad Dome Rib",     "ingredients": {"stone_chip": 2, "limestone_chip": 1},                              "output_id": "umayyad_dome_rib",    "output_count": 3},
    {"name": "Kufic Panel",          "ingredients": {"stone_chip": 3},                                                   "output_id": "kufic_panel",         "output_count": 2},
    {"name": "Patio Flower Wall",    "ingredients": {"clay": 2, "dye_extract_crimson": 1},                               "output_id": "patio_flower_wall",   "output_count": 3},
    {"name": "Cordoban Patio Tile",  "ingredients": {"clay": 2, "stone_chip": 1},                                        "output_id": "cordoban_patio_tile", "output_count": 4},
    {"name": "Star Vault Panel",     "ingredients": {"stone_chip": 2, "clay": 1},                                        "output_id": "star_vault_panel",    "output_count": 3},
    {"name": "Andalusian Fountain",  "ingredients": {"clay": 3, "stone_chip": 2},                                        "output_id": "andalusian_fountain", "output_count": 1},
    {"name": "Nasrid Honeycomb",     "ingredients": {"stone_chip": 3, "dye_extract_amber": 1},                           "output_id": "nasrid_honeycomb",    "output_count": 2},
    # Zellige tiles
    {"name": "Zellige Blue",         "ingredients": {"clay": 2, "dye_extract_cobalt": 1},   "output_id": "zellige_blue",       "output_count": 4},
    {"name": "Zellige Terracotta",   "ingredients": {"clay": 3},                             "output_id": "zellige_terracotta", "output_count": 4},
    {"name": "Zellige Emerald",      "ingredients": {"clay": 2, "dye_extract_verdant": 1},  "output_id": "zellige_emerald",    "output_count": 4},
    {"name": "Zellige Ivory",        "ingredients": {"clay": 2, "dye_extract_ivory": 1},    "output_id": "zellige_white",      "output_count": 4},
    # Geometric stone
    {"name": "Star Tile",            "ingredients": {"stone_chip": 3, "coal": 1},           "output_id": "garden_star_tile",   "output_count": 2},
    {"name": "Geometric Mosaic",     "ingredients": {"stone_chip": 2, "clay": 2},           "output_id": "geometric_mosaic",   "output_count": 2},
    # Water features
    {"name": "Water Channel",        "ingredients": {"stone_chip": 2},                      "output_id": "water_channel",      "output_count": 2},
    {"name": "Ornamental Pool",      "ingredients": {"stone_chip": 4},                      "output_id": "ornamental_pool",    "output_count": 1},
    {"name": "Fountain Basin",       "ingredients": {"stone_chip": 3, "iron_chunk": 1},     "output_id": "fountain_basin",     "output_count": 1},
    {"name": "Tiered Fountain",      "ingredients": {"stone_chip": 5, "iron_chunk": 2},     "output_id": "tiered_fountain",    "output_count": 1},
    # Architectural elements
    {"name": "Horseshoe Arch",       "ingredients": {"stone_chip": 4},                      "output_id": "horseshoe_arch",     "output_count": 1},
    {"name": "Muqarnas Panel",       "ingredients": {"stone_chip": 2, "clay": 2},           "output_id": "muqarnas_panel",     "output_count": 2},
    {"name": "Arabesque Screen",     "ingredients": {"stone_chip": 2, "iron_chunk": 1},     "output_id": "arabesque_screen",   "output_count": 2},
    {"name": "Garden Column",        "ingredients": {"stone_chip": 4},                      "output_id": "garden_column",      "output_count": 1},
    {"name": "Marble Plinth",        "ingredients": {"limestone_block": 1, "stone_chip": 2},"output_id": "marble_plinth",      "output_count": 1},
    {"name": "Garden Obelisk",       "ingredients": {"stone_chip": 5},                      "output_id": "garden_obelisk",     "output_count": 1},
    # Living elements
    {"name": "Topiary Cone",         "ingredients": {"lumber": 1, "sapling": 2},            "output_id": "topiary_cone",       "output_count": 1},
    {"name": "Topiary Sphere",       "ingredients": {"lumber": 1, "sapling": 2},            "output_id": "topiary_sphere",     "output_count": 1},
    {"name": "Box Hedge",            "ingredients": {"lumber": 1, "sapling": 1},            "output_id": "box_hedge",          "output_count": 2},
    {"name": "Climbing Rose",        "ingredients": {"lumber": 1, "lavender": 1},           "output_id": "climbing_rose",      "output_count": 1},
    # Furnishings
    {"name": "Stone Bench",          "ingredients": {"stone_chip": 3, "lumber": 1},         "output_id": "stone_bench",        "output_count": 1},
    {"name": "Stone Urn",            "ingredients": {"stone_chip": 3},                      "output_id": "stone_urn",          "output_count": 1},
    {"name": "Terracotta Planter",   "ingredients": {"clay": 3},                            "output_id": "terracotta_planter", "output_count": 1},
    {"name": "Sundial",              "ingredients": {"stone_chip": 2, "iron_chunk": 1},     "output_id": "sundial",            "output_count": 1},
    {"name": "Garden Lantern",       "ingredients": {"iron_chunk": 2},                      "output_id": "garden_lantern",     "output_count": 1},
    # Paths and ground
    {"name": "Gravel Path",          "ingredients": {"stone_chip": 1},                      "output_id": "gravel_path",        "output_count": 4},
    {"name": "Mosaic Path",          "ingredients": {"stone_chip": 2, "clay": 1},           "output_id": "mosaic_path",        "output_count": 2},
    {"name": "Terracotta Path",      "ingredients": {"clay": 2},                            "output_id": "terracotta_path",    "output_count": 4},
    {"name": "Cobble Circle",        "ingredients": {"stone_chip": 3},                      "output_id": "cobble_circle",      "output_count": 1},
    # --- Garden Workshop extension ---
    # Structural / architectural
    {"name": "Pergola Post",         "ingredients": {"lumber": 3, "sapling": 1},            "output_id": "pergola_post",        "output_count": 2},
    {"name": "Wisteria Arch",        "ingredients": {"stone_chip": 3, "lavender": 2},       "output_id": "wisteria_arch",       "output_count": 1},
    {"name": "Garden Gate",          "ingredients": {"iron_chunk": 3},                       "output_id": "garden_gate",         "output_count": 1},
    {"name": "Low Garden Wall",      "ingredients": {"stone_chip": 3, "limestone_chip": 1}, "output_id": "low_garden_wall",     "output_count": 2},
    {"name": "Pool Coping",          "ingredients": {"limestone_block": 1, "stone_chip": 1},"output_id": "pool_coping",         "output_count": 4},
    # Paths and flooring
    {"name": "Stepping Stone",       "ingredients": {"stone_chip": 2},                      "output_id": "stepping_stone",      "output_count": 3},
    {"name": "Opus Vermiculatum",    "ingredients": {"stone_chip": 2, "clay": 1},           "output_id": "opus_vermiculatum",   "output_count": 2},
    {"name": "Porphyry Tile",        "ingredients": {"stone_chip": 2, "ruby": 1},           "output_id": "porphyry_tile",       "output_count": 4},
    {"name": "Brick Edging",         "ingredients": {"clay": 1},                            "output_id": "brick_edging",        "output_count": 6},
    # Living elements
    {"name": "Spiral Topiary",       "ingredients": {"lumber": 1, "sapling": 3},            "output_id": "spiral_topiary",      "output_count": 1},
    {"name": "Maze Hedge",           "ingredients": {"lumber": 2, "sapling": 2},            "output_id": "maze_hedge",          "output_count": 1},
    {"name": "Wisteria Wall",        "ingredients": {"lumber": 1, "lavender": 3},           "output_id": "wisteria_wall",       "output_count": 2},
    {"name": "Potted Citrus",        "ingredients": {"clay": 2, "sapling": 1},              "output_id": "potted_citrus",       "output_count": 1},
    # Furnishings
    {"name": "Marble Statue",        "ingredients": {"limestone_block": 2, "stone_chip": 3},"output_id": "marble_statue",       "output_count": 1},
    {"name": "Marble Birdbath",      "ingredients": {"limestone_block": 1, "stone_chip": 2},"output_id": "marble_birdbath",     "output_count": 1},
    {"name": "Garden Table",         "ingredients": {"stone_chip": 4},                      "output_id": "garden_table",        "output_count": 1},
    {"name": "Iron Trellis",         "ingredients": {"iron_chunk": 2, "lumber": 1},         "output_id": "iron_trellis",        "output_count": 2},
    # Moorish / Mediterranean
    {"name": "Nasrid Panel",         "ingredients": {"stone_chip": 2, "clay": 3},           "output_id": "nasrid_panel",        "output_count": 2},
    {"name": "Scallop Niche",        "ingredients": {"stone_chip": 3},                      "output_id": "scallop_niche",       "output_count": 1},
    {"name": "Terrace Balustrade",   "ingredients": {"limestone_block": 1, "iron_chunk": 1},"output_id": "terrace_balustrade",  "output_count": 2},
    # Japanese garden blocks
    {"name": "Zen Gravel",          "ingredients": {"sand_grain": 2},                       "output_id": "zen_gravel",          "output_count": 4},
    {"name": "Karesansui Rock",     "ingredients": {"stone_chip": 3},                       "output_id": "karesansui_rock",     "output_count": 1},
    {"name": "Moss Carpet",         "ingredients": {"sapling": 1},                          "output_id": "moss_carpet",         "output_count": 4},
    {"name": "Tsukubai",            "ingredients": {"stone_chip": 3, "iron_chunk": 1},      "output_id": "tsukubai",            "output_count": 1},
    {"name": "Toro Lantern",        "ingredients": {"stone_chip": 4},                       "output_id": "toro_lantern",        "output_count": 1},
    {"name": "Yukimi Lantern",      "ingredients": {"stone_chip": 3},                       "output_id": "yukimi_lantern",      "output_count": 1},
    {"name": "Bamboo Fence",        "ingredients": {"lumber": 2},                           "output_id": "bamboo_fence_jp",     "output_count": 4},
    {"name": "Roji Stone",          "ingredients": {"stone_chip": 1},                       "output_id": "roji_stone",          "output_count": 3},
    {"name": "Cloud-Pruned Pine",   "ingredients": {"lumber": 1, "sapling": 3},             "output_id": "pine_topiary_jp",     "output_count": 1},
    {"name": "Japanese Maple",      "ingredients": {"sapling": 2, "dye_extract_crimson": 1},"output_id": "japanese_maple",      "output_count": 1},
    {"name": "Shishi-odoshi",       "ingredients": {"lumber": 2, "iron_chunk": 1},          "output_id": "shishi_odoshi",       "output_count": 1},
    {"name": "Arched Bridge",       "ingredients": {"lumber": 3, "iron_chunk": 1},          "output_id": "red_arch_bridge",     "output_count": 1},
    {"name": "Wave Ceramic",        "ingredients": {"clay": 2, "dye_extract_cobalt": 1},    "output_id": "wave_ceramic",        "output_count": 2},
    {"name": "Zen Sand Ring",       "ingredients": {"sand_grain": 3},                       "output_id": "zen_sand_ring",       "output_count": 2},
    {"name": "Bamboo Gate",         "ingredients": {"lumber": 3},                           "output_id": "bamboo_gate_jp",      "output_count": 1},
    {"name": "Wabi Stone",          "ingredients": {"stone_chip": 2},                       "output_id": "wabi_stone",          "output_count": 1},
    {"name": "Cherry Blossom Arch", "ingredients": {"lumber": 2, "lavender": 2},            "output_id": "cherry_arch",         "output_count": 1},
    {"name": "Tatami Paving",       "ingredients": {"lumber": 1, "clay": 1},                "output_id": "tatami_paving",       "output_count": 2},
    {"name": "Ikebana Stone",       "ingredients": {"stone_chip": 2},                       "output_id": "ikebana_stone",       "output_count": 1},
    {"name": "Kanji Stone",         "ingredients": {"stone_chip": 2, "coal": 1},            "output_id": "kanji_stone",         "output_count": 1},
    {"name": "Maple Leaf Tile",     "ingredients": {"clay": 2, "dye_extract_crimson": 1},   "output_id": "maple_leaf_tile",     "output_count": 4},
    {"name": "Noren Panel",         "ingredients": {"lumber": 1, "dye_extract_cobalt": 1},  "output_id": "noren_panel",         "output_count": 2},
    {"name": "Tsuru Tile",          "ingredients": {"clay": 2},                             "output_id": "tsuru_tile",          "output_count": 4},
    {"name": "Pine Screen",         "ingredients": {"lumber": 2},                           "output_id": "pine_screen_jp",      "output_count": 2},
    {"name": "Kare Bridge",         "ingredients": {"stone_chip": 3, "lumber": 1},          "output_id": "kare_bridge",         "output_count": 1},
    # Chinese garden blocks
    {"name": "Pebble Mosaic",       "ingredients": {"stone_chip": 2, "clay": 1},            "output_id": "pebble_mosaic_cn",    "output_count": 2},
    {"name": "Zigzag Bridge",       "ingredients": {"stone_chip": 4},                       "output_id": "zigzag_bridge",       "output_count": 2},
    {"name": "Cloud Wall",          "ingredients": {"clay": 3, "limestone_chip": 1},        "output_id": "cloud_wall",          "output_count": 2},
    {"name": "Dragon Wall",         "ingredients": {"clay": 3, "dye_extract_crimson": 1},   "output_id": "dragon_wall_cn",      "output_count": 1},
    {"name": "Lotus Pond",          "ingredients": {"stone_chip": 2, "sapling": 1},         "output_id": "lotus_pond",          "output_count": 1},
    {"name": "Hexagonal Pavilion",  "ingredients": {"stone_chip": 3},                       "output_id": "hex_pavilion_tile",   "output_count": 2},
    {"name": "Compass Paving",      "ingredients": {"stone_chip": 4},                       "output_id": "compass_paving",      "output_count": 1},
    {"name": "Wave Balustrade",     "ingredients": {"stone_chip": 3},                       "output_id": "wave_balustrade_cn",  "output_count": 2},
    {"name": "Ceramic Garden Seat", "ingredients": {"clay": 3, "dye_extract_cobalt": 1},    "output_id": "ceramic_seat",        "output_count": 1},
    {"name": "Bonsai Tray",         "ingredients": {"stone_chip": 2, "sapling": 1},         "output_id": "bonsai_tray",         "output_count": 1},
    {"name": "Scholar Screen",      "ingredients": {"lumber": 2, "stone_chip": 1},          "output_id": "scholar_screen",      "output_count": 2},
    {"name": "Chrysanthemum Tile",  "ingredients": {"clay": 2, "dye_extract_golden": 1},    "output_id": "chrysanthemum_tile",  "output_count": 4},
    {"name": "Plum Blossom Tile",   "ingredients": {"clay": 2, "dye_extract_rose": 1},      "output_id": "plum_blossom_tile",   "output_count": 4},
    {"name": "Moon Pavement",       "ingredients": {"stone_chip": 3},                       "output_id": "moon_pavement",       "output_count": 1},
    {"name": "Bamboo Grove",        "ingredients": {"lumber": 3, "sapling": 1},             "output_id": "bamboo_grove",        "output_count": 1},
    {"name": "Osmanthus Bush",      "ingredients": {"sapling": 2, "dye_extract_golden": 1}, "output_id": "osmanthus_bush",      "output_count": 1},
    {"name": "Water Lily",          "ingredients": {"stone_chip": 2, "sapling": 1},         "output_id": "water_lily_tile",     "output_count": 2},
    {"name": "Koi Pond",            "ingredients": {"stone_chip": 4, "iron_chunk": 1},      "output_id": "koi_pond",            "output_count": 1},
    {"name": "Lakeside Rock",       "ingredients": {"stone_chip": 2},                       "output_id": "lakeside_rock",       "output_count": 1},
    {"name": "Cloud Collar Tile",   "ingredients": {"clay": 2},                             "output_id": "cloud_collar_tile",   "output_count": 4},
    {"name": "Imperial Paving",     "ingredients": {"stone_chip": 5},                       "output_id": "imperial_paving",     "output_count": 1},
    {"name": "Pavilion Column",     "ingredients": {"lumber": 2, "dye_extract_crimson": 1}, "output_id": "pavilion_column_cn",  "output_count": 1},
    {"name": "Eight Diagram",       "ingredients": {"stone_chip": 3, "coal": 1},            "output_id": "eight_diagram",       "output_count": 1},
    {"name": "Teahouse Step",       "ingredients": {"limestone_block": 1, "stone_chip": 1}, "output_id": "tea_house_step",      "output_count": 2},
    {"name": "Lantern Festival",    "ingredients": {"lumber": 1, "dye_extract_crimson": 1}, "output_id": "lantern_festival",    "output_count": 3},
    # Renaissance garden blocks — Classical architecture
    {"name": "Ionic Column",        "ingredients": {"limestone_block": 2, "stone_chip": 2},  "output_id": "ionic_column_base",   "output_count": 1},
    {"name": "Doric Entablature",   "ingredients": {"limestone_block": 1, "stone_chip": 3},  "output_id": "doric_entablature",   "output_count": 2},
    {"name": "Rusticated Base",     "ingredients": {"stone_chip": 4},                         "output_id": "rusticated_base",     "output_count": 1},
    {"name": "Garden Loggia",       "ingredients": {"limestone_block": 2, "iron_chunk": 1},   "output_id": "garden_loggia",       "output_count": 1},
    {"name": "Triumphal Arch",      "ingredients": {"limestone_block": 3, "stone_chip": 2},   "output_id": "triumphal_arch_r",    "output_count": 1},
    {"name": "Exedra Seat",         "ingredients": {"limestone_block": 2},                    "output_id": "exedra_seat",         "output_count": 1},
    {"name": "Herm Pillar",         "ingredients": {"stone_chip": 3, "coal": 1},              "output_id": "herm_pillar",         "output_count": 1},
    {"name": "Nymphaeum Panel",     "ingredients": {"stone_chip": 2, "clay": 2},              "output_id": "nymphaeum_panel",     "output_count": 2},
    {"name": "Grotto Stone",        "ingredients": {"stone_chip": 2},                         "output_id": "grotto_stone",        "output_count": 4},
    {"name": "Amphitheater Tier",   "ingredients": {"stone_chip": 2, "sapling": 1},           "output_id": "amphitheater_tier",   "output_count": 2},
    # Water features
    {"name": "Giochi d'Acqua",      "ingredients": {"stone_chip": 2, "iron_chunk": 2},        "output_id": "giochi_acqua",        "output_count": 1},
    {"name": "Garden Rill",         "ingredients": {"stone_chip": 2},                         "output_id": "rill_block",          "output_count": 4},
    {"name": "Water Cascade",       "ingredients": {"stone_chip": 3, "iron_chunk": 1},        "output_id": "cascade_block",       "output_count": 1},
    {"name": "Grotto Pool",         "ingredients": {"stone_chip": 3},                         "output_id": "grotto_pool",         "output_count": 1},
    {"name": "Wall Fountain",       "ingredients": {"stone_chip": 3, "iron_chunk": 1},        "output_id": "wall_fountain",       "output_count": 1},
    {"name": "Basin Surround",      "ingredients": {"limestone_block": 1, "stone_chip": 2},   "output_id": "basin_surround",      "output_count": 2},
    {"name": "Formal Canal",        "ingredients": {"stone_chip": 3},                         "output_id": "canal_block",         "output_count": 2},
    {"name": "Terme Pool",          "ingredients": {"stone_chip": 4, "iron_chunk": 1},        "output_id": "terme_pool",          "output_count": 1},
    # Parterre and planting
    {"name": "Broderie Parterre",   "ingredients": {"sapling": 2},                            "output_id": "parterre_broderie",   "output_count": 2},
    {"name": "Parterre Bed",        "ingredients": {"sapling": 1, "clay": 1},                 "output_id": "parterre_compartment","output_count": 2},
    {"name": "Allée Tree",          "ingredients": {"lumber": 1, "sapling": 2},               "output_id": "allee_tree",          "output_count": 2},
    {"name": "Pleached Hedge",      "ingredients": {"lumber": 2, "sapling": 2},               "output_id": "pleached_hedge",      "output_count": 2},
    {"name": "Espalier Wall",       "ingredients": {"lumber": 2, "sapling": 1},               "output_id": "espalier_wall",       "output_count": 2},
    {"name": "Knot Garden",         "ingredients": {"sapling": 3},                            "output_id": "knot_garden",         "output_count": 1},
    {"name": "Turf Theater",        "ingredients": {"sapling": 1, "stone_chip": 1},           "output_id": "turf_theater",        "output_count": 2},
    {"name": "Carpet Bedding",      "ingredients": {"sapling": 2, "dye_extract_crimson": 1},  "output_id": "carpet_bed",          "output_count": 2},
    # Paths and flooring
    {"name": "Opus Sectile",        "ingredients": {"limestone_block": 1, "clay": 2},         "output_id": "opus_sectile",        "output_count": 2},
    {"name": "Travertine Floor",    "ingredients": {"limestone_chip": 3},                      "output_id": "travertine_floor",    "output_count": 4},
    {"name": "Herringbone Path",    "ingredients": {"clay": 2},                                "output_id": "herringbone_garden",  "output_count": 4},
    {"name": "Stone Ramp",          "ingredients": {"stone_chip": 3},                         "output_id": "ramp_stone",          "output_count": 2},
    {"name": "Garden Steps",        "ingredients": {"limestone_block": 1, "stone_chip": 2},   "output_id": "garden_steps",        "output_count": 2},
    {"name": "Sand Allée",          "ingredients": {"sand_grain": 2},                         "output_id": "sand_allee",          "output_count": 4},
    {"name": "Patterned Pavement",  "ingredients": {"stone_chip": 2, "limestone_chip": 2},    "output_id": "patterned_pavement",  "output_count": 2},
    {"name": "Inlaid Marble",       "ingredients": {"limestone_block": 1, "dye_extract_cobalt": 1}, "output_id": "inlaid_marble", "output_count": 2},
    # Furnishings and decorative
    {"name": "Tall Sundial",        "ingredients": {"stone_chip": 3, "iron_chunk": 1},        "output_id": "tall_sundial",        "output_count": 1},
    {"name": "Stone Vase",          "ingredients": {"limestone_block": 1, "stone_chip": 2},   "output_id": "stone_vase",          "output_count": 1},
    {"name": "Stone Sphere",        "ingredients": {"stone_chip": 2},                         "output_id": "stone_sphere",        "output_count": 1},
    {"name": "Curved Bench",        "ingredients": {"limestone_block": 1, "stone_chip": 2},   "output_id": "curved_bench",        "output_count": 1},
    {"name": "Ornate Gate",         "ingredients": {"iron_chunk": 4},                         "output_id": "ornate_gate",         "output_count": 1},
    {"name": "Lead Planter",        "ingredients": {"iron_chunk": 2, "stone_chip": 1},        "output_id": "lead_planter",        "output_count": 1},
    {"name": "Terrace Urn",         "ingredients": {"limestone_block": 1, "stone_chip": 3},   "output_id": "terrace_urn",         "output_count": 1},
    {"name": "Stone Pineapple",     "ingredients": {"stone_chip": 3},                         "output_id": "stone_pineapple",     "output_count": 1},
    # Structural elements
    {"name": "Grotto Arch",         "ingredients": {"stone_chip": 3, "coal": 1},              "output_id": "grotto_arch",         "output_count": 1},
    {"name": "Pergola Beam",        "ingredients": {"lumber": 3},                             "output_id": "pergola_beam",        "output_count": 2},
    {"name": "Loggia Arch",         "ingredients": {"limestone_block": 2, "stone_chip": 2},   "output_id": "loggia_arch",         "output_count": 1},
    {"name": "Wall Niche",          "ingredients": {"stone_chip": 3},                         "output_id": "garden_wall_niche",   "output_count": 1},
    {"name": "Orangery Window",     "ingredients": {"stone_chip": 2, "iron_chunk": 1},        "output_id": "orangery_window",     "output_count": 2},
    {"name": "Belvedere Panel",     "ingredients": {"limestone_block": 1, "stone_chip": 2},   "output_id": "belvedere_panel",     "output_count": 2},
    {"name": "Bosco Tree",          "ingredients": {"lumber": 2, "sapling": 2},               "output_id": "bosco_tree",          "output_count": 1},
    {"name": "Secret Garden Wall",  "ingredients": {"stone_chip": 3, "sapling": 1},           "output_id": "giardino_segreto",    "output_count": 2},
    # Renaissance palace decorative ornament
    {"name": "Cartouche",           "ingredients": {"limestone_block": 1, "stone_chip": 2},       "output_id": "cartouche_ren",        "output_count": 2},
    {"name": "Putti Frieze",        "ingredients": {"polished_marble": 2, "stone_chip": 1},       "output_id": "putti_frieze",         "output_count": 2},
    {"name": "Festoon Panel",       "ingredients": {"limestone_block": 1, "stone_chip": 1},       "output_id": "festoon_panel",        "output_count": 2},
    {"name": "Trophy Panel",        "ingredients": {"iron_chunk": 2, "stone_chip": 2},             "output_id": "trophy_panel_ren",     "output_count": 2},
    {"name": "Portrait Medallion",  "ingredients": {"polished_marble": 2, "gold_nugget": 1},      "output_id": "medallion_portrait",   "output_count": 2},
    {"name": "Laurel Frieze",       "ingredients": {"limestone_block": 1, "stone_chip": 2},       "output_id": "laurel_frieze",        "output_count": 2},
    # Gardening additions
    {"name": "Ornamental Grass",    "ingredients": {"sapling": 1},                                "output_id": "ornamental_grass",     "output_count": 2},
    {"name": "Flowering Shrub",     "ingredients": {"sapling": 2},                                "output_id": "flowering_shrub",      "output_count": 1},
    {"name": "Holly Shrub",         "ingredients": {"sapling": 2, "coal": 1},                    "output_id": "holly_shrub",          "output_count": 1},
    {"name": "Topiary Peacock",     "ingredients": {"lumber": 1, "sapling": 4},                  "output_id": "topiary_peacock",      "output_count": 1},
    {"name": "Topiary Bear",        "ingredients": {"lumber": 1, "sapling": 4},                  "output_id": "topiary_bear",         "output_count": 1},
    {"name": "Topiary Rabbit",      "ingredients": {"lumber": 1, "sapling": 3},                  "output_id": "topiary_rabbit",       "output_count": 1},
    {"name": "Rose Bed",            "ingredients": {"sapling": 2, "lavender": 1},                "output_id": "rose_bed",             "output_count": 1},
    {"name": "Tulip Bed",           "ingredients": {"sapling": 2, "dye_extract_crimson": 1},     "output_id": "tulip_bed",            "output_count": 1},
    {"name": "Cottage Garden",      "ingredients": {"sapling": 3},                               "output_id": "cottage_garden_bed",   "output_count": 1},
    {"name": "Cherub Fountain",     "ingredients": {"polished_marble": 2, "stone_chip": 3},      "output_id": "cherub_fountain",      "output_count": 1},
    {"name": "Lion Head Fountain",  "ingredients": {"stone_chip": 4, "iron_chunk": 1},           "output_id": "lion_head_fountain",   "output_count": 1},
    {"name": "Mosaic Fountain",     "ingredients": {"stone_chip": 3, "clay": 2},                 "output_id": "mosaic_fountain",      "output_count": 1},
    {"name": "Lavender Bed",        "ingredients": {"lavender": 2, "sapling": 1},                 "output_id": "lavender_bed",         "output_count": 1},
    {"name": "Sunflower Bed",       "ingredients": {"sapling": 2, "dye_extract_golden": 1},       "output_id": "sunflower_bed",        "output_count": 1},
    {"name": "Dahlia Bed",          "ingredients": {"sapling": 2, "dye_extract_crimson": 1},      "output_id": "dahlia_bed",           "output_count": 1},
    {"name": "Topiary Swan",        "ingredients": {"lumber": 1, "sapling": 4},                   "output_id": "topiary_swan",         "output_count": 1},
    {"name": "Topiary Fox",         "ingredients": {"lumber": 1, "sapling": 4},                   "output_id": "topiary_fox",          "output_count": 1},
    {"name": "Topiary Elephant",    "ingredients": {"lumber": 2, "sapling": 5},                   "output_id": "topiary_elephant",     "output_count": 1},
    {"name": "Peony Bush",          "ingredients": {"sapling": 2, "dye_extract_rose": 1},         "output_id": "peony_bush",           "output_count": 1},
    {"name": "Fern Clump",          "ingredients": {"sapling": 1},                                "output_id": "fern_clump",           "output_count": 2},
    {"name": "Raised Garden Bed",   "ingredients": {"lumber": 2, "dirt_clump": 2},                "output_id": "raised_garden_bed",    "output_count": 1},
    {"name": "Lily Pad Pond",       "ingredients": {"sapling": 2, "stone_chip": 1},               "output_id": "lily_pad_pond",        "output_count": 1},
    {"name": "Bee Skep",            "ingredients": {"straw": 3},                                  "output_id": "bee_skep",             "output_count": 1},
    {"name": "Garden Wheelbarrow",  "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "garden_wheelbarrow",   "output_count": 1},
    {"name": "Iris Bed",            "ingredients": {"sapling": 2, "dye_extract_violet": 1},       "output_id": "iris_bed",             "output_count": 1},
    {"name": "Poppy Bed",           "ingredients": {"sapling": 2, "dye_extract_crimson": 1},      "output_id": "poppy_bed",            "output_count": 1},
    {"name": "Foxglove Patch",      "ingredients": {"sapling": 2, "dye_extract_rose": 1},         "output_id": "foxglove_patch",       "output_count": 1},
    {"name": "Snowdrop Patch",      "ingredients": {"sapling": 1, "dye_extract_ivory": 1},        "output_id": "snowdrop_patch",       "output_count": 2},
    {"name": "Marigold Bed",        "ingredients": {"sapling": 2, "dye_extract_amber": 1},        "output_id": "marigold_bed",         "output_count": 1},
    {"name": "Boxwood Ball",        "ingredients": {"lumber": 1, "sapling": 2},                   "output_id": "boxwood_ball",         "output_count": 1},
    {"name": "Rhododendron",        "ingredients": {"sapling": 3, "dye_extract_rose": 1},         "output_id": "rhododendron_bush",    "output_count": 1},
    {"name": "Bamboo Clump",        "ingredients": {"lumber": 1, "sapling": 2},                   "output_id": "bamboo_clump",         "output_count": 2},
    {"name": "Agapanthus",          "ingredients": {"sapling": 2, "dye_extract_cobalt": 1},       "output_id": "agapanthus_patch",     "output_count": 1},
    {"name": "Topiary Dragon",      "ingredients": {"lumber": 2, "sapling": 5},                   "output_id": "topiary_dragon",       "output_count": 1},
    {"name": "Topiary Giraffe",     "ingredients": {"lumber": 2, "sapling": 5},                   "output_id": "topiary_giraffe",      "output_count": 1},
    {"name": "Topiary Hedgehog",    "ingredients": {"lumber": 1, "sapling": 3},                   "output_id": "topiary_hedgehog",     "output_count": 1},
    {"name": "Bubble Fountain",     "ingredients": {"stone_chip": 3},                             "output_id": "bubble_fountain",      "output_count": 1},
    {"name": "Shell Fountain",      "ingredients": {"stone_chip": 3, "limestone_chip": 2},        "output_id": "shell_fountain",       "output_count": 1},
    {"name": "Millstone Fountain",  "ingredients": {"stone_chip": 4},                             "output_id": "millstone_fountain",   "output_count": 1},
    {"name": "Trellis Arch",        "ingredients": {"lumber": 3, "sapling": 2},                   "output_id": "trellis_arch",         "output_count": 1},
    {"name": "Cold Frame",          "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "cold_frame",           "output_count": 1},
    {"name": "Garden Swing",        "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "garden_swing",         "output_count": 1},
    {"name": "Wicker Fence",        "ingredients": {"straw": 2},                                  "output_id": "wicker_fence",         "output_count": 3},
    {"name": "Hanging Basket",      "ingredients": {"straw": 1, "sapling": 2},                    "output_id": "hanging_basket",       "output_count": 1},
    {"name": "Standard Rose",       "ingredients": {"lumber": 1, "sapling": 2, "lavender": 1},    "output_id": "standard_rose",        "output_count": 1},
    {"name": "Garden Gnome",        "ingredients": {"clay": 2, "dye_extract_crimson": 1},         "output_id": "garden_gnome",         "output_count": 1},
    {"name": "Topiary Arch",        "ingredients": {"lumber": 2, "sapling": 4},                   "output_id": "topiary_arch",         "output_count": 1},
    {"name": "Chamomile Lawn",      "ingredients": {"chamomile": 2, "sapling": 1},                "output_id": "chamomile_lawn",       "output_count": 2},
    {"name": "Creeping Thyme",      "ingredients": {"thyme": 2, "sapling": 1},                    "output_id": "creeping_thyme",       "output_count": 2},
    {"name": "Hydrangea",           "ingredients": {"sapling": 3, "dye_extract_cobalt": 1},       "output_id": "hydrangea_bush",       "output_count": 1},
    {"name": "Allium Patch",        "ingredients": {"sapling": 2, "dye_extract_violet": 1},       "output_id": "allium_patch",         "output_count": 1},
    {"name": "Sweet Pea Trellis",   "ingredients": {"lumber": 1, "sapling": 2, "dye_extract_rose": 1}, "output_id": "sweet_pea_trellis", "output_count": 1},
    {"name": "Bleeding Heart",      "ingredients": {"sapling": 2, "dye_extract_crimson": 1},      "output_id": "bleeding_heart_patch", "output_count": 1},
    {"name": "Astilbe Patch",       "ingredients": {"sapling": 2, "dye_extract_rose": 1},         "output_id": "astilbe_patch",        "output_count": 1},
    {"name": "Wisteria Pillar",     "ingredients": {"stone_chip": 2, "sapling": 3},               "output_id": "wisteria_pillar",      "output_count": 1},
    {"name": "Topiary Snail",       "ingredients": {"lumber": 1, "sapling": 3},                   "output_id": "topiary_snail",        "output_count": 1},
    {"name": "Topiary Mushroom",    "ingredients": {"lumber": 1, "sapling": 3},                   "output_id": "topiary_mushroom",     "output_count": 1},
    {"name": "Topiary Owl",         "ingredients": {"lumber": 1, "sapling": 4},                   "output_id": "topiary_owl",          "output_count": 1},
    {"name": "Topiary Dinosaur",    "ingredients": {"lumber": 2, "sapling": 5},                   "output_id": "topiary_dinosaur",     "output_count": 1},
    {"name": "Koi Pool",            "ingredients": {"stone_chip": 4, "iron_chunk": 1},            "output_id": "koi_pool",             "output_count": 1},
    {"name": "Stone Trough",        "ingredients": {"stone_chip": 4},                             "output_id": "stone_trough_planter", "output_count": 1},
    {"name": "Rain Barrel",         "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "rain_barrel",          "output_count": 1},
    {"name": "Moss Patch",          "ingredients": {"sapling": 1, "dirt_clump": 1},               "output_id": "moss_patch",           "output_count": 3},
    {"name": "Clover Lawn",         "ingredients": {"sapling": 1},                                "output_id": "clover_lawn",          "output_count": 3},
    {"name": "Bark Mulch",          "ingredients": {"lumber": 1},                                 "output_id": "bark_mulch",           "output_count": 4},
    {"name": "Stone Frog",          "ingredients": {"stone_chip": 2},                             "output_id": "stone_frog",           "output_count": 1},
    {"name": "Garden Dovecote",     "ingredients": {"lumber": 2, "limestone_block": 1},           "output_id": "garden_dovecote",      "output_count": 1},
    {"name": "Stone Hedgehog",      "ingredients": {"stone_chip": 2},                             "output_id": "stone_hedgehog",       "output_count": 1},
    {"name": "Bird Table",          "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "bird_table",           "output_count": 1},
    {"name": "Garden Clock",        "ingredients": {"iron_chunk": 2, "stone_chip": 1},            "output_id": "garden_clock",         "output_count": 1},
    {"name": "Iron Obelisk",        "ingredients": {"iron_chunk": 3},                             "output_id": "garden_obelisk_metal", "output_count": 1},
    {"name": "Potting Table",       "ingredients": {"lumber": 2, "iron_chunk": 1},                "output_id": "potting_table",        "output_count": 1},
    {"name": "Compost Heap",        "ingredients": {"dirt_clump": 2, "sapling": 1},               "output_id": "compost_heap",         "output_count": 1},
    {"name": "Toad House",          "ingredients": {"clay": 2, "dye_extract_verdant": 1},         "output_id": "garden_toad_house",    "output_count": 1},
]

# ---------------------------------------------------------------------------
# Juicer recipes
# ---------------------------------------------------------------------------

JUICER_RECIPES = [
    # Single-fruit juices
    {"name": "Apple Juice",         "ingredients": {"apple": 3},                                          "output_id": "apple_juice",         "output_count": 2},
    {"name": "Pear Juice",          "ingredients": {"pear": 3},                                           "output_id": "pear_juice",          "output_count": 2},
    {"name": "Pomegranate Juice",   "ingredients": {"pomegranate": 3},                                    "output_id": "pomegranate_juice",   "output_count": 2},
    {"name": "Watermelon Juice",    "ingredients": {"watermelon": 2},                                     "output_id": "watermelon_juice",    "output_count": 2},
    {"name": "Fig Nectar",          "ingredients": {"fig": 3},                                            "output_id": "fig_nectar",          "output_count": 2},
    # Two-fruit blends
    {"name": "Lemonade",            "ingredients": {"lemon": 2, "apple": 1},                              "output_id": "lemonade",            "output_count": 2},
    {"name": "Strawberry Lemonade", "ingredients": {"strawberry": 2, "lemon": 1},                        "output_id": "strawberry_lemonade", "output_count": 2},
    {"name": "Berry Blast",         "ingredients": {"strawberry": 2, "pomegranate": 1},                   "output_id": "berry_blast",         "output_count": 2},
    {"name": "Citrus Sunrise",      "ingredients": {"lemon": 2, "pomegranate": 1},                        "output_id": "citrus_sunrise",      "output_count": 2},
    {"name": "Tropical Punch",      "ingredients": {"lemon": 1, "prickly_pear_fruit": 2},                 "output_id": "tropical_punch",      "output_count": 2},
    # Three-fruit blends
    {"name": "Orchard Blend",       "ingredients": {"apple": 1, "pear": 1, "pomegranate": 1},             "output_id": "orchard_blend",       "output_count": 2},
    {"name": "Desert Cooler",       "ingredients": {"prickly_pear_fruit": 1, "fig": 1, "lemon": 1},       "output_id": "desert_cooler",       "output_count": 2},
]

# ---------------------------------------------------------------------------
# Recipe book grouping — controls display order and category headers
# Maps group label -> list of output_ids in display order
# ---------------------------------------------------------------------------

RECIPE_GROUPS = {
    "Tools": [
        "stone_pickaxe", "iron_pickaxe", "gold_pickaxe", "tempered_pickaxe",
        "stone_axe", "iron_axe", "gold_axe", "tempered_axe",
        "shears", "bucket", "hoe", "watering_can", "hunting_knife",
    ],
    "Farming": [
        "compost_bin_item", "well_item", "farm_bot_item", "iron_farm_bot_item",
        "crystal_farm_bot_item", "garden_block",
        "strawberry_seed_premium", "tomato_seed_premium", "watermelon_seed_premium",
        "corn_seed_premium", "rice_seed_premium",
    ],
    "Building": [
        "wood_stairs", "ladder", "wood_fence", "iron_fence",
        "wood_door", "iron_door", "bed", "chest_item", "empty_barrel", "backhoe_item",
        "elevator_stop", "elevator_cable", "elevator_car",
        "mine_track", "mine_track_stop", "minecart",
        "trade_block",
    ],
    "Automation": [
        "coal_miner_item", "iron_miner_item", "crystal_miner_item",
        "automation_bench_item",
    ],
    "Rock & Gems": [
        "diamond", "tumbler_item", "crusher_item", "gem_cutter_item",
        "kiln_item", "resonance_item",
    ],
    "Smelting": [
        "smelter_item",
    ],
    "Cooking Stations": [
        "bakery_item", "wok_item", "steamer_item", "noodle_pot_item",
        "bbq_grill_item", "clay_pot_item", "desert_forge_item",
        "artisan_bench_item", "fossil_table_item", "juicer_item",
    ],
    "Coffee": [
        "roaster_item", "blend_station_item", "brew_station_item", "anaerobic_tank_item",
    ],
    "Wine": [
        "grape_press_item", "fermentation_item", "wine_cellar_item",
    ],
    "Spirits": [
        "still_item", "barrel_room_item", "bottling_item",
    ],
    "Brewery": [
        "brew_kettle_item", "ferm_vessel_item", "taproom_item",
    ],
    "Tea": [
        "withering_rack_item", "oxidation_station_item", "tea_cellar_item", "roasting_kiln_item",
    ],
    "Herbalism": [
        "drying_rack_item",
    ],
    "Textiles": [
        "spinning_wheel_item", "dye_vat_item", "loom_item",
    ],
    "Glassblowing": [
        "glass_kiln_item",
    ],
    "Cheese": [
        "dairy_vat_item", "cheese_press_item", "aging_cave_item",
    ],
    "Fishing": [
        "fishing_pole", "cane_rod", "composite_rod", "bait_station_item", "fish_trophy_item",
    ],
    "Wildlife": [
        "bird_feeder", "bird_bath", "binoculars", "bug_net", "insect_display_case", "light_trap",
        "wildflower_display",
    ],
    "Horses": [
        "saddle", "horse_brush", "horseshoe", "sugar_lump",
        "stable_item", "horse_trough_item", "cart",
    ],
    "Hunting": [
        "fletching_table_item",
        "wood_bow", "recurve_bow", "composite_bow", "longbow", "crossbow",
        "wood_arrow", "bone_arrow", "flint_arrow", "iron_arrow",
        "barbed_arrow", "broadhead_arrow", "poison_arrow", "gold_arrow",
    ],
    "Jewelry": [
        "jewelry_workbench_item",
    ],
    "Garden": [
        "garden_workshop_item",
    ],
    "Sculpture": [
        "chisel", "sculptors_bench_item",
    ],
    "Tapestry": [
        "weaving_needle", "tapestry_frame_item",
    ],
    "Pottery": [
        "pottery_wheel_item", "pottery_kiln_item",
    ],
    "Dogs": [
        "dog_collar", "dog_treat", "dog_whistle", "kennel_item", "dog_bowl_item",
    ],
    "Blacksmithing": [
        "forge_item", "weapon_rack_item", "weapon_assembler",
    ],
}

RECIPE_GROUPS_ORDER = [
    "Tools", "Farming", "Building", "Automation", "Rock & Gems", "Smelting",
    "Cooking Stations", "Coffee", "Wine", "Spirits", "Brewery", "Tea",
    "Herbalism", "Textiles", "Glassblowing", "Cheese", "Fishing", "Wildlife", "Horses", "Dogs", "Hunting", "Jewelry",
    "Garden", "Sculpture", "Pottery", "Tapestry", "Blacksmithing",
]


# Maps output_id -> research node_id required before that recipe is available.
RESEARCH_LOCKED_RECIPES = {
    # hoe and watering_can are freely craftable from the start — players need them immediately
    "compost_bin_item":      "irrigation",
    "farm_bot_item":         "soil_prep",
    "iron_farm_bot_item":    "selective_breeding",
    "crystal_farm_bot_item": "agri_automation",
    "roaster_item":          "coffee_basics",
    "blend_station_item":    "blend_arts",
    "brew_station_item":     "brew_expertise",
    "anaerobic_tank_item":   "anaerobic_processing",
    "grape_press_item":      "wine_basics",
    "fermentation_item":     "wine_basics",
    "wine_cellar_item":      "wine_basics",
    "still_item":            "distillation_basics",
    "barrel_room_item":      "distillation_basics",
    "bottling_item":         "distillation_basics",
    "brew_kettle_item":      "brewing_basics",
    "ferm_vessel_item":      "brewing_basics",
    "taproom_item":          "brewing_basics",
    "bird_feeder":           "bird_watching",
    "bird_bath":             "bird_sanctuary",
    "binoculars":            "bird_watching",
    "bug_net":               "entomology_basics",
    "insect_display_case":   "entomology_basics",
    "light_trap":            "entomology_basics",
    "wildflower_display":    "garden_workshop",
    "saddle":                "saddle_craft",
    "stable_item":           "saddle_craft",
    "drying_rack_item":      "herbalism_basics",
    "withering_rack_item":   "tea_cultivation",
    "oxidation_station_item":"tea_processing_arts",
    "tea_cellar_item":       "tea_ceremony",
    "roasting_kiln_item":    "tea_blending",
    "strawberry_seed_premium": "selective_breeding",
    "tomato_seed_premium":     "selective_breeding",
    "watermelon_seed_premium": "selective_breeding",
    "corn_seed_premium":       "selective_breeding",
    "rice_seed_premium":       "selective_breeding",
    "spinning_wheel_item":     "fiber_arts",
    "dye_vat_item":            "natural_dyes",
    "loom_item":               "loom_mastery",
    "glass_kiln_item":         "glassblowing",
    "dairy_vat_item":          "dairy_basics",
    "cheese_press_item":       "aging_arts",
    "aging_cave_item":         "aging_arts",
    "fletching_table_item":    "basic_archery",
    "wood_bow":                "basic_archery",
    "wood_arrow":              "basic_archery",
    "bone_arrow":              "basic_archery",
    "flint_arrow":             "flint_arrows",
    "iron_arrow":              "iron_arrows",
    "recurve_bow":             "recurve_bow",
    "barbed_arrow":            "barbed_arrows",
    "composite_bow":           "composite_bow",
    "broadhead_arrow":         "broadhead_arrows",
    "longbow":                 "longbow",
    "poison_arrow":            "poison_arrows",
    "crossbow":                "crossbow",
    "gold_arrow":              "gold_arrows",
    "jewelry_workbench_item":  "goldsmithing",
    "garden_workshop_item":    "garden_workshop",
    "sculptors_bench_item":    "stone_carving",
    "pottery_wheel_item":      "clay_working",
    "pottery_kiln_item":       "kiln_mastery",
    "evap_pan_item":           "salt_basics",
    "salt_grinder_item":       "salt_basics",
    "dog_collar":              "dog_basics",
    "dog_treat":               "dog_basics",
    "dog_bowl_item":           "dog_basics",
    "dog_whistle":             "scent_tracking",
    "kennel_item":             "kennel_mastery",
    "forge_item":              "basic_smithing",
    "weapon_rack_item":        "basic_smithing",
    "steel_ingot":             "steel_forging",
}


def match_recipe(grid):
    """Return (output_id, output_count) if grid matches a shaped recipe, else (None, 0)."""
    for recipe in RECIPES:
        pat = recipe["pattern"]
        if all(grid[r][c] == pat[r][c] for r in range(3) for c in range(3)):
            return recipe["output_id"], recipe["output_count"]
    return None, 0


def craft_costs(grid):
    """Return {item_id: count} for all non-None cells in the grid."""
    costs = {}
    for row in grid:
        for cell in row:
            if cell:
                costs[cell] = costs.get(cell, 0) + 1
    return costs


def can_craft(grid, inventory):
    """Return True if grid matches a recipe and inventory has the required items."""
    out_id, _ = match_recipe(grid)
    if not out_id:
        return False
    return all(inventory.get(iid, 0) >= needed
               for iid, needed in craft_costs(grid).items())


def is_research_locked(out_id, research):
    """Return True if out_id requires research that hasn't been unlocked."""
    if research is None or out_id not in RESEARCH_LOCKED_RECIPES:
        return False
    node = research.nodes.get(RESEARCH_LOCKED_RECIPES[out_id])
    return node is None or not node.unlocked


def can_craft_with_research(grid, inventory, research=None):
    """Like can_craft but also checks research locks."""
    out_id, _ = match_recipe(grid)
    if not out_id:
        return False
    if is_research_locked(out_id, research):
        return False
    return all(inventory.get(iid, 0) >= needed
               for iid, needed in craft_costs(grid).items())
