"""What the plugin directory's scanner looks for, and what this plugin has
decided never to do.

The plugin is instructions only: it runs no code, so nothing in it reads a
credential, launches a package or downloads and runs anything, and nothing that
the directory rejects is in the folder (a stray system file, a link to another
file, a submodule, a bundled binary, an executable folder). It also holds the
words this plugin has decided not to use: a price figure, a claim to be
anyone's own product, the word the directory's reviewers read as a claim of
endorsement, a claim that the platform has approved AdCopilot or counts it as a
partner, and an id that is never published here.

The patterns below are built from pieces on purpose: written whole, this file
would match itself. Run with `python3 -m unittest discover -s tests -v` from the
repository root (stdlib only; reads no environment variable).
"""

import hashlib
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", "__pycache__"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf"}
OWNER = "LinkedIn"

# An id that is never published in this repository, held as a SHA-256 digest
# so that this file does not publish it either: (length, digest). A run of
# letters and digits anywhere in a text file that hashes to it fails. Only a
# long id belongs here: a short one's digest is reversed by trying every value.
NEVER_PUBLISHED = {
    (14, "45eb83e8f21efde6cf0fae2ce207a8ffdbe592d9e3ec6e9ffc9405e006435cef"),
}

# A claim that the platform approved, certified or sponsored AdCopilot, or counts
# it as a partner. The Insight Tag's "partner ID" is the platform's own name for
# a tag setting, not a claim, so a partner followed by ID or IDs is left out.
CLAIM_PATTERNS = [
    r"(?i)\b(?:approv(?:ed|al)|certified|sponsored)\s+(?:by|from)\s+" + OWNER + r"\b",
    r"(?i)\b" + OWNER + r"(?:['’]s)?[\s-]+(?:has\s+)?(?:approv(?:e[sd]?|al)|certifi(?:ed|cation))\b",
    r"(?i)\b" + OWNER + r"(?:['’]s)?\s+(?:marketing\s+)?partn(?:ers?|ership)\b(?!\s+ids?\b)",
    r"(?i)\bpartner(?:ed|s|ship)?\s+(?:of|with)\s+" + OWNER + r"\b",
]


def plugin_files():
    """Relative names of every file in the plugin folder: tracked ones, plus
    untracked ones that are not ignored (as the directory sees the repository)."""
    names = None
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() == ROOT.resolve():
            out = subprocess.run(
                ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                cwd=ROOT, capture_output=True, check=True).stdout
            names = [n for n in out.decode("utf-8").split("\0") if n]
    except (OSError, subprocess.CalledProcessError):
        names = None
    if names is None:
        names = []
        for dirpath, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if not f.endswith(".pyc"):
                    names.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
    present = []
    for name in sorted(set(names)):
        path = ROOT / name
        if path.is_symlink() or path.is_file():
            present.append(name)
    return present


def text_files():
    return [n for n in plugin_files()
            if (ROOT / n).suffix.lower() not in BINARY_SUFFIXES and not (ROOT / n).is_symlink()]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def find(pattern, flags=0, skip=()):
    """(file, line number, line) for every line of a text file that matches."""
    rx = re.compile(pattern, flags)
    hits = []
    for name in text_files():
        if name in skip:
            continue
        for number, line in enumerate(read(name).splitlines(), 1):
            if rx.search(line):
                hits.append((name, number, line.strip()[:120]))
    return hits


class NoCredentialReads(unittest.TestCase):

    def test_nothing_reads_a_credential_from_the_users_environment_or_sends_one(self):
        patterns = [
            "os" + r"\.environ",
            "get" + r"env\(",
            "process" + r"\.env",
            r"\$\{[A-Za-z_]*(?:TOKEN|SECRET|KEY|PASSWORD)[A-Za-z_]*\}",
            "Author" + "ization:",
            "Bear" + "er ",
        ]
        for pattern in patterns:
            self.assertEqual(find(pattern), [], pattern)

    def test_nothing_is_launched_through_a_package_runner(self):
        launchers = [
            r"\b" + "np" + "x" + r"\b",
            r"\b" + "bun" + "x" + r"\b",
            r"\b" + "pnpm" + r" dlx\b",
            r"\b" + "yarn" + r" dlx\b",
            r"\b" + "uv" + "x" + r"\b",
            r"\b" + "pipx" + r" run\b",
            r"\b" + "uv" + r" run\b",
        ]
        for pattern in launchers:
            self.assertEqual(find(pattern), [], pattern)

    def test_nothing_downloads_and_runs_anything(self):
        # The directory's scanner holds this pattern anywhere in the repository,
        # prose included. The workflow file is left out, as the CI check leaves
        # it out: its comment describes the pattern, and its grep is the pattern.
        pattern = r"(curl|wget)[^|;]*\|[ \t]*(sudo[ \t]+)?(ba)?sh"
        self.assertEqual(find(pattern, skip={".github/workflows/checks.yml"}), [])

    def test_every_address_in_the_text_is_https(self):
        self.assertEqual(find("http" + r"://"), [])


