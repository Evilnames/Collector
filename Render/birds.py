import math
import pygame

from constants import SCREEN_W, SCREEN_H


# ------------------------------------------------------------------

def draw_birds(screen, cam_x, cam_y, birds):
    for bird in birds:
        sx = int(bird.x - cam_x)
        sy = int(bird.y - cam_y)
        if sx < -40 or sx > SCREEN_W + 40 or sy < -40 or sy > SCREEN_H + 40:
            continue
        _draw_bird(screen, bird, sx, sy)

def draw_nests(screen, cam_x, cam_y, nests):
    from constants import BLOCK_SIZE
    NEST_COLOR = (110, 80, 45)
    EGG_COLOR  = (240, 235, 210)
    for nest in nests:
        nx = int(nest.bx * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_x)
        ny = int(nest.by * BLOCK_SIZE - 4 - cam_y)
        if nx < -20 or nx > SCREEN_W + 20 or ny < -20 or ny > SCREEN_H + 20:
            continue
        pygame.draw.ellipse(screen, NEST_COLOR, (nx - 4, ny, 8, 5))
        for i in range(min(nest.eggs, 3)):
            ex = nx - 2 + i * 2
            pygame.draw.circle(screen, EGG_COLOR, (ex, ny + 2), 1)

def _draw_bird(screen, bird, sx, sy):
    sp = bird.SPECIES
    is_ground = getattr(bird, 'IS_GROUND', False)
    perching = is_ground or (bird.state == "perching")
    wing_flap = abs(math.sin(bird._wing_phase)) * 5 if not perching else 0

    # Clickable perch indicator — subtle white outline
    if bird.state == "perching":
        pygame.draw.rect(screen, (255, 255, 255),
                         (sx - 1, sy - 1, bird.W + 2, bird.H + 2), 1)

    if sp == "robin":
        _draw_robin(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "blue_jay":
        _draw_bluejay(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "eagle":
        _draw_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pelican":
        _draw_pelican(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "parrot":
        _draw_parrot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "sparrow":
        _draw_sparrow(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "heron":
        _draw_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hummingbird":
        _draw_hummingbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "owl":
        _draw_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "crow":
        _draw_crow(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "flamingo":
        _draw_flamingo(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "toucan":
        _draw_toucan(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cardinal":
        _draw_cardinal(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "puffin":
        _draw_puffin(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "vulture":
        _draw_vulture(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "roadrunner":
        _draw_roadrunner(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "peacock":
        _draw_peacock(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "kookaburra":
        _draw_kookaburra(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "sandpiper":
        _draw_sandpiper(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "kingfisher":
        _draw_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "woodpecker":
        _draw_woodpecker(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "finch":
        _draw_finch(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "stork":
        _draw_stork(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "macaw":
        _draw_macaw(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pheasant":
        _draw_pheasant(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "condor":
        _draw_condor(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "snow_bunting":
        _draw_snow_bunting(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "prairie_falcon":
        _draw_prairie_falcon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "nightjar":
        _draw_nightjar(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "ibis":
        _draw_ibis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "albatross":
        _draw_albatross(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "raven":
        _draw_raven(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "swallow":
        _draw_swallow(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "crane":
        _draw_crane(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "spoonbill":
        _draw_spoonbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "peregrine_falcon":
        _draw_peregrine_falcon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "barn_owl":
        _draw_barn_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "magpie":
        _draw_magpie(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "golden_oriole":
        _draw_golden_oriole(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hoopoe":
        _draw_hoopoe(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "sunbird":
        _draw_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "ptarmigan":
        _draw_ptarmigan(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "bittern":
        _draw_bittern(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cedar_waxwing":
        _draw_cedar_waxwing(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "mockingbird":
        _draw_mockingbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "egret":
        _draw_egret(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "arctic_tern":
        _draw_arctic_tern(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cormorant":
        _draw_cormorant(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "curlew":
        _draw_curlew(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "avocet":
        _draw_avocet(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "jacana":
        _draw_jacana(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "lyrebird":
        _draw_lyrebird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "bee_eater":
        _draw_bee_eater(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "roller":
        _draw_roller(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hornbill":
        _draw_hornbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "quetzal":
        _draw_quetzal(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "snowy_owl":
        _draw_snowy_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "osprey":
        _draw_osprey(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "golden_pheasant":
        _draw_golden_pheasant(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "treecreeper":
        _draw_treecreeper(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "wren":
        _draw_wren(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "nuthatch":
        _draw_nuthatch(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "gannet":
        _draw_gannet(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "frigatebird":
        _draw_frigatebird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "night_heron":
        _draw_night_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "lapwing":
        _draw_lapwing(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "wheatear":
        _draw_wheatear(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "redstart":
        _draw_redstart(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "warbler":
        _draw_warbler(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "long_tailed_tit":
        _draw_long_tailed_tit(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "oystercatcher":
        _draw_oystercatcher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "kite":
        _draw_kite(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "harrier":
        _draw_harrier(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "snipe":
        _draw_snipe(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "merlin":
        _draw_merlin(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "goshawk":
        _draw_goshawk(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "shoebill":
        _draw_shoebill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "booby":
        _draw_booby(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "tropicbird":
        _draw_tropicbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "dunlin":
        _draw_dunlin(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "godwit":
        _draw_godwit(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "oxpecker":
        _draw_oxpecker(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "dipper":
        _draw_dipper(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "skua":
        _draw_skua(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "firecrest":
        _draw_firecrest(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_crowned_crane":
        _draw_red_crowned_crane(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "mandarin_duck":
        _draw_mandarin_duck(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "chinese_monal":
        _draw_chinese_monal(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "silver_pheasant":
        _draw_silver_pheasant(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "crested_ibis":
        _draw_crested_ibis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "chinese_pond_heron":
        _draw_chinese_pond_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "fairy_pitta":
        _draw_fairy_pitta(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hwamei":
        _draw_hwamei(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "black_drongo":
        _draw_black_drongo(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_billed_blue_magpie":
        _draw_red_billed_blue_magpie(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_fish_eagle":
        _draw_african_fish_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "secretary_bird":
        _draw_secretary_bird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "martial_eagle":
        _draw_martial_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "marabou_stork":
        _draw_marabou_stork(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "superb_starling":
        _draw_superb_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cape_weaver":
        _draw_cape_weaver(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hamerkop":
        _draw_hamerkop(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_grey_parrot":
        _draw_african_grey_parrot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "ground_hornbill":
        _draw_ground_hornbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_penguin":
        _draw_african_penguin(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "lilac_breasted_roller":
        _draw_lilac_breasted_roller(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "carmine_bee_eater":
        _draw_carmine_bee_eater(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "white_fronted_bee_eater":
        _draw_white_fronted_bee_eater(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "little_bee_eater":
        _draw_little_bee_eater(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "abyssinian_roller":
        _draw_abyssinian_roller(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "malachite_kingfisher":
        _draw_malachite_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "giant_kingfisher":
        _draw_giant_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pygmy_kingfisher":
        _draw_pygmy_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pied_kingfisher":
        _draw_pied_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "grey_headed_kingfisher":
        _draw_grey_headed_kingfisher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "bateleur_eagle":
        _draw_bateleur_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "tawny_eagle":
        _draw_tawny_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "verreauxs_eagle":
        _draw_verreauxs_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "brown_snake_eagle":
        _draw_brown_snake_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "long_crested_eagle":
        _draw_long_crested_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_crowned_eagle":
        _draw_african_crowned_eagle(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "lanner_falcon":
        _draw_lanner_falcon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pygmy_falcon":
        _draw_pygmy_falcon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_kestrel":
        _draw_african_kestrel(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_necked_falcon":
        _draw_red_necked_falcon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "lappet_faced_vulture":
        _draw_lappet_faced_vulture(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "white_backed_vulture":
        _draw_white_backed_vulture(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "egyptian_vulture":
        _draw_egyptian_vulture(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "palm_nut_vulture":
        _draw_palm_nut_vulture(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "saddlebilled_stork":
        _draw_saddlebilled_stork(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "yellow_billed_stork":
        _draw_yellow_billed_stork(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "goliath_heron":
        _draw_goliath_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "purple_heron":
        _draw_purple_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "black_headed_heron":
        _draw_black_headed_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "great_egret":
        _draw_great_egret(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cattle_egret":
        _draw_cattle_egret(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "squacco_heron":
        _draw_squacco_heron(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "grey_crowned_crane":
        _draw_grey_crowned_crane(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hadeda_ibis":
        _draw_hadeda_ibis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "sacred_ibis":
        _draw_sacred_ibis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "glossy_ibis":
        _draw_glossy_ibis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_spoonbill":
        _draw_african_spoonbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "great_white_pelican":
        _draw_great_white_pelican(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_darter":
        _draw_african_darter(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "crowned_lapwing":
        _draw_crowned_lapwing(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "blackwinged_stilt":
        _draw_blackwinged_stilt(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "purple_swamphen":
        _draw_purple_swamphen(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_rail":
        _draw_african_rail(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_jacana":
        _draw_african_jacana(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_billed_quelea":
        _draw_red_billed_quelea(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "village_weaver":
        _draw_village_weaver(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "golden_bishop":
        _draw_golden_bishop(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "southern_red_bishop":
        _draw_southern_red_bishop(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "wattled_starling":
        _draw_wattled_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "malachite_sunbird":
        _draw_malachite_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "orange_breasted_sunbird":
        _draw_orange_breasted_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "scarlet_chested_sunbird":
        _draw_scarlet_chested_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "amethyst_sunbird":
        _draw_amethyst_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "collared_sunbird":
        _draw_collared_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "variable_sunbird":
        _draw_variable_sunbird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "violet_backed_starling":
        _draw_violet_backed_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "greater_blue_eared_starling":
        _draw_greater_blue_eared_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "plum_colored_starling":
        _draw_plum_colored_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pied_starling":
        _draw_pied_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "burchells_starling":
        _draw_burchells_starling(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_firefinch":
        _draw_african_firefinch(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "blue_waxbill":
        _draw_blue_waxbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "violet_eared_waxbill":
        _draw_violet_eared_waxbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "yellow_fronted_canary":
        _draw_yellow_fronted_canary(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "melba_finch":
        _draw_melba_finch(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_silverbill":
        _draw_african_silverbill(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "locust_finch":
        _draw_locust_finch(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "double_tooth_barbet":
        _draw_double_tooth_barbet(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "black_collared_barbet":
        _draw_black_collared_barbet(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_yellow_barbet":
        _draw_red_yellow_barbet(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_green_pigeon":
        _draw_african_green_pigeon(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "namaqua_dove":
        _draw_namaqua_dove(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "laughing_dove":
        _draw_laughing_dove(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "meyer_parrot":
        _draw_meyer_parrot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cape_parrot":
        _draw_cape_parrot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "rosy_faced_lovebird":
        _draw_rosy_faced_lovebird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "ostrich":
        _draw_ostrich(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "kori_bustard":
        _draw_kori_bustard(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "helmeted_guineafowl":
        _draw_helmeted_guineafowl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "namaqua_sandgrouse":
        _draw_namaqua_sandgrouse(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "fiscal_shrike":
        _draw_fiscal_shrike(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_backed_shrike":
        _draw_red_backed_shrike(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pied_crow":
        _draw_pied_crow(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "fan_tailed_raven":
        _draw_fan_tailed_raven(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "paradise_flycatcher":
        _draw_paradise_flycatcher(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "batis":
        _draw_batis(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "cape_robin_chat":
        _draw_cape_robin_chat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_stonechat":
        _draw_african_stonechat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pennant_winged_nightjar":
        _draw_pennant_winged_nightjar(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "alpine_swift":
        _draw_alpine_swift(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_palm_swift":
        _draw_african_palm_swift(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "red_knobbed_coot":
        _draw_red_knobbed_coot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_snipe":
        _draw_african_snipe(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "spotted_thick_knee":
        _draw_spotted_thick_knee(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "wattled_plover":
        _draw_wattled_plover(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "blacksmith_lapwing":
        _draw_blacksmith_lapwing(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "three_banded_plover":
        _draw_three_banded_plover(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "african_fish_owl":
        _draw_african_fish_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "verreauxs_eagle_owl":
        _draw_verreauxs_eagle_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "speckled_mousebird":
        _draw_speckled_mousebird(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "gambels_quail":
        _draw_gambels_quail(screen, bird, sx, sy, wing_flap, perching)
    # Bats
    elif sp in ("little_brown_bat", "big_brown_bat", "horseshoe_bat",
                "pipistrel_bat", "noctule_bat", "ghost_bat"):
        _draw_bat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "fruit_bat":
        _draw_fruit_bat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "vampire_bat":
        _draw_vampire_bat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "leaf_nosed_bat":
        _draw_leaf_nosed_bat(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "hammer_headed_bat":
        _draw_hammer_headed_bat(screen, bird, sx, sy, wing_flap, perching)
    # Penguins
    elif sp in ("gentoo_penguin", "chin_strap_penguin", "adelie_penguin",
                "snares_penguin", "fjordland_penguin", "little_blue_penguin"):
        _draw_penguin(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("emperor_penguin", "king_penguin"):
        _draw_penguin_cheek(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("macaroni_penguin", "rock_hopper_penguin"):
        _draw_crested_penguin(screen, bird, sx, sy, wing_flap, perching)
    # Nocturnal birds
    elif sp == "tawny_frogmouth":
        _draw_frogmouth(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "common_potoo":
        _draw_potoo(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("whip_poor_will", "common_poorwill"):
        _draw_nighthawk(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("elf_owl", "ferruginous_pygmy_owl", "common_scops_owl", "eastern_screech_owl"):
        _draw_small_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("barred_owl", "spectacled_owl"):
        _draw_large_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp in ("long_eared_owl", "short_eared_owl"):
        _draw_eared_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "burrowing_owl":
        _draw_burrowing_owl(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "kiwi":
        _draw_kiwi(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "night_parrot":
        _draw_night_parrot(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "brown_noddy":
        _draw_brown_noddy(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "white_tern":
        _draw_white_tern(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "pacific_golden_plover":
        _draw_pacific_golden_plover(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "common_myna":
        _draw_common_myna(screen, bird, sx, sy, wing_flap, perching)
    elif sp == "reef_heron":
        _draw_reef_heron(screen, bird, sx, sy, wing_flap, perching)

def _draw_robin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
    # Breast (orange-red)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 5))
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 1 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    # Head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Eye
    ex = hx + 3 if f == 1 else hx + 1
    pygame.draw.rect(screen, (20, 20, 20), (ex, sy + 1, 2, 2))
    # Beak
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

def _draw_bluejay(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # White underside
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 5, W - 6, H - 7))
    # Black necklace
    pygame.draw.rect(screen, (30, 30, 40), (sx + 3, sy + 4, W - 6, 2))
    # Head + crest
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Crest
    cx = hx + 2
    pygame.draw.line(screen, bird.BODY_COLOR, (cx, sy + 2), (cx - f, sy - 3), 2)
    # Eye
    ex = hx + 3 if f == 1 else hx + 1
    pygame.draw.rect(screen, (15, 15, 20), (ex, sy + 1, 2, 2))
    # Beak
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

def _draw_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wide wings when flying
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    # White head
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
    # Eye
    ex = hx + 4 if f == 1 else hx + 2
    pygame.draw.rect(screen, (30, 25, 10), (ex, sy + 2, 2, 2))
    # Hooked beak
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 5, 2, 2))
    # Tail fan
    tx = sx + 2 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 4, 4, 4))

def _draw_pelican(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 2))
    # Head
    hx = sx + W - 7 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
    # Long beak
    bx = hx + 6 if f == 1 else hx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 7, 2))
    # Pouch
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (bx + (0 if f == 1 else 2), sy + 5, 5, 3))
    # Eye
    ex = hx + 4 if f == 1 else hx + 1
    pygame.draw.rect(screen, (20, 20, 20), (ex, sy + 2, 2, 2))

def _draw_parrot(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (bright green)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
        # Yellow wing-bar
        pygame.draw.ellipse(screen, bird.ACCENT_COLOR,
                            (sx + 2, sy + 2 + int(wf), W - 4, 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Long tail
    tx = sx + 2 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, (30, 140, 45), (tx, sy + H - 2, 3, 5))
    # Red head
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Eye
    ex = hx + 3 if f == 1 else hx + 1
    pygame.draw.rect(screen, (240, 230, 50), (ex, sy + 1, 2, 2))
    # Curved beak
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, (200, 70, 30), (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (180, 60, 25), (bx + (0 if f == 1 else 1), sy + 4, 2, 2))

def _draw_sparrow(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Dark crown stripe
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy, 3, 2))
    # Beak
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))
def _draw_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing  # 1 for Right, -1 for Left
    
    # Colors
    LEG_COL = (180, 170, 130)
    EYE_COL = (20, 20, 20)
    
    # 1. LEGS (Draw first so they are behind the body)
    leg_y = sy + H - 8
    for lx_off in [3, W - 5]:
        pygame.draw.line(screen, LEG_COL, (sx + lx_off, leg_y), (sx + lx_off, sy + H), 2)

    # 2. BODY
    body_rect = (sx + 2, sy + 4, W - 4, H - 8)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, body_rect)

    # 3. WINGS (Dynamic flapping)
    if not perching:
        # Flap height determined by wf; shifts slightly up/down
        wing_y = sy + 3 + int(wf * 2) 
        wing_h = max(2, H - 6 - int(abs(wf)))
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, wing_y, W, wing_h))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))

    # 4. NECK & HEAD LOGIC
    # Calculate neck base based on direction
    neck_base_x = sx + W - 4 if f == 1 else sx + 4
    head_x = neck_base_x + (4 * f)
    head_y = sy - 2
    
    # Draw an "S" style neck using a thick line or narrow rect
    pygame.draw.line(screen, bird.HEAD_COLOR, (neck_base_x, sy + 6), (head_x, head_y), 3)

    # 5. HEAD & FEATURES
    # Head circle
    pygame.draw.circle(screen, bird.HEAD_COLOR, (head_x, head_y), 4)
    
    # Dagger Beak (Triangle looks sharper than a rect)
    beak_tip = head_x + (10 * f)
    pygame.draw.polygon(screen, bird.BEAK_COLOR, [
        (head_x, head_y - 1), 
        (head_x, head_y + 1), 
        (beak_tip, head_y)
    ])
    
    # Dark Crown (Sweeping back)
    crown_x = head_x - (3 * f)
    pygame.draw.line(screen, bird.ACCENT_COLOR, (head_x, head_y - 3), (crown_x, head_y - 1), 2)

    # Eye
    eye_x = head_x + (1 * f)
    pygame.draw.rect(screen, EYE_COL, (eye_x, head_y - 2, 2, 2))

def _draw_hummingbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Blur-wings (fast wingbeat) — wide translucent blur when flying
    if not perching:
        pygame.draw.ellipse(screen, (100, 200, 160),
                            (sx - 2, sy + 1, W + 4, 4))
    # Body (iridescent green)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Red throat
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, 3))
    # Head
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 2), 3)
    # Long thin beak
    bx = hx + 3 if f == 1 else hx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 6, 1))
    # Eye
    pygame.draw.rect(screen, (200, 200, 255), (hx + (1 if f == 1 else 0), sy + 1, 2, 2))

def _draw_owl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 2 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    # Body (rounded)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
    # Facial disc
    pygame.draw.circle(screen, bird.ACCENT_COLOR, (sx + W // 2, sy + 4), 5)
    # Big eyes
    el = sx + W // 2 - 3
    er = sx + W // 2 + 1
    pygame.draw.circle(screen, (255, 190, 40), (el, sy + 4), 2)
    pygame.draw.circle(screen, (255, 190, 40), (er, sy + 4), 2)
    pygame.draw.circle(screen, (20, 20, 20), (el, sy + 4), 1)
    pygame.draw.circle(screen, (20, 20, 20), (er, sy + 4), 1)
    # Small beak
    pygame.draw.rect(screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 6, 2, 2))
    # Ear tufts
    pygame.draw.rect(screen, bird.BODY_COLOR, (sx + W // 2 - 4, sy, 2, 3))
    pygame.draw.rect(screen, bird.BODY_COLOR, (sx + W // 2 + 2, sy, 2, 3))

def _draw_crow(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (all black)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 1, sy + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Fan tail
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 4, 5, 5))
    # Head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Sheen highlight
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + 1, sy, 2, 2))
    # Eye (white dot)
    ex = hx + 3 if f == 1 else hx + 1
    pygame.draw.rect(screen, (200, 210, 220), (ex, sy + 1, 2, 2))
    pygame.draw.rect(screen, (10, 10, 12), (ex, sy + 1, 1, 1))
    # Beak
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

# ------------------------------------------------------------------
# New species (11–35)
# ------------------------------------------------------------------

def _draw_flamingo(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long legs
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (200, 90, 105), (lx, sy + H - 6, 2, 6))
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 4 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 10))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 9))
    # Long S-curve neck
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
    # Head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    # Bent beak (knee-shaped)
    bx = nx + 3 if f == 1 else nx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (215, 180, 60), (bx, sy + 1, 2, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

def _draw_toucan(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    # Yellow chest
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 8))
    # Head
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Giant beak
    bx = hx + 5 if f == 1 else hx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 8, 3))
    pygame.draw.rect(screen, (60, 175, 60), (bx, sy + 2, 8, 1))
    pygame.draw.rect(screen, (210, 50, 30), (bx + (3 if f == 1 else 0), sy + 3, 5, 2))
    # Eye (yellow)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_cardinal(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Head + crest
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.line(screen, bird.BODY_COLOR, (hx + 2, sy + 2), (hx + 2 - f, sy - 3), 2)
    # Black mask
    pygame.draw.rect(screen, bird.ACCENT_COLOR,
                     (hx + (2 if f == 1 else 0), sy + 2, 3, 2))
    # Beak
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_puffin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (black)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    # Body (black)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # White belly
    pygame.draw.ellipse(screen, (245, 243, 240), (sx + 2, sy + 4, W - 7, H - 6))
    # White face
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    # Bright orange beak
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 3))
    pygame.draw.rect(screen, (245, 200, 50), (bx, sy + 2, 4, 1))

def _draw_vulture(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Very wide wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    # Body (hunched)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
    # Small bare head (skin-colored)
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Hooked beak
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 2, 2))
    # Eye
    pygame.draw.rect(screen, (15, 15, 15), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_roadrunner(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long tail extending behind body
    tx = sx if f == 1 else sx + W - 6
    pygame.draw.rect(screen, bird.WING_COLOR, (tx, sy + 3, 6, 3))
    # Wings (always folded — ground bird)
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    # Streaked pattern
    for i in range(3):
        pygame.draw.rect(screen, (130, 120, 90),
                         (sx + 5 + i * 3, sy + 3, 1, H - 5))
    # Head + crest
    hx = sx + W - 6 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.line(screen, (120, 100, 65), (hx + 2, sy + 1), (hx + 2 - f, sy - 2), 2)
    # Orange-red eye patch
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 0), sy + 1, 3, 2))
    # Eye
    pygame.draw.rect(screen, (15, 15, 15), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))
    # Long beak
    bx = hx + 5 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    # Legs
    lx1 = sx + W // 2 - 2
    lx2 = sx + W // 2 + 2
    pygame.draw.line(screen, (80, 65, 40), (lx1, sy + H - 2), (lx1, sy + H + 3), 1)
    pygame.draw.line(screen, (80, 65, 40), (lx2, sy + H - 2), (lx2, sy + H + 3), 1)

def _draw_peacock(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Tail fan (perching only — spread tail behind)
    if perching:
        for i in range(5):
            tx = sx + (W - 2 - i * 3) if f == 1 else sx + 2 + i * 3
            pygame.draw.line(screen, bird.ACCENT_COLOR,
                             (tx, sy + H - 2), (tx - f * 4, sy + H + 6 + i), 2)
            pygame.draw.circle(screen, (60, 40, 160), (tx - f * 4, sy + H + 6 + i), 2)
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body (teal)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Head + crown
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    for i in range(3):
        pygame.draw.circle(screen, bird.ACCENT_COLOR, (hx + i * 2, sy - 2), 1)
    # Eye
    pygame.draw.rect(screen, (240, 220, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    # Beak
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

def _draw_kookaburra(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (brown)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Blue wing-bar
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, W - 2, 3))
    # Body (cream)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Large head
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
    # Brown crown patch
    pygame.draw.rect(screen, bird.WING_COLOR, (hx, sy, 5, 3))
    # Big beak
    bx = hx + 6 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_sandpiper(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Pale belly
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, H - 6))
    # Thin legs
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (130, 110, 80), (lx, sy + H - 2, 1, 3))
    # Head
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    # Long thin beak
    bx = hx + 3 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + 1, sy, 1, 1))

def _draw_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (bright blue)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Orange breast
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, H - 6))
    # Large head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.BODY_COLOR, (hx + 2, sy + 2), 4)
    # Spear beak
    bx = hx + 5 if f == 1 else hx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 6, 2))
    # Eye
    pygame.draw.rect(screen, (240, 230, 200), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_woodpecker(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (black with white bars)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    # White wingbars
    for row in [4, 7]:
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2, sy + row, W - 4, 1))
    # Body (black)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 6))
    # White cheek patch
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.ACCENT_COLOR, (hx + 2, sy + 4), 4)
    # Red crown
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    # Chisel beak
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 3, 2, 2))

def _draw_finch(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (dark)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    # Body (yellow)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Head
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    # Conical beak
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))

def _draw_stork(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long legs
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (190, 80, 40), (lx, sy + H - 8, 2, 8))
    # Wings (white with black tips)
    if not perching:
        pygame.draw.ellipse(screen, (220, 220, 220),
                            (sx, sy + 4 + int(wf), W, H - 8))
        # Black wingtips
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), 4, H - 9))
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + W - 4, sy + 4 + int(wf), 4, H - 9))
    else:
        pygame.draw.ellipse(screen, (220, 220, 220), (sx + 1, sy + 5, W - 2, H - 10))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 10))
    # Long neck
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
    # Head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    # Long orange beak
    bx = nx + 3 if f == 1 else nx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy, 7, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 0), sy, 2, 2))

def _draw_macaw(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Blue wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 1, sy + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Red body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    # Green neck accent
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 4, W - 8, 4))
    # Long tail
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 3, 6))
    pygame.draw.rect(screen, bird.WING_COLOR, (tx + 1, sy + H - 2, 1, 6))
    # Yellow face
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Beak (curved)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_pheasant(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long tail
    tx = sx if f == 1 else sx + W - 7
    pygame.draw.rect(screen, (200, 120, 40), (tx, sy + 3, 7, 3))
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx + 3, sy + 2 + int(wf), W - 6, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 3, sy + 2, W - 6, H - 4))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
    # Dark green head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Red wattle
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 0), sy + 3, 3, 2))
    # Beak
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    # Eye (gold ring)
    pygame.draw.rect(screen, (230, 190, 60), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_condor(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Huge wings (near-black)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 3, sy + 3 + int(wf), W + 6, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 6))
    # White collar ruff
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 5, sy + 4, 10, 5))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 4, W - 8, H - 6))
    # Bare orange head
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    # Hooked beak
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 2, 2))
    # Eye
    pygame.draw.rect(screen, (220, 50, 30), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 1, 1, 1))

def _draw_snow_bunting(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Black wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    # White body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Buff tinge on sides
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, 3, H - 5))
    # Head (white)
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.BODY_COLOR, (hx + 1, sy + 1), 3)
    # Beak
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))

def _draw_prairie_falcon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Pointed wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 1, sy + 1 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body (pale brown)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    # Streaked belly
    for i in range(3):
        pygame.draw.rect(screen, (130, 100, 60), (sx + 4 + i * 3, sy + 5, 1, H - 7))
    # Head
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    # Dark malar stripe
    pygame.draw.rect(screen, bird.ACCENT_COLOR,
                     (hx + (2 if f == 1 else 0), sy + 3, 2, 3))
    # Beak with yellow cere
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (bx + (1 if f == 1 else -1), sy + 3, 2, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_nightjar(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Cryptic mottled wings (overlapping ellipses for pattern)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
        pygame.draw.ellipse(screen, (150, 130, 95), (sx + 2, sy + 1 + int(wf), W - 5, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(screen, (150, 130, 95), (sx + 2, sy + 2, W - 5, H - 4))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # White throat bar
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 6, 2))
    # Head (flat/cryptic)
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    # Tiny wide mouth (gape)
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 2, 3, 1))
    # Eye (large for nocturnal)
    pygame.draw.rect(screen, (80, 70, 50), (hx + (2 if f == 1 else 0), sy + 1, 3, 3))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy + 1, 2, 2))

def _draw_ibis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long legs
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (180, 60, 50), (lx, sy + H - 7, 2, 7))
    # Wings (scarlet)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 3 + int(wf), W, H - 7))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
    # Long curved neck
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 7))
    # Head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    # Down-curved beak
    bx = nx + 3 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 3, 3, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

def _draw_albatross(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Very wide dark wingtips
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 3, sy + 2 + int(wf), W + 6, H - 3))
        # White inner wing
        pygame.draw.ellipse(screen, bird.BODY_COLOR,
                            (sx + 2, sy + 2 + int(wf), W - 4, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    # White body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 5))
    # Head (white)
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
    # Large pale beak
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 5, 2))
    pygame.draw.rect(screen, (180, 150, 110), (bx + (2 if f == 1 else 0), sy + 5, 3, 2))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_raven(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Wings (glossy black)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 1, sy + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    # Purple iridescent sheen
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 2, W - 8, 4))
    # Wedge tail (distinctive from crow)
    tx = sx + 2 if f == 1 else sx + W - 6
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 4, 6, 5))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + 2, sy + H - 2, 2, 3))
    # Head (large)
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
    # Heavy beak
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 3, 2))
    # Eye (white iris)
    pygame.draw.rect(screen, (180, 185, 190), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_swallow(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Forked tail
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 4))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + 3, sy + H - 2, 2, 4))
    # Wings (sleek, swept-back)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    # Body (deep blue)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    # Orange-rust breast
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 6))
    # Head
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.BODY_COLOR, (hx + 1, sy + 1), 3)
    # Tiny beak
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_crane(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long legs
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (170, 165, 130), (lx, sy + H - 8, 2, 8))
    # Wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 4 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 10))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 10))
    # Long neck (extended forward when flying)
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx, sy + 1, 3, H - 7))
    # Head
    pygame.draw.circle(screen, (220, 220, 225), (nx + 1, sy + 1), 3)
    # Red crown cap
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy - 1, 3, 3))
    # Beak
    bx = nx + 3 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
    # Eye
    pygame.draw.rect(screen, (240, 235, 100), (nx + (2 if f == 1 else 0), sy, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 1, 1))

def _draw_spoonbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Long legs
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (160, 120, 130), (lx, sy + H - 7, 2, 7))
    # Wings (pink)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 3 + int(wf), W, H - 7))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
    # Yellow eye area
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 3, sy + 2, 6, 4))
    # Long neck
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 7))
    # Head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    # Spatula / spoon beak (flat wide tip)
    bx = nx + 3 if f == 1 else nx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy, 3, 4))
    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

# ------------------------------------------------------------------
# Species 36–85 draw functions
# ------------------------------------------------------------------

def _draw_peregrine_falcon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 6, W - 8, H - 8))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
    pygame.draw.rect(screen, bird.HEAD_COLOR, (hx + 1, sy + 5, 5, 3))
    bx = hx + 7 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 2, 2))
    pygame.draw.rect(screen, (240, 230, 200), (hx + (2 if f == 1 else 2), sy + 2, 2, 2))

def _draw_barn_owl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 4))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (sx + W // 2, sy + 4), 6)
    # Heart-shaped face disc
    pygame.draw.ellipse(screen, (250, 245, 235), (sx + W // 2 - 5, sy + 2, 10, 8))
    pygame.draw.circle(screen, (230, 180, 100), (sx + W // 2 - 2, sy + 4), 2)
    pygame.draw.circle(screen, (230, 180, 100), (sx + W // 2 + 2, sy + 4), 2)
    pygame.draw.circle(screen, (20, 20, 20), (sx + W // 2 - 2, sy + 4), 1)
    pygame.draw.circle(screen, (20, 20, 20), (sx + W // 2 + 2, sy + 4), 1)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 6, 2, 2))

def _draw_magpie(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 4, 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, (220, 230, 255), (hx + (1 if f == 1 else 1), sy, 3, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (200, 210, 230), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_golden_oriole(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (0 if f == 1 else 1), sy + 1, 4, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_hoopoe(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 4, W - 8, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    for i in range(4):
        pygame.draw.rect(screen, bird.HEAD_COLOR, (hx + 1 - i, sy - 1 - i, 2, 2))
        pygame.draw.rect(screen, (22, 22, 28), (hx + 1 - i, sy - 1 - i, 1, 1))
    bx = hx + 5 if f == 1 else hx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 6, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 4, H - 6))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

def _draw_ptarmigan(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 1), sy, 3, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_bittern(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (155, 128, 75), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 11))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

def _draw_cedar_waxwing(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 3, 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.line(screen, (22, 22, 28), (hx, sy + 2), (hx + 4, sy + 2), 1)
    cx = hx + 2
    pygame.draw.line(screen, bird.HEAD_COLOR, (cx, sy + 2), (cx - f, sy - 3), 2)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_mockingbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3, sy + 3, 5, 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_egret(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (170, 160, 120), (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 6))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy, 6, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

def _draw_arctic_tern(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 4))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + (0 if f == 1 else 2), sy + H - 3, 2, 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (240, 240, 245), (hx + (1 if f == 1 else 1), sy + 1, 2, 2))

def _draw_cormorant(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 1 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    nx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 3, 3, 2))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx + (1 if f == 1 else 1), sy + 3, 4, 2))
    pygame.draw.rect(screen, (230, 210, 180), (nx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_curlew(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (145, 118, 78), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 7))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 8
    for i in range(4):
        ox = i if f == 1 else -i
        pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + ox, sy + 1 + i // 2, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

def _draw_avocet(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (170, 160, 140), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 6))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 7))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 7))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 7
    for i in range(4):
        ox = i if f == 1 else -i
        pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + ox, sy + 2 - i // 3, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

def _draw_jacana(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4, sx + 5, sx + W - 7]:
        pygame.draw.rect(screen, (100, 52, 22), (lx, sy + H - 5, 1, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hx + (0 if f == 1 else 1), sy, 5, 3))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_lyrebird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx - 1, sy + H - 2, 2, 8))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx + 2, sy + H - 2, 2, 8))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 6))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_bee_eater(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (sx + 3, sy + 4, W - 8, H - 7))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 6, W - 10, H - 9))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_roller(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_hornbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (sx + 3, sy + 4, W - 7, H - 8))
    hx = sx + W - 7 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
    bx = hx + 6 if f == 1 else hx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 7, 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (bx, sy + 1, 5, 3))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

def _draw_quetzal(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.WING_COLOR, (tx, sy + H - 2, 3, 8))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.BODY_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (240, 230, 200), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_snowy_owl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (sx + W // 2, sy + 4), 6)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 5, sy + 2, 10, 8))
    pygame.draw.circle(screen, (240, 220, 80), (sx + W // 2 - 2, sy + 4), 3)
    pygame.draw.circle(screen, (240, 220, 80), (sx + W // 2 + 2, sy + 4), 3)
    pygame.draw.circle(screen, (20, 20, 20), (sx + W // 2 - 2, sy + 4), 2)
    pygame.draw.circle(screen, (20, 20, 20), (sx + W // 2 + 2, sy + 4), 2)
    pygame.draw.circle(screen, (255, 255, 255), (sx + W // 2 - 1, sy + 3), 1)
    pygame.draw.circle(screen, (255, 255, 255), (sx + W // 2 + 3, sy + 3), 1)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 7, 2, 2))

def _draw_osprey(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    pygame.draw.ellipse(screen, (245, 242, 238), (sx + 4, sy + 6, W - 10, H - 8))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
    pygame.draw.rect(screen, (45, 38, 30), (hx + (0 if f == 1 else 2), sy + 3, 7, 2))
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 3, 2))
    pygame.draw.rect(screen, (240, 225, 80), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_golden_pheasant(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 2, 3, 7))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, (240, 215, 30), (hx + (0 if f == 1 else 1), sy - 1, 4, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_treecreeper(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 4
    for i in range(3):
        ox = i if f == 1 else -i
        pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + ox, sy + 2 + i // 2, 1, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

def _draw_wren(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    tx = sx + W - 2 if f == 1 else sx
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy, 2, 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy, 2, 1))
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_nuthatch(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, (22, 22, 28), (hx + (0 if f == 1 else 1), sy + 1, W - 6, 2))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_gannet(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 3, sy + int(wf), W + 6, H - 2))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 2, W - 8, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 5))
    hx = sx + W - 8 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy, 8, 5))
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

def _draw_frigatebird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 3, sy + 1 + int(wf), W + 6, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 5, sy + 2, W - 10, H - 3))
    tx = sx + 2 if f == 1 else sx + W - 6
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 5))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + (3 if f == 1 else -3), sy + H - 3, 2, 5))
    hx = sx + W - 8 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + 1, sy + 4, 5, 4))
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (200, 210, 220), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

def _draw_night_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (165, 148, 108), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 7))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.rect(screen, (22, 22, 28), (nx - 1, sy, 5, 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx + (1 if f == 1 else 0), sy - 1, 2, 5))
    bx = nx + 4 if f == 1 else nx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (220, 80, 40), (nx + (3 if f == 1 else 1), sy, 2, 2))

def _draw_lapwing(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.line(screen, (22, 22, 28), (hx + 2, sy + 2), (hx + 2, sy - 4), 2)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_wheatear(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 5))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H - 3, 3, 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.WING_COLOR, (hx - 1, sy + 1, 4, 2))
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_redstart(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H - 3, 3, 5))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (200, 210, 230), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_warbler(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_long_tailed_tit(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.WING_COLOR, (tx, sy + H - 2, 2, 7))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.WING_COLOR, (hx, sy, 3, 2))
    bx = hx + 3 if f == 1 else hx - 1
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 1, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_oystercatcher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.circle(screen, (240, 50, 30), (hx + (3 if f == 1 else 1), sy + 1), 2)
    pygame.draw.circle(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1), 1)

def _draw_kite(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    tx = sx + 2 if f == 1 else sx + W - 6
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 5))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + (3 if f == 1 else -3), sy + H - 4, 2, 6))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    bx = hx + 6 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (240, 225, 100), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_harrier(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 4, sy + 6, W - 10, H - 8))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
    bx = hx + 6 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 5, 2, 2))
    pygame.draw.rect(screen, (240, 225, 80), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_snipe(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2, sy + 1, W - 6, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy, 4, 2))
    bx = hx + 4 if f == 1 else hx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy, 2, 2))

def _draw_merlin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (240, 220, 80), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_goshawk(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 4, sy + 5, W - 10, H - 7))
    for i in range(3):
        pygame.draw.rect(screen, bird.WING_COLOR,
                         (sx + 4 + i * 3, sy + 5, 2, H - 8))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
    pygame.draw.rect(screen, (22, 22, 32), (hx, sy + 1, 7, 3))
    pygame.draw.rect(screen, (235, 232, 220), (hx + 1, sy + 4, 5, 2))
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 3, 2))
    pygame.draw.rect(screen, (240, 230, 90), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_shoebill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (100, 115, 130), (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 10))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
    nx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 2, 4, 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 2, sy + 2), 4)
    bx = nx + 5 if f == 1 else nx - 7
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 7, 4))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (bx + (4 if f == 1 else 0), sy + 4, 3, 3))
    pygame.draw.rect(screen, (180, 80, 30), (nx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_booby(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
    bx = hx + 6 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3, sy + H - 4, W - 8, 3))
    pygame.draw.rect(screen, (230, 215, 180), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

def _draw_tropicbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + int(wf), W + 4, H - 2))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
    tx = sx + 2 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 2, 8))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_dunlin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 5, H - 5))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 2)
    bx = hx + 3 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

def _draw_godwit(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (160, 108, 55), (lx, sy + H - 5, 2, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 9))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 7
    for i in range(4):
        ox = i if f == 1 else -i
        pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + ox, sy + 1 - i // 4, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

def _draw_oxpecker(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy, 3, 3))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

def _draw_dipper(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 2, W - 5, H - 6))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (200, 210, 230), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

def _draw_skua(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 5, sy + 4, 8, 4))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    bx = hx + 6 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (180, 170, 130), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

def _draw_firecrest(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy - 1, 3, 2))
    bx = hx + 3 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

def _draw_red_crowned_crane(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (185, 175, 140), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx, sy + 4 + int(wf), W, H - 8))
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), 5, H - 10))
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + W - 5, sy + 4 + int(wf), 5, H - 10))
    else:
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 5, W - 2, H - 12))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 12))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 10))
    pygame.draw.circle(screen, bird.BODY_COLOR, (nx + 1, sy + 1), 3)
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx - 1, sy - 1, 5, 3))
    pygame.draw.rect(screen, (22, 22, 28), (nx, sy + 2, 3, 2))
    bx = nx + 3 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

