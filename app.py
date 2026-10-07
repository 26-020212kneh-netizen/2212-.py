import random
import streamlit as st


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="잊혀진 던전",
    page_icon="⚔️",
    layout="centered"
)


# =========================================================
# 상점 아이템
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


# =========================================================
# 일반 몬스터
# =========================================================

ENEMIES = [

    {
        "name": "슬라임",
        "hp": 30,
        "attack": 7,
        "defense": 2,
        "coins": 20,
        "exp": 15
    },

    {
        "name": "고블린",
        "hp": 45,
        "attack": 10,
        "defense": 4,
        "coins": 35,
        "exp": 25
    },

    {
        "name": "해골 전사",
        "hp": 70,
        "attack": 14,
        "defense": 7,
        "coins": 55,
        "exp": 40
    },

    {
        "name": "오크",
        "hp": 100,
        "attack": 20,
        "defense": 10,
        "coins": 90,
        "exp": 60
    }
]


# =========================================================
# 보스
# =========================================================

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


# =========================================================
# 스킬
# =========================================================

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
        "description": "HP를 크게 회복",
        "type": "heal"
    },

    "방어 태세": {
        "mana": 15,
        "description": "다음 공격의 피해를 크게 감소",
        "type": "defense"
    }
}


# =========================================================
# 강화
# =========================================================

def enhancement_cost(level):

    return 100 + (level * 100)


def enhancement_success_rate(level):

    return max(
        30,
        100 - (level * 8)
    )


# =========================================================
# 게임 초기화
# =========================================================

