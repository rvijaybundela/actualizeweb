from flask import Flask, render_template_string

# Design reference used:
# "ActualizeWeb — We Build Your Business Online (provided PDF)"
# The layout, content structure, dark/orange visual language, cards,
# CTA style and section flow are recreated as a Flask implementation.

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

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
            background:rgba(13,13,13,.94);
            backdrop-filter:blur(14px);
            border-bottom:1px solid #6b2c19;
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
            color:#ddd;
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
            padding:86px 0 110px;
            display:flex;
            align-items:center;
        }
        .hero-layout{
            display:grid;
            grid-template-columns:minmax(0,1.08fr) minmax(360px,.92fr);
            gap:58px;
            align-items:center;
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
        .hero-layout .hero-visual{width:100%;margin:0;height:390px}
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
        .dark-section{background:#1e1e1e}
        .section-head{display:flex;justify-content:space-between;align-items:end;gap:30px;margin-bottom:48px}
        h2{
            font-size:clamp(38px,5vw,60px);
            line-height:1;
            letter-spacing:-.045em;
        }
        .section-intro{max-width:680px;color:#aaa;font-size:16px;margin-top:16px}
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
        .check-list li:before{content:"";width:24px;height:24px;flex:none;border:1px solid #71351f;border-radius:50%;background:#2a1b14 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23e95b27' stroke-width='2.5'%3E%3Cpath d='m7 12 3 3 7-7'/%3E%3C/svg%3E") center/14px no-repeat}
        .metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#333}
        .metric{background:#111;padding:32px}
        .metric strong{font-size:43px;display:block;color:var(--orange);font-weight:500;letter-spacing:-.03em}
        .metric span{font-size:12px;color:var(--cream);line-height:1.7}

        .stories{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
        .story{
            background:#121212;
            border:1px solid #333;
            border-radius:15px;
            padding:34px;
        }
        .quote{font-size:18px;line-height:1.8;color:#e8e1d8;margin-bottom:25px}
        .person{font-size:12px;color:#aaa}
        .person strong{color:#eee;display:block;margin-bottom:4px}
        .person{position:relative;padding-left:48px;min-height:38px}
        .person:before{content:"";position:absolute;left:0;top:0;width:34px;height:34px;border-radius:50%;border:2px solid var(--orange);background:linear-gradient(145deg,#e8c1a2,#453029)}

        .cta{
            text-align:center;
            background:
                radial-gradient(circle at 50% 0%,rgba(241,90,36,.14),transparent 45%),
                #111;
            border-top:1px solid #3a2118;
            border-bottom:1px solid #3a2118;
        }
        .cta p{max-width:650px;margin:18px auto 30px;color:#aaa}
        footer{padding:65px 0 25px;background:#db5b2b}
        .footer-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:45px;padding-bottom:50px}
        .footer-brand p{max-width:330px;color:#888;font-size:13px;margin-top:15px}
        footer h4{font-size:12px;color:#fff;margin-bottom:16px}
        footer a,footer li{color:#fff;font-size:12px;margin-bottom:9px}
        footer a:hover{color:var(--orange)}
        footer .footer-brand p{color:rgba(255,255,255,.9)}
        footer a:hover{color:#17130a}
        .footer-list{list-style:none}
        .footer-bottom{
            border-top:1px solid rgba(255,255,255,.35);
            padding-top:22px;
            display:flex;
            justify-content:space-between;
            gap:20px;
            color:rgba(255,255,255,.8);
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

        @keyframes softRise{
            from{opacity:0;transform:translateY(18px)}
            to{opacity:1;transform:translateY(0)}
        }
        @keyframes softPulse{
            0%,100%{box-shadow:0 12px 30px rgba(244,202,67,.18)}
            50%{box-shadow:0 16px 42px rgba(244,202,67,.34)}
        }
        .hero-copy-block,.hero-visual{animation:softRise .75s ease both}
        .hero-visual{animation-delay:.12s}
        .btn-primary{animation:softPulse 3.8s ease-in-out infinite}
        .btn,.feature,.work-card,.story,.metric,.small-link{
            -webkit-tap-highlight-color:transparent;
            transition:transform .25s ease,box-shadow .25s ease,filter .25s ease,border-color .25s ease;
        }
        .btn:active{transform:translateY(2px) scale(.97);filter:brightness(.96)}
        .feature:active,.work-card:active,.story:active,.metric:active{transform:translateY(2px) scale(.99)}
        @media(prefers-reduced-motion:reduce){
            *,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}
        }

        /* Premium depth / 3D presentation */
        .hero-visual{
            transform:perspective(1200px) rotateX(2deg) rotateY(-2deg);
            transition:transform .6s ease, box-shadow .6s ease;
            box-shadow:0 35px 90px rgba(0,0,0,.58), 0 0 0 1px rgba(241,90,36,.16), 0 0 70px rgba(241,90,36,.08);
        }
        .hero-visual:hover{transform:perspective(1200px) rotateX(0deg) rotateY(0deg) translateY(-7px) scale(1.01);}
        .screen{transform:translateZ(25px);}
        .feature,.work-card,.story,.metric{
            transform:translateZ(0);
            transition:transform .35s ease, box-shadow .35s ease, border-color .35s ease;
        }
        .feature:hover,.work-card:hover,.story:hover,.metric:hover{
            transform:perspective(900px) rotateX(1deg) translateY(-8px);
            box-shadow:0 24px 55px rgba(0,0,0,.24);
            border-color:rgba(241,90,36,.65);
        }
        #services .section-head{text-align:center;display:block}
        #services .section-intro{max-width:680px;margin:18px auto 0}
        #services .small-link{display:none}
        #services .features{grid-template-columns:repeat(4,1fr);gap:30px;margin-top:68px}
        #services .feature{min-height:350px}
        .work-image{position:relative;overflow:hidden;}
        .work-image:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.13),transparent 32%,transparent 68%,rgba(241,90,36,.13));pointer-events:none;z-index:2;}
        .work-card:hover .work-image{transform:scale(1.01);}
        .work-card:hover .work-image[style]{background-position:center;}

        @media(max-width:850px){
            .container{width:min(var(--max),calc(100% - 34px))}
            .menu{display:none;position:absolute;left:0;right:0;top:86px;background:#111;padding:20px;flex-direction:column;align-items:flex-start;border-bottom:1px solid #5d2817}
            .menu.open{display:flex}
            .menu-toggle{display:block}
            .hero{min-height:auto;padding-top:60px}
            .hero-layout{grid-template-columns:1fr;gap:36px}
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
            .footer-top{grid-template-columns:1fr}
            .footer-bottom{flex-direction:column}
        }

        /* Reference theme: one consistent dark editorial system. */
        :root{
            --bg:#0e0e0e;
            --panel:#1d1d1d;
            --panel-2:#171717;
            --line:#73341f;
            --orange:#e95b27;
            --orange-soft:#c9481d;
            --cream:#f4efe7;
            --muted:#aaa39b;
            --yellow:#f4ca43;
            --max:1148px;
        }
        body{background:var(--bg);color:var(--cream);font-family:Inter,Arial,sans-serif}
        body:before{width:680px;height:680px;right:-300px;top:270px;background:radial-gradient(circle,rgba(233,91,39,.10),transparent 68%)}
        header{height:94px;background:rgba(14,14,14,.96);border-bottom:1px solid var(--orange);box-shadow:none}
        .nav{height:94px}
        .brand{font-size:24px;letter-spacing:.01em;white-space:nowrap}
        .brand span{color:var(--orange)}
        .menu{gap:28px;color:var(--cream);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
        .menu a{transition:color .2s ease}
        .menu a:last-child{background:var(--yellow);color:#17130a;border-radius:999px;padding:16px 19px}
        .menu a:last-child:hover{color:#17130a;filter:brightness(1.05)}
        .hero{min-height:720px;padding:98px 0 92px}
        .hero-layout{grid-template-columns:minmax(0,1fr) minmax(400px,.95fr);gap:74px}
        .hero-copy-block{padding-top:18px}
        .eyebrow{color:var(--orange);font-size:14px;letter-spacing:.24em;margin-bottom:27px}
        h1{font-size:clamp(58px,7.2vw,92px);line-height:.93;letter-spacing:-.065em;margin-bottom:31px}
        h1 span{color:var(--orange)}
        .hero-copy{max-width:610px;color:#e7e1da;font-size:17px;line-height:1.75;letter-spacing:.015em;margin-bottom:29px}
        .pills{gap:12px;margin-bottom:37px}
        .pill{border-color:var(--orange);color:var(--orange);padding:10px 16px;font-size:11px}
        .btn{min-height:54px;padding:0 29px;font-size:12px;letter-spacing:.12em}
        .btn-primary{background:var(--yellow);border-color:var(--yellow)}
        .btn-outline{border-color:var(--orange);color:var(--orange)}
        .hero-layout .hero-visual{height:382px;border-color:var(--orange);border-radius:18px}
        section{padding:118px 0}
        .dark-section{background:#1b1b1b}
        .section-head{margin-bottom:52px}
        h2{font-size:clamp(43px,5.2vw,67px);line-height:.94;letter-spacing:-.06em}
        .section-intro{color:#aaa39b;font-size:15px;line-height:1.75}
        .small-link{color:var(--orange);font-size:13px}
        .stats{border-color:#3c3c3c}
        .stat{padding:39px 20px;border-color:#3c3c3c}
        .stat-number{font-size:55px}
        .stat-label{color:#aaa39b}
        .features{gap:20px}
        .feature{min-height:235px;background:#121212;border-color:#71351f;border-radius:16px;padding:33px}
        .feature:hover{border-color:var(--orange)}
        .icon{background:#2a1911;color:var(--orange)}
        .feature p{color:#b8b0a8}
        .work-grid{grid-template-columns:repeat(3,1fr);gap:28px}
        .work-card{min-height:350px;background:#191919;border-color:#61301f;border-radius:15px}
        .work-image{height:245px}
        .work-body{padding:23px 25px}
        .work-body p{color:#aaa39b}
        .difference{gap:92px}
        .metric-grid{gap:1px;background:#3c3c3c}
        .metric{background:#121212;padding:35px}
        .stories{grid-template-columns:repeat(4,1fr);gap:20px}
        .story{background:#1b1b1b;border-color:#73341f;border-radius:15px;padding:31px}
        .quote{font-size:17px;color:#e8e1d8}
        .cta{background:radial-gradient(circle at 72% 0%,rgba(233,91,39,.13),transparent 40%),#111;border-color:#3a2118}
        footer{background:#db5b2b}
        .stats .stat-number{color:var(--orange);font-size:43px;font-weight:500;letter-spacing:-.03em}
        .stats .stat-label{color:var(--cream);font-size:15px}
        .stats .stat{padding:48px 20px}
        .stats{border-top:1px solid var(--orange);border-bottom:0}
        .stats .stat{border-right:0}
        .icon svg,.contact-icon svg{width:24px;height:24px;display:block}
        .portfolio-grid{
            display:grid;
            grid-template-columns:1.35fr .8fr .8fr;
            grid-template-rows:196px 196px 196px;
            gap:16px;
        }
        .portfolio-item{
            min-height:0;
            border:1px solid rgba(233,91,39,.8);
            border-radius:10px;
            background-size:cover;
            background-position:center;
            box-shadow:0 18px 40px rgba(0,0,0,.2);
            transition:transform .3s ease,filter .3s ease;
        }
        .portfolio-item:hover{transform:translateY(-5px);filter:saturate(1.12)}
        .portfolio-salon{grid-column:1 / 3;background-image:linear-gradient(rgba(10,12,20,.12),rgba(10,12,20,.25)),url('https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1400&q=90')}
        .portfolio-fitness{grid-column:3;grid-row:1 / 3;background-image:linear-gradient(rgba(9,10,30,.1),rgba(9,10,30,.35)),url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1000&q=90')}
        .portfolio-finance{grid-column:1;grid-row:2;background-image:linear-gradient(rgba(7,14,25,.12),rgba(7,14,25,.25)),url('https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1000&q=90')}
        .portfolio-store{grid-column:2;grid-row:2;background-image:linear-gradient(rgba(8,10,12,.08),rgba(8,10,12,.2)),url('https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&w=1000&q=90')}
        .portfolio-code{grid-column:1 / 3;grid-row:3;background-image:linear-gradient(rgba(8,10,12,.05),rgba(8,10,12,.18)),url('https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1400&q=90')}
        .portfolio-restaurant{grid-column:3;grid-row:3;background-image:linear-gradient(rgba(8,10,12,.04),rgba(8,10,12,.18)),url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1000&q=90')}
        .contact-layout{display:grid;grid-template-columns:1fr 1fr;gap:86px;align-items:center}
        .contact-copy h2{margin-bottom:28px}
        .contact-copy>p{max-width:600px;color:#e8e1da;font-size:17px;line-height:1.75}
        .contact-details{display:grid;gap:21px;margin-top:38px}
        .contact-detail{display:flex;align-items:center;gap:15px}
        .contact-icon{width:52px;height:52px;display:grid;place-items:center;border:1px solid #73341f;border-radius:11px;background:#2a1b14;color:var(--orange);font-size:23px}
        .contact-detail small,.contact-detail strong{display:block}
        .contact-detail small{font:500 11px "DM Mono",monospace;color:#ddd;text-transform:none;margin-bottom:4px}
        .contact-detail strong{font-size:13px;color:var(--cream)}
        .contact-card{background:#111;border:1px solid var(--orange);border-radius:16px;padding:42px}
        .contact-card h3{font-size:27px;line-height:1.15;margin-bottom:12px}
        .contact-card>p{color:#e1dcd5;font-size:13px;line-height:1.7}
        .contact-card ul{list-style:none;display:grid;gap:14px;margin:30px 0}
        .contact-card li{font-size:13px;color:#e1dcd5;padding-left:20px;position:relative}
        .contact-card li:before{content:"";width:7px;height:7px;border-radius:50%;background:var(--orange);position:absolute;left:0;top:8px}
        .contact-actions{display:flex;gap:14px}
        .contact-actions .btn{flex:1;text-align:center}
        .contact-note{text-align:center;margin-top:23px!important;font-size:12px!important}
        @media(max-width:850px){
            header,.nav{height:78px}
            .menu{top:78px}
            .hero{padding-top:65px}
            .hero-layout{grid-template-columns:1fr;gap:42px}
            .stories{grid-template-columns:repeat(2,1fr)}
            .hero-layout .hero-visual{height:300px}
            #services .features{grid-template-columns:repeat(2,1fr);gap:16px;margin-top:42px}
            .portfolio-grid{grid-template-columns:1fr 1fr;grid-template-rows:170px 170px 170px}
            .portfolio-salon{grid-column:1 / 3;grid-row:1}
            .portfolio-fitness{grid-column:1;grid-row:2 / 4}
            .portfolio-finance{grid-column:2;grid-row:2}
            .portfolio-store{grid-column:2;grid-row:3}
            .portfolio-code,.portfolio-restaurant{display:none}
            .contact-layout{grid-template-columns:1fr;gap:42px}
            .menu a:last-child{padding:0;background:none;color:var(--cream)}
        }
        @media(max-width:560px){
            #services .features{grid-template-columns:1fr                .portfolio-grid{grid-template-columns:1fr;grid-template-rows:220px 160px 160px 160px}
                .portfolio-item,.portfolio-salon,.portfolio-fitness,.portfolio-finance,.portfolio-store{grid-column:1;grid-row:auto}
                .portfolio-code,.portfolio-restaurant{display:block;grid-column:1;grid-row:auto}
                .contact-card{padding:25px}
                .contact-actions{flex-direction:column}
            }
            .stories{grid-template-columns:1fr}
        }
    </style>
</head>

<body id="top">
<header>
    <div class="container nav">
        <a href="#top" class="brand">Actualize<span>Web</span></a>

        <nav class="menu" id="menu">
            <a href="#services">Services</a>
            <a href="#portfolio">Portfolio</a>
            <a href="#why-us">Why Us</a>
            <a href="#testimonials">Testimonials</a>
            <a href="#contact">Start a Project</a>
        </nav>

        <button class="menu-toggle" onclick="toggleMenu()" aria-label="Open menu">☰</button>
    </div>
</header>

<main>

    <!-- HERO -->
    <section class="hero">
        <div class="container hero-layout">

            <div class="hero-copy-block">
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
                    <a href="#contact" class="btn btn-primary">Launch My Website</a>
                    <a href="#portfolio" class="btn btn-outline">View Our Work</a>
                </div>
            </div>

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
                <a href="#contact" class="small-link">Get a Free Quote →</a>
            </div>

            <div class="features">
                <article class="feature">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16M8 14h.01M12 14h.01M16 14h.01M8 17h.01M12 17h.01"/></svg></div>
                    <h3>Smart Booking</h3>
                    <p>Client-facing appointment pages with time slots, service selection, and confirmation flows — no third-party app required.</p>
                </article>
                <article class="feature">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 12h4l2-6 4 12 2-6h6"/></svg></div>
                    <h3>Business Monitoring</h3>
                    <p>Dashboards showing visit trends, inquiry volume, and lead sources — so you always know what's working.</p>
                </article>
                <article class="feature">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M18 8a4 4 0 0 0-7.2-2.4A4 4 0 1 0 7 13h10a4 4 0 0 0 1-5Z"/><path d="M12 13v7M9 20h6"/></svg></div>
                    <h3>Client Notifications</h3>
                    <p>Automated email and WhatsApp nudges that remind clients, confirm bookings, and re-engage dormant leads.</p>
                </article>
                <article class="feature">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg></div>
                    <h3>Safe Client Tools</h3>
                    <p>Secure portals, encrypted data handling, and SSL-protected pages — trust built in from day one.</p>
                </article>
            </div>
        </div>
    </section>

    <!-- WORK -->
    <section id="portfolio">
        <div class="container">
            <div class="section-head">
                <div>
                    <div class="eyebrow">Recent Work</div>
                    <h2>Built for Real Businesses</h2>
                </div>
                <a href="#contact" class="small-link">Request Yours</a>
            </div>

            <div class="portfolio-grid">
                <div class="portfolio-item portfolio-salon" aria-label="Salon website design"></div>
                <div class="portfolio-item portfolio-fitness" aria-label="Fitness website design"></div>
                <div class="portfolio-item portfolio-finance" aria-label="Finance dashboard design"></div>
                <div class="portfolio-item portfolio-store" aria-label="Online store website design"></div>
                <div class="portfolio-item portfolio-code" aria-label="Coding website design"></div>
                <div class="portfolio-item portfolio-restaurant" aria-label="Restaurant website design"></div>
            </div>
        </div>
    </section>

    <!-- DIFFERENCE -->
    <section id="why-us" class="dark-section">
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
    <section id="testimonials">
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
                        “I needed a credible website without agency pricing.
                        ActualizeWeb delivered a polished, fast site that my
                        enterprise clients actually compliment.”
                    </p>
                    <div class="person">
                        <strong>Rohit Verma</strong>
                        Principal, Verma Capital Advisory — Delhi
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
                <article class="story">
                    <p class="quote">
                        “Our clinic finally looks as professional online as it does
                        in person. New patients can find the right information and
                        reach us without calling around.”
                    </p>
                    <div class="person">
                        <strong>Dr. Priya Nair</strong>
                        Director, ClearPath Clinic — Bangalore
                    </div>
                </article>
            </div>
        </div>
    </section>

    <!-- CONTACT -->
    <section id="contact" class="cta">
        <div class="container contact-layout">
            <div class="contact-copy">
                <div class="eyebrow">Let's Build Together</div>
                <h2>Your Website<br>Starts Here</h2>
                <p>Tell us what your business does, who you serve, and what you need. We'll handle the rest — from design to launch — in days, not months.</p>
                <div class="contact-details">
                    <a href="https://wa.me/918889056138" target="_blank" rel="noopener" class="contact-detail">
                        <span class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 5h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H11l-5 3v-3H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z"/></svg></span>
                        <span><small>WhatsApp / Chat</small><strong>+91 88890 56138</strong></span>
                    </a>
                    <a href="mailto:ranvjbundela48@gmail.com" class="contact-detail">
                        <span class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg></span>
                        <span><small>Email Us</small><strong>info.actualizeweb@gmail.com</strong></span>
                    </a>
                    <div class="contact-detail">
                        <span class="contact-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 8v5l3 2"/></svg></span>
                        <span><small>Response Time</small><strong>Within 4 hours on business days</strong></span>
                    </div>
                </div>
            </div>
            <div class="contact-card">
                <h3>What We Need From You</h3>
                <p>Share these details over WhatsApp or email — we'll draft your proposal within 24 hours.</p>
                <ul>
                    <li>Your business name and what you do</li>
                    <li>Primary goal — bookings, leads, portfolio, or information</li>
                    <li>Sections or pages you'd like</li>
                    <li>Any website references you like</li>
                    <li>Rough budget range</li>
                </ul>
                <div class="contact-actions">
                    <a class="btn btn-primary" href="https://wa.me/918889056138?text=Hi%20ActualizeWeb%2C%20I%20want%20to%20start%20a%20website%20project." target="_blank" rel="noopener">Message on WhatsApp</a>
                    <a class="btn btn-outline" href="mailto:ranvjbundela48@gmail.com">Send an Email</a>
                </div>
                <p class="contact-note">No commitment required. First consultation is free.</p>
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
                    <li><a href="#portfolio">Portfolio</a></li>
                    <li><a href="#why-us">Why ActualizeWeb</a></li>
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
                    <li><a href="https://wa.me/918889056138" target="_blank">WhatsApp: +91 88890 56138</a></li>
                    <li><a href="mailto:ranvjbundela48@gmail.com">info.actualizeweb@gmail.com</a></li>
                    <li>Response within 4 hours on business days</li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <span>© 2026 ActualizeWeb. All rights reserved.</span>
            <span>Built with purpose — owned by you, forever.</span>
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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5006)
