import streamlit as st
from streamlit_lottie import st_lottie
from streamlit.components.v1 import html as components_html
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import plotly.express as px
import json, base64

# ----------------------- Config -----------------------
st.set_page_config(
    page_title="Rohan Kashyap — Data Science Portfolio",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------- Helpers -----------------------
@st.cache_data(show_spinner=False)
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def load_image_url(url: str):
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return Image.open(BytesIO(r.content))
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def load_lottie_file_b64(filepath: str):
    try:
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None

# ----------------------- CSS -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; scroll-behavior: smooth; }
#MainMenu, footer, header {visibility: hidden;}

.stApp { background: transparent; color: #E6EEF3; }
.block-container { max-width: 1200px; padding-top: 80px; padding-bottom: 80px; }

/* ---------- Background Overlay ---------- */
iframe[srcdoc*="LOTTIE_BG_MARKER"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: -9999 !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: none !important;
}
#bg-dim-overlay {
    position: fixed;
    inset: 0;
    z-index: -9998;
    pointer-events: none;
    background: linear-gradient(180deg, rgba(10,12,30,0.55), rgba(6,8,20,0.9));
}

/* ---------- Top Navigation ---------- */
.topnav {
    position: fixed;
    top: 0; left: 0; right: 0;
    padding: 14px 40px;
    z-index: 1000;
    background: rgba(15, 20, 35, 0.6);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.topnav .navlinks a {
    margin-left: 20px;
    text-decoration: none;
    color: #dbe9ff;
    font-weight: 500;
    transition: color 0.2s;
}
.topnav .navlinks a:hover { color: #7fb2ff; }

/* Mobile menu toggle */
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    color: #dbe9ff;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 8px;
    min-height: 44px;
    min-width: 44px;
}

.mobile-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(15, 20, 35, 0.95);
    backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.06);
    padding: 20px;
}

.mobile-menu.active {
    display: block;
}

.mobile-menu a {
    display: block;
    padding: 15px 0;
    text-decoration: none;
    color: #dbe9ff;
    font-weight: 500;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    transition: color 0.2s;
    min-height: 44px;
    font-size: 16px;
}

.mobile-menu a:hover { color: #7fb2ff; }
.mobile-menu a:last-child { border-bottom: none; }

/* ---------- Hero Section ---------- */
.hero-left h1 {
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.hero-left h3 {
    font-size: 1.2rem;
    color: #cfe6ff;
    font-weight: 400;
    max-width: 680px;
}
.metrics { display: flex; gap: 24px; margin-top: 8px; }
.metric { text-align: left; }

/* ---------- Glass Card ---------- */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 28px;
    margin-top: 18px;
}
.glass1 {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 28px;
    margin-top: 18px;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    margin-right: 6px;
    margin-bottom: 4px;
    border-radius: 8px;
    background: rgba(127,178,255,0.15);
    color: #9fc9ff;
    font-size: 12px;
    font-weight: 600;
}

/* ---------- Projects Grid ---------- */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 18px;
}
.project-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(8px);
    border-radius: 16px;
    padding: 20px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.project-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

