import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


hookscore = load("hookscore", "skills/ig-reel/hookscore.py")
beats = load("beats", "skills/ig-reel/beats.py")
caption = load("caption", "skills/ig-caption/caption.py")
humanize = load("humanize", "skills/ig-human/humanize.py")
detect = load("detect", "skills/ig-human/detect.py")
swipe = load("swipe", "skills/ig-viral/swipe.py")


class ToolSmokeTests(unittest.TestCase):
    def test_spanish_hook_is_detected_and_scored(self):
        text = "Nadie te dice que tus primeros 30 reels pueden fallar."
        self.assertEqual(hookscore.language(text), "es")
        checks, score, verdict, flags = hookscore.run(text, "es")
        self.assertIn("SPECIFICITY", checks)
        self.assertGreaterEqual(score, 0)
        self.assertIn(verdict, {"WEAK", "OK", "STRONG"})
        self.assertIsInstance(flags, list)

    def test_spanish_swipe_formula(self):
        fid, name = swipe.classify("Nadie te dice que los primeros reels fallan", [], "es")
        self.assertEqual(fid, 3)
        self.assertEqual(name, "Nadie te lo dice")

    def test_spanish_caption_ask(self):
        result = caption.analyse("Guarda este post para mañana.\n\n#automatizacion")
        self.assertEqual(result["asks"], ["guardar"])

    def test_beat_sheet_accepts_accents(self):
        result = beats.analyse("Álvaro perdió 2 horas.\nAhora Álvaro ahorra 2 horas.")
        self.assertGreater(result["total_words"], 4)
        self.assertEqual(len(result["beats"]), 2)

    def test_spanish_editorial_cleanup(self):
        lex = humanize.load_lexicon()
        clean, report = humanize.humanize("En este vídeo te voy a enseñar un hack definitivo.", lex)
        self.assertNotIn("te voy a enseñar", clean.lower())
        self.assertGreater(len(report["lexical"]), 0)

    def test_spanish_style_panel(self):
        lex = json.loads((ROOT / "skills/ig-human/slop.json").read_text(encoding="utf-8"))
        text = "Yo perdí 300 euros en Madrid. Pero aprendí algo. Tú puedes evitarlo. Guarda el contrato."
        results, score, verdict = detect.run(text, lex, "es")
        self.assertEqual(set(results), set(detect.CHECKS))
        self.assertGreaterEqual(score, 0)
        self.assertIn(verdict, {"FLAGGED", "REVIEW", "PASS"})


if __name__ == "__main__":
    unittest.main()