def _draw_mandarin_duck(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, 2))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 3, 3, 2))
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_chinese_monal(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 7
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + 3, 7, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2 + int(wf), W - 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (230, 190, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_silver_pheasant(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 7
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + 3, 7, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2 + int(wf), W - 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 0), sy + 3, 3, 2))
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (220, 195, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_crested_ibis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (185, 140, 130), (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 6))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 7))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy - 2, 2, 3))
    bx = nx + 3 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

def _draw_chinese_pond_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (180, 160, 90), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 7))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 8))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 8))
    nx = sx + W - 3 if f == 1 else sx + 1
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 2, H - 7))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
    bx = nx + 3 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
    pygame.draw.rect(screen, (20, 20, 20), (nx + (1 if f == 1 else 0), sy, 2, 2))

def _draw_fairy_pitta(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 7, H - 7))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (220, 190, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_hwamei(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, (210, 185, 140), (sx + 2, sy + 4, W - 5, H - 5))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 1, 4, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

def _draw_black_drongo(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 4))
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx + 3, sy + H - 3, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 3, W - 8, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (200, 30, 30), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_red_billed_blue_magpie(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx + 1 if f == 1 else sx + W - 5
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H - 3, 4, 7))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx + 1, sy + H + 1, 2, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
    pygame.draw.rect(screen, bird.HEAD_COLOR, (hx, sy + 3, 6, 4))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + W // 2 - 2, sy + 3, 4, 2))
    bx = hx + 6 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (240, 230, 50), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))
    pygame.draw.rect(screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 1, 1, 1))