def init_game():

    if "player" not in st.session_state:

        st.session_state.player = {

            "name": "용사",

            # 레벨
            "level": 1,
            "exp": 0,

            # 스탯 포인트
            "stat_points": 5,

            # 스탯
            "strength": 10,
            "vitality": 10,
            "defense": 5,
            "agility": 5,

            # 정신력
            "spirit": 0,

            # HP
            "hp": 200,

            # 경제
            "coins": 200,
            "potions": 3,

            # 던전
            "floor": 1,

            # 전투 상태
            "defending": False,

            # 인벤토리
            "inventory": {
                "weapons": [],
                "armors": [],
                "accessories": []
            },

            # 장비
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

    if "enemy" not in st.session_state:
        st.session_state.enemy = None

    if "logs" not in st.session_state:

        st.session_state.logs = [
            "🏰 잊혀진 던전에 입장했습니다."
        ]

    if "game_over" not in st.session_state:
        st.session_state.game_over = False


init_game()


# =========================================================
# 최대 HP
# =========================================================

def get_max_hp():

    player = st.session_state.player

    return 100 + (
        player["vitality"] * 10
    )


# =========================================================
# 최대 마나
# =========================================================

def get_max_mana():

    player = st.session_state.player

    accessory = player["equipment"]["accessory"]

    accessory_mana = accessory.get(
        "mana",
        0
    )

    # 기본 마나 50
    # 정신력 1당 +5
    # 악세사리 +5~15
    return (
        50
        + player["spirit"] * 5
        + accessory_mana
    )


# =========================================================
# 공격력
# =========================================================

def get_attack():

    player = st.session_state.player

    weapon = player["equipment"]["weapon"]

    accessory = player["equipment"]["accessory"]

    strength_attack = (
        player["strength"] * 2
    )

    weapon_attack = weapon["attack"]

    enhance_attack = (
        weapon["enhance"] * 3
    )

    accessory_attack = accessory.get(
        "attack",
        0
    )

    return (
        strength_attack
        + weapon_attack
        + enhance_attack
        + accessory_attack
    )


# =========================================================
# 방어력
# =========================================================

def get_defense():

    player = st.session_state.player

    armor = player["equipment"]["armor"]

    accessory = player["equipment"]["accessory"]

    return (
        player["defense"]
        + armor.get("defense", 0)
        + accessory.get("defense", 0)
    )


# =========================================================
# 치명타
# =========================================================

def get_critical_rate():

    player = st.session_state.player

    return min(
        50,
        player["agility"]
    )


# =========================================================
# 로그
# =========================================================

def add_log(message):

    st.session_state.logs.append(
        message
    )

    if len(st.session_state.logs) > 18:

        st.session_state.logs.pop(0)


# =========================================================
# 경험치
# =========================================================

def gain_exp(amount):

    player = st.session_state.player

    player["exp"] += amount

    required = (
        player["level"] * 50
    )

    while player["exp"] >= required:

        player["exp"] -= required

        player["level"] += 1

        # 레벨업 스탯 포인트
        player["stat_points"] += 5

        # 레벨업 HP 보너스
        player["hp"] = get_max_hp()

        # 마나 완전 회복
        player["mana"] = get_max_mana()

        add_log(
            f"✨ 레벨 업! "
            f"Lv.{player['level']}"
        )

        add_log(
            "📈 스탯 포인트 5 획득!"
        )

        add_log(
            "🔵 마나가 모두 회복되었습니다!"
        )

        required = (
            player["level"] * 50
        )


# =========================================================
# 일반 몬스터 생성
# =========================================================

def create_normal_enemy():

    template = random.choice(
        ENEMIES
    )

    floor = st.session_state.player[
        "floor"
    ]

    player_hp = get_max_hp()

    player_attack = get_attack()

    player_defense = get_defense()

    enemy = template.copy()

    # 층마다 기본적으로 12% 증가
    floor_scale = (
        1 + ((floor - 1) * 0.12)
    )

    enemy["hp"] = int(
        enemy["hp"] * floor_scale
    )

    enemy["attack"] = int(
        enemy["attack"] * floor_scale
    )

    enemy["defense"] = int(
        enemy["defense"] * floor_scale
    )

    enemy["coins"] = int(
        enemy["coins"]
        * (1 + (floor - 1) * 0.08)
    )

    enemy["exp"] = int(
        enemy["exp"]
        * (1 + (floor - 1) * 0.08)
    )

    # 플레이어 기준 최소 능력치
    enemy["hp"] = max(
        enemy["hp"],
        int(player_hp * 0.75)
    )

    enemy["attack"] = max(
        enemy["attack"],
        int(player_attack * 0.70)
    )

    enemy["defense"] = max(
        enemy["defense"],
        int(player_defense * 0.75)
    )

    # 약간의 랜덤성
    enemy["hp"] = int(
        enemy["hp"]
        * random.uniform(0.95, 1.10)
    )

    enemy["attack"] = int(
        enemy["attack"]
        * random.uniform(0.95, 1.08)
    )

    enemy["max_hp"] = enemy["hp"]

    enemy["is_boss"] = False

    return enemy


# =========================================================
# 보스 생성
# =========================================================

def create_boss():

    floor = st.session_state.player[
        "floor"
    ]

    player_hp = get_max_hp()

    player_attack = get_attack()

    player_defense = get_defense()

    # 10층 -> 첫 번째 보스
    boss_index = (
        (floor // 10) - 1
    )

    boss_index = min(
        boss_index,
        len(BOSSES) - 1
    )

    template = BOSSES[
        boss_index
    ]

    boss = template.copy()

    # 10층마다 강력하게 증가
    boss_scale = (
        1 + ((floor // 10 - 1) * 0.25)
    )

    boss["hp"] = int(
        boss["hp"] * boss_scale
    )

    boss["attack"] = int(
        boss["attack"] * boss_scale
    )

    boss["defense"] = int(
        boss["defense"] * boss_scale
    )

    boss["coins"] = int(
        boss["coins"] * boss_scale
    )

    boss["exp"] = int(
        boss["exp"] * boss_scale
    )

    # 플레이어보다 충분히 강하게
    boss["hp"] = max(
        boss["hp"],
        int(player_hp * 2.0)
    )

    boss["attack"] = max(
        boss["attack"],
        int(player_attack * 1.15)
    )

    boss["defense"] = max(
        boss["defense"],
        int(player_defense * 1.10)
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

    floor = st.session_state.player[
        "floor"
    ]

    # 10의 배수 층이면 보스
    if floor % 10 == 0:

        enemy = create_boss()

        st.session_state.enemy = enemy

        add_log(
            "🚨🚨🚨 BOSS 등장! 🚨🚨🚨"
        )

        add_log(
            f"👑 {enemy['name']}"
        )

        add_log(
            f"❤️ HP {enemy['hp']}"
        )

        add_log(
            f"⚔️ 공격 {enemy['attack']}"
        )

    else:

        enemy = create_normal_enemy()

        st.session_state.enemy = enemy

        add_log(
            f"👹 {enemy['name']} 등장!"
        )


# =========================================================
# 스탯 포인트
# =========================================================

def increase_stat(stat_name):

    player = st.session_state.player

    if player["stat_points"] <= 0:

        add_log(
            "❌ 사용할 스탯 포인트가 없습니다."
        )

        return

    player["stat_points"] -= 1

    player[stat_name] += 1

    if stat_name == "vitality":

        old_hp = player["hp"]

        player["hp"] = min(
            get_max_hp(),
            old_hp + 10
        )

    if stat_name == "spirit":

        # 정신력 상승 시 마나 증가
        player["mana"] = min(
            get_max_mana(),
            player["mana"] + 5
        )

    add_log(
        f"📈 {stat_name} +1"
    )


# =========================================================
# 적 공격
# =========================================================

def enemy_attack():

    player = st.session_state.player

    enemy = st.session_state.enemy

    # 회피
    dodge_chance = min(
        30,
        player["agility"] * 0.5
    )

    if random.random() * 100 < dodge_chance:

        add_log(
            f"💨 공격 회피!"
        )

        return

    raw_damage = random.randint(
        max(
            1,
            enemy["attack"] - 4
        ),
        enemy["attack"] + 4
    )

    defense = get_defense()

    damage = max(
        1,
        raw_damage - defense
    )

    # 방어 태세
    if player["defending"]:

        damage = max(
            1,
            damage // 2
        )

        player["defending"] = False

        add_log(
            "🛡️ 방어 태세로 피해 감소!"
        )

    player["hp"] -= damage

    add_log(
        f"💥 {enemy['name']}의 공격!"
    )

    add_log(
        f"🛡️ {damage} 피해"
    )

    if player["hp"] <= 0:

        player["hp"] = 0

        st.session_state.game_over = True

        add_log(
            "☠️ 당신은 던전에서 쓰러졌습니다."
        )


# =========================================================
# 일반 공격
# =========================================================

def attack():

    player = st.session_state.player

    enemy = st.session_state.enemy

    if enemy is None:

        spawn_enemy()

        return

    attack_power = get_attack()

    damage = random.randint(
        max(
            1,
            attack_power - 5
        ),
        attack_power + 5
    )

    # 치명타
    critical_rate = get_critical_rate()

    if (
        random.random() * 100
        < critical_rate
    ):

        damage *= 2

        add_log(
            f"💥 치명타!"
        )

    # 적 방어
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

    coins = enemy["coins"]

    exp = enemy["exp"]

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

    # 보스 보상
    if enemy["is_boss"]:

        boss_bonus = random.randint(
            200,
            500
        )

        player["coins"] += boss_bonus

        add_log(
            f"👑 보스 처치 보너스!"
        )

        add_log(
            f"🪙 추가 코인 +{boss_bonus}"
        )

        # 보스 처치 시 마나/HP 완전 회복
        player["hp"] = get_max_hp()

        player["mana"] = get_max_mana()

        add_log(
            "❤️ HP와 🔵 MP가 모두 회복되었습니다!"
        )

    else:

        # 일반 몬스터 보너스
        if random.random() < 0.25:

            bonus = random.randint(
                20,
                80
            )

            player["coins"] += bonus

            add_log(
                f"🎁 보너스 코인 +{bonus}!"
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

    skill = SKILLS[skill_name]

    mana_cost = skill["mana"]

    # 마나 부족
    if player["mana"] < mana_cost:

        add_log(
            f"🔵 마나가 부족합니다!"
        )

        add_log(
            f"필요 마나: {mana_cost}"
        )

        return

    # 전투 중이 아닌 경우
    if enemy is None:

        add_log(
            "❌ 전투 중에만 사용할 수 있습니다."
        )

        return

    # 마나 차감
    player["mana"] -= mana_cost

    # -----------------------------------------------------
    # 강타
    # -----------------------------------------------------

    if skill_name == "강타":

        attack_power = get_attack()

        damage = int(
            attack_power * 1.7
        )

        damage = max(
            1,
            damage - enemy["defense"]
        )

        enemy["hp"] -= damage

        add_log(
            f"⚔️ 강타!"
        )

        add_log(
            f"💥 {damage} 피해!"
        )

    # -----------------------------------------------------
    # 화염구
    # -----------------------------------------------------

    elif skill_name == "화염구":

        attack_power = get_attack()

        damage = int(
            attack_power * 2.0
        )

        # 화염구는 방어력 무시 50%
        damage = max(
            1,
            damage - (
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

    # -----------------------------------------------------
    # 대회복
    # -----------------------------------------------------

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
            f"💚 대회복!"
        )

        add_log(
            f"❤️ HP +{actual_heal}"
        )

    # -----------------------------------------------------
    # 방어 태세
    # -----------------------------------------------------

    elif skill_name == "방어 태세":

        player["defending"] = True

        add_log(
            "🛡️ 방어 태세!"
        )

        add_log(
            "다음 공격 피해가 50% 감소합니다."
        )

    # 적 처치 확인
    if enemy["hp"] <= 0:

        defeat_enemy()

        return

    # 공격/회복 스킬은 적 반격
    if skill_name != "방어 태세":

        enemy_attack()

    else:

        enemy_attack()


# =========================================================
# 포션
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
        f"🧪 포션 사용! HP +{heal}"
    )

    if st.session_state.enemy:

        enemy_attack()


# =========================================================
# 휴식
# =========================================================

def rest():

    player = st.session_state.player

    hp_heal = 15

    mana_heal = 10

    player["hp"] = min(
        get_max_hp(),
        player["hp"] + hp_heal
    )

    player["mana"] = min(
        get_max_mana(),
        player["mana"] + mana_heal
    )

    add_log(
        f"🔥 휴식!"
    )

    add_log(
        f"❤️ HP +{hp_heal}"
    )

    add_log(
        f"🔵 MP +{mana_heal}"
    )

    if st.session_state.enemy:

        enemy_attack()


# =========================================================
# 아이템 구매
# =========================================================

def buy_item(category, item):

    player = st.session_state.player

    price = item["price"]

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

def equip_item(category, item_index):

    player = st.session_state.player

    item = player["inventory"][
        category
    ][item_index]

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

        # 장비 변경 시 마나가 최대치를 넘지 않도록 조정
        player["mana"] = min(
            player["mana"],
            get_max_mana()
        )

        add_log(
            f"💍 {item['name']} 장착!"
        )


# =========================================================
# 무기 강화
# =========================================================

def enhance_weapon():

    player = st.session_state.player

    weapon = player["equipment"]["weapon"]

    level = weapon["enhance"]

    cost = enhancement_cost(level)

    success_rate = enhancement_success_rate(level)

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

        weapon["enhance"] += 1

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

        if weapon["enhance"] >= 3:

            weapon["enhance"] -= 1

            add_log(
                f"📉 강화 단계가 "
                f"+{weapon['enhance']}로 "
                f"하락했습니다."
            )


# =========================================================
# 재시작
# =========================================================

def restart_game():

    for key in [
        "player",
        "enemy",
        "logs",
        "game_over"
    ]:

        if key in st.session_state:

            del st.session_state[key]

    init_game()


# =========================================================
# 화면
# =========================================================

st.title("⚔️ 잊혀진 던전")

st.caption(
    "로그라이크 RPG · 보스 · 스킬 · 장비 · 강화"
)

player = st.session_state.player

enemy = st.session_state.enemy


# =========================================================
# 상단 정보
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Lv",
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


# HP

st.write(
    f"❤️ HP "
    f"{player['hp']} / {get_max_hp()}"
)

st.progress(
    min(
        1.0,
        player["hp"] / get_max_hp()
    )
)


# MP

st.write(
    f"🔵 MP "
    f"{player['mana']} / {get_max_mana()}"
)

st.progress(
    min(
        1.0,
        player["mana"] / get_max_mana()
    )
)


# EXP

required_exp = (
    player["level"] * 50
)

st.write(
    f"⭐ EXP "
    f"{player['exp']} / {required_exp}"
)

st.progress(
    min(
        1.0,
        player["exp"] / required_exp
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

    # 보스 경고
    if (
        player["floor"] % 10 == 0
        and enemy is None
    ):

        st.warning(
            f"🚨 {player['floor']}층은 "
            f"보스층입니다!"
        )

    if enemy:

        if enemy["is_boss"]:

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
            f"{enemy['hp']} / "
            f"{enemy['max_hp']}"
        )

        st.progress(
            max(
                0,
                enemy["hp"]
            ) / enemy["max_hp"]
        )

        st.write(
            f"⚔️ 공격력: "
            f"**{enemy['attack']}**"
        )

        st.write(
            f"🛡️ 방어력: "
            f"**{enemy['defense']}**"
        )

        if enemy["is_boss"]:

            st.write(
                f"👑 보상: "
                f"🪙 {enemy['coins']} / "
                f"⭐ {enemy['exp']}"
            )

    else:

        st.info(
            "현재 전투 중인 적이 없습니다."
        )


    # 게임 오버

    if st.session_state.game_over:

        st.error(
            "☠️ GAME OVER"
        )

        st.write(
            f"최종 층: "
            f"{player['floor']}"
        )

        st.write(
            f"최종 레벨: "
            f"{player['level']}"
        )

        if st.button(
            "🔄 다시 시작",
            use_container_width=True
        ):

            restart_game()

            st.rerun()

    else:

        # 탐험

        if enemy is None:

            if st.button(
                "🚪 다음 방 탐험",
                use_container_width=True
            ):

                spawn_enemy()

                st.rerun()

        # 전투

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

                skill = SKILLS[skill_name]

                with skill_cols[
                    index % 2
                ]:

                    if st.button(
                        f"{skill_name} "
                        f"({skill['mana']} MP)",
                        key=f"battle_skill_{skill_name}",
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
        key="strength_up",
        use_container_width=True
    ):

        increase_stat(
            "strength"
        )

        st.rerun()


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
        key="vitality_up",
        use_container_width=True
    ):

        increase_stat(
            "vitality"
        )

        st.rerun()


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
        key="defense_up",
        use_container_width=True
    ):

        increase_stat(
            "defense"
        )

        st.rerun()


    st.markdown(
        "### 💨 민첩"
    )

    st.write(
        f"현재: **{player['agility']}**"
    )

    st.caption(
        "민첩 1 → 치명타 +1%, 회피 +0.5%"
    )

    if st.button(
        "민첩 +1",
        key="agility_up",
        use_container_width=True
    ):

        increase_stat(
            "agility"
        )

        st.rerun()


    st.markdown(
        "### 🧠 정신력"
    )

    st.write(
        f"현재: **{player['spirit']}**"
    )

    st.caption(
        "정신력 1 → 최대 마나 +5"
    )

    if st.button(
        "정신력 +1",
        key="spirit_up",
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
        f"⚔️ 공격력: **{get_attack()}**"
    )

    st.write(
        f"🛡️ 방어력: **{get_defense()}**"
    )

    st.write(
        f"❤️ 최대 HP: **{get_max_hp()}**"
    )

    st.write(
        f"🔵 최대 MP: **{get_max_mana()}**"
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
        f"**{player['mana']} / "
        f"{get_max_mana()}**"
    )


    for skill_name, skill in SKILLS.items():

        st.markdown(
            f"### {skill_name}"
        )

        st.write(
            f"🔵 마나 소비: "
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
                "🔥 공격력의 200% 마법 피해"
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
                key=f"weapon_buy_{i}"
            ):

                buy_item(
                    "weapons",
                    item
                )

                st.rerun()


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
                key=f"armor_buy_{i}"
            ):

                buy_item(
                    "armors",
                    item
                )

                st.rerun()


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

            attack = item.get(
                "attack",
                0
            )

            defense = item.get(
                "defense",
                0
            )

            mana = item.get(
                "mana",
                0
            )

            st.write(
                f"**{item['name']}** "
                f"| ⚔️ +{attack} "
                f"| 🛡️ +{defense} "
                f"| 🔵 MP +{mana} "
                f"| 🪙 {item['price']}"
            )

        with col2:

            if st.button(
                "구매",
                key=f"accessory_buy_{i}"
            ):

                buy_item(
                    "accessories",
                    item
                )

                st.rerun()


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
                key=f"potion_buy_{i}"
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

    weapon = player["equipment"]["weapon"]

    armor = player["equipment"]["armor"]

    accessory = player["equipment"]["accessory"]


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
        f"🔵 악세사리 마나: "
        f"**+{accessory.get('mana', 0)}**"
    )


    st.divider()


    st.markdown(
        "### ⚔️ 보유 무기"
    )

    if not player["inventory"]["weapons"]:

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


    st.markdown(
        "### 🛡️ 보유 갑옷"
    )

    if not player["inventory"]["armors"]:

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


    st.markdown(
        "### 💍 보유 악세사리"
    )

    if not player["inventory"]["accessories"]:

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

    weapon = player["equipment"]["weapon"]

    level = weapon["enhance"]

    cost = enhancement_cost(level)

    success_rate = enhancement_success_rate(level)


    st.write(
        f"현재 무기: "
        f"**{weapon['name']} +{level}**"
    )

    st.write(
        f"기본 공격력: "
        f"**{weapon['attack']}**"
    )

    st.write(
        f"강화 보너스: "
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
        "+3 이상에서 실패하면 강화 단계가 하락할 수 있습니다."
    )


# =========================================================
# 모험 기록
# =========================================================

st.divider()

st.subheader(
    "📜 모험 기록"
)

for log in reversed(
    st.session_state.logs
):

    st.write(log)
