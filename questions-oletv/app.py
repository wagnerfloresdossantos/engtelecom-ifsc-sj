import base64
import json
import os
import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from questions import questions

st.set_page_config(
    page_title="Quiz OléTV",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = os.path.dirname(__file__)
LEADS_FILE = os.path.join(BASE_DIR, "leads.csv")
RANKING_FILE = os.path.join(BASE_DIR, "ranking.csv")
CONFIG_FILE = os.path.join(BASE_DIR, "event_config.json")
ADMIN_PASSWORD = "oletv2026"


def empty_leads_df():
    return pd.DataFrame(
        columns=[
            "timestamp",
            "evento",
            "nome",
            "empresa",
            "email",
            "whatsapp",
            "score",
            "tempo_segundos",
            "ganhou_brinde",
        ]
    )


def empty_ranking_df():
    return pd.DataFrame(
        columns=[
            "timestamp",
            "evento",
            "nome",
            "empresa",
            "score",
            "tempo_segundos",
        ]
    )


def read_leads_csv():
    if not os.path.exists(LEADS_FILE) or os.path.getsize(LEADS_FILE) == 0:
        df = empty_leads_df()
        df.to_csv(LEADS_FILE, index=False)
        return df
    try:
        return pd.read_csv(LEADS_FILE)
    except Exception:
        df = empty_leads_df()
        df.to_csv(LEADS_FILE, index=False)
        return df


def read_ranking_csv():
    if not os.path.exists(RANKING_FILE) or os.path.getsize(RANKING_FILE) == 0:
        df = empty_ranking_df()
        df.to_csv(RANKING_FILE, index=False)
        return df
    try:
        return pd.read_csv(RANKING_FILE)
    except Exception:
        df = empty_ranking_df()
        df.to_csv(RANKING_FILE, index=False)
        return df


def ensure_files():
    if not os.path.exists(LEADS_FILE):
        empty_leads_df().to_csv(LEADS_FILE, index=False)

    if not os.path.exists(RANKING_FILE):
        empty_ranking_df().to_csv(RANKING_FILE, index=False)

    default_config = {
        "event_name": "Desafio OléTV",
        "event_subtitle": "Teste seus conhecimentos sobre filmes, séries, streaming e telecom",
        "fair_name": "Evento Especial",
        "logo_text": "OléTV",
        "primary_color": "#00C2FF",
        "secondary_color": "#001B2E",
        "background_color": "#08101C",
        "background_color_2": "#032B43",
        "card_color": "rgba(7, 17, 31, 0.78)",
        "text_color": "#FFFFFF",
        "button_text_color": "#001B2E",
        "quiz_time_seconds": 120,
        "show_ranking": False,
        "oletv_logo_path": "assents/logo.png",
        "fair_logo_path": "assents/logo_bg.png",
        "questions_per_game": 10,
    }

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
    else:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            current = json.load(f)
        changed = False
        for k, v in default_config.items():
            if k not in current:
                current[k] = v
                changed = True
        if changed:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)


def load_config():
    ensure_files()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_base64_file(path):
    if not path:
        return None

    full_path = os.path.join(BASE_DIR, path)

    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    return None