def _draw_african_fish_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 5, sy + 4, W - 12, H - 6))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 5, 3, 2))
    pygame.draw.rect(screen, (30, 25, 15), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_secretary_bird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (215, 165, 130), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 13))
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 4, sy + H - 14, W - 10, 5))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 12))
    pygame.draw.circle(screen, bird.BODY_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx, sy + 1, 4, 4))
    for i in range(3):
        qx = nx + 1
        pygame.draw.line(screen, bird.WING_COLOR,
                         (qx, sy + 2), (qx - f * (2 + i), sy - 3 - i), 1)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_martial_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 5 + i * 4, sy + 5, 2, 2))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (235, 230, 215), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_marabou_stork(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (185, 165, 145), (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 4 + int(wf), W, H - 10))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 12))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 12))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 2, 3, H - 12))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (nx - 1, sy + 5, 5, 4))
    bx = nx + 4 if f == 1 else nx - 8
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 8, 3))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

def _draw_superb_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 4, 2))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (240, 235, 200), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_cape_weaver(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

def _draw_hamerkop(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
    nx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 4, H - 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 2, sy + 2), 4)
    cx = nx - 3 if f == 1 else nx + 5
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (cx, sy + 1, 5, 3))
    bx = nx + 5 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_african_grey_parrot(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx + 1 if f == 1 else sx + W - 4
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 3, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (245, 240, 230), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_ground_hornbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.BODY_COLOR,
                            (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx + 3, sy + 3 + int(wf), 8, H - 6))
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx + W - 11, sy + 3 + int(wf), 8, H - 6))
    else:
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 4, W - 6, H - 5))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.BODY_COLOR, (hx + 3, sy + 3), 5)
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (hx + 1, sy + 2, 6, 5))
    bx = hx + 7 if f == 1 else hx - 8
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 8, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -2), sy, 5, 3))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_african_penguin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 5))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 2, 3, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