/* ---------- Timeline ---------- */
.timeline {
    display: flex;
    flex-direction: column;
    gap: 18px;
    margin-top: 10px;
}
.timeline-item {
    padding-left: 16px;
    border-left: 3px solid #6f9bff;
    position: relative;
}
.timeline-item::before {
    content: "";
    position: absolute;
    left: -7px;
    top: 4px;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #6f9bff;
}
.when {
    font-size: 13px;
    color: #9fb5d6;
    margin-bottom: 4px;
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    padding: 20px 0;
    color: #9fb5d6;
    font-size: 13px;
    margin-top: 40px;
}
.footer a:hover { color: #7fb2ff; }

/* ---------- Button Styles ---------- */
.hero-buttons {
    margin-top: 18px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.hero-buttons a {
    padding: 10px 16px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 700;
    transition: all 0.2s ease;
    display: inline-block;
}

.btn-primary {
    background: linear-gradient(90deg,#4f7cff,#7fb2ff);
    color: #001022;
}

.btn-secondary {
    border: 1px solid rgba(127,178,255,0.12);
    color: #dbe9ff;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79,124,255,0.3);
}

.btn-secondary:hover {
    background: rgba(127,178,255,0.1);
    transform: translateY(-2px);
}

/* ---------- Mobile Profile Image ---------- */
.mobile-profile-image {
    display: none;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: 0 auto 20px auto;
    box-shadow: 0 15px 35px rgba(79,124,255,0.4);
    border: 3px solid rgba(127,178,255,0.3);
}

/* ---------- RESPONSIVE DESIGN ---------- */

/* Large tablets and small desktops (1024px and below) */
@media (max-width: 1024px) {
    .block-container {
        max-width: 95%;
        padding-left: 30px;
        padding-right: 30px;
    }

    .topnav {
        padding: 12px 30px;
    }

    .hero-left h1 {
        font-size: 2.8rem;
    }

    .hero-left h3 {
        font-size: 1.1rem;
    }

    .projects-grid {
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 16px;
    }
}

/* Tablets (768px and below) */
@media (max-width: 768px) {
    .block-container { 
        max-width: 100%;
        padding-top: 120px; 
        padding-left: 20px;
        padding-right: 20px;
        padding-bottom: 60px;
    }

    .topnav {
        padding: 12px 20px;
        position: relative;
    }

    .topnav > div {
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    .navlinks {
        display: none;
    }

    .mobile-menu-toggle {
        display: block;
    }

    /* Hide desktop avatar */
    .avatar-container {
        display: none !important;
    }

    /* Show mobile profile image */
    .mobile-profile-image {
        display: block;
    }

    .hero-left h1 {
        font-size: 2.4rem;
        text-align: center;
        line-height: 1.2;
    }

    .hero-left h3 {
        font-size: 1rem;
        text-align: center;
        max-width: 100%;
        line-height: 1.5;
    }

    .metrics {
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 4px;
    }

    .metric {
        text-align: center;
        min-width: 80px;
    }

    .hero-buttons {
        justify-content: center;
        margin-top: 24px;
    }

    .glass {
        padding: 20px;
        border-radius: 16px;
        margin-top: 24px;
    }
    
    .glass1 {
        padding: 20px;
        border-radius: 16px;
        margin-top: -100px;
    }

    .projects-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .project-card {
        padding: 18px;
    }

    .timeline-item {
        padding-left: 14px;
    }

    /* About section responsive layout */
    .about-content {
        flex-direction: column !important;
        gap: 20px !important;
    }

    .about-content > div:first-child {
        order: 2;
    }

    .about-content > div:last-child {
        order: 1;
        width: 100% !important;
        display: flex;
        justify-content: center;
    }

    /* Skills section improvements */
    .skill-item {
        margin: 10px 0 !important;
        padding: 12px !important;
    }

    .skill-item span {
        font-size: 16px !important;
    }
}

/* Mobile phones (480px and below) */
@media (max-width: 480px) {
    .block-container {
        padding-left: 15px;
        padding-right: 15px;
        padding-top: 140px;
    }

    .topnav {
        padding: 10px 15px;
    }

    .brand {
        flex-direction: row !important;
        gap: 8px !important;
        align-items: center !important;
    }

    .brand > div:first-child {
        width: 32px !important;
        height: 32px !important;
        font-size: 12px !important;
    }

    .brand > div:last-child div:first-child {
        font-size: 14px !important;
    }

    .brand > div:last-child div:last-child {
        font-size: 10px !important;
    }

    /* Mobile profile image sizing */
    .mobile-profile-image {
        width: 100px;
        height: 100px;
        margin-bottom: 15px;
    }

    .hero-left h1 {
        font-size: 2rem;
        line-height: 1.2;
    }

    .hero-left h3 {
        font-size: 0.95rem;
        line-height: 1.4;
        padding: 0 10px;
    }

    /* FIXED: Metrics responsive layout */
    .metrics {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-around !important;
        gap: 15px !important;
        margin-top: 0px !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        padding: 0 10px !important;
        -webkit-overflow-scrolling: touch !important;
    }

    .metric {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        text-align: center !important;
        min-width: 70px !important;
        flex-shrink: 0 !important;
    }

    .metric > div:first-child {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #4fc3ff !important;
    }

    .metric > div:last-child {
        font-size: 11px !important;
        color: #b0d8ff !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }

    .hero-buttons {
        flex-direction: column;
        width: 100%;
        margin-top: 24px;
        gap: 12px;
    }

    .hero-buttons a {
        text-align: center;
        padding: 14px 20px;
        width: 100%;
        box-sizing: border-box;
        font-size: 15px;
    }

    .glass {
        padding: 18px;
        margin-top: 24px;
        border-radius: 14px;
    }

    .glass h3 {
        font-size: 1.3rem;
        margin-bottom: 12px;
        text-align: center;
    }

    .project-card {
        padding: 16px;
    }

    .project-card strong {
        font-size: 15px !important;
    }

    .project-card p {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    .tag {
        font-size: 10px;
        padding: 3px 8px;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    .timeline-item {
        padding-left: 12px;
    }

    .when {
        font-size: 12px;
    }

    .timeline-item > div:nth-child(2) {
        font-size: 14px !important;
    }

    .timeline-item > div:nth-child(3) {
        font-size: 13px !important;
    }

    .footer {
        font-size: 12px;
        padding: 15px 0;
    }

    /* Contact form improvements */
    .contact-section {
        flex-direction: column !important;
    }

    .contact-section > div {
        width: 100% !important;
    }

    /* Skills section mobile improvements */
    .skill-item {
        margin: 8px 0 !important;
        padding: 12px !important;
    }

    .skill-item span {
        font-size: 14px !important;
    }

    .skill-item > div:first-child span:first-child {
        font-size: 15px !important;
    }

    .skill-item > div:first-child span:last-child {
        font-size: 13px !important;
    }

    /* Mobile menu improvements */
    .mobile-menu a {
        padding: 15px 0;
        font-size: 16px;
    }
}

/* Extra small mobile (360px and below) */
@media (max-width: 360px) {
    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    .topnav {
        padding: 8px 10px;
    }

    /* Extra small mobile profile image */
    .mobile-profile-image {
        width: 80px;
        height: 80px;
        margin-bottom: 12px;
    }

    .hero-left h1 {
        font-size: 1.8rem;
    }

    .hero-left h3 {
        font-size: 0.9rem;
        padding: 0 5px;
    }

    /* FIXED: Extra small metrics */
    .metrics {
        gap: 10px !important;
        padding: 0 5px !important;
    }

    .metric {
        min-width: 60px !important;
    }

    .metric > div:first-child {
        font-size: 16px !important;
    }

    .metric > div:last-child {
        font-size: 10px !important;
    }

    .glass {
        padding: 14px;
    }

    .project-card {
        padding: 14px;
    }

    .project-card p {
        font-size: 13px !important;
    }

    .hero-buttons a {
        padding: 12px 16px;
        font-size: 14px;
    }

    .brand > div:first-child {
        width: 28px !important;
        height: 28px !important;
        font-size: 11px !important;
    }
}

/* Responsive images and lottie animations */
@media (max-width: 768px) {
    .stImage > div {
        display: flex;
        justify-content: center;
    }

    .stImage img {
        max-width: 220px !important;
        width: 100% !important;
        height: auto !important;
        border-radius: 12px !important;
    }
}

@media (max-width: 480px) {
    .stImage img {
        max-width: 180px !important;
    }
}

@media (max-width: 360px) {
    .stImage img {
        max-width: 150px !important;
    }
}

/* Responsive text sizing */
@media (max-width: 768px) {
    div[data-testid="stMarkdownContainer"] p {
        font-size: 14px;
        line-height: 1.6;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        font-size: 18px;
    }
}

@media (max-width: 480px) {
    div[data-testid="stMarkdownContainer"] p {
        font-size: 13px;
        line-height: 1.5;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        font-size: 16px;
    }
}

/* Responsive forms */
@media (max-width: 768px) {
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    button[data-testid="baseButton-secondary"] {
        font-size: 14px !important;
        padding: 12px !important;
    }

    button[data-testid="baseButton-secondary"] {
        width: 100% !important;
        padding: 14px !important;
        border-radius: 10px !important;
        background: linear-gradient(90deg,#4f7cff,#7fb2ff) !important;
        color: #001022 !important;
        font-weight: 700 !important;
        border: none !important;
        min-height: 44px !important;
    }
}

@media (max-width: 480px) {
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 14px !important;
        min-height: 44px !important;
    }
}

/* Responsive plotly charts */
@media (max-width: 768px) {
    .js-plotly-plot {
        width: 100% !important;
    }

    .js-plotly-plot .plotly {
        width: 100% !important;
    }
}

/* Form container responsive */
@media (max-width: 768px) {
    div[data-testid="stForm"] {
        border: none !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
}

/* Streamlit column responsive behavior */
@media (max-width: 768px) {
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
    }
}

/* Mobile menu functionality improvements */
.mobile-menu-toggle:focus {
    outline: 2px solid #7fb2ff;
    outline-offset: 2px;
}

.mobile-menu a:focus {
    outline: 2px solid #7fb2ff;
    outline-offset: 2px;
}

@media (max-width: 480px) {
    .mobile-menu {
        padding: 15px;
    }

    .mobile-menu a {
        font-size: 16px;
        padding: 15px 0;
    }
}

/* Improved button hover states for touch devices */
@media (hover: none) {
    .project-card:hover {
        transform: none;
    }

    .btn-primary:hover,
    .btn-secondary:hover {
        transform: none;
    }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
        animation: none !important;
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .glass {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.2);
    }

    .project-card {
        border: 1px solid rgba(255,255,255,0.15);
    }
}

/* Additional mobile-specific fixes */
@media (max-width: 480px) {
    /* Ensure proper touch targets */
    a, button, [role="button"] {
        min-height: 44px;
        min-width: 44px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    /* Fix for brand logo spacing */
    .brand {
        flex-wrap: nowrap !important;
    }

    /* Better mobile typography */
    .hero-left h1 {
        word-break: break-word;
        hyphens: auto;
    }
    
    .hero-left h3 {
        word-break: break-word;
        hyphens: auto;
    }
}

/* Gradient text and animation styles for hero section */
.gradient-text {
    background: linear-gradient(135deg, #ffffff, #7fb2ff, #4fc3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-left: -35%;
}

.pill {
    border-radius: 25px !important;
}

/* Avatar and animation styles */
.avatar-container {
    transition: transform 0.3s ease;
}

.avatar-container:hover {
    transform: rotateY(15deg) rotateX(5deg);
}

/* Typing animation for subtitle */
#typed-subtitle {
    border-right: 2px solid #7fb2ff;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { border-color: #7fb2ff; }
    51%, 100% { border-color: transparent; }
}

/* Fade in animation */
.fade-in {
    opacity: 0;
    animation: fadeInUp 1s ease forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Mobile-specific responsive adjustments for gradient text */
@media (max-width: 768px) {
    .gradient-text {
        font-size: 2.8rem !important;
             margin-left: 15%;
    }

    #typed-subtitle {
        font-size: 1.1rem !important;
        min-height: 44px !important;
    }
}

@media (max-width: 480px) {
    .gradient-text {
        font-size: 2.4rem !important;
            margin-left: 15%;
    }

    #typed-subtitle {
        font-size: 1rem !important;
        min-height: 40px !important;
        border-right: 1.5px solid #7fb2ff !important;
    }
}

@media (max-width: 360px) {
    .gradient-text {
        font-size: 1.8rem !important;
            margin-left: 15%;
        
    }

    #typed-subtitle {
        font-size: 0.9rem !important;
        min-height: 36px !important;
    }
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; scroll-behavior: smooth; }
#MainMenu, footer, header {visibility: hidden;}

.stApp { background: transparent; color: #E6EEF3; }
.block-container { max-width: 1200px; padding-top: 80px; padding-bottom: 80px; }

/* ---------- Enhanced Background Overlay ---------- */
iframe[srcdoc*="LOTTIE_BG_MARKER"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: -9999 !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: none !important;
    object-fit: cover !important;
}

#bg-dim-overlay {
    position: fixed;
    inset: 0;
    z-index: -9998;
    pointer-events: none;
    background: linear-gradient(180deg, rgba(10,12,30,0.55), rgba(6,8,20,0.9));
}

/* Mobile Background Enhancements */
@media (max-width: 768px) {
    /* Reduce overlay opacity for better visibility */
    #bg-dim-overlay {
        background: linear-gradient(180deg, rgba(10,12,30,0.35), rgba(6,8,20,0.65)) !important;
    }
    
    /* Rotate and scale background for mobile */
    iframe[srcdoc*="LOTTIE_BG_MARKER"] {
        transform: rotate(90deg) scale(1.2) !important;
        transform-origin: center center !important;
      
        right:10
        width: 100vh !important;
        height: 100vw !important;
    }
}

@media (max-width: 480px) {
    #bg-dim-overlay {
        background: linear-gradient(180deg, rgba(10,12,30,0.25), rgba(6,8,20,0.55)) !important;
    }
    
    iframe[srcdoc*="LOTTIE_BG_MARKER"] {
        transform: rotate(90deg) scale(2.4) !important;
    }
}

@media (max-width: 360px) {
    #bg-dim-overlay {
        background: linear-gradient(180deg, rgba(10,12,30,0.2), rgba(6,8,20,0.45)) !important;
    }
    
    iframe[srcdoc*="LOTTIE_BG_MARKER"] {
        transform: rotate(90deg) scale(1.6) !important;
            
    }
}

/* ---------- About Section ---------- */
.about-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
    margin-top: 60px;
    margin-bottom: 60px;
    flex-wrap: wrap;
}

.about-content {
    flex: 1;
    max-width: 650px;
    padding: 30px;
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
    backdrop-filter: blur(14px);
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    animation: fadeInUp 1.2s ease forwards;
    border-left: 4px solid #4f7cff;
    position: relative;
    overflow: hidden;
}

.about-content::before {
    content: "";
    position: absolute;
    top: -40px;
    right: -40px;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(79,124,255,0.25), transparent 70%);
    z-index: 0;
}

