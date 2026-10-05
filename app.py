from flask import Flask, request, redirect, url_for, flash, render_template_string
import sqlite3
from datetime import datetime
from pathlib import Path
import os
import requests

# Design reference used:
# "ActualizeWeb — We Build Your Business Online (provided PDF)"
# The layout, content structure, light/green visual language, cards,
# CTA style and section flow are recreated as a Flask implementation.

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "actualizeweb.db"
GOOGLE_SHEET_WEBHOOK_URL = os.getenv("GOOGLE_SHEET_WEBHOOK_URL", "").strip()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                business TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                goal TEXT,
                message TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def save_to_google_sheet(form):
    """Send the same quote data to a Google Apps Script web app.
    SQLite remains the local fallback/database if Google Sheets is not configured.
    """
    if not GOOGLE_SHEET_WEBHOOK_URL or "REAL_SCRIPT_ID" in GOOGLE_SHEET_WEBHOOK_URL:
        return None

    payload = {
        "name": form.get("name", "").strip(),
        "business": form.get("business", "").strip(),
        "email": form.get("email", "").strip(),
        "phone": form.get("phone", "").strip(),
        "goal": form.get("goal", "").strip(),
        "message": form.get("message", "").strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, data=payload, timeout=8)
        if not response.ok:
            app.logger.warning(
                "Google Sheets webhook returned HTTP %s: %s",
                response.status_code,
                response.text[:200],
            )
            return False
        return True
    except requests.RequestException as exc:
        app.logger.warning("Google Sheets webhook request failed: %s", exc)
        return False