# ------------------------------------------------------------------
# African species draw functions

def _draw_lilac_breasted_roller(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 3
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H // 2 - 1, 3, 2))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + int(wf), W - 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 1, W - 4, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_carmine_bee_eater(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H // 2, 2, 2))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + int(wf), W - 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 3, sy + 1, W - 6, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 6 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, (240, 240, 235), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_white_fronted_bee_eater(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (tx, sy + H // 2, 2, 2))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + int(wf), W - 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 3, sy + 1, W - 6, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_little_bee_eater(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 1, 3, 1))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_abyssinian_roller(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 3, 5, 3))
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_malachite_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy - 1, 4, 2))
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_giant_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 4 + i * 4, sy + 5, 2, 2))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 1), 5)
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + i * 2, sy, 2, 1))
    bx = hx + 8 if f == 1 else hx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_pygmy_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy, 4, 1))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_pied_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    for i in range(2):
        pygame.draw.rect(screen, bird.WING_COLOR, (sx + 3 + i * 4, sy + 3, 3, 2))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    for i in range(2):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + i * 2, sy, 2, 1))
    bx = hx + 6 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_grey_headed_kingfisher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    bx = hx + 6 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_bateleur_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 5, sy + 3, W - 10, H - 3))
    hx = sx + W - 9 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 1, 7, 5))
    bx = hx + 8 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_tawny_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 3))
    hx = sx + W - 8 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_verreauxs_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 3, sy + 2 + int(wf), 6, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 5, sy + 3, W - 10, H - 3))
    hx = sx + W - 9 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (240, 235, 215), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_brown_snake_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 2 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    hx = sx + W - 8 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 6)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx + 1, sy + 3, 5, 4))
    bx = hx + 8 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (240, 235, 215), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_long_crested_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 2 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    for i in range(3):
        pygame.draw.rect(screen, bird.BODY_COLOR, (sx + 4 + i * 4, sy + 4, 2, 2))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    pygame.draw.line(screen, bird.WING_COLOR, (hx + 3, sy + 2), (hx + (1 if f == 1 else 5), sy - 4), 2)
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (240, 235, 215), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_african_crowned_eagle(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 3))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 5 + i * 3, sy + 5, 2, 2))
    hx = sx + W - 8 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    for i in range(2):
        pygame.draw.line(screen, bird.BODY_COLOR, (hx + 2 + i, sy + 2), (hx + (0 + i if f == 1 else 4 - i), sy - 5), 1)
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_lanner_falcon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 1 + int(wf), W + 2, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 2))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 1), 5)
    pygame.draw.ellipse(screen, bird.WING_COLOR, (hx, sy + 1, 6, 3))
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 3, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_pygmy_falcon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 1, 4, 2))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_kestrel(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 2))
    for i in range(3):
        pygame.draw.rect(screen, bird.WING_COLOR, (sx + 3 + i * 3, sy + 4, 2, 1))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 3, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_red_necked_falcon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 2))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 3, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_lappet_faced_vulture(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 3 + int(wf), W + 4, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 5, sy + 4, W - 10, H - 4))
    hx = sx + W - 9 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 2, 8, 5))
    bx = hx + 8 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 5, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_white_backed_vulture(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 3 + int(wf), W + 4, H - 3))
        pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 4, sy + 3 + int(wf), 8, H - 6))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 5, sy + 4, W - 10, H - 5))
    hx = sx + W - 9 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
    bx = hx + 7 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 5, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

