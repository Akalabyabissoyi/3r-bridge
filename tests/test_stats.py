import pytest

from bridge import stats


def test_two_group_unchanged():
    assert stats.n_per_group(1.0, 1.0) == 17


def test_unequal_groups_need_more_in_total():
    n1 = stats.n_per_group(1.0, 1.0)
    n_unequal = stats.n_per_group(1.0, 1.0, ratio=2)
    assert n_unequal < n1 and n_unequal + 2 * n_unequal > 2 * n1


def test_known_reference_values():
    assert stats.n_paired(1.0, 1.0) == 10
    assert stats.n_anova(0.25, 3) == 53
    assert stats.n_proportions(0.5, 0.25) == 58
    assert stats.survival_events(0.5) == 66


def test_attrition_and_nonparametric():
    assert stats.inflate_for_attrition(17, 0.1) == 19
    assert stats.inflate_for_attrition(17, 0) == 17
    assert stats.nonparametric_n(17) == 20


@pytest.mark.parametrize("call", [
    lambda: stats.n_per_group(0, 1), lambda: stats.n_per_group(1, -1), lambda: stats.n_per_group(1, 1, alpha=1.5),
    lambda: stats.n_anova(0.25, 2), lambda: stats.n_proportions(0.5, 0.5), lambda: stats.survival_events(1),
    lambda: stats.inflate_for_attrition(10, 1), lambda: stats.n_paired(1, 0),
])
def test_bad_inputs_raise(call):
    with pytest.raises(ValueError):
        call()
