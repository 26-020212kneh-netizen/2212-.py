import random
import streamlit as st


# =========================================================
# Streamlit 설정
# =========================================================

st.set_page_config(
    page_title="잊혀진 던전 RPG",
    page_icon="⚔️",
    layout="centered"
)


# =========================================================
# 게임 데이터
# =========================================================

SHOP_ITEMS = {

    "weapons": [
        {
            "name": "낡은 검",
            "price": 50,
            "attack": 5
        },
        {
            "name": "철검",
            "price": 150,
            "attack": 12
        },
        {
            "name": "강철 대검",
            "price": 350,
            "attack": 25
        },
        {
            "name": "용의 검",
            "price": 800,
            "attack": 45
        }
    ],

    "armors": [
        {
            "name": "천 갑옷",
            "price": 50,
            "defense": 5
        },
        {
            "name": "가죽 갑옷",
            "price": 150,
            "defense": 10
        },
        {
            "name": "강철 갑옷",
            "price": 350,
            "defense": 20
        },
        {
            "name": "용의 갑옷",
            "price": 800,
            "defense": 35
        }
    ],

    "accessories": [
        {
            "name": "힘의 반지",
            "price": 200,
            "attack": 8,
            "defense": 0,
            "mana": 0
        },
        {
            "name": "수호의 목걸이",
            "price": 250,
            "attack": 0,
            "defense": 10,
            "mana": 5
        },
        {
            "name": "마력의 반지",
            "price": 350,
            "attack": 0,
            "defense": 0,
            "mana": 10
        },
        {
            "name": "대마법사의 목걸이",
            "price": 700,
            "attack": 5,
            "defense": 5,
            "mana": 15
        },
        {
            "name": "용사의 반지",
            "price": 500,
            "attack": 20,
            "defense": 10,
            "mana": 10
        }
    ],

    "potions": [
        {
            "name": "소형 포션",
            "price": 30,
            "heal": 30
        },
        {
            "name": "중형 포션",
            "price": 70,
            "heal": 70
        },
        {
            "name": "대형 포션",
            "price": 150,
            "heal": 150
        }
    ]
}


ENEMIES = [

    {
        "name": "슬라임",
        "hp": 35,
        "attack": 8,
        "defense": 2,
        "coins": 20,
        "exp": 15
    },

    {
        "name": "고블린",
        "hp": 50,
        "attack": 11,
        "defense": 4,
        "coins": 35,
        "exp": 25
    },

    {
        "name": "해골 전사",
        "hp": 75,
        "attack": 15,
        "defense": 7,
        "coins": 55,
        "exp": 40
    },

    {
        "name": "오크",
        "hp": 110,
        "attack": 21,
        "defense": 10,
        "coins": 90,
        "exp": 60
    }
]


BOSSES = [

    {
        "name": "고블린 왕",
        "hp": 350,
        "attack": 32,
        "defense": 15,
        "coins": 500,
        "exp": 250
    },

    {
        "name": "죽음의 기사",
        "hp": 550,
        "attack": 45,
        "defense": 25,
        "coins": 800,
        "exp": 400
    },

    {
        "name": "고대 드래곤",
        "hp": 900,
        "attack": 65,
        "defense": 40,
        "coins": 1500,
        "exp": 700
    }
]


SKILLS = {

    "강타": {
        "mana": 15,
        "description": "강력한 물리 공격",
        "type": "damage"
    },

    "화염구": {
        "mana": 20,
        "description": "강력한 마법 공격",
        "type": "damage"
    },

    "대회복": {
        "mana": 25,
        "description": "최대 HP의 35%를 회복",
        "type": "heal"
    },

    "방어 태세": {
        "mana": 15,
        "description": "다음 공격 피해를 50% 감소",
        "type": "defense"
    }
}


# =========================================================
# 안전한 숫자 변환
# =========================================================

def safe_int(value, default=0):

    try:

        if value is None:
            return default

        return int(value)

    except (ValueError, TypeError):

        return default


# =========================================================
# 새 플레이어 생성
# =========================================================

def create_new_player():

    return {

        "name": "용사",

        "level": 1,
        "exp": 0,
        "stat_points": 5,

        "strength": 10,
        "vitality": 10,
        "defense": 5,
        "agility": 5,
        "spirit": 0,

        "hp": 200,

        # 기본 마나 50
        "mana": 50,

        "coins": 200,
        "potions": 3,

        "floor": 1,

        "defending": False,

        "inventory": {

            "weapons": [],

            "armors": [],

            "accessories": []
        },

        "equipment": {

            "weapon": {
                "name": "나무 검",
                "attack": 5,
                "enhance": 0
            },

            "armor": {
                "name": "낡은 옷",
                "defense": 0
            },

            "accessory": {
                "name": "없음",
                "attack": 0,
                "defense": 0,
                "mana": 0
            }
        }
    }


# =========================================================
# 기존 세이브 데이터 보정
# =========================================================