def _draw_egyptian_vulture(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 2 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.BEAK_COLOR, (hx, sy + 1, 6, 4))
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

def _draw_palm_nut_vulture(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + 2 + int(wf), W + 2, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 1, 7, 4))
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

def _draw_saddlebilled_stork(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (188, 168, 148), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 6, W - 4, H - 14))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 14))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 3), 4)
    bx = nx + 4 if f == 1 else nx - 8
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 8, 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (bx + (2 if f == 1 else 1), sy, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_yellow_billed_stork(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (185, 162, 138), (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 10))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 12))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 12))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 12))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (nx - 1, sy + 2, 5, 4))
    bx = nx + 4 if f == 1 else nx - 8
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 8, 3))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_goliath_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (188, 162, 128), (lx, sy + H - 12, 2, 12))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 5 + int(wf), W, H - 14))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 6, W - 2, H - 16))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 6, W - 4, H - 16))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 16))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_purple_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (168, 135, 108), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 14))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx, sy + 2, 3, H - 14))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.line(screen, bird.WING_COLOR, (nx + 1, sy + 3), (nx + 1, sy + 7), 1)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_black_headed_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (178, 155, 128), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 14))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 14))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx - 1, sy + 2, 5, 2))
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_great_egret(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (215, 205, 195), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 14))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 14))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_cattle_egret(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (205, 192, 175), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 10))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 10))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 10))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (nx - 1, sy + 1, 5, 3))
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 1, 1))

def _draw_squacco_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (195, 182, 155), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 10))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 10))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 10))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 3 if f == 1 else nx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 1, 1))