def save_quote(form):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO quotes
            (name, business, email, phone, goal, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form.get("name", "").strip(),
                form.get("business", "").strip(),
                form.get("email", "").strip(),
                form.get("phone", "").strip(),
                form.get("goal", "").strip(),
                form.get("message", "").strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="ActualizeWeb builds fast, custom business websites with lifetime ownership and no monthly fees.">
    <title>ActualizeWeb — We Build Your Business Online</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        :root{
            --bg:#0d0d0d;
            --panel:#121212;
            --panel-2:#191919;
            --line:#5d2817;
            --orange:#f15a24;
            --orange-soft:#d94d20;
            --cream:#f4efe6;
            --muted:#b9b2a8;
            --yellow:#f3c83f;
            --black:#111;
            --max:1180px;
        }

        *{box-sizing:border-box;margin:0;padding:0}
        /* Single light theme with a white and green palette. */
        :root{--bg:#f7fbf8;--panel:#ffffff;--panel-2:#eaf6ee;--line:#b9dcc4;--orange:#168447;--orange-soft:#106b38;--cream:#143321;--muted:#547060;--yellow:#d6a928;--black:#102318}

        html{scroll-behavior:smooth}
        body{
            background:var(--bg);
            color:var(--cream);
            font-family:Inter,Arial,sans-serif;
            line-height:1.6;
            overflow-x:hidden;
        }
        a{text-decoration:none;color:inherit}
        button,input,textarea,select{font:inherit}
        .container{width:min(var(--max),calc(100% - 48px));margin:auto}

        /* subtle orange glow matching the reference */
        body:before{
            content:"";
            position:fixed;
            width:520px;height:520px;
            right:-180px;top:220px;
            background:radial-gradient(circle,rgba(241,90,36,.13),transparent 67%);
            pointer-events:none;
            z-index:-1;
        }

        header{
            position:sticky;
            top:0;
            z-index:100;
            background:rgba(247,251,248,.96);
            backdrop-filter:blur(14px);
            border-bottom:1px solid #b9dcc4;
        }
        .nav{
            height:86px;
            display:flex;
            align-items:center;
            justify-content:space-between;
        }
        .brand{
            font-size:22px;
            letter-spacing:.02em;
            font-weight:500;
        }
        .brand span{color:var(--orange)}
        .menu{
            display:flex;
            gap:30px;
            align-items:center;
            font-size:13px;
            color:#315541;
        }
        .menu a:hover{color:var(--orange)}
        .menu-toggle{
            display:none;
            border:0;
            background:none;
            color:var(--cream);
            font-size:25px;
            cursor:pointer;
        }

        .hero{
            min-height:790px;
            padding:58px 0 78px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        }
        .hero-visual{
            width:min(820px,100%);
            height:330px;
            margin:0 auto 66px;
            position:relative;
            border:1px solid #a33f1d;
            border-radius:20px;
            overflow:hidden;
            background:
                radial-gradient(circle at 75% 35%,rgba(0,217,255,.55),transparent 24%),
                linear-gradient(135deg,#12353b 0%,#0e1d2d 43%,#20262e 100%);
            box-shadow:0 25px 80px rgba(0,0,0,.5);
        }
        .screen{
            position:absolute;
            width:73%;
            height:74%;
            left:13.5%;
            top:7%;
            border:8px solid #171717;
            border-radius:7px;
            background:#071126;
            box-shadow:0 10px 30px #000;
            overflow:hidden;
        }
        .screen-top{
            height:28px;
            background:#f5f5f5;
            display:flex;
            align-items:center;
            gap:7px;
            padding:0 12px;
        }
        .dot{width:6px;height:6px;border-radius:50%;background:#aaa}
        .dashboard{
            padding:18px;
            display:grid;
            grid-template-columns:1.5fr 1fr;
            gap:14px;
            height:calc(100% - 28px);
        }
        .chart-box,.mini-box{
            border:1px solid rgba(77,129,205,.25);
            border-radius:5px;
            background:rgba(13,30,63,.78);
            padding:12px;
        }
        .chart{
            height:120px;
            display:flex;
            align-items:flex-end;
            gap:7px;
            padding-top:20px;
        }
        .bar{
            flex:1;
            background:linear-gradient(to top,#1ed3ed,#3854ff);
            border-radius:3px 3px 0 0;
        }
        .mini-stack{display:grid;gap:12px}
        .mini-box{height:75px}
        .mini-line{height:7px;background:#1fcbdc;border-radius:5px;margin:7px 0}
        .mini-line:nth-child(2){width:65%}
        .laptop-base{
            position:absolute;
            left:9%;
            right:9%;
            bottom:-4px;
            height:43px;
            background:linear-gradient(#323232,#151515);
            clip-path:polygon(5% 0,95% 0,100% 100%,0 100%);
            border-radius:4px;
        }
        .launch-card{
            position:absolute;
            left:8%;
            bottom:22px;
            padding:17px 26px;
            min-width:270px;
            background:#171717;
            border:1px solid var(--orange);
            border-radius:16px;
            box-shadow:0 15px 35px rgba(0,0,0,.5);
        }
        .launch-card strong{display:block;font-size:14px;margin-bottom:3px}
        .launch-card p{font:12px "DM Mono",monospace;color:#ddd}
        .launch-card strong:before{
            content:"";
            display:inline-block;
            width:11px;height:11px;
            background:var(--orange);
            border-radius:50%;
            margin-right:12px;
        }

        .eyebrow{
            color:var(--orange);
            font:700 12px "DM Mono",monospace;
            letter-spacing:.25em;
            text-transform:uppercase;
            margin-bottom:18px;
        }
        h1{
            max-width:800px;
            font-size:clamp(52px,7vw,88px);
            line-height:.98;
            letter-spacing:-.055em;
            margin-bottom:25px;
        }
        h1 span{color:var(--orange)}
        .hero-copy{
            max-width:710px;
            color:#ddd5cc;
            font-size:18px;
            line-height:1.8;
            letter-spacing:.04em;
            margin-bottom:34px;
        }
        .pills{
            display:flex;
            flex-wrap:wrap;
            gap:10px;
            margin-bottom:35px;
        }
        .pill{
            border:1px solid #7c351d;
            border-radius:999px;
            padding:8px 16px;
            color:var(--orange);
            font:700 11px "DM Mono",monospace;
            letter-spacing:.12em;
        }
        .buttons{display:flex;gap:14px;flex-wrap:wrap}
        .btn{
            display:inline-flex;
            align-items:center;
            justify-content:center;
            min-height:52px;
            padding:0 28px;
            border-radius:28px;
            font-size:12px;
            font-weight:800;
            letter-spacing:.1em;
            text-transform:uppercase;
            transition:.25s ease;
            cursor:pointer;
            border:1px solid var(--orange);
        }
        .btn-primary{
            background:var(--yellow);
            border-color:var(--yellow);
            color:#17130a;
        }
        .btn-primary:hover{transform:translateY(-2px);filter:brightness(1.05)}
        .btn-outline{color:var(--orange);background:transparent}
        .btn-outline:hover{background:var(--orange);color:#111}

        section{padding:105px 0}
        .dark-section{background:#eaf6ee}
        .section-head{display:flex;justify-content:space-between;align-items:end;gap:30px;margin-bottom:48px}
        h2{
            font-size:clamp(38px,5vw,60px);
            line-height:1;
            letter-spacing:-.045em;
        }
        .section-intro{max-width:680px;color:#547060;font-size:16px;margin-top:16px}
        .small-link{
            color:var(--orange);
            font-size:12px;
            font-weight:800;
            letter-spacing:.1em;
            text-transform:uppercase;
            white-space:nowrap;
        }

        .stats{
            display:grid;
            grid-template-columns:repeat(3,1fr);
            border-top:1px solid #333;
            border-bottom:1px solid #333;
        }
        .stat{padding:45px 20px;border-right:1px solid #333}
        .stat:last-child{border-right:0}
        .stat-number{font-size:52px;font-weight:800;letter-spacing:-.05em}
        .stat-label{color:#aaa;font-size:14px}

        .features{
            display:grid;
            grid-template-columns:repeat(2,1fr);
            gap:22px;
        }
        .feature{
            min-height:245px;
            border:1px solid #78371f;
            border-radius:14px;
            padding:34px;
            background:#111;
            transition:.25s ease;
        }
        .feature:hover{
            transform:translateY(-4px);
            border-color:var(--orange);
            box-shadow:0 15px 40px rgba(0,0,0,.25);
        }
        .icon{
            width:44px;height:44px;
            display:grid;place-items:center;
            background:#26170f;
            color:var(--orange);
            border-radius:9px;
            margin-bottom:27px;
            font-size:19px;
        }
        .feature h3{font-size:19px;margin-bottom:12px}
        .feature p{max-width:450px;color:#bcb5ad;font-size:13px;line-height:1.8}

        .work-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
        .work-card{
            min-height:360px;
            border:1px solid #343434;
            border-radius:15px;
            overflow:hidden;
            background:#151515;
        }
        .work-image{
            height:205px;
            position:relative;
            overflow:hidden;
            background:linear-gradient(135deg,#20242d,#0a2830);
        }
        .work-image:after{
            content:"";
            position:absolute;
            inset:22px;
            border:1px solid rgba(255,255,255,.12);
            border-radius:10px;
        }
        .mock-screen{
            position:absolute;
            width:70%;height:62%;
            left:15%;top:19%;
            border-radius:6px;
            background:linear-gradient(140deg,#202c58,#07132b);
            box-shadow:0 12px 30px #000;
        }
        .work-body{padding:25px}
        .work-body h3{font-size:19px;margin-bottom:8px}
        .work-body p{font-size:13px;color:#aaa;line-height:1.7}

        .difference{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:70px;
            align-items:center;
        }
        .check-list{list-style:none;display:grid;gap:18px;margin-top:30px}
        .check-list li{display:flex;gap:13px;color:#d2cbc3;font-size:14px}
        .check-list li:before{content:"✓";color:var(--orange);font-weight:900}
        .metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#333}
        .metric{background:#111;padding:32px}
        .metric strong{font-size:43px;display:block}
        .metric span{font-size:12px;color:#999}

        .stories{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
        .story{
            background:#121212;
            border:1px solid #333;
            border-radius:15px;
            padding:34px;
        }
        .quote{font-size:18px;line-height:1.8;color:#e8e1d8;margin-bottom:25px}
        .person{font-size:12px;color:#aaa}
        .person strong{color:#eee;display:block;margin-bottom:4px}

        .cta{
            text-align:center;
            background:
                radial-gradient(circle at 50% 0%,rgba(241,90,36,.14),transparent 45%),
                #111;
            border-top:1px solid #3a2118;
            border-bottom:1px solid #3a2118;
        }
        .cta p{max-width:650px;margin:18px auto 30px;color:#aaa}
        .quote-wrap{max-width:820px;margin:45px auto 0;text-align:left}
        .form{
            background:#171717;
            border:1px solid #5c2b1b;
            border-radius:16px;
            padding:30px;
        }
        .form-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
        .field{display:flex;flex-direction:column;gap:7px}
        .field.full{grid-column:1/-1}
        label{font:500 11px "DM Mono",monospace;color:#aaa;text-transform:uppercase;letter-spacing:.12em}
        input,textarea,select{
            width:100%;
            border:1px solid #3b3b3b;
            background:#0e0e0e;
            color:#eee;
            border-radius:8px;
            padding:13px 14px;
            outline:none;
        }
        input:focus,textarea:focus,select:focus{border-color:var(--orange)}
        textarea{min-height:110px;resize:vertical}
        .form-actions{margin-top:20px;display:flex;justify-content:space-between;align-items:center;gap:20px}
        .note{font-size:11px;color:#777}

        footer{padding:65px 0 25px;background:#0b0b0b}
        .footer-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:45px;padding-bottom:50px}
        .footer-brand p{max-width:330px;color:#888;font-size:13px;margin-top:15px}
        footer h4{font-size:12px;color:#eee;margin-bottom:16px}
        footer a,footer li{color:#888;font-size:12px;margin-bottom:9px}
        footer a:hover{color:var(--orange)}
        .footer-list{list-style:none}
        .footer-bottom{
            border-top:1px solid #242424;
            padding-top:22px;
            display:flex;
            justify-content:space-between;
            gap:20px;
            color:#666;
            font-size:11px;
        }
        .flash{
            position:fixed;
            top:100px;
            right:22px;
            z-index:200;
            background:#f3c83f;
            color:#111;
            padding:13px 18px;
            border-radius:8px;
            font-size:13px;
            font-weight:700;
            box-shadow:0 12px 35px #000;
            animation:fade 5s forwards;
        }
        @keyframes fade{0%,80%{opacity:1}100%{opacity:0;pointer-events:none}}

        @media(max-width:850px){
            .container{width:min(var(--max),calc(100% - 34px))}
            .menu{display:none;position:absolute;left:0;right:0;top:86px;background:#111;padding:20px;flex-direction:column;align-items:flex-start;border-bottom:1px solid #5d2817}
            .menu.open{display:flex}
            .menu-toggle{display:block}
            .hero{min-height:auto;padding-top:38px}
            .hero-visual{height:270px;margin-bottom:45px}
            h1{font-size:54px}
            .stats,.features,.work-grid,.stories,.difference{grid-template-columns:1fr}
            .stat{border-right:0;border-bottom:1px solid #333}
            .stat:last-child{border-bottom:0}
            .difference{gap:45px}
            .footer-top{grid-template-columns:1fr 1fr}
        }
        @media(max-width:560px){
            section{padding:75px 0}
            .nav{height:72px}
            .menu{top:72px}
            .hero{padding-top:25px}
            .hero-visual{height:220px;border-radius:14px}
            .screen{width:76%;left:12%;height:69%}
            .launch-card{left:5%;bottom:12px;min-width:0;padding:12px 15px}
            .launch-card p{font-size:10px}
            h1{font-size:43px}
            .hero-copy{font-size:15px}
            .pill{font-size:9px}
            .btn{width:100%}
            .buttons{width:100%}
            .section-head{align-items:flex-start;flex-direction:column}
            .features{gap:15px}
            .feature{min-height:210px;padding:25px}
            .form-grid{grid-template-columns:1fr}
            .field.full{grid-column:auto}
            .form-actions{align-items:stretch;flex-direction:column}
            .footer-top{grid-template-columns:1fr}
            .footer-bottom{flex-direction:column}
        }
    </style>
</head>

<body id="top">

{% with messages = get_flashed_messages() %}
    {% if messages %}
        <div class="flash">{{ messages[-1] }}</div>
    {% endif %}
{% endwith %}

<header>
    <div class="container nav">
        <a href="#top" class="brand">Actualize<span>Web</span></a>

        <nav class="menu" id="menu">
            <a href="#services">Services</a>
            <a href="#work">Our Work</a>
            <a href="#difference">Why Us</a>
            <a href="#stories">Stories</a>
            <a href="#quote">Start a Project</a>
        </nav>

        <button class="menu-toggle" onclick="toggleMenu()" aria-label="Open menu">☰</button>
    </div>
</header>

<main>

    <!-- HERO -->
    <section class="hero">
        <div class="container">

            <div class="hero-visual" aria-label="Website dashboard preview">
                <div class="screen">
                    <div class="screen-top">
                        <i class="dot"></i><i class="dot"></i><i class="dot"></i>
                        <span style="margin-left:auto;font-size:7px;color:#777">ACTUALIZEWEB DASHBOARD</span>
                    </div>
                    <div class="dashboard">
                        <div class="chart-box">
                            <div style="font-size:9px;color:#9ba8c6">Website visits</div>
                            <div class="chart">
                                <i class="bar" style="height:35%"></i>
                                <i class="bar" style="height:48%"></i>
                                <i class="bar" style="height:42%"></i>
                                <i class="bar" style="height:66%"></i>
                                <i class="bar" style="height:53%"></i>
                                <i class="bar" style="height:82%"></i>
                                <i class="bar" style="height:73%"></i>
                                <i class="bar" style="height:95%"></i>
                            </div>
                        </div>
                        <div class="mini-stack">
                            <div class="mini-box">
                                <div style="font-size:8px;color:#9ba8c6">New leads</div>
                                <div class="mini-line" style="width:82%"></div>
                                <div class="mini-line"></div>
                            </div>
                            <div class="mini-box">
                                <div style="font-size:8px;color:#9ba8c6">Bookings</div>
                                <div class="mini-line" style="width:55%"></div>
                                <div class="mini-line" style="width:80%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="laptop-base"></div>

                <div class="launch-card">
                    <strong>Site Just Launched</strong>
                    <p>Salon Booking — Delivered in 5 days</p>
                </div>
            </div>

            <div class="eyebrow">Digital Growth Partner</div>

            <h1>We Build Your<br><span>Business Online</span></h1>

            <p class="hero-copy">
                From booking pages to client dashboards — ActualizeWeb delivers
                fast, custom websites that work hard for your business.
                You own it forever. No subscriptions. No lock-in.
            </p>

            <div class="pills">
                <span class="pill">◈ Lifetime Ownership</span>
                <span class="pill">⊘ No Monthly Fees</span>
                <span class="pill">ϟ Fast Delivery</span>
            </div>

            <div class="buttons">
                <a href="#quote" class="btn btn-primary">Launch My Website</a>
                <a href="#work" class="btn btn-outline">View Our Work</a>
            </div>
        </div>
    </section>

    <!-- STATS -->
    <section style="padding-top:0">
        <div class="container">
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">50+</div>
                    <div class="stat-label">Projects Delivered</div>
                </div>
                <div class="stat">
                    <div class="stat-number">7 Days</div>
                    <div class="stat-label">Average Launch Time</div>
                </div>
                <div class="stat">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Client Ownership</div>
                </div>
            </div>
        </div>
    </section>

    <!-- FEATURES -->
    <section id="services" class="dark-section">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="eyebrow">What We Build</div>
                    <h2>Tools That Run<br>Your Business</h2>
                    <p class="section-intro">
                        Custom-built features — not generic templates — designed
                        to convert visitors into paying clients.
                    </p>
                </div>
                <a href="#quote" class="small-link">Get a Free Quote →</a>
            </div>

            <div class="features">
                <article class="feature">
                    <div class="icon">▦</div>
                    <h3>Smart Booking</h3>
                    <p>Client-facing appointment pages with time slots, service selection, and confirmation flows — no third-party app required.</p>
                </article>
                <article class="feature">
                    <div class="icon">⌁</div>
                    <h3>Business Monitoring</h3>
                    <p>Dashboards showing visit trends, inquiry volume, and lead sources — so you always know what's working.</p>
                </article>
                <article class="feature">
                    <div class="icon">♧</div>
                    <h3>Client Notifications</h3>
                    <p>Automated email and WhatsApp nudges that remind clients, confirm bookings, and re-engage dormant leads.</p>
                </article>
                <article class="feature">
                    <div class="icon">▢</div>
                    <h3>Safe Client Tools</h3>
                    <p>Secure portals, encrypted data handling, and SSL-protected pages — trust built in from day one.</p>
                </article>
            </div>
        </div>
    </section>

    <!-- WORK -->
    <section id="work">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="eyebrow">Recent Work</div>
                    <h2>Built for Real Businesses</h2>
                </div>
                <a href="#quote" class="small-link">Request Yours</a>
            </div>

            <div class="work-grid">
                <article class="work-card">
                    <div class="work-image" style="background-image:linear-gradient(rgba(5,10,14,.20),rgba(5,10,14,.70)),url('https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1200&q=85');background-size:cover;background-position:center;">
                        <div class="mock-screen"></div>
                    </div>
                    <div class="work-body">
                        <h3>Salon & Spa Booking</h3>
                        <p>Elegant service pages, live appointment booking and confirmation flows that turn visitors into appointments.</p>
                    </div>
                </article>
                <article class="work-card">
                    <div class="work-image" style="background-image:linear-gradient(rgba(5,10,14,.15),rgba(5,10,14,.72)),url('https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=85');background-size:cover;background-position:center;">
                        <div class="mock-screen" style="background:linear-gradient(140deg,#503021,#160d0a)"></div>
                    </div>
                    <div class="work-body">
                        <h3>Business & Lead Systems</h3>
                        <p>Clear enquiry journeys, lead capture and business information designed for local service owners.</p>
                    </div>
                </article>
                <article class="work-card">
                    <div class="work-image" style="background-image:linear-gradient(rgba(5,10,14,.12),rgba(5,10,14,.74)),url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=85');background-size:cover;background-position:center;">
                        <div class="mock-screen" style="background:linear-gradient(140deg,#234a3a,#07150f)"></div>
                    </div>
                    <div class="work-body">
                        <h3>Fitness & Membership</h3>
                        <p>Modern schedules, membership enquiries and customer tools that replace scattered manual workflows.</p>
                    </div>
                </article>
            </div>
        </div>
    </section>

    <!-- DIFFERENCE -->
    <section id="difference" class="dark-section">
        <div class="container difference">
            <div>
                <div class="eyebrow">Our Difference</div>
                <h2>Own It.<br>Grow With It.<br>Pay Once.</h2>
                <p class="section-intro">
                    Most agencies lock you in with monthly retainers. We flip that model.
                    You get a fully custom site, delivered fast, and it's yours permanently.
                </p>
                <ul class="check-list">
                    <li>Lifetime ownership — pay once, no recurring fees ever</li>
                    <li>Budget-friendly packages for solo owners and growing shops</li>
                    <li>7–14 day delivery — not months of back-and-forth</li>
                    <li>Mobile-first design — most clients browse on their phones</li>
                    <li>Post-launch support included — we don't disappear at handoff</li>
                </ul>
            </div>

            <div class="metric-grid">
                <div class="metric"><strong>50+</strong><span>Businesses Live<br>Across salons, clinics, gyms, and more</span></div>
                <div class="metric"><strong>7d</strong><span>Avg. Launch<br>From requirements to live in one week</span></div>
                <div class="metric"><strong>0</strong><span>Recurring Fees<br>No subscriptions. Not now, not ever.</span></div>
                <div class="metric"><strong>98%</strong><span>Client Satisfaction<br>Based on post-launch reviews</span></div>
            </div>
        </div>
    </section>

    <!-- STORIES -->
    <section id="stories">
        <div class="container">
            <div class="eyebrow">Client Stories</div>
            <h2>They Launched.<br>They Grew.</h2>

            <div class="stories" style="margin-top:45px">
                <article class="story">
                    <p class="quote">
                        “ActualizeWeb had my salon booking page live in 6 days.
                        The first week I went live, three new clients booked entirely
                        through the website. Absolutely worth it.”
                    </p>
                    <div class="person">
                        <strong>Meera Shah</strong>
                        Owner, Luminé Salon — Mumbai
                    </div>
                </article>
                <article class="story">
                    <p class="quote">
                        “My gym membership inquiries doubled within a month of launch.
                        The class schedule section alone replaced the three WhatsApp
                        groups I was managing manually.”
                    </p>
                    <div class="person">
                        <strong>Arjun Mehta</strong>
                        Founder, IronEdge Fitness — Pune
                    </div>
                </article>
            </div>
        </div>
    </section>

    <!-- CTA + FORM -->
    <section id="quote" class="cta">
        <div class="container">
            <div class="eyebrow">Let's Build Together</div>
            <h2>Your Website Starts Here</h2>
            <p>
                Tell us what your business does, who you serve, and what you need.
                We'll handle the rest — from design to launch — in days, not months.
            </p>

            <div class="quote-wrap">
                <form class="form" method="POST" action="{{ url_for('quote') }}">
                    <div class="form-grid">
                        <div class="field">
                            <label>Your Name</label>
                            <input name="name" required placeholder="Your full name">
                        </div>
                        <div class="field">
                            <label>Business Name</label>
                            <input name="business" required placeholder="Your business">
                        </div>
                        <div class="field">
                            <label>Email</label>
                            <input type="email" name="email" required placeholder="you@example.com">
                        </div>
                        <div class="field">
                            <label>Phone / WhatsApp</label>
                            <input name="phone" placeholder="+91 ...">
                        </div>
                        <div class="field full">
                            <label>Primary Goal</label>
                            <select name="goal">
                                <option>Bookings</option>
                                <option>Lead Generation</option>
                                <option>Portfolio / Brand Website</option>
                                <option>Business Information</option>
                                <option>Custom System / Dashboard</option>
                            </select>
                        </div>
                        <div class="field full">
                            <label>What Do You Need?</label>
                            <textarea name="message" placeholder="Tell us about your business, required pages/features, references, budget, etc."></textarea>
                        </div>
                    </div>

                    <div class="form-actions">
                        <div class="note">No commitment required. First consultation is free.</div>
                        <button class="btn btn-primary" type="submit">Get a Free Quote</button>
                    </div>
                </form>
            </div>
        </div>
    </section>

</main>

<footer>
    <div class="container">
        <div class="footer-top">
            <div class="footer-brand">
                <div class="brand">Actualize<span>Web</span></div>
                <p>We build custom business websites that you own forever. Fast delivery, zero monthly fees, real results.</p>
            </div>

            <div>
                <h4>Explore</h4>
                <ul class="footer-list">
                    <li><a href="#services">Services</a></li>
                    <li><a href="#work">Portfolio</a></li>
                    <li><a href="#difference">Why ActualizeWeb</a></li>
                </ul>
            </div>

            <div>
                <h4>We Build For</h4>
                <ul class="footer-list">
                    <li>Salons & Spas</li>
                    <li>Fitness Studios</li>
                    <li>Clinics & Doctors</li>
                    <li>Local Businesses</li>
                </ul>
            </div>

            <div>
                <h4>Contact</h4>
                <ul class="footer-list">
                    <li><a href="https://wa.me/918889056138" target="_blank">WhatsApp: +91 8889056138</a></li>
                    <li><a href="mailto:actualizeweb@gmail.com">actualizeweb@gmail.com</a></li>
                    <li>Response within 4 hours on business days</li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <span>© 2026 ActualizeWeb. All rights reserved.</span>
        </div>
    </div>
</footer>

<script>
function toggleMenu(){
    document.getElementById("menu").classList.toggle("open");
}
document.querySelectorAll("#menu a").forEach(a => {
    a.addEventListener("click", () => document.getElementById("menu").classList.remove("open"));
});
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/quote", methods=["POST"])
def quote():
    required = ["name", "business", "email"]
    if not all(request.form.get(field, "").strip() for field in required):
        flash("Please fill in your name, business name and email.")
        return redirect(url_for("home") + "#quote")

    try:
        save_quote(request.form)
        sheet_saved = save_to_google_sheet(request.form)
        if sheet_saved is False:
            flash("Request saved locally, but Google Sheets could not be reached. Check your Google Sheet webhook URL.")
        else:
            flash("Thanks! Your project request has been received.")
    except sqlite3.Error:
        flash("Something went wrong while saving your request. Please try again.")

    return redirect(url_for("home") + "#quote")


if __name__ == "__main__":
    init_db()
    app.run(
        debug=os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes"},
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
    )