"""
NoteGenius AI - Comprehensive Unit & Integration Tests
======================================================
Tests PDF extraction, chunking, TF-IDF RAG retrieval, quiz scoring,
flashcard parsing, and error handling.
"""

import os
import sys
import io
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.pdf_reader import PDFReader, PDFReaderError
from modules.text_chunker import TextChunker
from modules.retriever import RAGRetriever
from modules.ai_service import GeminiService, AIServiceError
from modules.quiz_generator import QuizGenerator
from modules.flashcards import FlashcardGenerator


class TestNoteGeniusCore(unittest.TestCase):

    def setUp(self):
        self.pdf_reader = PDFReader()
        self.chunker = TextChunker(chunk_size=300, chunk_overlap=50)
        self.retriever = RAGRetriever(top_k=3, similarity_threshold=0.01)

    def test_text_chunking(self):
        """Test intelligent text chunking with metadata preservation."""
        sample_doc = {
            "doc_id": "test_doc_01",
            "filename": "biology_notes.pdf",
            "pages": [
                {
                    "page_number": 1,
                    "text": (
                        "Photosynthesis is the process used by plants and other organisms to convert "
                        "light energy into chemical energy. This chemical energy is stored in carbohydrate "
                        "molecules, such as sugars, which are synthesized from carbon dioxide and water. "
                        "In most cases, oxygen is also released as a waste product."
                    ),
                },
                {
                    "page_number": 2,
                    "text": (
                        "Cellular respiration is a set of metabolic reactions and processes that take place "
                        "in the cells of organisms to convert biochemical energy from nutrients into ATP. "
                        "The catabolic reactions involved in respiration include glycolysis, citric acid cycle, "
                        "and oxidative phosphorylation."
                    ),
                },
            ],
            "is_scanned_or_empty": False,
        }

        chunks = self.chunker.chunk_document(sample_doc)
        self.assertGreater(len(chunks), 0)
        first_chunk = chunks[0]

        self.assertIn("chunk_id", first_chunk)
        self.assertEqual(first_chunk["doc_name"], "biology_notes.pdf")
        self.assertEqual(first_chunk["page_number"], 1)
        self.assertIn("Photosynthesis", first_chunk["text"])

    def test_rag_retrieval(self):
        """Test TF-IDF indexing and cosine similarity retrieval."""
        sample_chunks = [
            {
                "chunk_id": "c1",
                "doc_name": "physics.pdf",
                "page_number": 1,
                "text": "Newton's First Law states that an object at rest stays at rest unless acted upon by a net external force.",
            },
            {
                "chunk_id": "c2",
                "doc_name": "physics.pdf",
                "page_number": 2,
                "text": "Newton's Second Law defines force as mass times acceleration, F = ma.",
            },
            {
                "chunk_id": "c3",
                "doc_name": "biology.pdf",
                "page_number": 5,
                "text": "Mitochondria produce ATP through cellular respiration, powering cell processes.",
            },
        ]

        indexed = self.retriever.build_index(sample_chunks)
        self.assertTrue(indexed)
        self.assertTrue(self.retriever.is_indexed())

        # Test relevant query
        results = self.retriever.retrieve("What is Newton's second law with force and acceleration?")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["chunk_id"], "c2")
        self.assertGreater(results[0]["similarity_score"], 0.1)

        # Test context formatting
        formatted = self.retriever.format_context_for_prompt(results)
        self.assertIn("[Source 1: physics.pdf | Page 2", formatted)
        self.assertIn("F = ma", formatted)

        # Test biology query
        bio_results = self.retriever.retrieve("How does the cell produce ATP energy?")
        self.assertGreater(len(bio_results), 0)
        self.assertEqual(bio_results[0]["chunk_id"], "c3")

    def test_quiz_scoring(self):
        """Test quiz calculation and evaluation."""
        sample_questions = [
            {
                "id": 1,
                "question": "What is the formula for force?",
                "options": {"A": "F = ma", "B": "E = mc^2", "C": "V = IR", "D": "PV = nRT"},
                "correct_answer": "A",
                "explanation": "Newton's second law states F = ma.",
            },
            {
                "id": 2,
                "question": "What organelle produces ATP?",
                "options": {"A": "Ribosome", "B": "Mitochondria", "C": "Nucleus", "D": "Vacuole"},
                "correct_answer": "B",
                "explanation": "Mitochondria produce ATP.",
            },
        ]

        # Scenario 1: Both correct (100%)
        user_answers = {1: "A", 2: "B"}
        score_100 = QuizGenerator.calculate_score(user_answers, sample_questions)
        self.assertEqual(score_100["correct_count"], 2)
        self.assertEqual(score_100["percentage"], 100.0)
        self.assertIn("Master Genius", score_100["badge"])

        # Scenario 2: One wrong (50%)
        user_answers_half = {1: "A", 2: "C"}
        score_50 = QuizGenerator.calculate_score(user_answers_half, sample_questions)
        self.assertEqual(score_50["correct_count"], 1)
        self.assertEqual(score_50["percentage"], 50.0)

    def test_flashcard_json_parsing(self):
        """Test flashcard JSON sanitization."""
        ai = GeminiService(api_key="mock_key")
        fc_gen = FlashcardGenerator(ai)

        raw_json_response = """```json
[
  {
    "id": 1,
    "topic": "Physics",
    "front": "What is inertia?",
    "back": "Resistance of an object to changes in its state of motion.",
    "hint": "Related to Newton's first law."
  }
]
```"""
        parsed = fc_gen._parse_flashcards_json(raw_json_response)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["front"], "What is inertia?")
        self.assertEqual(parsed[0]["topic"], "Physics")

    def test_missing_api_key_error(self):
        """Ensure missing API key triggers a clear, helpful error message for both providers."""
        ai = GeminiService(gemini_api_key="")
        with self.assertRaises(AIServiceError) as ctx:
            ai.generate_text("Hello")
        self.assertIn("Gemini API key is missing", str(ctx.exception))

        # Test Groq provider
        ai.set_provider("Groq Cloud")
        with self.assertRaises(AIServiceError) as ctx2:
            ai.generate_text("Hello")
        self.assertIn("Groq API key is missing", str(ctx2.exception))

    def test_provider_switching_and_models(self):
        """Test switching between Gemini and Groq providers and model selection."""
        ai = GeminiService(gemini_api_key="mock_gemini", groq_api_key="mock_groq")
        self.assertEqual(ai.provider, "Google Gemini")
        self.assertIn("gemini-3.8-flash", ai.get_available_models())

        ai.set_provider("Groq Cloud")
        self.assertEqual(ai.provider, "Groq Cloud")
        self.assertIn("openai/gpt-oss-120b", ai.get_available_models())
        self.assertEqual(ai.model_name, "openai/gpt-oss-120b")


if __name__ == "__main__":
    unittest.main()