class NothingTheDirectoryRejects(unittest.TestCase):

    def test_no_stray_system_file_link_submodule_or_bundle(self):
        files = plugin_files()
        banned_names = {".DS" + "_Store", "Thumbs" + ".db", "desktop" + ".ini"}
        for name in files:
            base = os.path.basename(name)
            self.assertNotIn(base, banned_names, name)
            self.assertNotIn("__" + "MACOSX", name.split("/"), name)
            self.assertFalse((ROOT / name).is_symlink(), "%s is a symbolic link" % name)
            self.assertNotIn(base, {".git" + "modules", ".git" + "attributes", "CLAUDE" + ".md"}, name)
            self.assertFalse(name.startswith("bin/"), name)
            self.assertNotRegex(name, r"\.(mcpb|dxt)$")

    def test_no_file_is_a_lockfile_or_a_package_manifest_or_a_script(self):
        for name in plugin_files():
            base = os.path.basename(name)
            self.assertNotIn(base, {"package" + ".json", "package-lock" + ".json", "yarn" + ".lock",
                                    "pnpm-lock" + ".yaml", "uv" + ".lock", "Pipfile", "pyproject" + ".toml"}, name)
            self.assertNotRegex(name, r"\.(sh|bash|zsh|ps1|bat|cmd|js|mjs|cjs|ts)$", name)

    def test_the_folders_are_the_ones_this_plugin_has(self):
        top = {n.split("/")[0] for n in plugin_files() if "/" in n}
        self.assertEqual(top, {".claude-plugin", ".github", "commands", "skills", "tests"})

    def test_an_icon_is_the_only_binary_file(self):
        binary = [n for n in plugin_files() if (ROOT / n).suffix.lower() in BINARY_SUFFIXES]
        self.assertEqual(binary, [".claude-plugin/icon.png"])


class WordsThisPluginDoesNotUse(unittest.TestCase):

    def test_no_price_figure_beyond_the_one_sentence_about_plans(self):
        self.assertEqual(find(r"\$" + r"\d"), [])
        self.assertEqual(find("/" + r"mo\b"), [])
        self.assertEqual(find("per " + r"month", re.I), [])
        sentence = ("The plugin is free (MIT). The AdCopilot connector is a hosted service: "
                    "Free plan available; paid plans on https://adcopilot.cloud/pricing")
        mentions = [n for n in text_files()
                    if not n.startswith("tests/") and "adcopilot.cloud/pricing" in read(n)]
        self.assertEqual(mentions, ["README.md"])
        self.assertEqual(read("README.md").count(sentence), 1)

    def test_it_never_calls_itself_by_a_word_that_reads_as_an_endorsement(self):
        self.assertEqual(find("offi" + "cial", re.I), [])

    def test_it_never_says_it_is_made_by_the_platform(self):
        allowed = ["not by " + OWNER, "Not affiliated with or endorsed by " + OWNER]
        for name in text_files():
            text = re.sub(r"\s+", " ", read(name))
            for phrase in allowed:
                text = text.replace(phrase, " ")
            for owner in (OWNER, "Google", "Meta", "TikTok", "Microsoft"):
                hit = re.search(r"(?i)\bby " + owner + r"\b", text)
                self.assertIsNone(hit, "%s says 'by %s'" % (name, owner))

    def test_it_makes_no_claim_that_the_platform_connection_exists_today(self):
        for name in text_files():
            if name.startswith("tests/"):
                continue
            text = re.sub(r"\s+", " ", read(name))
            for phrase in ("connects to your LinkedIn ad account", "reads your LinkedIn ad account",
                           "manages your LinkedIn", "LinkedIn Ads API access has been approved"):
                self.assertNotIn(phrase, text, name)

    def test_it_never_claims_the_platforms_approval_or_partnership(self):
        # Every text file, the tests included: the patterns are built from
        # pieces, so this file does not match itself.
        for name in text_files():
            text = re.sub(r"\s+", " ", read(name))
            for pattern in CLAIM_PATTERNS:
                hit = re.search(pattern, text)
                self.assertIsNone(hit, "%s says %r" % (name, hit and hit.group(0)))

    def test_the_approval_and_partnership_ban_catches_the_ways_it_is_said(self):
        # The phrases are built at run time, so this file carries none of them.
        caught = [
            "approved by {o}", "approval from {o}", "certified by {o}", "sponsored by {o}",
            "{o} approves", "{o}-approved", "{o} has approved", "pending {o} approval",
            "with {o}'s approval", "with {o}’s approval", "{o}-certified", "{o} certification",
            "{o} partner", "{o} Marketing Partners", "{o}'s partner program",
            "{o}’s Marketing Partner", "{o} partnership", "a partner of {o}",
            "partnered with {o}", "in partnership with {o}",
        ]
        passed = [
            "the {o} partner ID", "two {o} partner IDs", "{o} Sponsored Content",
            "Not affiliated with or endorsed by {o}",
            "Direct access to your {o} ad account is being built; there is no date.",
            "claims approval or partnership from {o}",
        ]
        def hits(phrase):
            return [p for p in CLAIM_PATTERNS if re.search(p, phrase.format(o=OWNER))]
        for phrase in caught:
            self.assertNotEqual(hits(phrase), [], phrase)
        for phrase in passed:
            self.assertEqual(hits(phrase), [], phrase)

    def test_it_never_carries_an_id_that_is_never_published_here(self):
        lengths = {length for length, _ in NEVER_PUBLISHED}
        for name in text_files():
            for run in re.findall(r"[A-Za-z0-9]+", read(name)):
                run = run.lower()
                for length in lengths:
                    for start in range(len(run) - length + 1):
                        window = run[start:start + length]
                        digest = hashlib.sha256(window.encode("ascii")).hexdigest()
                        self.assertNotIn((length, digest), NEVER_PUBLISHED,
                                         "%s carries an id that is never published here" % name)


if __name__ == "__main__":
    unittest.main()
