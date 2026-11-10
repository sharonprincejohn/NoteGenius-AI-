"""
NoteGenius AI – Intelligent Study Assistant
===========================================
Main application entry point. A complete, modern, lightweight Streamlit web app
for students to understand their study materials using Gemini AI and lightweight RAG.
"""

import os
import streamlit as st
from config import (
    APP_NAME,
    TAGLINE,
    APP_VERSION,
    THEME,
    NAV_DASHBOARD,
    NAV_MY_DOCUMENTS,
    NAV_SUMMARIZER,
    NAV_CHAT,
    NAV_QUIZ,
    NAV_FLASHCARDS,
    NAV_STUDY_MODE,
)
from modules.pdf_reader import PDFReader
from modules.text_chunker import TextChunker
from modules.retriever import RAGRetriever
from modules.ai_service import GeminiService, AIServiceError
from modules.summarizer import NotesSummarizer
from modules.quiz_generator import QuizGenerator
from modules.flashcards import FlashcardGenerator
from modules.study_mode import StudyModeTutor
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.document_cards import render_documents_manager


# Streamlit Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} – Intelligent Study Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_custom_css():
    """Inject clean, modern soft lavender & purple styling."""
    st.markdown(
        f"""
        <style>
            /* Global font and background */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"] {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }}

            .main .block-container {{
                padding-top: 1.8rem;
                padding-bottom: 3rem;
                max-width: 1200px;
            }}

            /* Sidebar custom styling */
            [data-testid="stSidebar"] {{
                background-color: #FBFBFE;
                border-right: 1px solid #EDE9FE;
            }}

            /* Metric Cards */
            .metric-card {{
                background: white;
                border: 1px solid #EDE9FE;
                border-radius: 12px;
                padding: 18px 20px;
                box-shadow: 0 4px 12px rgba(124, 58, 237, 0.04);
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(124, 58, 237, 0.08);
            }}
            .metric-icon {{
                font-size: 1.6rem;
                margin-bottom: 6px;
            }}
            .metric-value {{
                font-size: 1.7rem;
                font-weight: 800;
                color: #1E1B4B;
                line-height: 1.1;
            }}
            .metric-label {{
                font-size: 0.8rem;
                font-weight: 500;
                color: #64748B;
                margin-top: 4px;
            }}

            /* Feature Action Cards */
            .feature-card {{
                background: white;
                border: 1px solid #EDE9FE;
                border-radius: 12px;
                padding: 16px 14px;
                min-height: 140px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 2px 8px rgba(124, 58, 237, 0.03);
                margin-bottom: 8px;
            }}
            .feat-icon {{
                font-size: 1.8rem;
                margin-bottom: 6px;
            }}
            .feat-title {{
                font-weight: 700;
                font-size: 0.95rem;
                color: #1E1B4B;
                margin-bottom: 4px;
            }}
            .feat-desc {{
                font-size: 0.78rem;
                color: #64748B;
                line-height: 1.3;
            }}

            /* Flashcard Styling */
            .flashcard-box {{
                background: white;
                border: 2px solid #DDD6FE;
                border-radius: 16px;
                padding: 40px 32px;
                min-height: 260px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                box-shadow: 0 8px 24px rgba(124, 58, 237, 0.08);
                transition: all 0.3s ease;
                margin: 16px 0;
            }}
            .flashcard-front {{
                border-color: #DDD6FE;
                background: linear-gradient(180deg, #FFFFFF 0%, #FAF8FF 100%);
            }}
            .flashcard-back {{
                border-color: #7C3AED;
                background: linear-gradient(180deg, #F5F3FF 0%, #EDE9FE 100%);
            }}

            /* Primary Button Styling */
            .stButton>button[kind="primary"] {{
                background-color: #7C3AED;
                color: white;
                border-radius: 10px;
                font-weight: 600;
                border: none;
                padding: 0.5rem 1.2rem;
                box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
            }}
            .stButton>button[kind="primary"]:hover {{
                background-color: #6D28D9;
                box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
            }}

            /* Source Citation Card */
            .source-tag {{
                display: inline-block;
                background: #EDE9FE;
                color: #6D28D9;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 3px 8px;
                border-radius: 6px;
                margin: 2px 4px 2px 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize persistent Streamlit session state."""
    if "documents" not in st.session_state:
        st.session_state["documents"] = []
    if "chunks" not in st.session_state:
        st.session_state["chunks"] = []
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "active_nav" not in st.session_state:
        st.session_state["active_nav"] = NAV_DASHBOARD
    if "retriever" not in st.session_state:
        st.session_state["retriever"] = RAGRetriever()
    if "pdf_reader" not in st.session_state:
        st.session_state["pdf_reader"] = PDFReader()
    if "chunker" not in st.session_state:
        st.session_state["chunker"] = TextChunker()
    if "ai_service" not in st.session_state:
        st.session_state["ai_service"] = GeminiService()
    if "quiz_data" not in st.session_state:
        st.session_state["quiz_data"] = None
    if "quiz_results" not in st.session_state:
        st.session_state["quiz_results"] = None
    if "quiz_user_answers" not in st.session_state:
        st.session_state["quiz_user_answers"] = {}
    if "flashcards_data" not in st.session_state:
        st.session_state["flashcards_data"] = None
    if "current_flashcard_idx" not in st.session_state:
        st.session_state["current_flashcard_idx"] = 0
    if "flashcard_flipped" not in st.session_state:
        st.session_state["flashcard_flipped"] = False
    if "study_explanation" not in st.session_state:
        st.session_state["study_explanation"] = None


def navigate_to(page_name: str):
    """Change active navigation page."""
    st.session_state.active_nav = page_name


def delete_document_callback(doc_id: str):
    """Remove a document from session memory and re-index remaining chunks."""
    st.session_state["documents"] = [
        d for d in st.session_state["documents"] if d["doc_id"] != doc_id
    ]
    # Rebuild chunks and retriever
    all_chunks = []
    for d in st.session_state["documents"]:
        all_chunks.extend(st.session_state["chunker"].chunk_document(d))
    st.session_state["chunks"] = all_chunks
    st.session_state["retriever"].build_index(all_chunks)


# ---------------------------------------------------------------------------
# View 3: AI Summarizer
# ---------------------------------------------------------------------------
def render_summarizer_view(ai_service: GeminiService):
    st.markdown("## 📝 AI Notes Summarizer")
    st.markdown(
        "Generate student-friendly summaries, exam study guides, or definition cheat sheets "
        "grounded strictly in your uploaded notes."
    )

    documents = st.session_state.get("documents", [])
    if not documents:
        st.info("📚 Please upload at least one PDF in the **Dashboard** before generating summaries.")
        if st.button("⬅️ Go to Dashboard to Upload", type="primary"):
            navigate_to(NAV_DASHBOARD)
            st.rerun()
        return

    summarizer = NotesSummarizer(ai_service)

    # Document selection
    doc_options = ["All Uploaded Documents"] + [d["filename"] for d in documents]
    selected_doc_name = st.selectbox(
        "Select Material to Summarize",
        options=doc_options,
        help="Summarize a specific document or all documents combined.",
    )

    # Format choices
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        summary_type = st.radio(
            "Summary Format",
            options=["quick", "detailed", "cheat_sheet"],
            format_func=lambda x: NotesSummarizer.SUMMARY_TYPES[x]["title"],
            help="Choose the depth of your summary.",
        )
    with col_t2:
        st.markdown(
            f"""
            <div style="background: #F5F3FF; border: 1px solid #DDD6FE; border-radius: 10px; padding: 14px; margin-top: 10px;">
                <strong style="color: #6D28D9;">Format Highlights:</strong><br>
                <span style="font-size: 0.85rem; color: #4B5563;">
                    {NotesSummarizer.SUMMARY_TYPES[summary_type]["description"]}<br>
                    <strong>Target Length:</strong> {NotesSummarizer.SUMMARY_TYPES[summary_type]["target_words"]}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    custom_focus = st.text_input(
        "Optional: Focus on specific topics or questions",
        placeholder="e.g. Focus on Newton's laws, or formulas for Chapter 2",
    )

    # Prepare document text
    if selected_doc_name == "All Uploaded Documents":
        doc_text = "\n\n".join([d.get("full_text", "") for d in documents])
        doc_display_name = f"All Notes ({len(documents)} documents)"
    else:
        target_doc = next((d for d in documents if d["filename"] == selected_doc_name), None)
        doc_text = target_doc.get("full_text", "") if target_doc else ""
        doc_display_name = selected_doc_name

    if st.button("✨ Generate AI Summary", type="primary", use_container_width=True):
        if not ai_service.is_configured():
            st.error("Please configure your Gemini API Key in the sidebar first.")
            return

        with st.spinner("Analyzing study notes and synthesizing summary with Gemini..."):
            try:
                summary_output = summarizer.generate_summary(
                    document_text=doc_text,
                    document_name=doc_display_name,
                    summary_type=summary_type,
                    custom_focus=custom_focus if custom_focus.strip() else None,
                )
                st.session_state["last_summary"] = summary_output
            except AIServiceError as ae:
                st.error(str(ae))
            except Exception as e:
                st.error(f"Failed to generate summary: {e}")

    # Display generated summary
    if "last_summary" in st.session_state and st.session_state["last_summary"]:
        st.markdown("<hr style='border: none; border-top: 1px solid #EDE9FE; margin: 24px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📄 Generated Study Summary")

        st.markdown(
            f"""
            <div style="
                background: white;
                border: 1px solid #EDE9FE;
                border-radius: 12px;
                padding: 24px 28px;
                box-shadow: 0 4px 16px rgba(124, 58, 237, 0.04);
                line-height: 1.65;
            ">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state["last_summary"])
        st.markdown("</div>", unsafe_allow_html=True)

        col_dl, _ = st.columns([1, 3])
        with col_dl:
            st.download_button(
                label="📥 Download Summary (.md)",
                data=st.session_state["last_summary"],
                file_name=f"NoteGenius_Summary_{summary_type}.md",
                mime="text/markdown",
                use_container_width=True,
            )


# ---------------------------------------------------------------------------
# View 4: Chat with PDF (RAG)
# ---------------------------------------------------------------------------
def render_chat_view(ai_service: GeminiService, retriever: RAGRetriever):
    st.markdown("## 💬 Chat with PDF (RAG Assistant)")
    st.markdown(
        "Ask questions about your uploaded documents. Answers are strictly grounded in your notes "
        "with page references. If information is absent, the AI will honestly say so."
    )

    documents = st.session_state.get("documents", [])
    chunks = st.session_state.get("chunks", [])

    if not documents or not chunks:
        st.info("📚 No documents uploaded yet. Upload your PDF notes in the **Dashboard** to begin chatting.")
        if st.button("⬅️ Go to Dashboard to Upload", type="primary"):
            navigate_to(NAV_DASHBOARD)
            st.rerun()
        return

    # Ensure index is built
    if not retriever.is_indexed():
        retriever.build_index(chunks)

    # Grounding banner
    st.markdown(
        f"""
        <div style="
            background: #F5F3FF;
            border: 1px solid #DDD6FE;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 0.82rem;
            color: #6D28D9;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        ">
            <div>
                🔍 <strong>RAG Search Active:</strong> Searching across <strong>{len(documents)}</strong> document(s), 
                <strong>{sum(d.get('total_pages', 0) for d in documents)}</strong> pages, 
                and <strong>{len(chunks)}</strong> indexed text chunks.
            </div>
            <div>
                <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">Zero-Hallucination Mode</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Suggested Prompts pills
    st.markdown("<span style='font-size: 0.78rem; font-weight: 600; color: #64748B;'>Suggested Questions:</span>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    preset_query = None
    with q_col1:
        if st.button("📌 What are the main definitions?", use_container_width=True):
            preset_query = "What are the main definitions and key terms covered in these notes?"
    with q_col2:
        if st.button("⚖️ Explain the primary formula or law", use_container_width=True):
            preset_query = "Explain the primary formulas or fundamental laws discussed in these notes."
    with q_col3:
        if st.button("📝 Give me 3 review questions", use_container_width=True):
            preset_query = "Based on these notes, what are 3 key questions likely to appear on an exam?"

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🧠"):
                st.markdown(msg["content"])
                # Show source citations if available
                sources = msg.get("sources", [])
                if sources:
                    with st.expander(f"📚 View {len(sources)} Source References Cited"):
                        for s in sources:
                            doc_n = s.get("doc_name", "Doc")
                            p_num = s.get("page_number", "?")
                            score = s.get("similarity_score", 0.0)
                            st.markdown(
                                f"""
                                <div style="background: #F8F9FE; border-left: 3px solid #7C3AED; padding: 6px 12px; margin-bottom: 6px; font-size: 0.82rem;">
                                    <strong>{doc_n}</strong> — Page {p_num} (Relevance: {int(score * 100)}%)<br>
                                    <span style="color: #475569;">"{s.get('text', '')[:220]}..."</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

    # Chat Input
    user_query = st.chat_input("Ask a question about your study materials...") or preset_query

    if user_query:
        if not ai_service.is_configured():
            st.error("Please configure your Gemini API Key in the sidebar first.")
            return

        # Append student message
        st.session_state["chat_history"].append({
            "role": "user",
            "content": user_query,
            "sources": [],
        })

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_query)

        # Retrieve relevant chunks using TF-IDF + Cosine Similarity
        with st.spinner("Searching document chunks with TF-IDF similarity..."):
            retrieved_chunks = retriever.retrieve(user_query, top_k=4, threshold=0.04)

        with st.chat_message("assistant", avatar="🧠"):
            if not retrieved_chunks:
                grounded_answer = (
                    "I searched through your uploaded study materials, but couldn't find any relevant "
                    "information related to your question.\n\n"
                    "*(NoteGenius AI does not invent answers that are absent from your uploaded notes.)*"
                )
                st.markdown(grounded_answer)
                st.session_state["chat_history"].append({
                    "role": "assistant",
                    "content": grounded_answer,
                    "sources": [],
                })
            else:
                context_block = retriever.format_context_for_prompt(retrieved_chunks)

                rag_prompt = f"""
Student Question:
"{user_query}"

Relevant Passages from Uploaded Study Materials:
{context_block}

Instructions:
1. Answer the question thoroughly and clearly using ONLY the provided passages.
2. If the context does not contain enough information to answer, state: "This information is not found in your uploaded study notes."
3. Cite the document name and page number for every key claim (e.g. "[Physics.pdf, Page 4]").
4. Organize your response with bullet points where appropriate.
"""
                system_instruction = (
                    "You are NoteGenius AI tutor. You strictly answer questions using only the provided notes. "
                    "Never invent facts or use external knowledge not in the context. Be encouraging and clear."
                )

                try:
                    # Stream response for real-time interactivity
                    response_placeholder = st.empty()
                    collected_response = ""
                    for chunk_text in ai_service.generate_stream(
                        prompt=rag_prompt,
                        system_instruction=system_instruction,
                        temperature=0.2,
                    ):
                        collected_response += chunk_text
                        response_placeholder.markdown(collected_response + "▌")

                    response_placeholder.markdown(collected_response)

                    # Show sources expander
                    with st.expander(f"📚 View {len(retrieved_chunks)} Source References Cited"):
                        for s in retrieved_chunks:
                            st.markdown(
                                f"""
                                <div style="background: #F8F9FE; border-left: 3px solid #7C3AED; padding: 6px 12px; margin-bottom: 6px; font-size: 0.82rem;">
                                    <strong>{s.get('doc_name')}</strong> — Page {s.get('page_number')} (Relevance: {int(s.get('similarity_score', 0) * 100)}%)<br>
                                    <span style="color: #475569;">"{s.get('text', '')[:220]}..."</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # Record assistant message
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": collected_response,
                        "sources": retrieved_chunks,
                    })

                except AIServiceError as ae:
                    st.error(str(ae))
                except Exception as ex:
                    st.error(f"Error answering question: {ex}")

    # Clear chat button
    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state["chat_history"] = []
            st.rerun()


# ---------------------------------------------------------------------------
# View 5: Quiz Generator
# ---------------------------------------------------------------------------
def render_quiz_view(ai_service: GeminiService):
    st.markdown("## 🎯 AI Quiz Generator")
    st.markdown(
        "Generate interactive multiple-choice quizzes grounded in your study notes. "
        "Test your understanding with instant scoring, answer feedback, and explanations."
    )

    documents = st.session_state.get("documents", [])
    if not documents:
        st.info("📚 Please upload PDF study notes in the **Dashboard** before generating quizzes.")
        if st.button("⬅️ Go to Dashboard to Upload", type="primary"):
            navigate_to(NAV_DASHBOARD)
            st.rerun()
        return

    quiz_gen = QuizGenerator(ai_service)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        doc_names = ["All Notes Combined"] + [d["filename"] for d in documents]
        selected_doc = st.selectbox("Select Material for Quiz", options=doc_names)
    with col2:
        num_q = st.selectbox("Number of Questions", options=[3, 5, 8, 10], index=1)
    with col3:
        difficulty = st.selectbox("Difficulty", options=["Easy", "Medium", "Hard"], index=1)

    topic_focus = st.text_input("Optional: Specific topic or chapter", placeholder="e.g. Cell Division or Chapter 4")

    # Get document text
    if selected_doc == "All Notes Combined":
        doc_text = "\n\n".join([d.get("full_text", "") for d in documents])
    else:
        target = next((d for d in documents if d["filename"] == selected_doc), None)
        doc_text = target.get("full_text", "") if target else ""

    if st.button("🎲 Generate Practice Quiz", type="primary", use_container_width=True):
        if not ai_service.is_configured():
            st.error("Please configure your Gemini API Key in the sidebar first.")
            return

        with st.spinner(f"Generating {num_q} {difficulty}-level questions strictly from your notes..."):
            try:
                questions = quiz_gen.generate_quiz(
                    document_text=doc_text,
                    num_questions=num_q,
                    difficulty=difficulty,
                    topic_focus=topic_focus if topic_focus.strip() else None,
                )
                st.session_state["quiz_data"] = questions
                st.session_state["quiz_user_answers"] = {}
                st.session_state["quiz_results"] = None
                st.success(f"Generated {len(questions)} questions successfully!")
            except AIServiceError as ae:
                st.error(str(ae))
            except Exception as e:
                st.error(f"Failed to generate quiz: {e}")

    # Render Active Quiz
    quiz_questions = st.session_state.get("quiz_data")
    if quiz_questions:
        st.markdown("<hr style='border: none; border-top: 1px solid #EDE9FE; margin: 24px 0;'>", unsafe_allow_html=True)
        st.markdown(f"### 📝 Quiz: {len(quiz_questions)} Questions ({difficulty})")

        results = st.session_state.get("quiz_results")

        # Form for answers
        with st.form("quiz_form"):
            for q in quiz_questions:
                q_id = q["id"]
                st.markdown(
                    f"""
                    <div style="font-weight: 600; font-size: 1rem; color: #1E1B4B; margin-top: 14px; margin-bottom: 8px;">
                        Question {q_id}: {q['question']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                opts = q["options"]
                opt_keys = ["A", "B", "C", "D"]
                opt_labels = [f"**{k}**: {opts.get(k, '')}" for k in opt_keys]

                # Pre-fill previous selection if any
                previous_choice = st.session_state["quiz_user_answers"].get(q_id, None)
                def_idx = opt_keys.index(previous_choice) if previous_choice in opt_keys else None

                selected_opt = st.radio(
                    f"Select answer for question {q_id}",
                    options=opt_keys,
                    format_func=lambda k: f"{k}) {opts.get(k, '')}",
                    index=def_idx if def_idx is not None else 0,
                    key=f"q_radio_{q_id}",
                    label_visibility="collapsed",
                )
                st.session_state["quiz_user_answers"][q_id] = selected_opt
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            submit_quiz = st.form_submit_button("✅ Submit Answers & View Score", type="primary", use_container_width=True)

            if submit_quiz:
                calculated = QuizGenerator.calculate_score(
                    st.session_state["quiz_user_answers"], quiz_questions
                )
                st.session_state["quiz_results"] = calculated
                st.rerun()

        # Display Results Banner and Explanation Breakdown
        if results:
            st.markdown("<hr style='border: none; border-top: 2px solid #EDE9FE; margin: 24px 0;'>", unsafe_allow_html=True)
            pct = results["percentage"]
            badge = results["badge"]
            msg = results["message"]
            correct = results["correct_count"]
            total = results["total_questions"]

            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
                    border: 2px solid #7C3AED;
                    border-radius: 14px;
                    padding: 24px;
                    text-align: center;
                    margin-bottom: 24px;
                ">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #7C3AED;">{badge}</div>
                    <div style="font-size: 2.4rem; font-weight: 800; color: #1E1B4B; margin: 6px 0;">
                        {correct} / {total} Correct ({pct}%)
                    </div>
                    <p style="margin: 0; color: #4B5563; font-size: 0.95rem;">{msg}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 🔍 Answer Review & Explanations")
            for item in results["details"]:
                q_id = item["id"]
                is_correct = item["is_correct"]
                user_c = item["user_choice"]
                corr_c = item["correct_choice"]
                explanation = item["explanation"]
                options = item["options"]

                card_border = "#10B981" if is_correct else "#EF4444"
                status_icon = "✅ Correct" if is_correct else "❌ Incorrect"
                status_color = "#065F46" if is_correct else "#991B1B"
                status_bg = "#ECFDF5" if is_correct else "#FEE2E2"

                st.markdown(
                    f"""
                    <div style="
                        background: white;
                        border-left: 4px solid {card_border};
                        border-radius: 10px;
                        padding: 16px 20px;
                        margin-bottom: 14px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: #1E1B4B;">Question {q_id}: {item['question']}</span>
                            <span style="background: {status_bg}; color: {status_color}; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">
                                {status_icon}
                            </span>
                        </div>
                        <div style="font-size: 0.88rem; margin: 8px 0; color: #374151;">
                            <div>Your Answer: <strong>Option {user_c} ({options.get(user_c, '')})</strong></div>
                            <div>Correct Answer: <strong>Option {corr_c} ({options.get(corr_c, '')})</strong></div>
                        </div>
                        <div style="background: #F8F9FE; padding: 10px 14px; border-radius: 8px; font-size: 0.84rem; color: #4B5563; margin-top: 8px;">
                            💡 <strong>Why?</strong> {explanation}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------------------------
# View 6: AI Flashcards
# ---------------------------------------------------------------------------
def render_flashcards_view(ai_service: GeminiService):
    st.markdown("## 🗂️ AI Flashcard Generator")
    st.markdown(
        "Active recall flashcards for fast memorization. Study one card at a time, "
        "reveal the answer when ready, and navigate through your study deck."
    )

    documents = st.session_state.get("documents", [])
    if not documents:
        st.info("📚 Please upload study materials in the **Dashboard** to generate flashcards.")
        if st.button("⬅️ Go to Dashboard to Upload", type="primary"):
            navigate_to(NAV_DASHBOARD)
            st.rerun()
        return

    flashcard_gen = FlashcardGenerator(ai_service)

    # Flashcard generation controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        doc_names = ["All Notes Combined"] + [d["filename"] for d in documents]
        selected_doc = st.selectbox("Select Study Material", options=doc_names, key="fc_doc_sel")
    with col2:
        num_cards = st.selectbox("Deck Size", options=[5, 8, 10, 15], index=1, key="fc_num_sel")
    with col3:
        focus_topic = st.text_input("Topic Focus (Optional)", placeholder="e.g. Definitions only")

    # Get document text
    if selected_doc == "All Notes Combined":
        doc_text = "\n\n".join([d.get("full_text", "") for d in documents])
    else:
        target = next((d for d in documents if d["filename"] == selected_doc), None)
        doc_text = target.get("full_text", "") if target else ""

    if st.button("🎴 Create Flashcard Deck", type="primary", use_container_width=True):
        if not ai_service.is_configured():
            st.error("Please configure your Gemini API Key in the sidebar first.")
            return

        with st.spinner(f"Creating {num_cards} study flashcards from your notes..."):
            try:
                cards = flashcard_gen.generate_flashcards(
                    document_text=doc_text,
                    num_cards=num_cards,
                    focus_area=focus_topic if focus_topic.strip() else None,
                )
                st.session_state["flashcards_data"] = cards
                st.session_state["current_flashcard_idx"] = 0
                st.session_state["flashcard_flipped"] = False
                st.success(f"Generated deck of {len(cards)} flashcards!")
            except AIServiceError as ae:
                st.error(str(ae))
            except Exception as e:
                st.error(f"Failed to create flashcards: {e}")

    # Active Flashcard Player
    cards = st.session_state.get("flashcards_data")
    if cards and len(cards) > 0:
        idx = st.session_state.get("current_flashcard_idx", 0)
        idx = max(0, min(idx, len(cards) - 1))
        st.session_state["current_flashcard_idx"] = idx

        current_card = cards[idx]
        is_flipped = st.session_state.get("flashcard_flipped", False)

        st.markdown("<hr style='border: none; border-top: 1px solid #EDE9FE; margin: 20px 0;'>", unsafe_allow_html=True)

        # Progress bar
        progress_val = int(((idx + 1) / len(cards)) * 100)
        st.progress(progress_val, text=f"Card {idx + 1} of {len(cards)} ({progress_val}%)")

        topic_tag = current_card.get("topic", "General")
        hint_text = current_card.get("hint", "")

        # Flashcard Box
        if not is_flipped:
            # Front of card
            st.markdown(
                f"""
                <div class="flashcard-box flashcard-front">
                    <span style="background: #EDE9FE; color: #6D28D9; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 16px;">
                        📌 {topic_tag} • Front
                    </span>
                    <h2 style="color: #1E1B4B; font-weight: 700; margin: 0 0 16px 0; max-width: 600px;">
                        {current_card['front']}
                    </h2>
                    <p style="color: #64748B; font-size: 0.85rem; margin: 0;">
                        💡 <em>Hint: {hint_text}</em>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Back of card
            st.markdown(
                f"""
                <div class="flashcard-box flashcard-back">
                    <span style="background: #7C3AED; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 16px;">
                        ✨ {topic_tag} • Answer Revealed
                    </span>
                    <div style="font-size: 1.15rem; color: #1E1B4B; font-weight: 500; line-height: 1.6; max-width: 650px; text-align: left;">
                        {current_card['back']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Flashcard Navigation Controls
        btn_prev, btn_flip, btn_next = st.columns([1, 2, 1])

        with btn_prev:
            if st.button("⬅️ Previous Card", use_container_width=True, disabled=(idx == 0)):
                st.session_state["current_flashcard_idx"] = idx - 1
                st.session_state["flashcard_flipped"] = False
                st.rerun()

        with btn_flip:
            flip_label = "🔄 Flip to Question" if is_flipped else "🔍 Flip to Reveal Answer"
            if st.button(flip_label, type="primary", use_container_width=True):
                st.session_state["flashcard_flipped"] = not is_flipped
                st.rerun()

        with btn_next:
            if st.button("Next Card ➡️", use_container_width=True, disabled=(idx == len(cards) - 1)):
                st.session_state["current_flashcard_idx"] = idx + 1
                st.session_state["flashcard_flipped"] = False
                st.rerun()

        # Deck overview drawer
        with st.expander(f"📑 Browse All {len(cards)} Cards in Deck"):
            for i, c in enumerate(cards, 1):
                st.markdown(f"**{i}. {c['front']}**")
                st.markdown(f"> *{c['back']}*")
                st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px dashed #EDE9FE;'>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# View 7: Study Mode
# ---------------------------------------------------------------------------
def render_study_mode_view(ai_service: GeminiService):
    st.markdown("## 💡 Study Mode: Deep-Dive Concept Tutor")
    st.markdown(
        "Master tricky concepts with simple analogies, intuitive explanations, "
        "and practice exercises grounded strictly in your study materials."
    )

    documents = st.session_state.get("documents", [])
    if not documents:
        st.info("📚 Please upload study materials in the **Dashboard** to use Study Mode.")
        if st.button("⬅️ Go to Dashboard to Upload", type="primary"):
            navigate_to(NAV_DASHBOARD)
            st.rerun()
        return

    tutor = StudyModeTutor(ai_service)
    combined_text = "\n\n".join([d.get("full_text", "") for d in documents])

    # Auto-discover topics
    if "discovered_topics" not in st.session_state or not st.session_state["discovered_topics"]:
        if ai_service.is_configured():
            with st.spinner("Analyzing uploaded notes to detect key topics..."):
                st.session_state["discovered_topics"] = tutor.discover_topics(combined_text)
        else:
            st.session_state["discovered_topics"] = []

    topics = st.session_state.get("discovered_topics", [])
    topic_options = ["Custom Topic / Question..."] + topics

    col1, col2 = st.columns([2, 1])
    with col1:
        chosen_topic_item = st.selectbox(
            "Select a Detected Topic from Your Notes",
            options=topic_options,
            help="Choose an auto-detected topic or type your own concept below.",
        )
    with col2:
        style = st.selectbox(
            "Explanation Style",
            options=[
                "Intuitive & Analogy-Driven (ELI5)",
                "Standard Academic with Examples",
                "Rigorous & Formula-Focused",
            ],
            index=0,
        )

    if chosen_topic_item == "Custom Topic / Question...":
        custom_topic = st.text_input("Enter Concept to Master", placeholder="e.g. Mitosis vs Meiosis, or Ohm's Law")
        final_concept = custom_topic
    else:
        final_concept = chosen_topic_item

    if st.button("🚀 Explain & Teach Me This Concept", type="primary", use_container_width=True):
        if not final_concept or not final_concept.strip():
            st.warning("Please enter or select a topic to study.")
            return

        if not ai_service.is_configured():
            st.error("Please configure your Gemini API Key in the sidebar first.")
            return

        with st.spinner(f"Preparing comprehensive lesson on '{final_concept}'..."):
            try:
                explanation = tutor.explain_concept(
                    concept=final_concept,
                    context_text=combined_text,
                    depth=style,
                )
                st.session_state["study_explanation"] = explanation
                st.session_state["study_concept_title"] = final_concept
            except AIServiceError as ae:
                st.error(str(ae))
            except Exception as e:
                st.error(f"Error generating study explanation: {e}")

    # Render Explanation
    if "study_explanation" in st.session_state and st.session_state["study_explanation"]:
        title = st.session_state.get("study_concept_title", "Concept Lesson")
        st.markdown("<hr style='border: none; border-top: 1px solid #EDE9FE; margin: 24px 0;'>", unsafe_allow_html=True)
        st.markdown(f"### 📖 Masterclass: {title}")

        st.markdown(
            """
            <div style="
                background: white;
                border: 1px solid #EDE9FE;
                border-radius: 14px;
                padding: 28px 32px;
                box-shadow: 0 4px 20px rgba(124, 58, 237, 0.05);
                line-height: 1.7;
            ">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state["study_explanation"])
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main Application Router
# ---------------------------------------------------------------------------
def main():
    initialize_session_state()
    inject_custom_css()

    ai_service: GeminiService = st.session_state["ai_service"]
    pdf_reader: PDFReader = st.session_state["pdf_reader"]
    chunker: TextChunker = st.session_state["chunker"]
    retriever: RAGRetriever = st.session_state["retriever"]

    # Render Sidebar and get active view
    active_nav = render_sidebar(ai_service)

    # Dispatch to appropriate page view
    if active_nav == NAV_DASHBOARD:
        render_dashboard(pdf_reader, chunker, retriever, navigate_to)
    elif active_nav == NAV_MY_DOCUMENTS:
        render_documents_manager(
            documents=st.session_state.get("documents", []),
            delete_callback=delete_document_callback,
        )
    elif active_nav == NAV_SUMMARIZER:
        render_summarizer_view(ai_service)
    elif active_nav == NAV_CHAT:
        render_chat_view(ai_service, retriever)
    elif active_nav == NAV_QUIZ:
        render_quiz_view(ai_service)
    elif active_nav == NAV_FLASHCARDS:
        render_flashcards_view(ai_service)
    elif active_nav == NAV_STUDY_MODE:
        render_study_mode_view(ai_service)
    else:
        render_dashboard(pdf_reader, chunker, retriever, navigate_to)


if __name__ == "__main__":
    main()