def repair_player_data(player):

    if not isinstance(player, dict):

        return create_new_player()


    # 기본 스탯

    defaults = {

        "name": "용사",

        "level": 1,
        "exp": 0,
        "stat_points": 0,

        "strength": 10,
        "vitality": 10,
        "defense": 5,
        "agility": 5,
        "spirit": 0,

        "hp": 200,

        "mana": 50,

        "coins": 200,
        "potions": 3,

        "floor": 1,

        "defending": False
    }


    for key, value in defaults.items():

        if key not in player or player[key] is None:

            player[key] = value


    # 숫자 데이터 강제 변환

    number_keys = [

        "level",
        "exp",
        "stat_points",

        "strength",
        "vitality",
        "defense",
        "agility",
        "spirit",

        "hp",
        "mana",

        "coins",
        "potions",

        "floor"
    ]


    for key in number_keys:

        player[key] = safe_int(
            player.get(key),
            defaults[key]
        )


    # 마나는 절대 음수가 되지 않도록

    player["mana"] = max(
        0,
        player["mana"]
    )


    # 인벤토리

    if not isinstance(
        player.get("inventory"),
        dict
    ):

        player["inventory"] = {}


    for category in [
        "weapons",
        "armors",
        "accessories"
    ]:

        if not isinstance(
            player["inventory"].get(category),
            list
        ):

            player["inventory"][category] = []


    # 장비

    if not isinstance(
        player.get("equipment"),
        dict
    ):

        player["equipment"] = {}


    if not isinstance(
        player["equipment"].get("weapon"),
        dict
    ):

        player["equipment"]["weapon"] = {

            "name": "나무 검",
            "attack": 5,
            "enhance": 0
        }


    if not isinstance(
        player["equipment"].get("armor"),
        dict
    ):

        player["equipment"]["armor"] = {

            "name": "낡은 옷",
            "defense": 0
        }


    if not isinstance(
        player["equipment"].get("accessory"),
        dict
    ):

        player["equipment"]["accessory"] = {

            "name": "없음",
            "attack": 0,
            "defense": 0,
            "mana": 0
        }


    accessory = player["equipment"]["accessory"]


    if accessory.get("attack") is None:
        accessory["attack"] = 0

    if accessory.get("defense") is None:
        accessory["defense"] = 0

    if accessory.get("mana") is None:
        accessory["mana"] = 0


    accessory["attack"] = safe_int(
        accessory.get("attack"),
        0
    )

    accessory["defense"] = safe_int(
        accessory.get("defense"),
        0
    )

    accessory["mana"] = safe_int(
        accessory.get("mana"),
        0
    )


    weapon = player["equipment"]["weapon"]

    if weapon.get("attack") is None:
        weapon["attack"] = 5

    if weapon.get("enhance") is None:
        weapon["enhance"] = 0


    weapon["attack"] = safe_int(
        weapon.get("attack"),
        5
    )

    weapon["enhance"] = safe_int(
        weapon.get("enhance"),
        0
    )


    armor = player["equipment"]["armor"]

    if armor.get("defense") is None:
        armor["defense"] = 0

    armor["defense"] = safe_int(
        armor.get("defense"),
        0
    )


    return player


# =========================================================
# 게임 초기화
# =========================================================

def init_game():

    if "player" not in st.session_state:

        st.session_state.player = (
            create_new_player()
        )

    else:

        st.session_state.player = (
            repair_player_data(
                st.session_state.player
            )
        )


    if "enemy" not in st.session_state:

        st.session_state.enemy = None


    if "logs" not in st.session_state:

        st.session_state.logs = [
            "🏰 잊혀진 던전에 입장했습니다."
        ]


    if "game_over" not in st.session_state:

        st.session_state.game_over = False


# 게임 초기화 실행

init_game()


# =========================================================
# 스탯 계산
# =========================================================

def get_max_hp():

    player = st.session_state.player

    vitality = safe_int(
        player.get("vitality"),
        10
    )

    return 100 + (
        vitality * 10
    )


def get_max_mana():

    player = st.session_state.player

    spirit = safe_int(
        player.get("spirit"),
        0
    )


    equipment = player.get(
        "equipment",
        {}
    )


    accessory = equipment.get(
        "accessory",
        {}
    )


    if not isinstance(
        accessory,
        dict
    ):

        accessory = {}


    accessory_mana = safe_int(
        accessory.get("mana"),
        0
    )


    # 기본 50
    # 정신력 1당 +5
    # 악세사리 +5~15

    return max(
        50,
        50
        + (spirit * 5)
        + accessory_mana
    )


def get_attack():

    player = st.session_state.player

    weapon = player["equipment"]["weapon"]

    accessory = player["equipment"]["accessory"]


    strength = safe_int(
        player.get("strength"),
        10
    )

    weapon_attack = safe_int(
        weapon.get("attack"),
        5
    )

    enhance = safe_int(
        weapon.get("enhance"),
        0
    )

    accessory_attack = safe_int(
        accessory.get("attack"),
        0
    )


    return (
        strength * 2
        + weapon_attack
        + enhance * 3
        + accessory_attack
    )


def get_defense():

    player = st.session_state.player

    armor = player["equipment"]["armor"]

    accessory = player["equipment"]["accessory"]


    defense = safe_int(
        player.get("defense"),
        5
    )

    armor_defense = safe_int(
        armor.get("defense"),
        0
    )

    accessory_defense = safe_int(
        accessory.get("defense"),
        0
    )


    return (
        defense
        + armor_defense
        + accessory_defense
    )


