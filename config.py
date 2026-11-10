"""
NoteGenius AI - Configuration & Constants
=========================================
Application settings, theme constants, Gemini model configurations,
and prompt templates for NoteGenius AI.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
MODULES_DIR = BASE_DIR / "modules"
COMPONENTS_DIR = BASE_DIR / "components"

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Application Metadata
APP_NAME = "NoteGenius AI"
TAGLINE = "Upload. Understand. Learn Smarter."
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "An intelligent, AI-powered study assistant designed for students to understand "
    "their study materials faster through RAG-based chat, smart summarization, "
    "interactive quizzes, and flashcards."
)

# AI Provider & Model Configuration
PROVIDER_GEMINI = "Google Gemini"
PROVIDER_GROQ = "Groq Cloud"
SUPPORTED_PROVIDERS = [PROVIDER_GEMINI, PROVIDER_GROQ]
DEFAULT_AI_PROVIDER = os.getenv("AI_PROVIDER", PROVIDER_GEMINI)

# Google Gemini Models (Free tier quota)
FREE_GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Groq Cloud Models (Free tier quota, ultra-fast inference)
FREE_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Feature Specific Temperatures
AI_TEMPERATURES = {
    "summarizer": 0.3,
    "chat": 0.2,
    "quiz": 0.4,
    "flashcard": 0.3,
    "study_mode": 0.5,
}

# RAG & Chunking Configuration (Optimized for 8GB RAM laptops)
MAX_UPLOAD_SIZE_MB = 25
MAX_PAGE_COUNT = 150
DEFAULT_CHUNK_SIZE = 750
DEFAULT_CHUNK_OVERLAP = 150
TOP_K_RETRIEVAL = 4
SIMILARITY_THRESHOLD = 0.05

# Navigation Views
NAV_DASHBOARD = "Dashboard"
NAV_MY_DOCUMENTS = "My Documents"
NAV_SUMMARIZER = "AI Summarizer"
NAV_CHAT = "Chat with PDF"
NAV_QUIZ = "Quiz Generator"
NAV_FLASHCARDS = "Flashcards"
NAV_STUDY_MODE = "Study Mode"

NAV_OPTIONS = [
    NAV_DASHBOARD,
    NAV_MY_DOCUMENTS,
    NAV_SUMMARIZER,
    NAV_CHAT,
    NAV_QUIZ,
    NAV_FLASHCARDS,
    NAV_STUDY_MODE,
]

# UI Color Palette & Design Tokens
# White and soft lavender with vibrant purple accents
THEME = {
    "primary": "#7C3AED",        # Deep royal purple
    "primary_dark": "#6D28D9",   # Dark violet
    "primary_light": "#8B5CF6",  # Medium purple
    "lavender_bg": "#F5F3FF",    # Soft lavender tint
    "lavender_border": "#DDD6FE",# Soft lavender border
    "lavender_glow": "rgba(124, 58, 237, 0.12)",
    "bg_main": "#F8F9FE",        # Crisp modern background
    "bg_card": "#FFFFFF",        # Clean white card
    "text_main": "#1E1B4B",      # Deep navy-purple text
    "text_muted": "#64748B",     # Slate muted text
    "accent_green": "#10B981",   # Success badge
    "accent_amber": "#F59E0B",   # Warning badge
    "accent_rose": "#F43F5E",    # Danger badge
    "border_radius": "14px",
    "card_shadow": "0 4px 20px -2px rgba(124, 58, 237, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.04)",
}

# System Grounding Directives
SYSTEM_GROUNDING_PROMPT = (
    "You are NoteGenius AI, a helpful, patient, and knowledgeable AI study tutor. "
    "Your mission is to help students learn effectively from their uploaded study notes. "
    "Rules you must strictly follow:\n"
    "1. Base your answers strictly on the provided document excerpts and context.\n"
    "2. If an answer cannot be determined or is absent from the provided context, state clearly: "
    "'This information is not found in your uploaded study notes.' Do NOT fabricate or hallucinate facts.\n"
    "3. Use student-friendly language, clear headings, and concise bullet points.\n"
    "4. Always cite source documents and page numbers where applicable.\n"
    "5. Be encouraging and promote active learning."
)