def _draw_grey_crowned_crane(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (188, 162, 138), (lx, sy + H - 10, 2, 10))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), W, H - 12))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 14))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 2, 3, H - 14))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
    for i in range(5):
        pygame.draw.line(screen, bird.ACCENT_COLOR, (nx + 1, sy + 1), (nx + 1 + (i - 2), sy - 4 - i % 3), 1)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_hadeda_ibis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 3, W - 8, H - 8))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_sacred_ibis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + W // 2 - 3, sy + 4, 6, H - 8))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_glossy_ibis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 2, W - 8, H - 8))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_african_spoonbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 6))
    pygame.draw.circle(screen, bird.ACCENT_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 6
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.ellipse(screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy, 3, 4))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_great_white_pelican(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 2))
    hx = sx + W - 8 if f == 1 else sx + 4
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 1), 5)
    bx = hx + 7 if f == 1 else hx - 8
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 8, 2))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (bx + (1 if f == 1 else 0), sy + 3, 6, 3))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_african_darter(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3 + i * 4, sy + 4, 3, 1))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 6))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 2, 2, 2))

def _draw_crowned_lapwing(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (215, 185, 148), (lx, sy + H - 4, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy - 1, 4, 2))
    pygame.draw.line(screen, bird.ACCENT_COLOR, (hx + 2, sy - 1), (hx + 2, sy - 4), 1)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_blackwinged_stilt(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (lx, sy + H - 8, 2, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 9))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 9))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_purple_swamphen(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (148, 128, 108), (lx, sy + H - 5, 2, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 5))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy - 1, 3, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_african_rail(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (148, 128, 98), (lx, sy + H - 4, 1, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_jacana(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 1, sx + W - 3]:
        pygame.draw.rect(screen, (148, 128, 98), (lx, sy + H - 4, 1, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy - 1, 4, 2))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_red_billed_quelea(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_village_weaver(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 1, 5, 3))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_golden_bishop(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_southern_red_bishop(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, 3))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_wattled_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 3, 5, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_malachite_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H // 2, 2, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_orange_breasted_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 2, W - 5, 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_scarlet_chested_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 5, H - 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_amethyst_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 3, 4, 2))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_collared_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, W - 2, 2))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_variable_sunbird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 5, 2))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_violet_backed_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (240, 235, 215), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_greater_blue_eared_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, 3))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_plum_colored_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_pied_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 4, H - 5))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 2, 2))

def _draw_burchells_starling(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 2, W - 5, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

def _draw_african_firefinch(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 2, sy + 3, 1, 1))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_blue_waxbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_violet_eared_waxbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 2, 4, 1))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_yellow_fronted_canary(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 2, W - 4, 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_melba_finch(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 3, 3, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_silverbill(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 3))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_locust_finch(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_double_tooth_barbet(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 3, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx - 1, sy + 2, 6, 2))
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 3))
    pygame.draw.rect(screen, bird.HEAD_COLOR, (bx + (1 if f == 1 else 0), sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_black_collared_barbet(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, (188, 178, 168), (sx + 1, sy + 3, W - 2, H - 4))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, W - 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx - 1, sy + 4, 6, 2))
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_red_yellow_barbet(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 3, sy + 4, 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_african_green_pigeon(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 3, sy + 4, W - 7, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_namaqua_dove(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 3, 5, 1))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_laughing_dove(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 5, 3))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_meyer_parrot(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2, sy + 2, W - 5, 2))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 1, 4, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_cape_parrot(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 1, 5, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_rosy_faced_lovebird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2, sy + 6, W - 5, 2))
    hx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_ostrich(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 5, sx + W - 7]:
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (lx, sy + H - 14, 3, 14))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + H - 26, W - 2, 18))
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 3, sy + H - 24, W - 8, 8))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + H - 34, 3, 12))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + H - 34), 4)
    bx = nx + 4 if f == 1 else nx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + H - 34, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + H - 35, 2, 2))

def _draw_kori_bustard(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 4, sx + W - 6]:
        pygame.draw.rect(screen, (185, 165, 128), (lx, sy + H - 8, 3, 8))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 8))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 9))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 1, W - 4, H - 9))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3 + i * 4, sy + 2, 2, 3))
    nx = sx + W - 5 if f == 1 else sx + 3
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy - 2, 3, 8))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy - 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx - 1, sy - 3, 5, 2))
    bx = nx + 4 if f == 1 else nx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy - 2, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy - 3, 2, 2))

def _draw_helmeted_guineafowl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (155, 135, 108), (lx, sy + H - 5, 2, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    for i in range(8):
        pygame.draw.rect(screen, (245, 240, 225), (sx + 2 + (i % 4) * 3, sy + 2 + (i // 4) * 3, 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + 1, sy - 1, 2, 3))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hx + (4 if f == 1 else -2), sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_namaqua_sandgrouse(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 3, sy + 3, 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_fiscal_shrike(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.WING_COLOR, (hx, sy + 2, 5, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_red_backed_shrike(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 2, 5, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 2, 2, 2))

def _draw_pied_crow(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 5)
    bx = hx + 6 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_fan_tailed_raven(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 5
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (tx, sy + H - 4, 5, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
    hx = sx + W - 7 if f == 1 else sx + 3
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 3, sy + 1), 5)
    bx = hx + 7 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

def _draw_paradise_flycatcher(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    tx = sx if f == 1 else sx + W - 3
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, sy + H, 3, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 5, H - 3))
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    pygame.draw.ellipse(screen, bird.BEAK_COLOR, (hx, sy + 1, 5, 3))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_batis(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, W - 2, 2))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_cape_robin_chat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, 3))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_stonechat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 3, 5, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_pennant_winged_nightjar(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pw = sx if f == 1 else sx + W - 3
        pygame.draw.line(screen, bird.ACCENT_COLOR, (pw, sy + 4), (pw + (f * -18), sy + 14), 1)
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3 + i * 4, sy + 3, 3, 1))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_alpine_swift(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + int(wf), W + 4, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 1, W - 8, H - 2))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 5, sy + 3, W - 10, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_palm_swift(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 1, sy + int(wf), W + 2, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 4, sy + 1, W - 8, H - 2))
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 5, sy + 3, W - 10, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_red_knobbed_coot(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (88, 78, 68), (lx, sy + H - 4, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 5))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy - 1, 2, 3))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_african_snipe(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (148, 128, 95), (lx, sy + H - 3, 2, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    for i in range(3):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 3, sy + 2, 2, 1))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    bx = hx + 4 if f == 1 else hx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_spotted_thick_knee(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (185, 162, 112), (lx, sy + H - 5, 2, 5))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 3, sy + 2, 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 1, 5, 3))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_wattled_plover(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (178, 155, 118), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 6))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 3, 5, 2))
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_blacksmith_lapwing(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (155, 138, 108), (lx, sy + H - 4, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx - 1, sy + 1, 6, 2))
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

def _draw_three_banded_plover(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 2, sx + W - 4]:
        pygame.draw.rect(screen, (148, 128, 95), (lx, sy + H - 3, 1, 3))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    for i in range(2):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 1, sy + 3 + i * 2, W - 2, 1))
    hx = sx + W - 4 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx, sy + 1, 4, 1))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

def _draw_african_fish_owl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 6))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 3 + i * 3, sy + 6, 2, 3))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (sx + W // 2, sy + 3), 6)
    for ox in [-4, 4]:
        pygame.draw.ellipse(screen, (235, 200, 55), (sx + W // 2 + ox - 2, sy + 1, 4, 4))
        pygame.draw.rect(screen, (22, 22, 22), (sx + W // 2 + ox - 1, sy + 2, 2, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 3, 2, 3))
    for ox in [-3, 3]:
        pygame.draw.line(screen, bird.HEAD_COLOR, (sx + W // 2 + ox, sy + 3), (sx + W // 2 + ox, sy - 1), 1)

def _draw_verreauxs_eagle_owl(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 4))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 6))
    for i in range(5):
        pygame.draw.rect(screen, bird.WING_COLOR, (sx + 3 + i * 3, sy + 6, 2, 3))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (sx + W // 2, sy + 3), 7)
    for ox in [-4, 4]:
        pygame.draw.ellipse(screen, (215, 148, 165), (sx + W // 2 + ox - 2, sy + 1, 4, 5))
        pygame.draw.ellipse(screen, (235, 215, 205), (sx + W // 2 + ox - 1, sy + 2, 2, 3))
        pygame.draw.rect(screen, (22, 22, 22), (sx + W // 2 + ox - 1, sy + 2, 2, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 4, 2, 3))

def _draw_speckled_mousebird(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    ty = sy + H - 2
    tx = sx if f == 1 else sx + W - 3
    pygame.draw.rect(screen, bird.BODY_COLOR, (tx, ty, 3, 6))
    pygame.draw.line(screen, bird.WING_COLOR, (tx + 1, ty + 4), (tx + 1 + f * 2, ty + 9), 1)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    for i in range(4):
        pygame.draw.rect(screen, bird.ACCENT_COLOR, (sx + 2 + i * 3, sy + 3, 2, 2))
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hx, sy, 4, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
    pygame.draw.rect(screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_gambels_quail(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    # Plump body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 3))
    # Wing overlay
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 4, W - 4, H - 5))
    # Small round head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    # Topknot — forward-curving teardrop
    tk_x = hx + (3 if f == 1 else 1)
    pygame.draw.line(screen, bird.ACCENT_COLOR, (tk_x, sy + 1), (tk_x + f * 2, sy - 2), 2)
    pygame.draw.circle(screen, bird.ACCENT_COLOR, (tk_x + f * 2, sy - 3), 1)
    # Eye
    pygame.draw.rect(screen, (15, 15, 15), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))
    # Short beak
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
    # Legs
    lx1 = sx + W // 2 - 2
    lx2 = sx + W // 2 + 2
    pygame.draw.line(screen, (75, 55, 30), (lx1, sy + H - 2), (lx1, sy + H + 3), 1)
    pygame.draw.line(screen, (75, 55, 30), (lx2, sy + H - 2), (lx2, sy + H + 3), 1)

# ------------------------------------------------------------------
# Nocturnal birds

def _draw_small_owl(screen, bird, sx, sy, wf, perching):
    """Elf Owl, Ferruginous Pygmy Owl, Common Scops Owl, Eastern Screech Owl."""
    W, H = bird.W, bird.H
    hcx = sx + W // 2
    r = max(W // 2 - 2, 3)
    # Wings / lower body
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + r * 2 + 1, W - 2, H - r * 2 - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + r * 2 + 2, W - 4, H - r * 2 - 3))
    # Large round head (dominant feature of owls)
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r + 1), r)
    # Facial disk
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR,
                        (hcx - r + 1, sy + 1, max((r - 1) * 2, 2), r * 2 - 1))
    # Two forward-facing yellow eyes
    pygame.draw.rect(screen, (215, 175, 28), (hcx - 2, sy + r, 2, 2))
    pygame.draw.rect(screen, (215, 175, 28), (hcx + 1, sy + r, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (hcx - 1, sy + r, 1, 1))
    pygame.draw.rect(screen, (12, 12, 12), (hcx + 2, sy + r, 1, 1))
    # Small hooked beak
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hcx - 1, sy + r + 2, 3, 2))

def _draw_large_owl(screen, bird, sx, sy, wf, perching):
    """Barred Owl, Spectacled Owl — large round-headed, no ear tufts, barred chest."""
    W, H = bird.W, bird.H
    hcx = sx + W // 2
    r = W // 2 - 2
    chest_top = sy + r * 2 + 2
    chest_h = max(H - r * 2 - 4, 2)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, chest_top, W - 2, chest_h + 1))
    # Barred / streaked chest
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, chest_top, W - 4, chest_h))
    for i in range(0, chest_h - 1, 3):
        pygame.draw.line(screen, bird.ACCENT_COLOR,
                         (sx + 3, chest_top + i + 1), (sx + W - 4, chest_top + i + 1), 1)
    # Large round head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r + 1), r)
    # Facial disk
    fd_r = max(r - 2, 1)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR,
                        (hcx - fd_r, sy + 2, fd_r * 2, r * 2 - 2))
    # Eyes
    pygame.draw.rect(screen, (215, 175, 28), (hcx - 2, sy + r, 2, 2))
    pygame.draw.rect(screen, (215, 175, 28), (hcx + 1, sy + r, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (hcx - 1, sy + r, 1, 1))
    pygame.draw.rect(screen, (12, 12, 12), (hcx + 2, sy + r, 1, 1))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hcx - 1, sy + r + 2, 3, 2))