def get_critical_rate():

    player = st.session_state.player

    agility = safe_int(
        player.get("agility"),
        5
    )

    return min(
        50,
        agility
    )


# =========================================================
# 마나 안전 처리
# =========================================================

def get_mana():

    player = st.session_state.player

    mana = safe_int(
        player.get("mana"),
        50
    )

    return max(
        0,
        mana
    )


def set_mana(value):

    player = st.session_state.player

    max_mana = get_max_mana()

    value = safe_int(
        value,
        0
    )

    player["mana"] = max(
        0,
        min(
            value,
            max_mana
        )
    )


def restore_mana(amount=None):

    if amount is None:

        set_mana(
            get_max_mana()
        )

        return


    set_mana(
        get_mana() + amount
    )


# =========================================================
# 로그
# =========================================================

def add_log(message):

    if "logs" not in st.session_state:

        st.session_state.logs = []


    st.session_state.logs.append(
        message
    )


    if len(
        st.session_state.logs
    ) > 20:

        st.session_state.logs.pop(0)


# =========================================================
# 경험치 / 레벨업
# =========================================================

def gain_exp(amount):

    player = st.session_state.player

    amount = max(
        0,
        safe_int(
            amount,
            0
        )
    )


    player["exp"] += amount


    while True:

        required = (
            player["level"] * 50
        )


        if player["exp"] < required:

            break


        player["exp"] -= required

        player["level"] += 1

        player["stat_points"] += 5


        player["hp"] = get_max_hp()

        restore_mana()


        add_log(
            f"✨ 레벨 업! "
            f"Lv.{player['level']}"
        )

        add_log(
            "📈 스탯 포인트 +5"
        )

        add_log(
            "❤️ HP / 🔵 MP 완전 회복"
        )


# =========================================================
# 일반 몬스터 생성
# =========================================================

def create_normal_enemy():

    player = st.session_state.player

    floor = safe_int(
        player.get("floor"),
        1
    )


    template = random.choice(
        ENEMIES
    )


    enemy = template.copy()


    scale = (
        1
        + ((floor - 1) * 0.12)
    )


    enemy["hp"] = int(
        enemy["hp"] * scale
    )

    enemy["attack"] = int(
        enemy["attack"] * scale
    )

    enemy["defense"] = int(
        enemy["defense"] * scale
    )

    enemy["coins"] = int(
        enemy["coins"]
        * (
            1
            + ((floor - 1) * 0.08)
        )
    )

    enemy["exp"] = int(
        enemy["exp"]
        * (
            1
            + ((floor - 1) * 0.08)
        )
    )


    # 플레이어보다 너무 약해지지 않도록

    enemy["hp"] = max(
        enemy["hp"],
        int(get_max_hp() * 0.70)
    )

    enemy["attack"] = max(
        enemy["attack"],
        int(get_attack() * 0.65)
    )

    enemy["defense"] = max(
        enemy["defense"],
        int(get_defense() * 0.70)
    )


    # 약간의 랜덤성

    enemy["hp"] = int(
        enemy["hp"]
        * random.uniform(
            0.95,
            1.10
        )
    )


    enemy["attack"] = int(
        enemy["attack"]
        * random.uniform(
            0.95,
            1.08
        )
    )


    enemy["max_hp"] = enemy["hp"]

    enemy["is_boss"] = False


    return enemy


# =========================================================
# 보스 생성
# =========================================================

def create_boss():

    player = st.session_state.player

    floor = safe_int(
        player.get("floor"),
        10
    )


    boss_number = (
        floor // 10
    )


    index = min(
        boss_number - 1,
        len(BOSSES) - 1
    )


    template = BOSSES[index]

    boss = template.copy()


    scale = (
        1
        + (
            (boss_number - 1)
            * 0.25
        )
    )


    boss["hp"] = int(
        boss["hp"] * scale
    )

    boss["attack"] = int(
        boss["attack"] * scale
    )

    boss["defense"] = int(
        boss["defense"] * scale
    )

    boss["coins"] = int(
        boss["coins"] * scale
    )

    boss["exp"] = int(
        boss["exp"] * scale
    )


    # 플레이어보다 강하게

    boss["hp"] = max(
        boss["hp"],
        int(get_max_hp() * 2.0)
    )

    boss["attack"] = max(
        boss["attack"],
        int(get_attack() * 1.15)
    )

    boss["defense"] = max(
        boss["defense"],
        int(get_defense() * 1.10)
    )


    boss["max_hp"] = boss["hp"]

    boss["is_boss"] = True


    return boss


# =========================================================
# 적 생성
# =========================================================

def spawn_enemy():

    if st.session_state.enemy is not None:

        return


    floor = safe_int(
        st.session_state.player.get(
            "floor"
        ),
        1
    )


    if floor % 10 == 0:

        enemy = create_boss()

        st.session_state.enemy = enemy


        add_log(
            "🚨🚨🚨 BOSS 등장! 🚨🚨🚨"
        )

        add_log(
            f"👑 {enemy['name']}"
        )


    else:

        enemy = create_normal_enemy()

        st.session_state.enemy = enemy


        add_log(
            f"👹 {enemy['name']} 등장!"
        )


