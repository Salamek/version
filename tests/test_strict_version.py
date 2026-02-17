import pytest
from version.StrictVersion import StrictVersion


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def v100():
    return StrictVersion("1.0.0")


@pytest.fixture
def v123():
    return StrictVersion("1.2.3")


# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------

class TestInstantiation:
    def test_creates_from_valid_string(self):
        v = StrictVersion("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.micro == 3

    def test_is_strict_version_instance(self):
        assert isinstance(StrictVersion("0.0.1"), StrictVersion)

    def test_string_representation(self):
        assert str(StrictVersion("2.4.6")) == "2.4.6"


# ---------------------------------------------------------------------------
# advance_major
# ---------------------------------------------------------------------------

class TestAdvanceMajor:
    def test_default_step(self, v123):
        result = v123.advance_major()
        assert result.major == 2

    def test_resets_minor_to_zero(self, v123):
        result = v123.advance_major()
        assert result.minor == 0

    def test_resets_patch_to_zero(self, v123):
        result = v123.advance_major()
        assert result.micro == 0

    def test_custom_step(self, v100):
        result = v100.advance_major(by=3)
        assert result.major == 4

    def test_returns_strict_version(self, v123):
        result = v123.advance_major()
        assert isinstance(result, StrictVersion)

    def test_does_not_mutate_original(self, v123):
        v123.advance_major()
        assert v123.major == 1

    def test_string_output(self, v123):
        assert str(v123.advance_major()) == "2.0.0"


# ---------------------------------------------------------------------------
# advance_minor
# ---------------------------------------------------------------------------

class TestAdvanceMinor:
    def test_default_step(self, v123):
        result = v123.advance_minor()
        assert result.minor == 3

    def test_preserves_major(self, v123):
        result = v123.advance_minor()
        assert result.major == 1

    def test_resets_patch_to_zero(self, v123):
        result = v123.advance_minor()
        assert result.micro == 0

    def test_custom_step(self, v123):
        result = v123.advance_minor(by=5)
        assert result.minor == 7

    def test_returns_strict_version(self, v123):
        result = v123.advance_minor()
        assert isinstance(result, StrictVersion)

    def test_does_not_mutate_original(self, v123):
        v123.advance_minor()
        assert v123.minor == 2

    def test_string_output(self, v123):
        assert str(v123.advance_minor()) == "1.3.0"


# ---------------------------------------------------------------------------
# advance_patch
# ---------------------------------------------------------------------------

class TestAdvancePatch:
    def test_default_step(self, v123):
        result = v123.advance_patch()
        assert result.micro == 4

    def test_preserves_major(self, v123):
        result = v123.advance_patch()
        assert result.major == 1

    def test_preserves_minor(self, v123):
        result = v123.advance_patch()
        assert result.minor == 2

    def test_custom_step(self, v123):
        result = v123.advance_patch(by=10)
        assert result.micro == 13

    def test_returns_strict_version(self, v123):
        result = v123.advance_patch()
        assert isinstance(result, StrictVersion)

    def test_does_not_mutate_original(self, v123):
        v123.advance_patch()
        assert v123.micro == 3

    def test_string_output(self, v123):
        assert str(v123.advance_patch()) == "1.2.4"


# ---------------------------------------------------------------------------
# _new_from_release (internal helper)
# ---------------------------------------------------------------------------

class TestNewFromRelease:
    def test_returns_strict_version(self, v100):
        result = v100._new_from_release((2, 3, 4))
        assert isinstance(result, StrictVersion)

    def test_correct_release_values(self, v100):
        result = v100._new_from_release((5, 6, 7))
        assert (result.major, result.minor, result.micro) == (5, 6, 7)


# ---------------------------------------------------------------------------
# Chaining
# ---------------------------------------------------------------------------

class TestChaining:
    def test_chain_major_then_patch(self):
        v = StrictVersion("1.2.3").advance_major().advance_patch()
        assert str(v) == "2.0.1"

    def test_chain_minor_then_minor(self):
        v = StrictVersion("1.0.0").advance_minor().advance_minor()
        assert str(v) == "1.2.0"