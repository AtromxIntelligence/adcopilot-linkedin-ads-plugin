"""The plugin's own text: its skills, its commands and its README.

This plugin is instructions only, so what it promises is what its files say. These
tests hold the text to what it can back, without a model:

* every skill and command has front matter that parses, a `name` equal to its
  folder or file name, and a one-line text `description`;
* every tool a skill or command names is one the AdCopilot connector serves
  (tests/connector_tools.txt) and one that skill is meant to use, so a skill
  that is not meant to use a tool names none, and none names a Google Ads tool;
* tools are named by their bare names, never by the full name a client builds,
  because that name belongs to whichever AdCopilot plugin loaded first;
* every `get_org_context` call carries this plugin's own `source`, never the
  bare marker, which hands the turn to skills that are not installed here, and
  never a version alone, which reads as an old version of the main plugin;
* every skill says that every change is proposed first and made only on a yes;
* the first answer of every skill and of the setup command says what works today
  and what does not, in the same words;
* the README carries the trademark line, the plans line and the version
  paragraph, and has more than the directory's 40 words outside code.

Run with `python3 -m unittest discover -s tests -v` from the repository root
(stdlib only; reads no environment variable).
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
NAME = PLUGIN["name"]
VERSION = PLUGIN["version"]
SOURCE = "claude-plugin/%s/%s" % (NAME, VERSION)

# Said once, in the first answer, in these words: a plugin for an ad platform
# says plainly what works today and what does not.
TODAY_LATER = (
    "Today it checks your LinkedIn Insight Tag in Google Tag Manager, reports "
    "LinkedIn traffic and key events in Google Analytics (GA4) by source, medium "
    "and campaign, finds UTM mistakes, guides conversion setup, plans B2B "
    "campaigns, drafts Sponsored Content copy and does the budget pacing math. "
    "It cannot read your LinkedIn ad account yet: direct access is planned for "
    "when LinkedIn approves AdCopilot's API access, and there is no date."
)

# The approval promise, in every skill.
APPROVAL = (
    "Every change is proposed first, with what it changes and how to undo it, and "
    "is applied only after the customer's explicit yes in this conversation."
)

TRADEMARK = "Not affiliated with or endorsed by LinkedIn or Google."
TRADEMARK_OWNER = "LinkedIn is a trademark of LinkedIn Corporation"
TRADEMARK_GOOGLE = "Google Analytics and Google Tag Manager are trademarks of Google LLC."
PLANS_LINE = ("The plugin is free (MIT). The AdCopilot connector is a hosted service: "
              "Free plan available; paid plans on https://adcopilot.cloud/pricing")

# The tools each skill is meant to use. A tool outside its own set fails, so a
# skill cannot start to read or change what it was not written for.
SKILL_TOOLS = {
    "linkedin-ads-tracking": {
        "get_org_context", "gtm_list_accounts", "gtm_list_containers",
        "gtm_list_workspaces", "gtm_list_tags", "gtm_list_triggers",
        "gtm_list_version_headers", "gtm_create_trigger", "gtm_create_tag",
    },
    "linkedin-ads-traffic": {
        "get_org_context", "ga4_list_account_summaries", "ga4_get_metadata",
        "ga4_run_report", "ga4_list_conversion_events",
    },
    "linkedin-ads-plan": {"get_org_context"},
    "linkedin-ads-budget": set(),
}
# The commands: setup is its own work, check and plan follow a skill.
COMMAND_TOOLS = {
    "setup": {"get_org_context"},
    "check": set(),
    "plan": set(),
}
COMMAND_FOLLOWS = {"check": "linkedin-ads-tracking", "plan": "linkedin-ads-plan"}

# Words in backticks that are written in snake_case and are not a tool: the
# connector's own field names, parameter names and UTM keys.
NOT_TOOLS = {
    "next_step", "needs_readd", "start_date", "end_date", "firing_trigger_id",
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
}

SNAKE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
BARE_TOOL = re.compile(r"\b(?:gsc|ga4|gtm)_[a-z0-9_]*[a-z0-9]\b|\b(?:get|save)_org_context\b")
BACKTICKED = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"```.*?```", re.S)


def squash(text):
    return re.sub(r"\s+", " ", text)


def connector_tools():
    names = set()
    for line in (ROOT / "tests" / "connector_tools.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            names.add(line)
    return names


def skill_files():
    return sorted((ROOT / "skills").glob("*/SKILL.md"))


def command_files():
    return sorted((ROOT / "commands").glob("*.md"))


def front_matter(path):
    """(fields, body). Front matter here is flat `key: value` lines between two
    `---` lines, which is all a skill or a command carries."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError("%s does not start with ---" % path)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("%s has no closing ---" % path)
    fields = {}
    for line in text[4:end].split("\n"):
        match = re.match(r"^([a-z][a-z-]*): (.+)$", line)
        if not match:
            raise AssertionError("%s: front matter line is not `key: value`: %r" % (path, line))
        key, value = match.groups()
        if key in fields:
            raise AssertionError("%s: %s is given twice" % (path, key))
        fields[key] = value
    return fields, text[end + 5:]