def init_state():
    defaults = {
        "step": "home",
        "user": {},
        "score": 0,
        "q_index": 0,
        "quiz_started_at": None,
        "quiz_deadline": None,
        "already_saved": False,
        "admin_ok": False,
        "admin_selected_event": None,
        "game_questions": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def build_game_questions(total_questions):
    selected = random.sample(questions, min(total_questions, len(questions)))
    shuffled_questions = []

    for q in selected:
        options = q["options"][:]
        random.shuffle(options)
        shuffled_questions.append(
            {
                "question": q["question"],
                "options": options,
                "answer": q["answer"],
            }
        )

    return shuffled_questions


def inject_css(cfg):
    st.markdown(
        f"""
        <style>
            :root {{
                --primary: {cfg["primary_color"]};
                --secondary: {cfg["secondary_color"]};
                --bg1: {cfg["background_color"]};
                --bg2: {cfg["background_color_2"]};
                --card: {cfg["card_color"]};
                --text: {cfg["text_color"]};
                --button-text: {cfg["button_text_color"]};
            }}

            html, body, .stApp, [data-testid="stAppViewContainer"] {{
                margin: 0 !important;
                padding: 0 !important;
                height: 100% !important;
                overflow: hidden !important;
                overscroll-behavior: none !important;
            }}

            [data-testid="stAppViewContainer"] {{
                overflow: hidden !important;
            }}

            [data-testid="stHeader"] {{
                display: none !important;
                height: 0 !important;
                min-height: 0 !important;
            }}

            header {{
                display: none !important;
                height: 0 !important;
                min-height: 0 !important;
            }}

            [data-testid="stToolbar"] {{
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
            }}

            div[data-testid="stAppViewBlockContainer"] {{
                padding-top: 0 !important;
                margin-top: 0 !important;
            }}

            .main .block-container {{
                padding-top: 0 !important;
                margin-top: 0 !important;
                max-width: 1280px;
                padding-left: 1rem;
                padding-right: 1rem;
                padding-bottom: 0 !important;
                height: 100vh !important;
                overflow: hidden !important;
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top left, rgba(0,194,255,0.10), transparent 30%),
                    radial-gradient(circle at bottom right, rgba(0,194,255,0.08), transparent 28%),
                    linear-gradient(135deg, var(--bg1), var(--bg2));
                color: var(--text);
                min-height: 100vh;
            }}

            h1, h2, h3, h4, h5, h6, p, span, label, div {{
                color: var(--text) !important;
            }}

            .hero-screen {{
                height: 100vh;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }}

            .hero-wrapper {{
                width: 100%;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px;
                box-sizing: border-box;
            }}

            .hero-box {{
                width: 100%;
                max-width: 900px;
                max-height: 94vh;
                overflow: hidden;
                border-radius: 28px;
                padding: 24px 28px;
                background: rgba(7, 17, 31, 0.62);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 50px rgba(0,0,0,0.35);
                backdrop-filter: blur(8px);
                text-align: center;
                position: relative;
            }}

            .hero-glow {{
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 20% 20%, rgba(0,194,255,0.10), transparent 28%),
                    radial-gradient(circle at 80% 80%, rgba(0,194,255,0.08), transparent 24%);
                pointer-events: none;
            }}

            .hero-content {{
                position: relative;
                z-index: 2;
            }}

            .hero-logos {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 22px;
                flex-wrap: wrap;
                margin-bottom: 16px;
            }}

            .hero-logos img {{
                max-height: 68px;
                width: auto;
                display: block;
            }}

            .hero-badge {{
                display: inline-block;
                background: var(--primary);
                color: var(--button-text) !important;
                padding: 8px 16px;
                border-radius: 999px;
                font-weight: 900;
                margin-bottom: 14px;
                font-size: 0.95rem;
            }}

            .hero-title {{
                font-size: 3rem;
                font-weight: 900;
                line-height: 1.02;
                margin-bottom: 10px;
            }}

            .hero-subtitle {{
                font-size: 1.06rem;
                opacity: 0.96;
                margin-bottom: 16px;
            }}

            .totem-info {{
                font-size: 1rem;
                margin-bottom: 6px;
            }}

            .hero-action {{
                margin-top: 18px;
                text-align: center;
            }}

            .hero-start-link {{
                display: inline-block;
                min-width: 260px;
                padding: 16px 28px;
                border-radius: 18px;
                background: var(--primary);
                color: var(--button-text) !important;
                font-size: 1.16rem;
                font-weight: 900;
                text-decoration: none;
                cursor: pointer;
                box-sizing: border-box;
                animation: pulseStart 1.6s infinite;
                box-shadow: 0 0 0 0 rgba(0,194,255,0.45);
            }}

            .hero-start-link:hover {{
                opacity: 0.94;
                transform: scale(1.01);
            }}

            .touch-hint {{
                margin-top: 12px;
                font-size: 0.98rem;
                opacity: 0.92;
                animation: fadeHint 1.8s infinite;
            }}

            @keyframes pulseStart {{
                0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(0,194,255,0.42); }}
                70% {{ transform: scale(1.02); box-shadow: 0 0 0 18px rgba(0,194,255,0); }}
                100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(0,194,255,0); }}
            }}

            @keyframes fadeHint {{
                0% {{ opacity: 0.55; }}
                50% {{ opacity: 1; }}
                100% {{ opacity: 0.55; }}
            }}

            .card-box {{
                background: var(--card);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 24px;
                padding: 22px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.24);
                backdrop-filter: blur(6px);
            }}

            .centered {{
                text-align: center;
            }}

            .big-score {{
                font-size: 4rem;
                font-weight: 900;
                color: var(--primary) !important;
            }}

            .stButton > button {{
                width: 100%;
                min-height: 60px;
                border-radius: 18px;
                border: none;
                background: var(--primary) !important;
                color: var(--button-text) !important;
                font-size: 1.08rem;
                font-weight: 900;
                cursor: pointer;
            }}

            div[data-testid="stFormSubmitButton"] > button {{
                width: 100%;
                min-height: 60px;
                border-radius: 18px;
                border: none;
                background: var(--primary) !important;
                color: var(--button-text) !important;
                font-size: 1.08rem;
                font-weight: 900;
                cursor: pointer;
            }}

            div[data-testid="stFormSubmitButton"] {{
                background: transparent !important;
            }}

            .stDownloadButton > button {{
                width: 100%;
                min-height: 54px;
                border-radius: 18px;
                border: none;
                background: var(--primary) !important;
                color: var(--button-text) !important;
                font-size: 1rem;
                font-weight: 900;
            }}

            .stTextInput input {{
                min-height: 52px;
                border-radius: 14px;
            }}

            .timer-box {{
                text-align: center;
                font-size: 1.25rem;
                font-weight: 900;
                padding: 12px;
                border-radius: 18px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.14);
                margin-bottom: 12px;
            }}

            section[data-testid="stSidebar"] {{
                background: rgba(8, 12, 20, 0.96);
            }}

            @media (max-width: 1366px) {{
                .hero-box {{
                    max-width: 820px;
                    padding: 20px 22px;
                    max-height: 92vh;
                }}

                .hero-logos img {{
                    max-height: 56px;
                }}

                .hero-title {{
                    font-size: 2.45rem;
                }}

                .hero-subtitle {{
                    font-size: 0.98rem;
                    margin-bottom: 12px;
                }}

                .totem-info {{
                    font-size: 0.92rem;
                    margin-bottom: 4px;
                }}

                .hero-start-link {{
                    min-width: 220px;
                    padding: 14px 22px;
                    font-size: 1rem;
                }}
            }}

            @media (max-height: 768px) {{
                .hero-wrapper {{
                    padding: 8px;
                }}

                .hero-box {{
                    padding: 18px 20px;
                    max-height: 93vh;
                }}

                .hero-logos {{
                    margin-bottom: 10px;
                }}

                .hero-logos img {{
                    max-height: 50px;
                }}

                .hero-badge {{
                    margin-bottom: 10px;
                    font-size: 0.88rem;
                }}

                .hero-title {{
                    font-size: 2.2rem;
                    margin-bottom: 8px;
                }}

                .hero-subtitle {{
                    font-size: 0.95rem;
                    margin-bottom: 10px;
                }}

                .totem-info {{
                    font-size: 0.9rem;
                    margin-bottom: 3px;
                }}

                .hero-action {{
                    margin-top: 12px;
                }}

                .touch-hint {{
                    margin-top: 8px;
                    font-size: 0.9rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_kiosk_js():
    st.components.v1.html(
        """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                document.body.style.overflow = "hidden";
                document.documentElement.style.overflow = "hidden";

                document.addEventListener("keydown", function(e) {
                    const key = e.key.toLowerCase();
                    if (
                        key === "f5" ||
                        (e.ctrlKey && key === "r") ||
                        (e.metaKey && key === "r") ||
                        key === "f11"
                    ) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                }, true);

                document.addEventListener("contextmenu", function(e) {
                    e.preventDefault();
                });

                const hideStreamlitChrome = () => {
                    const toolbar = window.parent.document.querySelector('[data-testid="stToolbar"]');
                    const header = window.parent.document.querySelector('[data-testid="stHeader"]');
                    if (toolbar) toolbar.style.display = "none";
                    if (header) header.style.display = "none";
                };

                setInterval(hideStreamlitChrome, 500);
                hideStreamlitChrome();
            });
        </script>
        """,
        height=0,
    )


def play_sound(success=True):
    freq = 880 if success else 220
    duration = 0.18 if success else 0.28
    st.components.v1.html(
        f"""
        <script>
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContextClass();
        const oscillator = ctx.createOscillator();
        const gain = ctx.createGain();
        oscillator.type = "sine";
        oscillator.frequency.setValueAtTime({freq}, ctx.currentTime);
        gain.gain.setValueAtTime(0.001, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + {duration});
        oscillator.connect(gain);
        gain.connect(ctx.destination);
        oscillator.start();
        oscillator.stop(ctx.currentTime + {duration});
        </script>
        """,
        height=0,
    )


def reset_game():
    st.session_state.step = "home"
    st.session_state.user = {}
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.quiz_started_at = None
    st.session_state.quiz_deadline = None
    st.session_state.already_saved = False
    st.session_state.game_questions = []


def remaining_seconds(cfg):
    if st.session_state.quiz_deadline is None:
        return cfg["quiz_time_seconds"]
    return max(0, int(st.session_state.quiz_deadline - time.time()))


def format_seconds(total_seconds):
    mm = int(total_seconds) // 60
    ss = int(total_seconds) % 60
    return f"{mm:02d}:{ss:02d}"


def save_result(cfg):
    if st.session_state.already_saved:
        return

    elapsed = cfg["quiz_time_seconds"] - remaining_seconds(cfg)
    total_game_questions = len(st.session_state.game_questions)
    ganhou = "SIM" if st.session_state.score == total_game_questions else "NÃO"

    lead_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": cfg["fair_name"],
        "nome": st.session_state.user.get("nome", ""),
        "empresa": st.session_state.user.get("empresa", ""),
        "email": st.session_state.user.get("email", ""),
        "whatsapp": st.session_state.user.get("whatsapp", ""),
        "score": st.session_state.score,
        "tempo_segundos": elapsed,
        "ganhou_brinde": ganhou,
    }

    rank_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": cfg["fair_name"],
        "nome": st.session_state.user.get("nome", ""),
        "empresa": st.session_state.user.get("empresa", ""),
        "score": st.session_state.score,
        "tempo_segundos": elapsed,
    }

    leads_df = read_leads_csv()
    leads_df = pd.concat([leads_df, pd.DataFrame([lead_row])], ignore_index=True)
    leads_df.to_csv(LEADS_FILE, index=False)

    ranking_df = read_ranking_csv()
    ranking_df = pd.concat([ranking_df, pd.DataFrame([rank_row])], ignore_index=True)
    ranking_df.to_csv(RANKING_FILE, index=False)

    st.session_state.already_saved = True


def show_timer(cfg):
    secs = remaining_seconds(cfg)
    st.markdown(
        f"""
        <div class="timer-box">
            ⏱️ Tempo restante: {format_seconds(secs)}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if secs <= 0 and st.session_state.step == "quiz":
        st.session_state.step = "result"
        st.rerun()