def _draw_eared_owl(screen, bird, sx, sy, wf, perching):
    """Long-eared Owl, Short-eared Owl — prominent ear tufts."""
    W, H = bird.W, bird.H
    hcx = sx + W // 2
    r = W // 2 - 2
    chest_top = sy + r * 2 + 2
    chest_h = max(H - r * 2 - 4, 2)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, chest_top, W - 2, chest_h + 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, chest_top, W - 4, chest_h))
    # Ear tufts drawn before head so head overlaps their base
    pygame.draw.line(screen, bird.HEAD_COLOR, (hcx - 3, sy + 2), (hcx - 4, sy - 4), 2)
    pygame.draw.line(screen, bird.HEAD_COLOR, (hcx + 3, sy + 2), (hcx + 4, sy - 4), 2)
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r + 1), r)
    fd_r = max(r - 2, 1)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR,
                        (hcx - fd_r, sy + 2, fd_r * 2, r * 2 - 2))
    pygame.draw.rect(screen, (215, 175, 28), (hcx - 2, sy + r, 2, 2))
    pygame.draw.rect(screen, (215, 175, 28), (hcx + 1, sy + r, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (hcx - 1, sy + r, 1, 1))
    pygame.draw.rect(screen, (12, 12, 12), (hcx + 2, sy + r, 1, 1))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hcx - 1, sy + r + 2, 3, 2))

def _draw_frogmouth(screen, bird, sx, sy, wf, perching):
    """Tawny Frogmouth — wide flat head, enormous gaping beak, mottled bark-like camouflage."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3, W, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 6))
    # Wide flat head
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (hcx - 5, sy, 10, 7))
    # Enormous wide beak (gape points toward facing direction)
    bx = hcx + (3 if f == 1 else -7)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
    pygame.draw.line(screen, (12, 12, 12), (bx, sy + 3), (bx + 5, sy + 3), 1)
    # Rictal bristles (stiff whisker-like feathers at beak base)
    for i in range(3):
        wx = bx + (-i if f == 1 else i)
        pygame.draw.line(screen, bird.ACCENT_COLOR, (wx, sy + 2), (wx - f * 2, sy), 1)
    # Eyes (amber, close together on wide face)
    ex1 = hcx - 3
    ex2 = hcx + 2
    pygame.draw.rect(screen, (215, 165, 38), (ex1, sy + 1, 2, 2))
    pygame.draw.rect(screen, (215, 165, 38), (ex2, sy + 1, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (ex1 + 1, sy + 1, 1, 1))
    pygame.draw.rect(screen, (12, 12, 12), (ex2 + 1, sy + 1, 1, 1))

def _draw_potoo(screen, bird, sx, sy, wf, perching):
    """Common Potoo — slim camouflaged body, enormous eye, tiny bill, stump posture."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        # Stump-like upright posture
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 4, W - 6, H - 5))
    # Slightly elongated head
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (hcx - 3, sy, 6, 6))
    # Enormous single visible eye (potoos are famous for these)
    ex = hcx + (1 if f == 1 else -2)
    pygame.draw.ellipse(screen, (215, 165, 38), (ex - 1, sy + 1, 3, 3))
    pygame.draw.rect(screen, (12, 12, 12), (ex, sy + 2, 1, 1))
    # Tiny beak (hidden in camouflage)
    bx = hcx + (2 if f == 1 else -3)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 3, 2, 1))

def _draw_nighthawk(screen, bird, sx, sy, wf, perching):
    """Whip-poor-will, Common Poorwill — flat low body, wide gaping mouth, white throat."""
    W, H = bird.W, bird.H
    f = bird.facing
    # Flat wide wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    # Small rounded head offset to facing side
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    # Wide gaping mouth (characteristic nightjar feature)
    mx = hx + 4 if f == 1 else hx - 4
    pygame.draw.rect(screen, (12, 12, 12), (mx, sy + 2, 4, 2))
    # White / pale throat patch
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (hx, sy + 3, 4, 2))
    # Amber eye
    pygame.draw.rect(screen, (215, 165, 38), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (hx + (3 if f == 1 else 2), sy + 1, 1, 1))

def _draw_burrowing_owl(screen, bird, sx, sy, wf, perching):
    """Burrowing Owl — upright ground owl with long legs, white eyebrow stripe."""
    W, H = bird.W, bird.H
    hcx = sx + W // 2
    r = max(W // 2 - 1, 3)
    body_top = sy + r * 2
    body_h = max(H - r * 2 - 4, 2)
    # Upright body
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, body_top, W - 2, body_h + 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, body_top + 1, W - 4, body_h - 1))
    # White eyebrow stripes (distinctive of burrowing owl)
    pygame.draw.line(screen, bird.ACCENT_COLOR,
                     (hcx - 3, sy + r), (hcx + 2, sy + r), 1)
    # Round head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r), r)
    # Eyes
    pygame.draw.rect(screen, (215, 175, 28), (hcx - 2, sy + r, 2, 2))
    pygame.draw.rect(screen, (215, 175, 28), (hcx + 1, sy + r, 2, 2))
    pygame.draw.rect(screen, (12, 12, 12), (hcx - 1, sy + r, 1, 1))
    pygame.draw.rect(screen, (12, 12, 12), (hcx + 2, sy + r, 1, 1))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hcx - 1, sy + r + 2, 2, 2))
    # Long legs (burrowing owls stand tall on the ground)
    leg_c = (188, 155, 98)
    pygame.draw.line(screen, leg_c, (hcx - 2, sy + H - 3), (hcx - 2, sy + H + 4), 2)
    pygame.draw.line(screen, leg_c, (hcx + 2, sy + H - 3), (hcx + 2, sy + H + 4), 2)

def _draw_kiwi(screen, bird, sx, sy, wf, perching):
    """Kiwi — round fluffy body, tiny vestigial wings hidden, extremely long curved bill."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    # Fluffy round body (kiwi feathers resemble coarse hair)
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx, sy + 2, W, H - 2))
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 2, sy + 4, W - 4, H - 5))
    # Small head
    hx = sx + W - 5 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 3), 3)
    # Enormously long, gently downward-curved bill (the kiwi's signature feature)
    tip_x = (sx + W + 3) if f == 1 else (sx - 3)
    tip_y = sy + 6
    pygame.draw.line(screen, bird.BEAK_COLOR,
                     (hx + (3 if f == 1 else 2), sy + 4), (tip_x, tip_y), 2)
    # Eye (very small — kiwis have poor eyesight)
    pygame.draw.rect(screen, (12, 12, 12), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))
    # Sturdy legs
    pygame.draw.line(screen, (105, 80, 50), (hcx - 2, sy + H - 2), (hcx - 2, sy + H + 3), 2)
    pygame.draw.line(screen, (105, 80, 50), (hcx + 2, sy + H - 2), (hcx + 2, sy + H + 3), 2)

def _draw_night_parrot(screen, bird, sx, sy, wf, perching):
    """Night Parrot — plump mottled green, hooked parrot beak, yellow eye ring."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    # Plump body
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 5))
    # Short rounded tail
    tx = sx if f == 1 else sx + W - 3
    pygame.draw.rect(screen, bird.WING_COLOR, (tx, sy + H - 4, 3, 4))
    # Head
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    # Hooked parrot beak
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 1))
    # Yellow eye ring (ACCENT_COLOR) + dark pupil
    ex = hx + (3 if f == 1 else 1)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (ex - 1, sy + 1, 3, 3), 1)
    pygame.draw.rect(screen, (12, 12, 12), (ex, sy + 1, 2, 2))

# ------------------------------------------------------------------
# Bats

def _draw_bat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    cx = sx + W // 2
    # Wide membrane wings
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (cx - 4, sy + 1, 8, H - 1))
    # Small body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (cx - 3, sy + 1, 6, H - 1))
    # Head
    pygame.draw.circle(screen, bird.BODY_COLOR, (cx, sy + 2), 3)
    # Pointed ears
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx - 1, sy + 1), (cx - 3, sy - 3), (cx, sy)])
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx + 1, sy + 1), (cx + 3, sy - 3), (cx, sy)])
    # Eye
    pygame.draw.rect(screen, (8, 8, 15), (cx - 1, sy + 1, 1, 1))

