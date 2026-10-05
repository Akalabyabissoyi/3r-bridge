import subprocess
import sys
from datetime import date, timedelta

from bridge import cli
from bridge.regions import REGIONS


def test_cli_find_and_samplesize(capsys):
    assert cli.main(["find", "--area", "sensory", "--need", "organism", "--need", "behaviour"]) == 0
    assert "Drosophila" in capsys.readouterr().out
    assert cli.main(["samplesize", "two_group", "--diff", "1", "--sd", "1"]) == 0
    assert "17 per group" in capsys.readouterr().out


def test_cli_errors_cleanly(capsys):
    assert cli.main(["samplesize", "two_group", "--diff", "-1", "--sd", "1"]) == 2


def test_module_entry_point():
    out = subprocess.run([sys.executable, "-m", "bridge", "find", "--area", "gut", "--format", "json"],
                         capture_output=True, text=True, check=True).stdout
    assert '"catalogue_version"' in out


def test_regions_complete():
    for r in REGIONS.values():
        assert {"name", "law", "protected", "authorisation", "alternatives", "read_next"} <= set(r)


def test_staleness_script():
    sys.path.insert(0, "scripts")
    import check_staleness as cs
    assert cs.stale_items(date.today(), 180) == []
    assert cs.stale_items(date.today() + timedelta(days=400), 180)


def test_review_stats_agreement():
    import review_stats as rs
    rows = [dict(reviewer=r, model_key="spheroid", area_key="hepatotox", score=s) for r, s in zip("ABC", (3, 3, 1))]
    out = rs.summarise(rows)[0]
    assert out["median"] == 3 and out["catalogue"] == 3 and not out["differs"]
    rows2 = [dict(reviewer=r, model_key="spheroid", area_key="hepatotox", score=0) for r in "ABC"]
    assert rs.summarise(rows2)[0]["differs"]