ensure_files()
config = load_config()
init_state()
inject_css(config)
inject_kiosk_js()

with st.sidebar:
    st.markdown("## Admin")
    pwd = st.text_input("Senha do admin", type="password")
    if pwd == ADMIN_PASSWORD:
        st.session_state.admin_ok = True

    if st.session_state.admin_ok:
        st.success("Admin liberado")

        with st.expander("🎨 Personalização", expanded=True):
            event_name = st.text_input("Título principal", value=config["event_name"])
            event_subtitle = st.text_input("Subtítulo", value=config["event_subtitle"])
            fair_name = st.text_input("Nome da feira/evento", value=config["fair_name"])
            logo_text = st.text_input("Texto alternativo", value=config["logo_text"])

            primary_color = st.color_picker("Cor principal", value=config["primary_color"])
            secondary_color = st.color_picker("Cor secundária", value=config["secondary_color"])
            background_color = st.color_picker("Cor de fundo 1", value=config["background_color"])
            background_color_2 = st.color_picker("Cor de fundo 2", value=config["background_color_2"])
            text_color = st.color_picker("Cor do texto", value=config["text_color"])
            button_text_color = st.color_picker("Cor do texto do botão", value=config["button_text_color"])

            quiz_time_seconds = st.number_input(
                "Tempo total do quiz (segundos)",
                min_value=30,
                max_value=600,
                value=int(config["quiz_time_seconds"]),
                step=10,
            )

            questions_per_game = st.number_input(
                "Perguntas por partida",
                min_value=5,
                max_value=min(20, len(questions)),
                value=int(config.get("questions_per_game", 10)),
                step=1,
            )

            show_ranking = st.checkbox("Mostrar ranking", value=config["show_ranking"])
            oletv_logo_path = st.text_input("Logo OléTV", value=config["oletv_logo_path"])
            fair_logo_path = st.text_input("Logo da feira", value=config["fair_logo_path"])

            if st.button("Salvar configurações"):
                new_cfg = {
                    "event_name": event_name,
                    "event_subtitle": event_subtitle,
                    "fair_name": fair_name,
                    "logo_text": logo_text,
                    "primary_color": primary_color,
                    "secondary_color": secondary_color,
                    "background_color": background_color,
                    "background_color_2": background_color_2,
                    "card_color": config.get("card_color", "rgba(7, 17, 31, 0.78)"),
                    "text_color": text_color,
                    "button_text_color": button_text_color,
                    "quiz_time_seconds": int(quiz_time_seconds),
                    "show_ranking": show_ranking,
                    "oletv_logo_path": oletv_logo_path,
                    "fair_logo_path": fair_logo_path,
                    "questions_per_game": int(questions_per_game),
                }
                save_config(new_cfg)
                st.success("Configuração salva. Recarregue a página.")

        leads_df = read_leads_csv()
        ranking_df = read_ranking_csv()

        all_events = []
        if not leads_df.empty:
            all_events.extend(leads_df["evento"].dropna().astype(str).unique().tolist())
        if not ranking_df.empty:
            all_events.extend(ranking_df["evento"].dropna().astype(str).unique().tolist())

        all_events = sorted(set(all_events))
        if not all_events:
            all_events = [config["fair_name"]]

        default_event = config["fair_name"] if config["fair_name"] in all_events else all_events[0]
        selected_event = st.selectbox(
            "Filtrar por feira/evento",
            options=all_events,
            index=all_events.index(default_event),
        )
        st.session_state.admin_selected_event = selected_event

        filtered_leads = leads_df[leads_df["evento"] == selected_event].copy() if not leads_df.empty else pd.DataFrame()
        filtered_ranking = ranking_df[ranking_df["evento"] == selected_event].copy() if not ranking_df.empty else pd.DataFrame()

        with st.expander("📊 Dados do evento", expanded=True):
            st.write(f"Evento selecionado: {selected_event}")
            st.write(f"Leads do evento: {len(filtered_leads)}")
            st.write(f"Registros de ranking: {len(filtered_ranking)}")

            st.download_button(
                "Exportar leads do evento",
                data=filtered_leads.to_csv(index=False).encode("utf-8"),
                file_name=f"leads_{selected_event}.csv",
                mime="text/csv",
            )

            st.download_button(
                "Exportar ranking do evento",
                data=filtered_ranking.to_csv(index=False).encode("utf-8"),
                file_name=f"ranking_{selected_event}.csv",
                mime="text/csv",
            )

        with st.expander("🧹 Ações"):
            if st.button("Limpar ranking do evento selecionado"):
                if not ranking_df.empty:
                    ranking_df = ranking_df[ranking_df["evento"] != selected_event]
                    ranking_df.to_csv(RANKING_FILE, index=False)
                st.success("Ranking removido.")

            if st.button("Reiniciar jogo atual"):
                reset_game()
                st.success("Jogo reiniciado.")


