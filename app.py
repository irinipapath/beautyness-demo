"""BEAUTYNESS — Beyond the Surface. Fictional, locally running Streamlit demo."""
import math
import random
from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="BEAUTYNESS | Beyond the Surface", page_icon="🌸", layout="wide", initial_sidebar_state="expanded")
PINK="#d65b80"; INK="#352e35"; CREAM="#fff9f7"; LILAC="#a18bbb"
st.markdown(f"""<style>
.stApp {{background:{CREAM};color:{INK}}}
.block-container {{padding-top:2rem;max-width:1250px}}
h1,h2,h3 {{letter-spacing:-.035em}}
[data-testid="stMetric"] {{background:white;border:1px solid #f1e5e7;border-radius:17px;padding:15px}}
[data-testid="stSidebar"] {{background:#f9eef1}}
div.stButton>button[kind="primary"] {{background:{PINK};border-color:{PINK}}}
.note {{background:#fff;border:1px solid #f0dfe5;border-left:4px solid {PINK};border-radius:14px;padding:15px;margin:10px 0}}
.eyebrow {{color:{PINK};font-weight:750;letter-spacing:.14em;font-size:12px}}
</style>""", unsafe_allow_html=True)

# Every value in this dataset is invented for the demonstration, including location weather and biomarkers.
@st.cache_data
def demo_data():
    rng=random.Random(42)
    dates=pd.date_range('2026-07-01','2026-10-18',freq='D')
    period_starts=[date(2026,7,21),date(2026,8,4),date(2026,9,9),date(2026,10,11)]
    # Irregular spacing mirrors the visual example; do not use this for fertility or phase prediction.
    records=[]
    for t in dates:
        d=t.date(); days_since=min((d-p).days for p in period_starts if d>=p) if any(d>=p for p in period_starts) else -99
        on_period=any(0 <= (d-p).days < (4 if p.month==7 else (3 if p.month==8 else 4 if p.month==9 else 2)) for p in period_starts)
        near_period=any(-3 <= (d-p).days <= 3 for p in period_starts)
        sleep=round(max(4.8,min(9.2,rng.gauss(7.2,0.85))),1)
        stress=max(1,min(10,round(rng.gauss(5.1,1.7))))
        temp=round(25-0.13*(t-dates[0]).days+3*math.sin((t-dates[0]).days/10)+rng.uniform(-2,2),1)
        humidity=max(30,min(92,round(61+15*math.sin((t-dates[0]).days/12)+rng.gauss(0,7))))
        uv=max(1,round(7-0.045*(t-dates[0]).days+rng.uniform(-1,1),1))
        breakouts=max(0,min(10,round(1.4+(3.1 if near_period else 0)+(0.8 if sleep<6.5 else 0)+rng.gauss(0,.85))))
        redness=max(0,min(10,round(2.8+(1.1 if stress>=7 else 0)+rng.gauss(0,.9))))
        oiliness=max(0,min(10,round(5.8+(1 if near_period else 0)+rng.gauss(0,1))))
        water=round(max(.6,min(3.5,rng.gauss(1.8,.45))),1)
        records.append(dict(date=t,sleep_hours=sleep,stress=stress,breakouts=breakouts,redness=redness,oiliness=oiliness,water_l=water,temperature_c=temp,humidity_pct=humidity,uv_index=uv,period=on_period,near_period=near_period,steps=round(rng.uniform(4200,11500))))
    return pd.DataFrame(records),period_starts