.about-content h3 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: #ffffff;
    background: linear-gradient(135deg, #ffffff, #7fb2ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    z-index: 1;
}

.about-content p {
    font-size: 1rem;
    line-height: 1.7;
    color: #dbe9ff;
    margin-bottom: 15px;
    position: relative;
    z-index: 1;
}

.about-profile {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.about-profile iframe {
    width: 260px;
    height: 260px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid rgba(127,178,255,0.3);
    box-shadow: 0 15px 40px rgba(79,124,255,0.4);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.about-profile iframe:hover {
    transform: scale(1.05) rotate(3deg);
    box-shadow: 0 20px 50px rgba(79,124,255,0.55);
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .about-section {
        flex-direction: column;
        gap: 30px;
    }
    .about-content, .about-profile {
        max-width: 100%;
    }
    .about-profile iframe {
        width: 200px;
        height: 200px;
    }
}
            
</style>
<div id="bg-dim-overlay"></div>
""", unsafe_allow_html=True)

# ----------------------- Background Lottie via iframe -----------------------
marker = "LOTTIE_BG_MARKER"
b64 = load_lottie_file_b64("Background looping animation.json")

if b64:
    html_srcdoc = f"""<!--{marker}-->
    <html><body style="margin:0;">
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player autoplay loop background="transparent" speed="1"
      src="data:application/json;base64,{b64}"
      style="width:100vw;height:100vh;display:block;"></lottie-player>
    </body></html>"""
    components_html(html_srcdoc, height=0)

# ----------------------- Top Navigation with Mobile Menu -----------------------
st.markdown("""
<div class="topnav glass1">
    <div style="display:flex; align-items:center; justify-content:space-between;">
        <div class="brand" style="display:flex; gap:12px; align-items:center;">
            <div style="width:36px; height:36px; border-radius:8px; background: linear-gradient(135deg,#4f7cff,#7fb2ff); box-shadow:0 6px 20px rgba(127,178,255,0.14); display:flex; align-items:center; justify-content:center; font-weight:800;">RK</div>
            <div style="display:flex; flex-direction:column; line-height:1;">
                <div style="font-weight:800; color:#fff;">Rohan Kashyap</div>
                <div style="font-size:12px; color:#9fb5d6;">Data Science • ML • AI</div>
            </div>
        </div>
        <div class="navlinks">
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#projects">Projects</a>
            <a href="#experience">Experience</a>
            <a href="#contact">Contact</a>
        </div>
        <button class="mobile-menu-toggle" onclick="toggleMobileMenu()">☰</button>
    </div>
    <div class="mobile-menu" id="mobileMenu">
        <a href="#about" onclick="closeMobileMenu()">About</a>
        <a href="#skills" onclick="closeMobileMenu()">Skills</a>
        <a href="#projects" onclick="closeMobileMenu()">Projects</a>
        <a href="#experience" onclick="closeMobileMenu()">Experience</a>
        <a href="#contact" onclick="closeMobileMenu()">Contact</a>
    </div>
</div>

<script>
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('active');
}

function closeMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.remove('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('mobileMenu');
    const toggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.topnav');

    if (!nav.contains(event.target)) {
        menu.classList.remove('active');
    }
});
</script>
""", unsafe_allow_html=True)

# ----------------------- HERO -----------------------
st.markdown('<a id="about"></a>', unsafe_allow_html=True)
hero_col1, hero_col2 = st.columns([2, 1])

with hero_col1:
    st.markdown('''
    <div class="hero-left fade-in" style="animation: fadeInUp 1s ease forwards;"><!-- Mobile Profile Image - Only shows on mobile --><img src="img/ap.jpeg" alt="Rohan Kashyap Profile" class="mobile-profile-image"><h1 class="gradient-text" style="font-weight:900; font-size:3.8rem; margin-bottom:12px; letter-spacing: -0.03em; text-align: center; ">Rohan Kashyap</h1>''', unsafe_allow_html=True)
        # ----------------------- Typing Animation -----------------------
    components_html("""<div style="margin-left: 0px; ">
    <span style="color:#a9c9ff;font-weight:600;">I'm a </span>
    <span id="typed-subtitle" style="color:#7fb2ff;font-weight:700; font-size:20px"></span>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
    <script>
    var typed = new Typed("#typed-subtitle", {
        strings: ["Data Scientist", "AI Enthusiast", "Machine Learning Engineer"],
        typeSpeed: 100,
        backSpeed: 50,
        backDelay: 1500,
        startDelay: 200,
        smartBackspace: true,
        loop: true,
        showCursor: true,
        cursorChar: "|"
    });
    </script>
    """, height=50)

    st.markdown('''<h3 id="typed-subtitle" style="font-size:1.25rem; font-weight:500; max-width:680px; line-height:1.4; color:#a9c9ff; min-height:52px;"></h3>
        <div class="metrics" style=" display:flex; gap:30px; align-items:center;">
            <div class="metric" style="min-width: 100px;">
                <div style="font-size:22px; font-weight:700; color:#4fc3ff;">2+</div>
                <div style="font-size:13px; color:#b0d8ff; font-weight:600;">Years Experience</div>
            </div>
            <div class="metric" style="min-width: 100px;">
                <div style="font-size:22px; font-weight:700; color:#4fc3ff;">18</div>
                <div style="font-size:13px; color:#b0d8ff; font-weight:600;">Projects</div>
            </div>
            <div class="metric" style="min-width: 100px;">
                <div style="font-size:22px; font-weight:700; color:#4fc3ff;">7</div>
                <div style="font-size:13px; color:#b0d8ff; font-weight:600;">Deployed Apps</div>
            </div>
        </div>
        <div class="hero-buttons" style="margin-top:36px; display:flex; gap:16px;">
            <a href="#contact" class="btn-primary pill" style="font-size:16px; padding:14px 28px; color:#ffffff;">
        &#9993; Contact Me
    </a>
            <a href="#" class="btn-secondary pill" style="font-size:16px; padding:14px 28px;">
                &#8681; Download CV
            </a>
        </div>
    </div>
    ''', unsafe_allow_html=True)


with hero_col2:
    avatar = load_image_url("https://avatars.githubusercontent.com/u/9919?s=200&v=4")
    if avatar:
        st.markdown('''
        <div class="avatar-container" style="width: 320px; margin: auto; perspective: 900px;">
            <img id="avatar-img" src="https://avatars.githubusercontent.com/u/9919?s=200&v=4" 
            alt="Rohan Kashyap avatar" style="width: 100%; border-radius: 20px; box-shadow: 0 20px 40px rgba(79,124,255,0.4); transition: transform 0.3s ease;">
        </div>
        ''', unsafe_allow_html=True)

# ----------------------- About Section -----------------------
st.markdown('<div class="about-section">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="about-content">
        <h3>About Me</h3>
        <p>Hello! I’m <b>Rohan Kashyap</b>, a passionate Computer Science Engineering student, 
        data enthusiast, and aspiring software engineer. I love transforming raw data into 
        meaningful insights, designing scalable systems, and building intelligent dashboards.</p>
        <p>With hands-on experience in <b>Python, SQL, Power BI, MERN stack, and Machine Learning</b>, 
        I aim to merge creativity and analytics to craft innovative solutions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="about-profile"><iframe src="https://drive.google.com/file/d/13m_2g7LvMloCjCdZk4586bFUhtRGXtb9/preview" width="640" height="480" allow="autoplay"></iframe></div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

Lottie_small = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
if Lottie_small:
    st_lottie(Lottie_small, height=160, key="small_anim")
st.markdown('</div></div></div>', unsafe_allow_html=True)

# ----------------------- Skills — Proficiency -----------------------
st.markdown("## 🚀 Skills — Proficiency")

skills = {
    "Python": 90,
    "Machine Learning": 80,
    "Data Analysis": 85,
    "SQL & Databases": 75,
    "Streamlit / Dash": 88,
    "Power BI / Tableau": 70,
    "HTML / CSS / JS": 65,
}

# Interactive progress bars
for skill, level in skills.items():
    color = "green" if level >= 80 else "orange" if level >= 70 else "red"

    st.markdown(f"""
    <div class="skill-item" style="
        margin: 12px 0;
        padding: 12px;
        border-radius: 12px;
        background: #1e1e1e;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    ">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:18px; font-weight:600;">{skill}</span>
            <span style="font-size:16px; font-weight:500; color:{color};">{level}%</span>
        </div>
        <div style="
            background: #333;
            border-radius: 20px;
            margin-top: 8px;
            height: 16px;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                width: {level}%;
                background: linear-gradient(90deg, #00ffcc, #0077ff);
                height: 100%;
                border-radius: 20px;
                transition: width 1.2s ease-in-out;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------- Projects -----------------------
st.markdown('<div class="glass"><h3 id="projects">Selected Projects</h3>', unsafe_allow_html=True)
st.markdown('<div class="projects-grid">', unsafe_allow_html=True)
projects = [
    {"title":"Smart E-Learning Platform", "desc":"Adaptive learning platform with recommendations, analytics dashboards, and content personalization.", "tags":["MERN","ML","PowerBI"]},
    {"title":"Influencer Recommendation System", "desc":"ML-powered scoring model to recommend influencers based on engagement & ROI.", "tags":["Python","Streamlit","SQL"]},
    {"title":"Anomaly Detection for Sensors", "desc":"Hybrid models for IoT anomaly detection with explainability and alerting.", "tags":["TimeSeries","PyTorch","MLOps"]},
    {"title":"Ad Analytics Pipeline", "desc":"Scalable ETL and reporting for daily ad metrics with partitioned data model.", "tags":["Airflow","BigQuery","Dash"]},
]
for p in projects:
    tags_html = ' '.join([f'<span class="tag">{t}</span>' for t in p["tags"]])
    st.markdown(f"""
        <div class="project-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="font-size:16px;">{p["title"]}</strong>
                <div style="font-size:12px; color:#9fb5d6;">Featured</div>
            </div>
            <p style="color:#cfe6ff; margin-top:8px;">{p["desc"]}</p>
            <div style="margin-top:8px;">{tags_html}</div>
            <div style="margin-top:12px;"><a href="#" style="text-decoration:none; padding:8px 12px; border-radius:8px; background:linear-gradient(90deg,#6f9bff,#5bd1ff); color:#001522; font-weight:700;">View Case Study</a></div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ----------------------- Timeline -----------------------
st.markdown('<div class="glass"><h3 id="experience">Experience & Timeline</h3>', unsafe_allow_html=True)
st.markdown('<div class="timeline">', unsafe_allow_html=True)
timeline = [
    {"when":"Jan 2025 – Present", "title":"ML Engineer Intern — 10xConstruction.ai", "desc":"Worked on computer vision pipelines, model optimizations, and deployment."},
    {"when":"Jun 2024 – Dec 2024", "title":"Data Science Intern — Larsen & Toubro (L&T)", "desc":"Built predictive models and dashboards; improved inference latency by 28%."},
    {"when":"2023", "title":"Freelance — Data Apps", "desc":"Delivered analytics apps and prototypes for multiple clients using Streamlit."},
    {"when":"2021 – 2025", "title":"B.Tech CSE — Chandigarh University", "desc":"Specialization in AI & Data Science."},
]
for t in timeline:
    st.markdown(f"""
        <div class="timeline-item">
            <div class="when">{t["when"]}</div>
            <div style="font-weight:700; color:#fff;">{t["title"]}</div>
            <div style="color:#cfe6ff; margin-top:6px;">{t["desc"]}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# ----------------------- Contact -----------------------
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown('<div class="glass"><h3>Contact</h3>', unsafe_allow_html=True)
cols = st.columns([2,1])
with cols[0]:
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your name")
        email = st.text_input("Email")
        message = st.text_area("Message", height=140)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            try:
                rec = pd.DataFrame([{"name":name, "email":email, "message":message}])
                try:
                    old = pd.read_csv("messages.csv")
                    out = pd.concat([old, rec], ignore_index=True)
                except Exception:
                    out = rec
                out.to_csv("messages.csv", index=False)
                st.success("Thanks — message received. I'll reply soon.")
            except Exception:
                st.error("Could not save message locally.")
with cols[1]:
    contact_anim = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")
    if contact_anim:
        st_lottie(contact_anim, height=220, key="contact_anim")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------- Footer -----------------------
st.markdown('<div class="footer">© 2025 • Rohan Kashyap • <a href="https://github.com" target="_blank">GitHub</a> • <a href="https://linkedin.com" target="_blank">LinkedIn</a></div>', unsafe_allow_html=True)
