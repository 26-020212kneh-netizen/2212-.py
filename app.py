import random
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------

st.set_page_config(
    page_title="잊혀진 던전",
    page_icon="⚔️",
    layout="centered"
)

# -----------------------------
# 게임 데이터
# -----------------------------

ENEMIES = [
    {
        "name": "슬라임",
        "hp": 30,
        "attack": 7,
        "gold": 10,
        "exp": 15
    },
    {
        "name": "고블린",
        "hp": 45,
        "attack": 10,
        "gold": 20,
        "exp": 25
    },
    {
        "name": "해골 전사",
        "hp": 60,
        "attack": 13,
        "gold": 30,
        "exp": 35
    }
]


# -----------------------------
# 세션 상태 초기화
# -----------------------------

def init_game():
    if "player" not in st.session_state:
        st.session_state.player = {
            "name": "용사",
            "level": 1,
            "exp": 0,
            "max_hp": 100,
            "hp": 100,
            "attack": 15,
            "gold": 0,
            "potions": 3,
            "floor": 1
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


# -----------------------------
# 유틸리티
# -----------------------------

def add_log(message):
    st.session_state.logs.append(message)

    # 로그가 너무 길어지지 않도록 제한
    if len(st.session_state.logs) > 12:
        st.session_state.logs.pop(0)


def create_enemy():
    template = random.choice(ENEMIES)

    enemy = template.copy()

    # 던전 층에 따라 적 강화
    floor = st.session_state.player["floor"]

    enemy["hp"] += (floor - 1) * 10
    enemy["max_hp"] = enemy["hp"]
    enemy["attack"] += (floor - 1) * 2

    return enemy


def spawn_enemy():
    if st.session_state.enemy is None:
        st.session_state.enemy = create_enemy()

        add_log(
            f"👹 {st.session_state.enemy['name']}이(가) 나타났습니다!"
        )


def gain_exp(amount):
    player = st.session_state.player

    player["exp"] += amount

    required_exp = player["level"] * 50

    if player["exp"] >= required_exp:
        player["exp"] -= required_exp
        player["level"] += 1

        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["attack"] += 5

        add_log(
            f"✨ 레벨 업! Lv.{player['level']}이 되었습니다."
        )


# -----------------------------
# 전투
# -----------------------------

def attack():
    player = st.session_state.player
    enemy = st.session_state.enemy

    if enemy is None:
        spawn_enemy()
        return

    damage = random.randint(
        max(1, player["attack"] - 4),
        player["attack"] + 5
    )

    enemy["hp"] -= damage

    add_log(
        f"⚔️ {enemy['name']}에게 {damage}의 피해를 입혔습니다."
    )

    # 적 처치
    if enemy["hp"] <= 0:
        gold = enemy["gold"]
        exp = enemy["exp"]

        player["gold"] += gold

        add_log(
            f"💀 {enemy['name']} 처치!"
        )

        add_log(
            f"💰 골드 +{gold} / ⭐ 경험치 +{exp}"
        )

        gain_exp(exp)

        # 다음 층
        player["floor"] += 1

        add_log(
            f"🚪 던전 {player['floor']}층으로 이동합니다."
        )

        st.session_state.enemy = None
        return

    # 적의 반격
    enemy_attack()


def enemy_attack():
    player = st.session_state.player
    enemy = st.session_state.enemy

    damage = random.randint(
        max(1, enemy["attack"] - 3),
        enemy["attack"] + 3
    )

    player["hp"] -= damage

    add_log(
        f"💥 {enemy['name']}의 공격! "
        f"{damage}의 피해를 받았습니다."
    )

    if player["hp"] <= 0:
        player["hp"] = 0
        st.session_state.game_over = True

        add_log("☠️ 당신은 던전에서 쓰러졌습니다.")


def use_potion():
    player = st.session_state.player

    if player["potions"] <= 0:
        add_log("❌ 포션이 없습니다.")
        return

    if player["hp"] >= player["max_hp"]:
        add_log("❤️ 체력이 이미 가득합니다.")
        return

    heal = 30

    player["hp"] = min(
        player["max_hp"],
        player["hp"] + heal
    )

    player["potions"] -= 1

    add_log(
        f"🧪 포션 사용! HP +{heal}"
    )

    # 포션 사용 후 적 반격
    if st.session_state.enemy:
        enemy_attack()


def rest():
    player = st.session_state.player

    heal = 15

    player["hp"] = min(
        player["max_hp"],
        player["hp"] + heal
    )

    add_log(
        f"🔥 잠시 휴식했습니다. HP +{heal}"
    )

    if st.session_state.enemy:
        enemy_attack()


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


# -----------------------------
# 화면
# -----------------------------

st.title("⚔️ 잊혀진 던전")
st.caption("텍스트 로그라이크 RPG")

player = st.session_state.player
enemy = st.session_state.enemy


# -----------------------------
# 플레이어 정보
# -----------------------------

st.subheader("🧙 플레이어")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "레벨",
        player["level"]
    )

with col2:
    st.metric(
        "공격력",
        player["attack"]
    )

with col3:
    st.metric(
        "골드",
        player["gold"]
    )


# HP 표시

st.write(
    f"❤️ HP: {player['hp']} / {player['max_hp']}"
)

st.progress(
    player["hp"] / player["max_hp"]
)

required_exp = player["level"] * 50

st.write(
    f"⭐ EXP: {player['exp']} / {required_exp}"
)

st.progress(
    player["exp"] / required_exp
)

st.write(
    f"🏰 던전 {player['floor']}층"
)

st.divider()


# -----------------------------
# 적 정보
# -----------------------------

if enemy:
    st.subheader("👹 적")

    st.write(
        f"### {enemy['name']}"
    )

    st.write(
        f"❤️ HP: {enemy['hp']} / {enemy['max_hp']}"
    )

    st.progress(
        max(0, enemy["hp"]) / enemy["max_hp"]
    )

else:
    st.info(
        "현재 전투 중인 적이 없습니다."
    )


# -----------------------------
# 게임 오버
# -----------------------------

if st.session_state.game_over:

    st.error(
        "☠️ GAME OVER"
    )

    st.write(
        f"최종 도달 층: {player['floor']}"
    )

    st.write(
        f"최종 레벨: {player['level']}"
    )

    if st.button(
        "🔄 다시 시작",
        use_container_width=True
    ):
        restart_game()
        st.rerun()

else:

    # 적이 없으면 탐험 버튼
    if enemy is None:

        if st.button(
            "🚪 다음 방 탐험",
            use_container_width=True
        ):
            spawn_enemy()
            st.rerun()

    else:

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "⚔️ 공격",
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


# -----------------------------
# 로그
# -----------------------------

st.divider()

st.subheader("📜 모험 기록")

for log in reversed(st.session_state.logs):
    st.write(log)