# =========================================================
# 스탯 증가
# =========================================================

def increase_stat(stat_name):

    player = st.session_state.player


    if player["stat_points"] <= 0:

        add_log(
            "❌ 스탯 포인트가 없습니다."
        )

        return


    player["stat_points"] -= 1

    player[stat_name] += 1


    if stat_name == "vitality":

        player["hp"] = min(
            get_max_hp(),
            player["hp"] + 10
        )


    if stat_name == "spirit":

        restore_mana(5)


    add_log(
        f"📈 {stat_name} +1"
    )


# =========================================================
# 적 공격
# =========================================================

def enemy_attack():

    player = st.session_state.player

    enemy = st.session_state.enemy


    if enemy is None:

        return


    # 회피

    agility = safe_int(
        player.get("agility"),
        5
    )


    dodge_chance = min(
        30,
        agility * 0.5
    )


    if (
        random.random() * 100
        < dodge_chance
    ):

        add_log(
            "💨 공격을 회피했습니다!"
        )

        return


    raw_damage = random.randint(
        max(
            1,
            enemy["attack"] - 4
        ),
        enemy["attack"] + 4
    )


    damage = max(
        1,
        raw_damage - get_defense()
    )


    # 방어 태세

    if player["defending"]:

        damage = max(
            1,
            damage // 2
        )

        player["defending"] = False

        add_log(
            "🛡️ 방어 태세 발동!"
        )


    player["hp"] -= damage


    add_log(
        f"💥 {enemy['name']}의 공격!"
    )

    add_log(
        f"❤️ HP -{damage}"
    )


    if player["hp"] <= 0:

        player["hp"] = 0

        st.session_state.game_over = True

        add_log(
            "☠️ 당신은 쓰러졌습니다."
        )


# =========================================================
# 일반 공격
# =========================================================

def attack():

    enemy = st.session_state.enemy


    if enemy is None:

        return


    damage = random.randint(
        max(
            1,
            get_attack() - 5
        ),
        get_attack() + 5
    )


    # 치명타

    if (
        random.random() * 100
        < get_critical_rate()
    ):

        damage *= 2

        add_log(
            "💥 치명타!"
        )


    damage = max(
        1,
        damage - enemy["defense"]
    )


    enemy["hp"] -= damage


    add_log(
        f"⚔️ {enemy['name']}에게 "
        f"{damage} 피해!"
    )


    if enemy["hp"] <= 0:

        defeat_enemy()

        return


    enemy_attack()


# =========================================================
# 몬스터 처치
# =========================================================

def defeat_enemy():

    player = st.session_state.player

    enemy = st.session_state.enemy


    if enemy is None:

        return


    coins = safe_int(
        enemy.get("coins"),
        0
    )

    exp = safe_int(
        enemy.get("exp"),
        0
    )


    player["coins"] += coins


    gain_exp(exp)


    add_log(
        f"💀 {enemy['name']} 처치!"
    )

    add_log(
        f"🪙 코인 +{coins}"
    )

    add_log(
        f"⭐ EXP +{exp}"
    )


    # 보스

    if enemy.get("is_boss", False):

        bonus = random.randint(
            200,
            500
        )


        player["coins"] += bonus


        add_log(
            f"👑 보스 처치 보너스!"
        )

        add_log(
            f"🪙 추가 코인 +{bonus}"
        )


        player["hp"] = get_max_hp()

        restore_mana()


        add_log(
            "❤️ HP / 🔵 MP 완전 회복!"
        )


    # 일반 몬스터

    else:

        if random.random() < 0.25:

            bonus = random.randint(
                20,
                80
            )

            player["coins"] += bonus

            add_log(
                f"🎁 보너스 코인 +{bonus}"
            )


    # 다음 층

    player["floor"] += 1


    add_log(
        f"🚪 {player['floor']}층으로 이동!"
    )


    st.session_state.enemy = None


# =========================================================
# 스킬 사용
# =========================================================