df,period_starts=demo_data()
st.sidebar.markdown("<div class='eyebrow'>BEAUTYNESS</div>",unsafe_allow_html=True)
st.sidebar.title("Beyond the Surface")
st.sidebar.caption("Milan, Italy")
page=st.sidebar.radio("Explore",["Beauty ID","Your Data","My Routine","Inside Out","Let's Chat"],label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.warning("**FICTIONAL DEMO** — all measurements, history, products, weather and biomarker values are invented. No clinical or AI skin analysis is performed.")
st.sidebar.caption("Screenshots supplied by the user informed the interface concepts. This demo does not copy, verify or import private cycle records or third-party skin scores.")

if 'goals' not in st.session_state: st.session_state.goals=['Calm redness','Reduce breakouts']
if 'skin' not in st.session_state: st.session_state.skin='Oily / combination'
if 'routine_done' not in st.session_state: st.session_state.routine_done=[]
if 'messages' not in st.session_state: st.session_state.messages=[]

st.markdown("<div class='eyebrow'>BEAUTY THAT EVOLVES WITH YOU</div>",unsafe_allow_html=True)

def note(title,body): st.markdown(f'<div class="note"><b>{title}</b><br>{body}</div>',unsafe_allow_html=True)
def trend_chart(data,columns,title,yaxis="Self-reported severity (0–10)"):
    fig=go.Figure()
    for col,label,color in columns:
        fig.add_trace(go.Scatter(x=data.date,y=data[col],name=label,mode='lines',line=dict(color=color,width=2.6)))
    for p in period_starts:
        if data.date.min().date()<=p<=data.date.max().date(): fig.add_vrect(x0=str(p),x1=str(p+timedelta(days=2)),fillcolor=PINK,opacity=.11,line_width=0)
    fig.update_layout(title=title,height=330,margin=dict(l=10,r=10,t=45,b=15),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',yaxis_title=yaxis,legend=dict(orientation='h',y=-.3),hovermode='x unified')
    st.plotly_chart(fig,use_container_width=True)

def recent_data():
    days=st.select_slider("Timeline",options=[14,30,60,110],value=60,format_func=lambda x:f"Last {x} days")
    return df.tail(days)

if page=="Beauty ID":
    st.title("Your beauty, today.")
    st.caption("Hi Irini, wishing you a beautiful day and a glowing complexion!")
    a,b,c,d=st.columns(4)
    a.metric("Latest skin profile",st.session_state.skin)
    b.metric("Sleep last night",f"{df.iloc[-1].sleep_hours:.1f} h")
    c.metric("Milan UV index",f"{df.iloc[-1].uv_index:.1f}")
    d.metric("Next photo check-in","Sunday")
    left,right=st.columns([1.5,1])
    with left:
        st.subheader("Your daily edit")
        note("☀️ Weather-aware care","Milan's UV reading suggests planning sun protection. Use broad-spectrum SPF 30+ and reapply as appropriate when outdoors.")
        note("🌙 Sleep context",f"You logged {df.iloc[-1].sleep_hours:.1f} hours of sleep. Notice how you feel today; a single night does not explain skin changes.")
        note("🌸 Cycle-aware observation","Your period log includes October 11–12. Compare breakouts around recorded dates in Your Data; patterns are observations, not proof of causation.")
        note("📷 Weekly ritual","Take a makeup-free photo in similar lighting, angle and distance. Note redness, breakouts and any new products.")
    with right:
        st.subheader("Your Beauty ID")
        with st.form("profile"):
            skin=st.selectbox("Self-reported skin type",["Oily / combination","Dry","Normal","Sensitive","Unsure"],index=["Oily / combination","Dry","Normal","Sensitive","Unsure"].index(st.session_state.skin))
            goals=st.multiselect("Your beauty goals",["Calm redness","Reduce breakouts","Support hydration","Simplify routine","Hair care","Makeup confidence"],default=st.session_state.goals)
            submitted=st.form_submit_button("Save profile",type="primary")
            if submitted: st.session_state.skin=skin;st.session_state.goals=goals;st.success("Profile updated for this session")
        st.markdown("**Current goals:** "+(", ".join(st.session_state.goals) or "Choose your goals above"))
        st.caption("Skin type and concerns are user-entered for the demo. No image-derived diagnosis is implied.")

elif page=="Your Data":
    st.title("Your Data")
    st.caption("See your evolution: weekly check-ins, skin trends and optional life context")
    selection=recent_data()
    x,y,z=st.columns(3)
    x.metric("Avg. breakouts · sample",f"{selection.breakouts.mean():.1f} / 10")
    y.metric("Avg. sleep · sample",f"{selection.sleep_hours.mean():.1f} h")
    z.metric("Photo check-ins · sample","12")
    trend_chart(selection,[("breakouts","Breakouts",PINK),("redness","Redness",LILAC)],"Skin changes over time (pink shading = logged period)")
    avg_near=df.loc[df.near_period,'breakouts'].mean();avg_other=df.loc[~df.near_period,'breakouts'].mean()
    note("🌸 Possible cycle pattern",f"Your breakouts average <b>{avg_near:.1f}/10</b> within three days of logged period starts versus <b>{avg_other:.1f}/10</b> on other days.")
    a,b=st.columns(2)
    with a:
        fig=px.scatter(selection,x='sleep_hours',y='breakouts',color='near_period',color_discrete_map={True:PINK,False:LILAC},labels={'sleep_hours':'Sleep (hours)','breakouts':'Breakouts (0–10)','near_period':'Near period'},title="Sleep vs. breakouts · exploratory")
        fig.update_layout(height=350,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.scatter(selection,x='humidity_pct',y='redness',color='stress',color_continuous_scale='Purples',labels={'humidity_pct':'Humidity (%)','redness':'Redness (0–10)','stress':'Stress (0–10)'},title="Milan humidity vs. redness · exploratory")
        fig.update_layout(height=350,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig,use_container_width=True)
    st.subheader("Weekly skin check-in")
    with st.form('checkin'):
        photo=st.file_uploader("Optional photo (shown locally, not analyzed)",type=['jpg','jpeg','png'])
        breakout=st.slider("How noticeable are breakouts today?",0,10,3)
        redness=st.slider("How noticeable is redness today?",0,10,3)
        observation=st.text_area("What changed this week?",placeholder="New product, stress, sleep, travel, etc.")
        saved=st.form_submit_button("Preview check-in")
    if saved:
        st.success(f"Check-in preview: breakouts {breakout}/10, redness {redness}/10. This is not saved permanently.")
        if photo:st.image(photo,caption="Your uploaded photo — not analyzed",width=260)
        if observation:st.write("Your note:",observation)
    st.caption("For real longitudinal tracking, photo consent, storage, consistent conditions and validated methods would be needed.")

elif page=="My Routine":
    st.title("My Routine")
    am,pm=st.columns(2)
    with am:
        st.subheader("☀️ Morning")
        st.checkbox("Gentle cleanser",key='am1')
        st.checkbox("Lightweight moisturizer",key='am2')
        st.checkbox("Broad-spectrum SPF 30+",key='am3')
    with pm:
        st.subheader("🌙 Evening")
        st.checkbox("Remove makeup / cleanse",key='pm1')
        st.checkbox("Moisturizer",key='pm2')
        st.checkbox("Record reactions to new products",key='pm3')
    st.subheader("Personalized focus")
    if 'Calm redness' in st.session_state.goals:note("Focus: comfort","Avoid introducing many new active ingredients at once. Persistent or worsening redness warrants professional assessment.")
    if 'Reduce breakouts' in st.session_state.goals:note("Focus: consistency","Keep your routine simple while tracking breakouts and potential irritants. A dermatologist can assess persistent acne.")
    if 'Support hydration' in st.session_state.goals:note("Focus: hydration","Choose a moisturizer that feels comfortable and suits your preferences.")
    st.subheader("Product discovery · fictional catalogue")
    st.dataframe(pd.DataFrame([['Gentle Cloud Cleanser','Cleanser','€18'],['Daily Veil SPF 50','Sunscreen','€24'],['Barrier Comfort Cream','Moisturizer','€26'],['Soft Finish Tint','Makeup','€29'] ],columns=['Fictional BEAUTYNESS product','Category','Illustrative price']),hide_index=True,use_container_width=True)
    st.caption("Products and prices are invented; buttons for purchasing are not connected to a shop.")

elif page=="Inside Out":
    st.title("Inside Out")
    st.caption("Optional context, entered here and explored alongside skin trends in Your Data")
    tabs=st.tabs(['Cycle','Lifestyle & wearables','Milan environment','Biomarkers'])
    with tabs[0]:
        st.subheader("Menstrual cycle diary ")
        st.write("Sample logged starts: **21 Jul · 4 Aug · 9 Sep · 11 Oct 2026**")
        period_table=pd.DataFrame([{'Logged period start':p.isoformat(),'Source':'Fictional sample entry'} for p in period_starts])
        st.dataframe(period_table,hide_index=True,use_container_width=True)
        note("Privacy first","Cycle tracking should be entirely opt-in, removable, and not used to predict fertility or diagnose hormonal conditions in this demo.")
    with tabs[1]:
        st.subheader("Lifestyle context")
        week=df.tail(21)
        trend_chart(week,[("sleep_hours","Sleep (hours)",LILAC)],"Sleep over the last three weeks", "Hours")
        c1,c2,c3=st.columns(3)
        c1.metric('Avg. sleep · sample',f'{week.sleep_hours.mean():.1f} h')
        c2.metric('Avg. steps · sample',f'{week.steps.mean():,.0f}')
        c3.metric('Avg. water · sample',f'{week.water_l.mean():.1f} L')
        st.caption('These are generated wearable-style and self-reported figures, not connected to Apple Health or Oura.')
    with tabs[2]:
        st.subheader("Milan weather · invented historical series")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=df.date,y=df.temperature_c,name='Temperature °C',line=dict(color=PINK)))
        fig.add_trace(go.Scatter(x=df.date,y=df.humidity_pct,name='Humidity %',yaxis='y2',line=dict(color=LILAC)))
        fig.update_layout(height=360,yaxis=dict(title='Temperature °C'),yaxis2=dict(title='Humidity %',overlaying='y',side='right'),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(orientation='h',y=-.25))
        st.plotly_chart(fig,use_container_width=True)
        note('Environment is context, not diagnosis','UV, temperature and humidity can inform practical reminders. This chart is fabricated for the Milan scenario, not historical weather observations.')
    with tabs[3]:
        st.subheader('Bloodwork and biomarkers · fictional examples')
        labs=pd.DataFrame([['Ferritin','2026-03-15','32','µg/L'],['Ferritin','2026-09-15','38','µg/L'],['Vitamin D','2026-03-15','26','ng/mL'],['Vitamin D','2026-09-15','30','ng/mL'],['TSH','2026-09-15','2.1','mIU/L']],columns=['Marker','Sample date','Value','Unit'])
        st.dataframe(labs,hide_index=True,use_container_width=True)
        note('Clinical interpretation required','These invented values are not a diagnosis or a recommendation to test, supplement or treat. Real interpretation requires symptoms, lab-specific ranges and qualified clinical review.')

else:
    st.title("Let's Chat")
    st.caption('Guided demonstration — no external AI API is connected')
    choices=['Why might I be breaking out near my period?','How can I build a simple makeup routine?','What should I know about Botox or fillers?','What do my blood tests mean?']
    choice=st.selectbox('Choose a sample question',choices)
    answers={
        choices[0]:"More breakouts seem to appear around recorded period dates. Hormonal changes can be one possible factor, but these data cannot establish a cause. Track for longer and consider a dermatologist if acne is persistent or troubling.",
        choices[1]:"Start with your preferred finish, coverage and skin comfort. For oily or redness-prone skin, consider lightweight formulas and avoid products that irritate you. Product choices should also reflect shade match, budget and personal style.",
        choices[2]:"Botox and fillers are medical procedures with potential benefits, risks and contraindications. A qualified clinician should discuss your goals, alternatives, expected results and complications before any decision.",
        choices[3]:"Bloodwork cannot be interpreted safely from an isolated number. A qualified clinician can review symptoms, reference ranges, medical history and whether testing was indicated."
    }
    if st.button('Ask BEAUTYNESS',type='primary'):
        st.session_state.messages.append((choice,answers[choice]))
    for question,answer in reversed(st.session_state.messages):
        with st.chat_message('user'):st.write(question)
        with st.chat_message('assistant'):st.write(answer)
    st.divider()
    st.subheader('Expert Connect · future service')
    st.write('Explore dermatology, aesthetic medicine and other qualified professional consultations. Scheduling and clinical care are not implemented in this prototype.')

st.divider()
st.caption('BEAUTYNESS • Beyond the Surface | Student strategy prototype | All data synthetic. This app does not diagnose, provide medical treatment, or use an AI skin model.')
