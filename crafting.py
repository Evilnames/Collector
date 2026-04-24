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
]

# ---------------------------------------------------------------------------
# Desert Forge recipes (ingredient dict → output, same pattern as cooking stations)
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
    {"name": "Aztec Sunstone",       "ingredients": {"stone_chip": 2, "obsidian_slab": 1},                "output_id": "aztec_sunstone",          "output_count": 2},
    {"name": "Azulejo Tile",         "ingredients": {"clay": 1, "crystal_shard": 1},                      "output_id": "azulejo_tile",            "output_count": 2},
    {"name": "Bamboo Panel",         "ingredients": {"lumber": 1, "sand_grain": 1},                       "output_id": "bamboo_panel",            "output_count": 2},
    {"name": "Bamboo Screen",        "ingredients": {"lumber": 2, "sand_grain": 1},                       "output_id": "bamboo_screen",           "output_count": 2},
    {"name": "Baroque Ornament",     "ingredients": {"limestone_block": 1, "gold_nugget": 2},             "output_id": "baroque_ornament",        "output_count": 2},
    {"name": "Baroque Trim",         "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "baroque_trim",            "output_count": 2},
    {"name": "Barrel Vault",         "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "barrel_vault",            "output_count": 2},
    {"name": "Basalt Column",        "ingredients": {"stone_chip": 2, "coal": 2},                         "output_id": "basalt_column",           "output_count": 2},
    {"name": "Benin Relief",         "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "benin_relief",            "output_count": 2},
    {"name": "Blue & White Tile",    "ingredients": {"clay": 1, "crystal_shard": 1, "sand_grain": 1},     "output_id": "blue_white_tile",         "output_count": 2},
    {"name": "Brick Nogging",        "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "brick_nogging",           "output_count": 2},
    {"name": "Brutalist Panel",      "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "brutalist_panel",         "output_count": 2},
    {"name": "Byzantine Mosaic",     "ingredients": {"sand_grain": 1, "gold_nugget": 2},                  "output_id": "byzantine_mosaic",        "output_count": 2},
    {"name": "Carved Plaster",       "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "carved_plaster",          "output_count": 2},
    {"name": "Cedar Panel",          "ingredients": {"lumber": 2, "iron_chunk": 1},                       "output_id": "cedar_panel",             "output_count": 2},
    {"name": "Celtic Knotwork",      "ingredients": {"stone_chip": 2, "obsidian_slab": 1},                "output_id": "celtic_knotwork",         "output_count": 2},
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
    {"name": "Cornice",              "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "cornice_block",           "output_count": 2},
    {"name": "Craftsman Panel",      "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "craftsman_panel",         "output_count": 2},
    {"name": "Cream Brick",          "ingredients": {"sand_grain": 3},                                    "output_id": "cream_brick",             "output_count": 2},
    {"name": "Crenellation",         "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "crenellation",            "output_count": 2},
    {"name": "Crimson Brick",        "ingredients": {"dirt_clump": 2, "ruby": 1},                         "output_id": "crimson_brick",           "output_count": 2},
    {"name": "Crimson Cedar Door",   "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "crimson_cedar_door",      "output_count": 1},
    {"name": "Dancheong",            "ingredients": {"lumber": 1, "ruby": 1, "crystal_shard": 1},         "output_id": "dancheong",               "output_count": 2},
    {"name": "Dark Slate Roof",      "ingredients": {"stone_chip": 2, "coal": 1},                         "output_id": "dark_slate_roof",         "output_count": 2},
    {"name": "Dentil Trim",          "ingredients": {"limestone_block": 2},                               "output_id": "dentil_trim",             "output_count": 2},
    {"name": "Diagonal Tile",        "ingredients": {"clay": 1, "sand_grain": 2},                         "output_id": "diagonal_tile",           "output_count": 2},
    {"name": "Dougong",              "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "dougong",                 "output_count": 2},
    {"name": "Dragon Tile",          "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "dragon_tile",             "output_count": 2},
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
    {"name": "Garden Rock",          "ingredients": {"stone_chip": 2, "obsidian_slab": 1},                "output_id": "garden_rock_block",       "output_count": 2},
    {"name": "Gargoyle Block",       "ingredients": {"stone_chip": 2, "obsidian_slab": 1},                "output_id": "gargoyle_block",          "output_count": 2},
    {"name": "Georgian Fanlight",    "ingredients": {"sand_grain": 2, "iron_chunk": 1},                   "output_id": "georgian_fanlight",       "output_count": 2},
    {"name": "Gilded Brick",         "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "gilded_brick",            "output_count": 2},
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
    {"name": "Inca Ashlar",          "ingredients": {"stone_chip": 3},                                    "output_id": "inca_ashlar",             "output_count": 2},
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
    {"name": "Limestone",            "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "limestone_block",         "output_count": 2},
    {"name": "Linen Fold",           "ingredients": {"lumber": 2, "gold_nugget": 1},                      "output_id": "linen_fold",              "output_count": 2},
    {"name": "Lotus Capital",        "ingredients": {"limestone_block": 1, "stone_chip": 2},              "output_id": "lotus_capital",           "output_count": 2},
    {"name": "Mahogany Plank",       "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "mahogany_plank",          "output_count": 2},
    {"name": "Mansard Slate",        "ingredients": {"stone_chip": 2, "coal": 2},                         "output_id": "mansard_slate",           "output_count": 2},
    {"name": "Manueline Panel",      "ingredients": {"limestone_block": 2, "iron_chunk": 1},              "output_id": "manueline_panel",         "output_count": 2},
    {"name": "Marble Inlay",         "ingredients": {"sand_grain": 1, "gold_nugget": 1, "crystal_shard": 1}, "output_id": "marble_inlay",         "output_count": 2},
    {"name": "Mashrabiya",           "ingredients": {"lumber": 2, "iron_chunk": 1},                       "output_id": "mashrabiya",              "output_count": 2},
    {"name": "Maya Relief",          "ingredients": {"stone_chip": 3},                                    "output_id": "maya_relief",             "output_count": 2},
    {"name": "Māori Carving",        "ingredients": {"lumber": 2, "obsidian_slab": 1},                    "output_id": "maori_carving",           "output_count": 2},
    {"name": "Metope",               "ingredients": {"limestone_block": 1, "stone_chip": 1},              "output_id": "metope",                  "output_count": 2},
    {"name": "Moon Gate",            "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "moon_gate",               "output_count": 2},
    {"name": "Moorish Column",       "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "moorish_column",          "output_count": 2},
    {"name": "Moorish Star Tile",    "ingredients": {"stone_chip": 1, "crystal_shard": 1},                "output_id": "moorish_star_tile",       "output_count": 2},
    {"name": "Mossy Brick",          "ingredients": {"stone_chip": 2, "dirt_clump": 1},                   "output_id": "mossy_brick",             "output_count": 2},
    {"name": "Mughal Arch",          "ingredients": {"limestone_block": 2, "crystal_shard": 1},           "output_id": "mughal_arch",             "output_count": 2},
    {"name": "Mughal Jali",          "ingredients": {"limestone_block": 2, "sand_grain": 1},              "output_id": "mughal_jali",             "output_count": 2},
    {"name": "Muqarnas",             "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "muqarnas_block",          "output_count": 2},
    {"name": "Nordic Plank",         "ingredients": {"lumber": 2, "coal": 2},                             "output_id": "nordic_plank",            "output_count": 2},
    {"name": "Oak Panel",            "ingredients": {"lumber": 2, "stone_chip": 1},                       "output_id": "oak_panel",               "output_count": 2},
    {"name": "Obsidian Cut",         "ingredients": {"obsidian_slab": 2, "stone_chip": 1},                "output_id": "obsidian_cut",            "output_count": 2},
    {"name": "Obsidian Tile",        "ingredients": {"obsidian_slab": 1, "stone_chip": 2},                "output_id": "obsidian_tile",           "output_count": 2},
    {"name": "Ogee Arch",            "ingredients": {"stone_chip": 2, "crystal_shard": 1},                "output_id": "ogee_arch",               "output_count": 2},
    {"name": "Onion Dome Tile",      "ingredients": {"clay": 1, "crystal_shard": 1, "gold_nugget": 1},    "output_id": "onion_dome_tile",         "output_count": 2},
    {"name": "Onyx Inlay",           "ingredients": {"obsidian_slab": 1, "coal": 1},                      "output_id": "onyx_inlay",              "output_count": 2},
    {"name": "Opus Incertum",        "ingredients": {"stone_chip": 2, "dirt_clump": 1},                   "output_id": "opus_incertum",           "output_count": 2},
    {"name": "Opus Signinum",        "ingredients": {"stone_chip": 1, "sand_grain": 1, "ruby": 1},        "output_id": "opus_signinum",           "output_count": 2},
    {"name": "Ottoman Arch",         "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "ottoman_arch",            "output_count": 2},
    {"name": "Ottoman Tile",         "ingredients": {"sand_grain": 2, "crystal_shard": 1},                "output_id": "ottoman_tile",            "output_count": 2},
    {"name": "Pagoda Eave",          "ingredients": {"lumber": 1, "ruby": 1, "crystal_shard": 1},         "output_id": "pagoda_eave",             "output_count": 2},
    {"name": "Painted Beam",         "ingredients": {"lumber": 2, "ruby": 1},                             "output_id": "painted_beam",            "output_count": 2},
    {"name": "Palladian Window",     "ingredients": {"limestone_block": 2, "crystal_shard": 1},           "output_id": "palladian_window",        "output_count": 2},
    {"name": "Paper Lantern",        "ingredients": {"lumber": 1, "crystal_shard": 1},                    "output_id": "paper_lantern",           "output_count": 2},
    {"name": "Parquet Floor",        "ingredients": {"lumber": 2, "sand_grain": 1},                       "output_id": "parquet_floor",           "output_count": 2},
    {"name": "Pavilion Floor",       "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "pavilion_floor",          "output_count": 2},
    {"name": "Pebble Dash",          "ingredients": {"stone_chip": 1, "sand_grain": 2},                   "output_id": "pebble_dash",             "output_count": 2},
    {"name": "Persian Iwan",         "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "persian_iwan",            "output_count": 2},
    {"name": "Persian Tile",         "ingredients": {"clay": 1, "crystal_shard": 2},                      "output_id": "persian_tile",            "output_count": 2},
    {"name": "Pietra Dura",          "ingredients": {"sand_grain": 1, "gold_nugget": 1, "ruby": 1},       "output_id": "pietra_dura",             "output_count": 2},
    {"name": "Pilaster",             "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "pilaster",                "output_count": 2},
    {"name": "Plinth Block",         "ingredients": {"stone_chip": 2, "sand_grain": 1},                   "output_id": "plinth_block",            "output_count": 2},
    {"name": "Pointed Arch",         "ingredients": {"stone_chip": 2, "limestone_block": 1},              "output_id": "pointed_arch",            "output_count": 2},
    {"name": "Polished Granite",     "ingredients": {"stone_chip": 2},                                    "output_id": "polished_granite",        "output_count": 2},
    {"name": "Polished Marble",      "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "polished_marble",         "output_count": 2},
    {"name": "Polynesian Carved",    "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "polynesian_carved",       "output_count": 2},
    {"name": "Portuguese Cork",      "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "portuguese_cork",         "output_count": 2},
    {"name": "Quartz Pillar",        "ingredients": {"stone_chip": 3, "crystal_shard": 1},                "output_id": "quartz_pillar",           "output_count": 2},
    {"name": "Relief Panel",         "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "relief_panel",            "output_count": 2},
    {"name": "Roman Mosaic",         "ingredients": {"sand_grain": 1, "stone_chip": 1},                   "output_id": "roman_mosaic",            "output_count": 2},
    {"name": "Romanesque Arch",      "ingredients": {"stone_chip": 1, "sand_grain": 2},                   "output_id": "romanesque_arch",         "output_count": 2},
    {"name": "Rose Quartz",          "ingredients": {"stone_chip": 2, "ruby": 1},                         "output_id": "rose_quartz_block",       "output_count": 2},
    {"name": "Rose Window",          "ingredients": {"stone_chip": 1, "crystal_shard": 2},                "output_id": "rose_window",             "output_count": 2},
    {"name": "Rune Stone",           "ingredients": {"stone_chip": 2, "coal": 1},                         "output_id": "rune_stone",              "output_count": 2},
    {"name": "Rusticated Stone",     "ingredients": {"stone_chip": 3},                                    "output_id": "rusticated_stone",        "output_count": 2},
    {"name": "Russian Kokoshnik",    "ingredients": {"limestone_block": 1, "gold_nugget": 1},             "output_id": "russian_kokoshnik",       "output_count": 2},
    {"name": "Saffron Door",         "ingredients": {"lumber": 2, "gold_nugget": 2},                      "output_id": "saffron_door",            "output_count": 1},
    {"name": "Saltillo Tile",        "ingredients": {"clay": 1, "sand_grain": 1},                         "output_id": "saltillo_tile",           "output_count": 2},
    {"name": "Sandstone Ashlar",     "ingredients": {"sand_grain": 2, "stone_chip": 1},                   "output_id": "sandstone_ashlar",        "output_count": 2},
    {"name": "Sandstone Column",     "ingredients": {"sand_grain": 2, "limestone_block": 1},              "output_id": "sandstone_column",        "output_count": 2},
    {"name": "Scottish Rubble",      "ingredients": {"stone_chip": 3},                                    "output_id": "scottish_rubble",         "output_count": 2},
    {"name": "Sett Stone",           "ingredients": {"stone_chip": 3},                                    "output_id": "sett_stone",              "output_count": 3},
    {"name": "Silver Panel",         "ingredients": {"iron_chunk": 2, "crystal_shard": 1},                "output_id": "silver_panel",            "output_count": 2},
    {"name": "Slate Tile",           "ingredients": {"stone_chip": 2, "coal": 1},                         "output_id": "slate_tile",              "output_count": 2},
    {"name": "Spanish Roof Tile",    "ingredients": {"clay": 1, "dirt_clump": 1},                         "output_id": "spanish_roof_tile",       "output_count": 2},
    {"name": "Stained Glass (Blue)", "ingredients": {"sand_grain": 1, "crystal_shard": 2},                "output_id": "stained_glass_blue",      "output_count": 2},
    {"name": "Stained Glass (Green)","ingredients": {"sand_grain": 2, "crystal_shard": 1, "dirt_clump": 1}, "output_id": "stained_glass_green",  "output_count": 2},
    {"name": "Stained Glass (Red)",  "ingredients": {"sand_grain": 2, "ruby": 1},                         "output_id": "stained_glass_red",       "output_count": 2},
    {"name": "Stave Plank",          "ingredients": {"lumber": 2, "coal": 1},                             "output_id": "stave_plank",             "output_count": 2},
    {"name": "Stepped Wall",         "ingredients": {"clay": 2, "stone_chip": 1},                         "output_id": "stepped_wall",            "output_count": 2},
    {"name": "Stone Lantern",        "ingredients": {"stone_chip": 2, "gold_nugget": 1},                  "output_id": "stone_lantern",           "output_count": 2},
    {"name": "Striped Arch",         "ingredients": {"limestone_block": 1, "stone_chip": 1, "coal": 1},   "output_id": "striped_arch",            "output_count": 2},
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
    {"name": "Triglyph Panel",       "ingredients": {"limestone_block": 2, "stone_chip": 1},              "output_id": "triglyph_panel",          "output_count": 2},
    {"name": "Tudor Beam",           "ingredients": {"lumber": 2, "dirt_clump": 1},                       "output_id": "tudor_beam",              "output_count": 2},
    {"name": "Tudor Rose",           "ingredients": {"limestone_block": 1, "ruby": 1},                    "output_id": "tudor_rose",              "output_count": 2},
    {"name": "Venetian Floor",       "ingredients": {"sand_grain": 1, "gold_nugget": 1},                  "output_id": "venetian_floor",          "output_count": 2},
    {"name": "Venetian Plaster",     "ingredients": {"limestone_block": 2, "gold_nugget": 1},             "output_id": "venetian_plaster",        "output_count": 2},
    {"name": "Verdigris Copper",     "ingredients": {"iron_chunk": 1, "crystal_shard": 1},                "output_id": "verdigris_copper",        "output_count": 2},
    {"name": "Viking Carving",       "ingredients": {"lumber": 2, "obsidian_slab": 1},                    "output_id": "viking_carving",          "output_count": 2},
    {"name": "Walnut Plank",         "ingredients": {"lumber": 2, "coal": 1},                             "output_id": "walnut_plank",            "output_count": 2},
    {"name": "Wat Finial",           "ingredients": {"stone_chip": 1, "gold_nugget": 2},                  "output_id": "wat_finial",              "output_count": 2},
    {"name": "Wattle & Daub",        "ingredients": {"lumber": 1, "dirt_clump": 2},                       "output_id": "wattle_daub",             "output_count": 2},
    {"name": "White Plaster Wall",   "ingredients": {"limestone_block": 2, "sand_grain": 1},              "output_id": "white_plaster_wall",      "output_count": 2},
    {"name": "Woven Rug",            "ingredients": {"lumber": 1, "dirt_clump": 1, "ruby": 1},            "output_id": "woven_rug",               "output_count": 1},
    {"name": "Wrought Iron Grille",  "ingredients": {"iron_chunk": 2, "coal": 1},                         "output_id": "wrought_iron_grille",     "output_count": 2},
    {"name": "Zellige Tile",         "ingredients": {"sand_grain": 2, "crystal_shard": 1},                "output_id": "zellige_tile",            "output_count": 2},
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
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
            [None,         None,         None],
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
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
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
            ["iron_chunk", "gold_nugget", "iron_chunk"],
            ["iron_chunk", "coal",        "iron_chunk"],
            ["iron_chunk", "gold_nugget", "iron_chunk"],
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
            ["iron_chunk", "gold_nugget", "iron_chunk"],
            ["gold_nugget", "iron_chunk", "gold_nugget"],
            ["iron_chunk", "gold_nugget", "iron_chunk"],
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
        "name": "Garden Block",
        "pattern": [
            [None,          None,          None        ],
            ["lumber",      "dirt_clump",  "lumber"    ],
            ["lumber",      "stone_chip",  "lumber"    ],
        ],
        "output_id":    "garden_block",
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
]

# ---------------------------------------------------------------------------
# Bait Station recipes
# ---------------------------------------------------------------------------

BAIT_STATION_RECIPES = [
    {"name": "Worm Bait",   "ingredients": {"wheat": 2},                          "output_id": "worm_bait",   "output_count": 4},
    {"name": "Insect Bait", "ingredients": {"mint": 1, "rosemary": 1},            "output_id": "insect_bait", "output_count": 4},
    {"name": "Grain Bait",  "ingredients": {"corn": 2, "wheat": 1},               "output_id": "grain_bait",  "output_count": 4},
    {"name": "Berry Bait",  "ingredients": {"strawberry": 3},                     "output_id": "berry_bait",  "output_count": 4},
    {"name": "Meat Bait",   "ingredients": {"fish": 2},                           "output_id": "meat_bait",   "output_count": 4},
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
    ],
    "Automation": [
        "coal_miner_item", "iron_miner_item", "crystal_miner_item",
    ],
    "Rock & Gems": [
        "diamond", "tumbler_item", "crusher_item", "gem_cutter_item",
        "kiln_item", "resonance_item",
    ],
    "Cooking Stations": [
        "bakery_item", "wok_item", "steamer_item", "noodle_pot_item",
        "bbq_grill_item", "clay_pot_item", "desert_forge_item",
        "artisan_bench_item", "fossil_table_item",
    ],
    "Coffee": [
        "roaster_item", "blend_station_item", "brew_station_item",
    ],
    "Wine": [
        "grape_press_item", "fermentation_item", "wine_cellar_item",
    ],
    "Spirits": [
        "still_item", "barrel_room_item", "bottling_item",
    ],
    "Tea": [
        "withering_rack_item", "oxidation_station_item", "tea_cellar_item",
    ],
    "Herbalism": [
        "drying_rack_item",
    ],
    "Textiles": [
        "spinning_wheel_item", "dye_vat_item", "loom_item",
    ],
    "Fishing": [
        "fishing_pole", "bait_station_item",
    ],
    "Wildlife": [
        "bird_feeder", "bird_bath", "bug_net", "insect_display_case",
    ],
    "Horses": [
        "saddle", "horse_brush", "horseshoe", "sugar_lump",
        "stable_item", "horse_trough_item",
    ],
}

RECIPE_GROUPS_ORDER = [
    "Tools", "Farming", "Building", "Automation", "Rock & Gems",
    "Cooking Stations", "Coffee", "Wine", "Spirits", "Tea",
    "Herbalism", "Textiles", "Fishing", "Wildlife", "Horses",
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
    "grape_press_item":      "wine_basics",
    "fermentation_item":     "wine_basics",
    "wine_cellar_item":      "wine_basics",
    "still_item":            "distillation_basics",
    "barrel_room_item":      "distillation_basics",
    "bottling_item":         "distillation_basics",
    "bird_feeder":           "bird_watching",
    "bird_bath":             "bird_sanctuary",
    "bug_net":               "entomology_basics",
    "insect_display_case":   "entomology_basics",
    "saddle":                "saddle_craft",
    "stable_item":           "saddle_craft",
    "drying_rack_item":      "herbalism_basics",
    "withering_rack_item":   "tea_cultivation",
    "oxidation_station_item":"tea_processing_arts",
    "tea_cellar_item":       "tea_ceremony",
    "strawberry_seed_premium": "selective_breeding",
    "tomato_seed_premium":     "selective_breeding",
    "watermelon_seed_premium": "selective_breeding",
    "corn_seed_premium":       "selective_breeding",
    "rice_seed_premium":       "selective_breeding",
    "spinning_wheel_item":     "fiber_arts",
    "dye_vat_item":            "natural_dyes",
    "loom_item":               "loom_mastery",
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