def use_skill(skill_name):

    player = st.session_state.player

    enemy = st.session_state.enemy


    if enemy is None:

        add_log(
            "❌ 전투 중에만 스킬을 사용할 수 있습니다."
        )

        return


    if skill_name not in SKILLS:

        return


    skill = SKILLS[skill_name]

    mana_cost = safe_int(
        skill.get("mana"),
        0
    )


    current_mana = get_mana()


    # 마나 부족

    if current_mana < mana_cost:

        add_log(
            "🔵 마나가 부족합니다!"
        )

        add_log(
            f"필요 MP: {mana_cost}"
        )

        return


    # 마나 차감

    set_mana(
        current_mana - mana_cost
    )


    # =====================================================
    # 강타
    # =====================================================

    if skill_name == "강타":

        damage = int(
            get_attack() * 1.7
        )


        damage = max(
            1,
            damage - enemy["defense"]
        )


        enemy["hp"] -= damage


        add_log(
            "⚔️ 강타!"
        )

        add_log(
            f"💥 {damage} 피해!"
        )


    # =====================================================
    # 화염구
    # =====================================================

    elif skill_name == "화염구":

        damage = int(
            get_attack() * 2.0
        )


        damage = max(
            1,
            damage
            - (
                enemy["defense"] // 2
            )
        )


        enemy["hp"] -= damage


        add_log(
            "🔥 화염구!"
        )

        add_log(
            f"💥 {damage} 마법 피해!"
        )


    # =====================================================
    # 대회복
    # =====================================================

    elif skill_name == "대회복":

        heal = int(
            get_max_hp() * 0.35
        )


        old_hp = player["hp"]


        player["hp"] = min(
            get_max_hp(),
            player["hp"] + heal
        )


        actual_heal = (
            player["hp"] - old_hp
        )


        add_log(
            "💚 대회복!"
        )

        add_log(
            f"❤️ HP +{actual_heal}"
        )


    # =====================================================
    # 방어 태세
    # =====================================================

    elif skill_name == "방어 태세":

        player["defending"] = True


        add_log(
            "🛡️ 방어 태세!"
        )

        add_log(
            "다음 공격 피해 50% 감소"
        )


    # 적 처치

    if enemy["hp"] <= 0:

        defeat_enemy()

        return


    # 적 반격

    enemy_attack()


# =========================================================
# 포션 사용
# =========================================================

def use_potion():

    player = st.session_state.player


    if player["potions"] <= 0:

        add_log(
            "❌ 포션이 없습니다."
        )

        return


    if player["hp"] >= get_max_hp():

        add_log(
            "❤️ HP가 이미 가득합니다."
        )

        return


    heal = 30


    player["hp"] = min(
        get_max_hp(),
        player["hp"] + heal
    )


    player["potions"] -= 1


    add_log(
        f"🧪 포션 사용! "
        f"❤️ HP +{heal}"
    )


    if st.session_state.enemy:

        enemy_attack()


# =========================================================
# 휴식
# =========================================================

def rest():

    player = st.session_state.player


    hp_heal = 15

    mp_heal = 10


    player["hp"] = min(
        get_max_hp(),
        player["hp"] + hp_heal
    )


    restore_mana(
        mp_heal
    )


    add_log(
        "🔥 휴식했습니다."
    )

    add_log(
        f"❤️ HP +{hp_heal}"
    )

    add_log(
        f"🔵 MP +{mp_heal}"
    )


    if st.session_state.enemy:

        enemy_attack()


# =========================================================
# 아이템 구매
# =========================================================

def buy_item(category, item):

    player = st.session_state.player


    price = safe_int(
        item.get("price"),
        0
    )


    if player["coins"] < price:

        add_log(
            "❌ 코인이 부족합니다."
        )

        return


    player["coins"] -= price


    if category == "potions":

        player["potions"] += 1

        add_log(
            f"🧪 {item['name']} 구매!"
        )

        return


    player["inventory"][
        category
    ].append(
        item.copy()
    )


    add_log(
        f"🛒 {item['name']} 구매!"
    )


# =========================================================
# 장비 장착
# =========================================================

def equip_item(
    category,
    index
):

    player = st.session_state.player


    inventory = player[
        "inventory"
    ][category]


    if index < 0 or index >= len(
        inventory
    ):

        return


    item = inventory[index].copy()


    if category == "weapons":

        player["equipment"][
            "weapon"
        ] = item


        add_log(
            f"⚔️ {item['name']} 장착!"
        )


    elif category == "armors":

        player["equipment"][
            "armor"
        ] = item


        add_log(
            f"🛡️ {item['name']} 장착!"
        )


    elif category == "accessories":

        player["equipment"][
            "accessory"
        ] = item


        # 악세사리 교체 후
        # 현재 MP가 최대치를 넘지 않게 조정

        set_mana(
            get_mana()
        )


        add_log(
            f"💍 {item['name']} 장착!"
        )


# =========================================================
# 무기 강화
# =========================================================

def enhancement_cost(level):

    return 100 + (
        level * 100
    )


def enhancement_success_rate(level):

    return max(
        30,
        100 - (
            level * 8
        )
    )


def enhance_weapon():

    player = st.session_state.player

    weapon = player[
        "equipment"
    ]["weapon"]


    level = safe_int(
        weapon.get("enhance"),
        0
    )


    cost = enhancement_cost(
        level
    )


    success_rate = enhancement_success_rate(
        level
    )


    if player["coins"] < cost:

        add_log(
            "❌ 강화 코인이 부족합니다."
        )

        return


    player["coins"] -= cost


    roll = random.randint(
        1,
        100
    )


    if roll <= success_rate:

        weapon["enhance"] = (
            level + 1
        )


        add_log(
            "🔨 강화 성공!"
        )

        add_log(
            f"⚔️ {weapon['name']} "
            f"+{weapon['enhance']}"
        )


    else:

        add_log(
            "💥 강화 실패!"
        )


        if level >= 3:

            weapon["enhance"] = (
                level - 1
            )


            add_log(
                f"📉 강화 단계 하락!"
            )


# =========================================================
# 게임 초기화
# =========================================================

