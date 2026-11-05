"""Offline regression checks for the committed privacy caller contract."""
from pathlib import Path
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/docs.yml'
PIN = 'reihlinstinct/repo-checks/actions/privacy@c9a60fadeecab75bde9674e96b3d76a5e2fe6645'


class PrivacyWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding='utf-8')
        self.privacy = self.text.split('\n  privacy:\n', 1)[1].split('\n  alert:', 1)[0]

    def test_pinned_isolated_action(self):
        self.assertIn('uses: ' + PIN + '\n', self.privacy)
        self.assertIn('checkout-root: ${{ github.workspace }}', self.privacy)
        self.assertNotIn('continue-on-error', self.privacy)

    def test_checkout_and_bounded_job(self):
        self.assertIn('persist-credentials: false', self.privacy)
        self.assertIn('timeout-minutes: 3', self.privacy)
        self.assertIn('actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1', self.privacy)

    def test_summary_includes_privacy_even_on_failure(self):
        summary = self.text.split('\n  summary:\n', 1)[1]
        self.assertIn('if: always()', summary)
        self.assertIn('needs: [docs, privacy]', summary)
        self.assertIn('NEEDS_JSON: ${{ toJSON(needs) }}', summary)

    def test_scheduled_alert_waits_for_privacy(self):
        alert = self.text.split('\n  alert:\n', 1)[1].split('\n  summary:', 1)[0]
        self.assertIn('needs: [docs, privacy, summary]', alert)
        self.assertIn("if: failure() && github.event_name == 'schedule'", alert)

    def test_existing_checks_kept(self):
        self.assertIn('python3 scripts/validate_docs.py', self.text)
        self.assertIn('python3 -m unittest discover -s tests -v', self.text)
        self.assertIn('permissions:\n  contents: read\n', self.text)