def tool_names_in(text):
    """Every tool-like name a text uses: backticked snake_case words that are not
    known field names, and bare gsc_/ga4_/gtm_ names or get_/save_org_context."""
    found = set(BARE_TOOL.findall(text))
    for span in BACKTICKED.findall(text):
        word = span.strip()
        if SNAKE.match(word) and word not in NOT_TOOLS:
            found.add(word)
    return found


class SkillsAndCommands(unittest.TestCase):

    def test_the_skills_are_the_decided_ones(self):
        self.assertEqual(sorted(p.parent.name for p in skill_files()), sorted(SKILL_TOOLS))
        self.assertEqual(sorted(p.stem for p in command_files()), sorted(COMMAND_TOOLS))

    def test_front_matter_parses_and_names_match(self):
        for path in skill_files() + command_files():
            fields, body = front_matter(path)
            self.assertEqual(sorted(fields), ["description", "name"], path)
            expected = path.parent.name if path.name == "SKILL.md" else path.stem
            self.assertEqual(fields["name"], expected, path)
            self.assertTrue(body.strip(), "%s has no body" % path)

    def test_a_description_is_one_text_line_a_yaml_reader_takes_as_text(self):
        for path in skill_files() + command_files():
            fields, _ = front_matter(path)
            description = fields["description"]
            self.assertGreater(len(description), 30, path)
            self.assertLessEqual(len(description), 1000, path)
            # Plain YAML text: nothing that opens a list, a map, a quote or a
            # comment, and no `: ` or ` #` inside it.
            self.assertNotRegex(description[0], r"""[\[\]{}*&!|>'"%@`#,?-]""", path)
            self.assertNotIn(": ", description, path)
            self.assertNotIn(" #", description, path)
        for path in skill_files():
            self.assertIn("Use when", front_matter(path)[0]["description"], path)

    def test_commands_follow_a_skill_that_exists(self):
        for command, skill in COMMAND_FOLLOWS.items():
            body = front_matter(ROOT / "commands" / ("%s.md" % command))[1]
            self.assertIn("Follow the `%s` skill" % skill, squash(body), command)
            self.assertTrue((ROOT / "skills" / skill / "SKILL.md").is_file(), skill)

    def test_every_tool_named_is_one_the_connector_serves_and_the_file_is_meant_to_use(self):
        served = connector_tools()
        self.assertIn("get_org_context", served)
        self.assertIn("gtm_create_tag", served)
        for path in skill_files():
            skill = path.parent.name
            used = tool_names_in(path.read_text(encoding="utf-8"))
            self.assertFalse(used - served, "%s names a tool the connector does not serve: %s"
                             % (skill, sorted(used - served)))
            self.assertFalse(used - SKILL_TOOLS[skill], "%s names a tool outside its own set: %s"
                             % (skill, sorted(used - SKILL_TOOLS[skill])))
        for path in command_files():
            used = tool_names_in(path.read_text(encoding="utf-8"))
            self.assertFalse(used - served, path)
            self.assertFalse(used - COMMAND_TOOLS[path.stem], "%s names a tool outside its own set: %s"
                             % (path.stem, sorted(used - COMMAND_TOOLS[path.stem])))

    def test_each_skill_names_every_tool_it_is_meant_to_use(self):
        for path in skill_files():
            skill = path.parent.name
            used = tool_names_in(path.read_text(encoding="utf-8"))
            self.assertFalse(SKILL_TOOLS[skill] - used,
                             "%s never names: %s" % (skill, sorted(SKILL_TOOLS[skill] - used)))

    def test_no_file_names_a_tool_by_its_full_client_name(self):
        for path in skill_files() + command_files() + [ROOT / "README.md"]:
            self.assertNotIn("mcp__plugin_", path.read_text(encoding="utf-8"), path)

    def test_get_org_context_carries_this_plugins_own_source(self):
        needle = "source: \"%s\"" % SOURCE
        for path in skill_files() + command_files():
            text = squash(path.read_text(encoding="utf-8"))
            calls = "get_org_context" in tool_names_in(text)
            if calls:
                self.assertIn(needle, text, "%s calls get_org_context without its source" % path)
        # Never the bare marker, and never a version with no plugin name.
        bare = re.compile(r"(?<![A-Za-z0-9-])claude-plugin(?![A-Za-z0-9-])(?!/)")
        versioned = re.compile(r"(?<![A-Za-z0-9-])claude-plugin/(?!%s(?![A-Za-z0-9.-]))" % re.escape(NAME + "/" + VERSION))
        for path in skill_files() + command_files() + [ROOT / "README.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(bare.search(text), "%s sends the bare claude-plugin marker" % path)
            self.assertIsNone(versioned.search(text), "%s sends a source that is not %s" % (path, SOURCE))

    def test_a_scheduled_run_is_marked_and_nothing_is_scheduled(self):
        for path in skill_files() + command_files():
            text = squash(path.read_text(encoding="utf-8"))
            if "get_org_context" in tool_names_in(text):
                self.assertIn('source: "claude-scheduled"', text, path)
                self.assertIn("This plugin schedules nothing.", text, path)

    def test_every_skill_holds_the_approval_paragraph(self):
        for path in skill_files():
            self.assertIn(APPROVAL, squash(path.read_text(encoding="utf-8")), path)

    def test_a_skill_that_writes_says_where_and_never_publishes(self):
        text = squash((ROOT / "skills" / "linkedin-ads-tracking" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("workspace named `AdCopilot`", text)
        self.assertIn("nothing goes live", text)
        self.assertIn("Nothing is ever deleted.", text)
        for skill in ("linkedin-ads-traffic", "linkedin-ads-plan", "linkedin-ads-budget"):
            other = squash((ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("Nothing is ever deleted.", other, skill)

    def test_the_first_answer_says_what_works_today_and_what_does_not(self):
        for path in skill_files() + [ROOT / "commands" / "setup.md"]:
            text = squash(path.read_text(encoding="utf-8"))
            self.assertEqual(text.count(TODAY_LATER), 1, "%s must say it exactly once" % path)

    def test_a_product_that_is_not_connected_is_said_in_the_servers_words(self):
        for skill in ("linkedin-ads-tracking", "linkedin-ads-traffic"):
            text = squash((ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("`unlocks` field", text, skill)
            self.assertIn("never a link from memory", text, skill)

    def test_every_skill_names_what_it_cannot_see(self):
        for path in skill_files():
            self.assertIn("## What this cannot see", path.read_text(encoding="utf-8"), path)

    def test_no_skill_makes_a_claim_it_cannot_back(self):
        for path in skill_files() + command_files():
            text = squash(path.read_text(encoding="utf-8")).lower()
            for phrase in ("guarantee", "guaranteed", "we will approve", "benchmark of"):
                self.assertNotIn(phrase, text, "%s says %r" % (path, phrase))


class Readme(unittest.TestCase):

    def setUp(self):
        self.text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.flat = squash(self.text)

    def test_the_trademark_line_and_the_plans_line(self):
        self.assertIn(TRADEMARK, self.flat)
        self.assertIn(TRADEMARK_OWNER, self.flat)
        self.assertIn(TRADEMARK_GOOGLE, self.flat)
        self.assertIn("Made by Atromx Intelligence (https://adcopilot.cloud).", self.flat)
        self.assertIn(PLANS_LINE, self.flat)

    def test_it_has_more_than_the_directorys_forty_words_outside_code(self):
        prose = FENCE.sub(" ", self.text)
        words = re.findall(r"[A-Za-z0-9'][A-Za-z0-9'.-]*", prose)
        self.assertGreater(len(words), 40)
        self.assertGreaterEqual(len(words), 600)
        self.assertLessEqual(len(words), 1300)

    def test_it_says_what_works_today_and_what_comes_later(self):
        self.assertIn("**What comes later.** AdCopilot cannot read your LinkedIn ad account yet.", self.flat)
        self.assertIn("and there is no date.", self.flat)

    def test_it_holds_the_sections_the_directory_expects(self):
        for heading in ("# AdCopilot for LinkedIn Ads", "## Install", "## Already use another AdCopilot plugin?",
                        "## What you get", "## What it will not do", "## Data", "## Support",
                        "## Version", "## Licence", "## What CI runs"):
            self.assertIn(heading, self.text)
        self.assertIn("### Claude Code", self.text)
        self.assertIn("### Cowork", self.text)

    def test_one_connector_one_account_and_the_way_back_in(self):
        self.assertIn("There is one connector and one AdCopilot account, whichever "
                      "AdCopilot plugins you add.", self.flat)
        self.assertIn("under whichever AdCopilot plugin loaded first, and the sign-in "
                      "belongs to that entry.", self.flat)
        self.assertIn("If Claude asks you to sign in again after you add or remove an "
                      "AdCopilot plugin, run `/mcp` and sign in once.", self.flat)

    def test_install_steps_name_this_plugin_and_this_repository(self):
        self.assertIn("/plugin marketplace add AtromxIntelligence/adcopilot-linkedin-ads-plugin", self.text)
        self.assertIn("/plugin install %s@adcopilot-linkedin-ads-plugin" % NAME, self.text)

    def test_the_data_paragraph_discloses_every_destination(self):
        self.assertIn("The plugin is instructions only: it runs no code and sends nothing anywhere itself.",
                      self.flat)
        for destination in ("mcp.adcopilot.cloud", "https://adcopilot.cloud/privacy",
                            "https://adcopilot.cloud/terms", "https://app.adcopilot.cloud"):
            self.assertIn(destination, self.text)

    def test_the_version_paragraph_matches_the_manifest(self):
        match = re.search(r"\*\*(\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2}), written against AdCopilot "
                          r"(v\d+\.\d+\.\d+), live since (\d{4}-\d{2}-\d{2})\)\*\*", self.flat)
        self.assertIsNotNone(match, "the version paragraph is missing")
        self.assertEqual(match.group(1), VERSION)
        self.assertEqual(match.group(3), "v2.44.0")

    def test_no_image_is_named_in_backticks(self):
        for span in BACKTICKED.findall(self.text):
            self.assertNotRegex(span, r"(?i)\.(png|jpe?g|gif|svg|webp|ico)$", span)

    def test_every_command_and_skill_it_names_exists(self):
        for command in re.findall(r"`/%s:([a-z-]+)`" % re.escape(NAME), self.text):
            self.assertIn(command, COMMAND_TOOLS, command)
        for skill in SKILL_TOOLS:
            self.assertIn("`%s`" % skill, self.text, skill)
        used = tool_names_in(self.text)
        allowed = set().union(*SKILL_TOOLS.values())
        self.assertFalse(used - allowed, sorted(used - allowed))
        self.assertFalse(used - connector_tools(), sorted(used - connector_tools()))


if __name__ == "__main__":
    unittest.main()