def reset_game():

    for key in list(
        st.session_state.keys()
    ):

        del st.session_state[key]


    init_game()


# =========================================================
# 화면 시작
# =========================================================

player = st.session_state.player

enemy = st.session_state.enemy


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    st.header("⚙️ 게임 관리")


    st.write(
        f"🏰 현재 층: "
        f"**{player['floor']}**"
    )

    st.write(
        f"🪙 코인: "
        f"**{player['coins']}**"
    )


    st.divider()


    if st.button(
        "🗑️ 게임 데이터 초기화",
        use_container_width=True
    ):

        reset_game()

        st.rerun()


# =========================================================
# 제목
# =========================================================

st.title("⚔️ 잊혀진 던전")

st.caption(
    "RPG · 던전 · 보스 · 스킬 · 장비 · 강화"
)


# =========================================================
# 상단 상태
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "레벨",
        player["level"]
    )


with col2:

    st.metric(
        "🪙 코인",
        player["coins"]
    )


with col3:

    st.metric(
        "⚔️ 공격",
        get_attack()
    )


with col4:

    st.metric(
        "🛡️ 방어",
        get_defense()
    )


# =========================================================
# HP
# =========================================================

st.write(
    f"❤️ HP "
    f"**{player['hp']} / {get_max_hp()}**"
)


st.progress(
    max(
        0.0,
        min(
            1.0,
            player["hp"]
            / get_max_hp()
        )
    )
)


# =========================================================
# MP
# =========================================================

current_mana = get_mana()

max_mana = get_max_mana()


st.write(
    f"🔵 MP "
    f"**{current_mana} / {max_mana}**"
)


st.progress(
    max(
        0.0,
        min(
            1.0,
            current_mana
            / max_mana
        )
    )
)


# =========================================================
# EXP
# =========================================================

required_exp = (
    player["level"] * 50
)


st.write(
    f"⭐ EXP "
    f"**{player['exp']} / {required_exp}**"
)


st.progress(
    max(
        0.0,
        min(
            1.0,
            player["exp"]
            / required_exp
        )
    )
)


st.write(
    f"🏰 던전 "
    f"**{player['floor']}층**"
)


# =========================================================
# 탭
# =========================================================

tab_game, tab_stats, tab_skills, tab_shop, tab_inventory, tab_upgrade = st.tabs(
    [
        "⚔️ 던전",
        "📊 스탯",
        "🔥 스킬",
        "🏪 상점",
        "🎒 장비",
        "🔨 강화"
    ]
)


# =========================================================
# 던전
# =========================================================

with tab_game:

    st.subheader("🏰 던전")


    if (
        player["floor"] % 10 == 0
        and enemy is None
    ):

        st.warning(
            f"🚨 {player['floor']}층은 "
            f"보스층입니다!"
        )


    if enemy is not None:

        if enemy.get(
            "is_boss",
            False
        ):

            st.error(
                f"👑 BOSS "
                f"{enemy['name']}"
            )

        else:

            st.subheader(
                f"👹 {enemy['name']}"
            )


        st.write(
            f"❤️ HP "
            f"**{enemy['hp']} / "
            f"{enemy['max_hp']}**"
        )


        st.progress(
            max(
                0.0,
                min(
                    1.0,
                    enemy["hp"]
                    / enemy["max_hp"]
                )
            )
        )


        st.write(
            f"⚔️ 공격력: "
            f"**{enemy['attack']}**"
        )


        st.write(
            f"🛡️ 방어력: "
            f"**{enemy['defense']}**"
        )


        if enemy.get(
            "is_boss",
            False
        ):

            st.write(
                f"👑 보상 "
                f"🪙 {enemy['coins']} / "
                f"⭐ {enemy['exp']}"
            )


    else:

        st.info(
            "현재 전투 중인 적이 없습니다."
        )


    # =====================================================
    # 게임 오버
    # =====================================================

    if st.session_state.game_over:

        st.error(
            "☠️ GAME OVER"
        )


        st.write(
            f"도달 층: "
            f"**{player['floor']}층**"
        )


        st.write(
            f"레벨: "
            f"**{player['level']}**"
        )


        if st.button(
            "🔄 다시 시작",
            use_container_width=True
        ):

            reset_game()

            st.rerun()


    else:

        # =================================================
        # 탐험
        # =================================================

        if enemy is None:

            if st.button(
                "🚪 다음 방 탐험",
                use_container_width=True
            ):

                spawn_enemy()

                st.rerun()


        # =================================================
        # 전투
        # =================================================

        else:

            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "⚔️ 일반 공격",
                    use_container_width=True
                ):

                    attack()

                    st.rerun()


            with col2:

                if st.button(
                    "🧪 포션",
                    use_container_width=True
                ):

                    use_potion()

                    st.rerun()


            if st.button(
                "🔥 휴식",
                use_container_width=True
            ):

                rest()

                st.rerun()


            st.markdown(
                "### 🔥 스킬"
            )


            skill_cols = st.columns(2)


            for index, skill_name in enumerate(
                SKILLS
            ):

                skill = SKILLS[
                    skill_name
                ]


                with skill_cols[
                    index % 2
                ]:

                    if st.button(
                        f"{skill_name} "
                        f"({skill['mana']} MP)",
                        key=(
                            "battle_skill_"
                            + skill_name
                        ),
                        use_container_width=True
                    ):

                        use_skill(
                            skill_name
                        )

                        st.rerun()