def _draw_fruit_bat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    cx = sx + W // 2
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (cx - 5, sy + 1, 10, H - 1))
    # Heavier body
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (cx - 4, sy + 1, 8, H))
    # Large fox-like head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (cx, sy + 2), 4)
    # Rounded ears
    pygame.draw.polygon(screen, bird.HEAD_COLOR,
                        [(cx - 1, sy + 1), (cx - 3, sy - 2), (cx, sy + 1)])
    pygame.draw.polygon(screen, bird.HEAD_COLOR,
                        [(cx + 1, sy + 1), (cx + 3, sy - 2), (cx, sy + 1)])
    # Snout
    nx = cx + (2 if f == 1 else -4)
    pygame.draw.ellipse(screen, bird.BEAK_COLOR, (nx, sy + 2, 3, 2))
    # Eye
    ex = cx + (2 if f == 1 else -2)
    pygame.draw.rect(screen, (8, 8, 15), (ex, sy + 1, 2, 2))

def _draw_vampire_bat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    cx = sx + W // 2
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (cx - 4, sy + 1, 8, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (cx - 3, sy + 1, 6, H - 1))
    pygame.draw.circle(screen, bird.BODY_COLOR, (cx, sy + 2), 3)
    # Extra-pointed ears
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx - 1, sy + 1), (cx - 4, sy - 4), (cx, sy)])
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx + 1, sy + 1), (cx + 4, sy - 4), (cx, sy)])
    # Red eyes
    pygame.draw.rect(screen, bird.BEAK_COLOR, (cx - 1, sy + 1, 2, 2))
    # Tiny white fangs
    fang_x = cx + (0 if f == 1 else -2)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (fang_x, sy + 3, 1, 2))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (fang_x + 2, sy + 3, 1, 2))

def _draw_leaf_nosed_bat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    cx = sx + W // 2
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (cx - 4, sy + 1, 8, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (cx - 3, sy + 1, 6, H - 1))
    pygame.draw.circle(screen, bird.BODY_COLOR, (cx, sy + 2), 3)
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx - 1, sy + 1), (cx - 3, sy - 3), (cx, sy)])
    pygame.draw.polygon(screen, bird.BODY_COLOR,
                        [(cx + 1, sy + 1), (cx + 3, sy - 3), (cx, sy)])
    # Triangular nose leaf
    nx = cx + (1 if f == 1 else -3)
    pygame.draw.polygon(screen, bird.HEAD_COLOR,
                        [(nx, sy + 3), (nx + 2, sy + 3), (nx + 1, sy + 1)])
    pygame.draw.rect(screen, (8, 8, 15), (cx - 1, sy + 1, 1, 1))

def _draw_hammer_headed_bat(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    cx = sx + W // 2
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + int(wf), W, H))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (cx - 5, sy + 1, 10, H - 1))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (cx - 4, sy + 1, 8, H))
    # Wide elongated head offset to facing side
    hx = cx + (2 if f == 1 else -6)
    pygame.draw.ellipse(screen, bird.HEAD_COLOR, (hx, sy, 6, 5))
    # Ears
    pygame.draw.polygon(screen, bird.HEAD_COLOR,
                        [(cx - 1, sy + 1), (cx - 3, sy - 3), (cx, sy)])
    pygame.draw.polygon(screen, bird.HEAD_COLOR,
                        [(cx + 1, sy + 1), (cx + 3, sy - 3), (cx, sy)])
    # Elongated muzzle
    nx = hx + (5 if f == 1 else -3)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (nx, sy + 1, 4, 2))
    # Eye
    ex = hx + (3 if f == 1 else 2)
    pygame.draw.rect(screen, (8, 8, 15), (ex, sy + 1, 1, 1))

# ------------------------------------------------------------------
# Penguins

def _draw_penguin(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    r = max(W // 2 - 1, 2)
    # Dark back fills the upright body
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy, W, H - 2))
    # White belly
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + H // 3, W - 4, H * 2 // 3))
    # Head
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r), r)
    # Beak
    bx = hcx + (r if f == 1 else -r - 2)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + r, 3, 2))
    # Eye — white sclera with dark pupil
    ex = hcx + (r - 2 if f == 1 else -r + 1)
    pygame.draw.rect(screen, (240, 240, 240), (ex, sy + r - 1, 2, 2))
    pygame.draw.rect(screen, (15, 15, 15), (ex + (1 if f == 1 else 0), sy + r - 1, 1, 1))
    # Flipper
    fx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.WING_COLOR, (fx, sy + H // 3, 2, H // 3))
    # Feet
    lx = hcx
    pygame.draw.line(screen, (200, 110, 20), (lx - 2, sy + H - 2), (lx - 2, sy + H + 3), 2)
    pygame.draw.line(screen, (200, 110, 20), (lx + 2, sy + H - 2), (lx + 2, sy + H + 3), 2)

def _draw_penguin_cheek(screen, bird, sx, sy, wf, perching):
    """Emperor and King penguins — large with coloured cheek/neck patches."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    r = max(W // 2 - 1, 2)
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + H // 3, W - 4, H * 2 // 3))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r), r)
    # Coloured cheek/auricular patch (ACCENT_COLOR)
    patch_x = hcx + (r - 2 if f == 1 else -r)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (patch_x - 1, sy + r, 3, 5))
    # Longer curved beak
    bx = hcx + (r if f == 1 else -r - 3)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + r, 4, 2))
    pygame.draw.rect(screen, bird.BEAK_COLOR,
                     (bx + (2 if f == 1 else 0), sy + r + 2, 2, 1))
    # Eye
    ex = hcx + (r - 2 if f == 1 else -r + 1)
    pygame.draw.rect(screen, (240, 240, 240), (ex, sy + r - 1, 2, 2))
    pygame.draw.rect(screen, (15, 15, 15), (ex + (1 if f == 1 else 0), sy + r - 1, 1, 1))
    # Flipper
    fx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.WING_COLOR, (fx, sy + H // 3, 2, H // 3))
    # Feet
    lx = hcx
    pygame.draw.line(screen, (200, 110, 20), (lx - 2, sy + H - 2), (lx - 2, sy + H + 3), 2)
    pygame.draw.line(screen, (200, 110, 20), (lx + 2, sy + H - 2), (lx + 2, sy + H + 3), 2)

def _draw_crested_penguin(screen, bird, sx, sy, wf, perching):
    """Macaroni and Rockhopper penguins — yellow/orange spiky crest."""
    W, H = bird.W, bird.H
    f = bird.facing
    hcx = sx + W // 2
    r = max(W // 2 - 1, 2)
    pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy, W, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + H // 3, W - 4, H * 2 // 3))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hcx, sy + r), r)
    # Spiky crest above head (ACCENT_COLOR)
    for i in range(-2, 3):
        tip_y = sy + r - 2 - (3 - abs(i))
        pygame.draw.line(screen, bird.ACCENT_COLOR,
                         (hcx + i, sy + r - 1), (hcx + i, tip_y), 1)
    # Beak
    bx = hcx + (r if f == 1 else -r - 2)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + r, 3, 2))
    # Yellow/orange eye ring
    ex = hcx + (r - 2 if f == 1 else -r + 1)
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (ex - 1, sy + r - 2, 4, 4), 1)
    pygame.draw.rect(screen, (240, 240, 240), (ex, sy + r - 1, 2, 2))
    pygame.draw.rect(screen, (15, 15, 15), (ex + (1 if f == 1 else 0), sy + r - 1, 1, 1))
    # Flipper
    fx = sx if f == 1 else sx + W - 2
    pygame.draw.rect(screen, bird.WING_COLOR, (fx, sy + H // 3, 2, H // 3))
    # Feet
    lx = hcx
    pygame.draw.line(screen, (200, 110, 20), (lx - 2, sy + H - 2), (lx - 2, sy + H + 3), 2)
    pygame.draw.line(screen, (200, 110, 20), (lx + 2, sy + H - 2), (lx + 2, sy + H + 3), 2)

def _draw_brown_noddy(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    bx = hx + 5 if f == 1 else hx - 4
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 2))
    pygame.draw.rect(screen, (10, 10, 10), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

def _draw_white_tern(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx - 3, sy + int(wf), W + 6, H - 1))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
    bx = hx + 4 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 1), sy, 2, 1))

def _draw_pacific_golden_plover(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (120, 105, 75), (lx, sy + H - 4, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
    pygame.draw.ellipse(screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 2, 2))
    bx = hx + 4 if f == 1 else hx - 2
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
    pygame.draw.rect(screen, (10, 10, 10), (hx + (2 if f == 1 else 1), sy + 2, 1, 1))

def _draw_common_myna(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (150, 130, 80), (lx, sy + H - 4, 2, 4))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 1 + int(wf), W, H - 3))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
    # White wing patch
    pygame.draw.rect(screen, (230, 225, 215), (sx + W // 2 - 2, sy + H - 5, 5, 3))
    hx = sx + W - 6 if f == 1 else sx + 2
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 4)
    pygame.draw.rect(screen, bird.BEAK_COLOR, (hx + (4 if f == 1 else -1), sy + 1, 4, 2))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 2), sy, 4, 3))
    pygame.draw.rect(screen, (240, 240, 240), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

def _draw_reef_heron(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing
    for lx in [sx + 3, sx + W - 5]:
        pygame.draw.rect(screen, (100, 118, 132), (lx, sy + H - 6, 2, 6))
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 7))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
    pygame.draw.ellipse(screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
    nx = sx + W - 4 if f == 1 else sx + 2
    pygame.draw.rect(screen, bird.HEAD_COLOR, (nx, sy + 2, 3, 5))
    pygame.draw.circle(screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
    bx = nx + 4 if f == 1 else nx - 5
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
    pygame.draw.rect(screen, bird.ACCENT_COLOR, (nx + (2 if f == 1 else 0), sy + 4, 2, 2))
    pygame.draw.rect(screen, (10, 10, 10), (nx + (2 if f == 1 else 1), sy + 2, 1, 1))

# ------------------------------------------------------------------
# Insects