if st.session_state.step == "home":
    if "start" in st.query_params:
        st.session_state.step = "register"
        st.query_params.clear()
        st.rerun()

    oletv_logo = get_base64_file(config.get("oletv_logo_path"))
    fair_logo = get_base64_file(config.get("fair_logo_path"))

    logos_html = '<div class="hero-logos">'
    if oletv_logo:
        logos_html += f'<img src="data:image/png;base64,{oletv_logo}" alt="OléTV">'
    if fair_logo:
        logos_html += f'<img src="data:image/png;base64,{fair_logo}" alt="Feira">'
    logos_html += "</div>"

    home_html = f"""
    <div class="hero-screen">
        <div class="hero-wrapper">
            <div class="hero-box">
                <div class="hero-glow"></div>
                <div class="hero-content">
                    {logos_html}
                    <div class="hero-badge">{config["fair_name"]}</div>
                    <div class="hero-title">{config["event_name"]}</div>
                    <div class="hero-subtitle">{config["event_subtitle"]}</div>
                    <div class="totem-info">📝 Faça seu cadastro</div>
                    <div class="totem-info">🎯 Responda {config.get("questions_per_game", 10)} perguntas</div>
                    <div class="totem-info">⏱️ Tempo total: {config["quiz_time_seconds"]} segundos</div>
                    <div class="totem-info">🎁 Quem acertar tudo ganha um brinde</div>
                    <div class="hero-action">
                        <a class="hero-start-link" href="?start=1">TOQUE PARA COMEÇAR</a>
                        <div class="touch-hint">Toque na tela para iniciar o desafio</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    st.markdown(home_html, unsafe_allow_html=True)

elif st.session_state.step == "register":
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### 📝 Cadastro do participante")

    with st.form("lead_form"):
        nome = st.text_input("Nome completo")
        empresa = st.text_input("Empresa")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")
        submitted = st.form_submit_button("Ir para o quiz")

    if submitted:
        if not nome.strip() or not empresa.strip() or not email.strip() or not whatsapp.strip():
            st.error("Preencha todos os campos.")
        else:
            leads_df = read_leads_csv()

            email_limpo = email.strip()
            whatsapp_limpo = whatsapp.strip()

            registros_mesma_pessoa = leads_df[
                (leads_df["email"].astype(str) == email_limpo) |
                (leads_df["whatsapp"].astype(str) == whatsapp_limpo)
            ].copy()

            ja_ganhou = False
            if not registros_mesma_pessoa.empty and "ganhou_brinde" in registros_mesma_pessoa.columns:
                ja_ganhou = (
                    registros_mesma_pessoa["ganhou_brinde"]
                    .astype(str)
                    .str.upper()
                    .eq("SIM")
                    .any()
                )

            if ja_ganhou:
                st.error("Você já ganhou um brinde neste desafio e não pode participar novamente.")
                st.stop()

            st.session_state.user = {
                "nome": nome.strip(),
                "empresa": empresa.strip(),
                "email": email_limpo,
                "whatsapp": whatsapp_limpo,
            }
            st.session_state.score = 0
            st.session_state.q_index = 0
            st.session_state.quiz_started_at = time.time()
            st.session_state.quiz_deadline = time.time() + int(config["quiz_time_seconds"])
            st.session_state.already_saved = False
            st.session_state.game_questions = build_game_questions(int(config.get("questions_per_game", 10)))
            st.session_state.step = "quiz"
            st.rerun()

    if st.button("Voltar"):
        reset_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == "quiz":
    show_timer(config)

    if st.session_state.q_index >= len(st.session_state.game_questions):
        st.session_state.step = "result"
        st.rerun()

    q = st.session_state.game_questions[st.session_state.q_index]

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown(f"### Pergunta {st.session_state.q_index + 1} de {len(st.session_state.game_questions)}")
    st.write(q["question"])

    answer = st.radio(
        "Escolha uma opção:",
        q["options"],
        key=f"q_{st.session_state.q_index}",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Responder"):
            if answer == q["answer"]:
                st.session_state.score += 1
                play_sound(success=True)
            else:
                play_sound(success=False)

            st.session_state.q_index += 1
            time.sleep(0.15)

            if st.session_state.q_index >= len(st.session_state.game_questions):
                st.session_state.step = "result"

            st.rerun()

    with col2:
        if st.button("Encerrar quiz"):
            st.session_state.step = "result"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == "result":
    save_result(config)

    elapsed = config["quiz_time_seconds"] - remaining_seconds(config)
    total_game_questions = len(st.session_state.game_questions)
    ganhou = st.session_state.score == total_game_questions

    st.markdown('<div class="card-box centered">', unsafe_allow_html=True)
    st.markdown("### Resultado final")
    st.markdown(
        f'<div class="big-score">{st.session_state.score}/{total_game_questions}</div>',
        unsafe_allow_html=True,
    )
    st.write(f"Tempo total: {format_seconds(elapsed)}")

    if ganhou:
        st.success("🎉 Parabéns! Você ganhou um brinde.")
        st.markdown(
            '<div class="result-callout">Procure nossa equipe para retirar o brinde 🎁</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("Obrigado por participar.")
        st.markdown(
            '<div class="result-callout">Passe no stand da OléTV para conhecer nossas soluções.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Novo participante"):
        reset_game()
        st.rerun()