# =========================================================
# 스탯
# =========================================================

with tab_stats:

    st.subheader(
        "📊 캐릭터 스탯"
    )


    st.info(
        f"사용 가능한 스탯 포인트: "
        f"**{player['stat_points']}**"
    )


    # 힘

    st.markdown(
        "### 💪 힘"
    )

    st.write(
        f"현재: **{player['strength']}**"
    )

    st.caption(
        "힘 1 → 공격력 +2"
    )


    if st.button(
        "힘 +1",
        key="stat_strength",
        use_container_width=True
    ):

        increase_stat(
            "strength"
        )

        st.rerun()


    # 체력

    st.markdown(
        "### ❤️ 체력"
    )

    st.write(
        f"현재: **{player['vitality']}**"
    )

    st.caption(
        "체력 1 → 최대 HP +10"
    )


    if st.button(
        "체력 +1",
        key="stat_vitality",
        use_container_width=True
    ):

        increase_stat(
            "vitality"
        )

        st.rerun()


    # 방어

    st.markdown(
        "### 🛡️ 방어"
    )

    st.write(
        f"현재: **{player['defense']}**"
    )

    st.caption(
        "방어 1 → 받는 피해 감소"
    )


    if st.button(
        "방어 +1",
        key="stat_defense",
        use_container_width=True
    ):

        increase_stat(
            "defense"
        )

        st.rerun()


    # 민첩

    st.markdown(
        "### 💨 민첩"
    )

    st.write(
        f"현재: **{player['agility']}**"
    )

    st.caption(
        "민첩 1 → 치명타 +1%"
    )


    if st.button(
        "민첩 +1",
        key="stat_agility",
        use_container_width=True
    ):

        increase_stat(
            "agility"
        )

        st.rerun()


    # 정신력

    st.markdown(
        "### 🧠 정신력"
    )

    st.write(
        f"현재: **{player['spirit']}**"
    )

    st.caption(
        "정신력 1 → 최대 MP +5"
    )


    if st.button(
        "정신력 +1",
        key="stat_spirit",
        use_container_width=True
    ):

        increase_stat(
            "spirit"
        )

        st.rerun()


    st.divider()


    st.markdown(
        "### 📋 최종 능력치"
    )


    st.write(
        f"⚔️ 공격력: "
        f"**{get_attack()}**"
    )


    st.write(
        f"🛡️ 방어력: "
        f"**{get_defense()}**"
    )


    st.write(
        f"❤️ 최대 HP: "
        f"**{get_max_hp()}**"
    )


    st.write(
        f"🔵 최대 MP: "
        f"**{get_max_mana()}**"
    )


    st.write(
        f"💥 치명타: "
        f"**{get_critical_rate()}%**"
    )


    st.write(
        f"💨 회피: "
        f"**{min(30, player['agility'] * 0.5):.1f}%**"
    )


# =========================================================
# 스킬
# =========================================================

with tab_skills:

    st.subheader(
        "🔥 스킬"
    )


    st.write(
        f"현재 MP: "
        f"**{get_mana()} / {get_max_mana()}**"
    )


    for skill_name, skill in SKILLS.items():

        st.markdown(
            f"### {skill_name}"
        )


        st.write(
            f"🔵 MP 소비: "
            f"**{skill['mana']}**"
        )


        st.write(
            skill["description"]
        )


        if skill_name == "강타":

            st.write(
                "⚔️ 공격력의 170% 피해"
            )


        elif skill_name == "화염구":

            st.write(
                "🔥 공격력의 200% 피해"
            )


        elif skill_name == "대회복":

            st.write(
                "💚 최대 HP의 35% 회복"
            )


        elif skill_name == "방어 태세":

            st.write(
                "🛡️ 다음 공격 피해 50% 감소"
            )


        st.divider()


# =========================================================
# 상점
# =========================================================

