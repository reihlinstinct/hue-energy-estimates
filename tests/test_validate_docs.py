import tempfile
import unittest
from pathlib import Path
from scripts.validate_docs import REQUIRED, validate


class DocsValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for filename, phrases in REQUIRED.items():
            path = self.root / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('\n'.join(phrases), encoding='utf-8')

    def test_valid_synthetic_tree(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_file(self):
        (self.root / 'README.md').unlink()
        self.assertTrue(validate(self.root))

    def test_missing_guardrail(self):
        (self.root / 'docs/DESIGN.md').write_text('placeholder')
        self.assertTrue(validate(self.root))

    def test_nul_is_rejected(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\x00')
        self.assertTrue(validate(self.root))


if __name__ == '__main__':
    unittest.main()
