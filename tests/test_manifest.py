"""The manifests: .claude-plugin/plugin.json, .claude-plugin/marketplace.json and
.mcp.json.

What they hold is what the plugin directory's pre-submission checklist asks for
(a lowercase hyphenated name, a display name, a description, a semantic version,
the author, the homepage, a licence, keywords, an icon) and what this plugin has
decided: its name and listing name never change, and the connector file names
one server, `adcopilot`, at the one address every AdCopilot plugin uses, so
Claude, which matches a plugin's server by its address, connects it once.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; reads no environment variable).
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPO = "adcopilot-linkedin-ads-plugin"
NAME = "adcopilot-linkedin-ads"
DISPLAY_NAME = "AdCopilot for LinkedIn Ads"
OWNER = "LinkedIn"

# The field set, in the order the manifest writes it.
PLUGIN_KEYS = [
    "name", "version", "description", "author", "homepage", "privacyPolicyUrl",
    "documentationUrl", "termsOfServiceUrl", "supportUrl", "repository",
    "license", "keywords", "displayName", "icon",
]

# The connector file, held to one exact text: the server key `adcopilot` and the
# address spelled one way (lowercase, no trailing slash, no query string), so
# Claude sees the same server as every other AdCopilot plugin's and asks for one
# sign-in.
MCP_CANONICAL = {
    "mcpServers": {
        "adcopilot": {"type": "http", "url": "https://mcp.adcopilot.cloud/mcp"}
    }
}
MCP_CANONICAL_TEXT = (
    '{"mcpServers":{"adcopilot":{"type":"http","url":"https://mcp.adcopilot.cloud/mcp"}}}\n'
)

NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
KEYWORD = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PluginManifest(unittest.TestCase):

    def setUp(self):
        self.plugin = load(".claude-plugin/plugin.json")

    def test_the_fields_are_exactly_these_in_this_order(self):
        self.assertEqual(list(self.plugin), PLUGIN_KEYS)

    def test_name_and_display_name_are_the_decided_ones(self):
        self.assertRegex(self.plugin["name"], NAME_PATTERN)
        self.assertEqual(self.plugin["name"], NAME)
        self.assertEqual(self.plugin["displayName"], DISPLAY_NAME)

    def test_version_is_semver(self):
        self.assertRegex(self.plugin["version"], SEMVER)

    def test_author_and_links(self):
        self.assertEqual(self.plugin["author"],
                         {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})
        self.assertEqual(self.plugin["homepage"], "https://adcopilot.cloud")
        self.assertEqual(self.plugin["documentationUrl"], "https://adcopilot.cloud/docs/")
        self.assertEqual(self.plugin["privacyPolicyUrl"], "https://adcopilot.cloud/privacy")
        self.assertEqual(self.plugin["termsOfServiceUrl"], "https://adcopilot.cloud/terms")
        self.assertEqual(self.plugin["supportUrl"],
                         "https://github.com/AtromxIntelligence/%s/issues" % REPO)
        self.assertEqual(self.plugin["repository"],
                         "https://github.com/AtromxIntelligence/%s" % REPO)
        self.assertEqual(self.plugin["license"], "MIT")

    def test_every_url_in_the_manifests_is_https(self):
        urls = []

        def walk(value):
            if isinstance(value, dict):
                for v in value.values():
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
            elif isinstance(value, str) and "://" in value:
                urls.append(value)

        for relative in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".mcp.json"):
            walk(load(relative))
        self.assertGreater(len(urls), 5)
        for url in urls:
            self.assertTrue(url.startswith("https://"), url)

    def test_description_says_what_it_does_today_and_what_it_does_not(self):
        description = self.plugin["description"]
        self.assertIsInstance(description, str)
        self.assertLessEqual(len(description), 600)
        self.assertTrue(description.startswith("LinkedIn Ads"), description)
        self.assertIn("Direct access to your LinkedIn ad account is being built; there is no date.",
                      description)
        self.assertIn("proposed first", description)
        self.assertTrue(description.endswith("Made by Atromx Intelligence, not by %s." % OWNER),
                        description)

    def test_keywords_are_at_most_fifteen_and_kebab_case(self):
        keywords = self.plugin["keywords"]
        self.assertIsInstance(keywords, list)
        self.assertLessEqual(len(keywords), 15)
        self.assertEqual(len(set(keywords)), len(keywords), "a keyword is listed twice")
        for keyword in keywords:
            self.assertRegex(keyword, KEYWORD)

    def test_icon_is_our_own_png(self):
        self.assertEqual(self.plugin["icon"], "./.claude-plugin/icon.png")
        icon = ROOT / ".claude-plugin" / "icon.png"
        self.assertTrue(icon.is_file())
        self.assertEqual(icon.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        # One icon, ours: no vector copy beside it.
        self.assertFalse((ROOT / ".claude-plugin" / "icon.svg").exists())


class MarketplaceManifest(unittest.TestCase):

    def test_it_names_this_plugin_with_source_dot_slash_and_no_listing_fields(self):
        market = load(".claude-plugin/marketplace.json")
        self.assertEqual(market["name"], REPO)
        self.assertEqual(market["owner"],
                         {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})
        self.assertIsInstance(market["description"], str)
        self.assertEqual(len(market["plugins"]), 1)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], NAME)
        self.assertEqual(entry["source"], "./")
        self.assertEqual(entry["category"], "Marketing")
        self.assertIsInstance(entry["description"], str)
        # The directory's listing fields belong in plugin.json: validate reports
        # them in a marketplace entry as unknown.
        self.assertEqual(sorted(entry), ["category", "description", "name", "source"])


class ConnectorFile(unittest.TestCase):

    def test_mcp_json_is_the_canonical_file_exactly(self):
        self.assertEqual(load(".mcp.json"), MCP_CANONICAL)
        raw = (ROOT / ".mcp.json").read_text(encoding="utf-8")
        self.assertEqual(raw, MCP_CANONICAL_TEXT)

    def test_it_holds_one_server_called_adcopilot_with_no_launcher_and_no_header(self):
        servers = load(".mcp.json")["mcpServers"]
        self.assertEqual(list(servers), ["adcopilot"])
        self.assertEqual(sorted(servers["adcopilot"]), ["type", "url"])


if __name__ == "__main__":
    unittest.main()