with tab_shop:

    st.subheader(
        "🏪 던전 상점"
    )


    st.write(
        f"🪙 보유 코인: "
        f"**{player['coins']}**"
    )


    # 무기

    st.markdown(
        "### ⚔️ 무기"
    )


    for i, item in enumerate(
        SHOP_ITEMS["weapons"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"**{item['name']}** "
                f"| 공격 +{item['attack']} "
                f"| 🪙 {item['price']}"
            )


        with col2:

            if st.button(
                "구매",
                key=f"buy_weapon_{i}"
            ):

                buy_item(
                    "weapons",
                    item
                )

                st.rerun()


    # 갑옷

    st.markdown(
        "### 🛡️ 갑옷"
    )


    for i, item in enumerate(
        SHOP_ITEMS["armors"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"**{item['name']}** "
                f"| 방어 +{item['defense']} "
                f"| 🪙 {item['price']}"
            )


        with col2:

            if st.button(
                "구매",
                key=f"buy_armor_{i}"
            ):

                buy_item(
                    "armors",
                    item
                )

                st.rerun()


    # 악세사리

    st.markdown(
        "### 💍 악세사리"
    )


    for i, item in enumerate(
        SHOP_ITEMS["accessories"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"**{item['name']}** "
                f"| ⚔️ +{item.get('attack', 0)} "
                f"| 🛡️ +{item.get('defense', 0)} "
                f"| 🔵 MP +{item.get('mana', 0)} "
                f"| 🪙 {item['price']}"
            )


        with col2:

            if st.button(
                "구매",
                key=f"buy_accessory_{i}"
            ):

                buy_item(
                    "accessories",
                    item
                )

                st.rerun()


    # 포션

    st.markdown(
        "### 🧪 포션"
    )


    for i, item in enumerate(
        SHOP_ITEMS["potions"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"**{item['name']}** "
                f"| HP +{item['heal']} "
                f"| 🪙 {item['price']}"
            )


        with col2:

            if st.button(
                "구매",
                key=f"buy_potion_{i}"
            ):

                buy_item(
                    "potions",
                    item
                )

                st.rerun()


# =========================================================
# 장비
# =========================================================

with tab_inventory:

    st.subheader(
        "🎒 장비"
    )


    weapon = player[
        "equipment"
    ]["weapon"]


    armor = player[
        "equipment"
    ]["armor"]


    accessory = player[
        "equipment"
    ]["accessory"]


    st.markdown(
        "### 현재 장비"
    )


    st.write(
        f"⚔️ 무기: "
        f"**{weapon['name']} "
        f"+{weapon['enhance']}**"
    )


    st.write(
        f"🛡️ 갑옷: "
        f"**{armor['name']}**"
    )


    st.write(
        f"💍 악세사리: "
        f"**{accessory['name']}**"
    )


    st.write(
        f"🔵 악세사리 MP: "
        f"**+{accessory.get('mana', 0)}**"
    )


    st.divider()


    # 무기

    st.markdown(
        "### ⚔️ 보유 무기"
    )


    if not player[
        "inventory"
    ]["weapons"]:

        st.info(
            "보유한 무기가 없습니다."
        )


    for i, item in enumerate(
        player["inventory"]["weapons"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"{item['name']} "
                f"| 공격 +{item['attack']}"
            )


        with col2:

            if st.button(
                "장착",
                key=f"equip_weapon_{i}"
            ):

                equip_item(
                    "weapons",
                    i
                )

                st.rerun()


    # 갑옷

    st.markdown(
        "### 🛡️ 보유 갑옷"
    )


    if not player[
        "inventory"
    ]["armors"]:

        st.info(
            "보유한 갑옷이 없습니다."
        )


    for i, item in enumerate(
        player["inventory"]["armors"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"{item['name']} "
                f"| 방어 +{item['defense']}"
            )


        with col2:

            if st.button(
                "장착",
                key=f"equip_armor_{i}"
            ):

                equip_item(
                    "armors",
                    i
                )

                st.rerun()


    # 악세사리

    st.markdown(
        "### 💍 보유 악세사리"
    )


    if not player[
        "inventory"
    ]["accessories"]:

        st.info(
            "보유한 악세사리가 없습니다."
        )


    for i, item in enumerate(
        player["inventory"]["accessories"]
    ):

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            st.write(
                f"{item['name']} "
                f"| ⚔️ +{item.get('attack', 0)} "
                f"| 🛡️ +{item.get('defense', 0)} "
                f"| 🔵 MP +{item.get('mana', 0)}"
            )


        with col2:

            if st.button(
                "장착",
                key=f"equip_accessory_{i}"
            ):

                equip_item(
                    "accessories",
                    i
                )

                st.rerun()


    st.divider()


    st.write(
        f"🧪 포션: "
        f"**{player['potions']}개**"
    )


# =========================================================
# 강화
# =========================================================

with tab_upgrade:

    st.subheader(
        "🔨 무기 강화"
    )


    weapon = player[
        "equipment"
    ]["weapon"]


    level = safe_int(
        weapon.get("enhance"),
        0
    )


    cost = enhancement_cost(
        level
    )


    success_rate = enhancement_success_rate(
        level
    )


    st.write(
        f"현재 무기: "
        f"**{weapon['name']} +{level}**"
    )


    st.write(
        f"기본 공격력: "
        f"**{weapon['attack']}**"
    )


    st.write(
        f"강화 공격력 보너스: "
        f"**+{level * 3}**"
    )


    st.divider()


    st.write(
        f"🪙 강화 비용: "
        f"**{cost} 코인**"
    )


    st.write(
        f"🎯 성공 확률: "
        f"**{success_rate}%**"
    )


    if st.button(
        f"🔨 +{level + 1} 강화",
        use_container_width=True
    ):

        enhance_weapon()

        st.rerun()


    st.info(
        "강화 단계가 높아질수록 성공 확률이 감소합니다. "
        "+3 이상에서 강화 실패 시 단계가 내려갈 수 있습니다."
    )


# =========================================================
# 로그
# =========================================================

st.divider()

st.subheader(
    "📜 모험 기록"
)


for log in reversed(
    st.session_state.logs
):

    st.write(log)
