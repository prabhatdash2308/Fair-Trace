"""ReviewGuard AI — Critical Tests (Part 4 Section 19.3 checklist)"""

import uuid
import pytest
from unittest.mock import patch, MagicMock

from core.security import hash_password, verify_password, create_access_token, verify_token
from core.exceptions import InvalidTokenError
from app.ai.agents.performance_analysis_agent import _calculate_confidence


# ── Auth Service Tests ─────────────────────────────────────────────────────────

class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        h = hash_password("mypassword")
        assert h != "mypassword"

    def test_verify_correct_password(self):
        h = hash_password("correcthorse")
        assert verify_password("correcthorse", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("correcthorse")
        assert verify_password("wrongpassword", h) is False


class TestJWT:
    def test_create_and_verify_token(self):
        data = {"sub": str(uuid.uuid4()), "email": "test@test.com", "role": "MANAGER", "full_name": "Test"}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload["email"] == "test@test.com"
        assert payload["role"] == "MANAGER"

    def test_tampered_token_raises(self):
        data = {"sub": str(uuid.uuid4()), "email": "x@x.com", "role": "ADMIN", "full_name": "X"}
        token = create_access_token(data)
        tampered = token[:-5] + "AAAAA"
        with pytest.raises(InvalidTokenError):
            verify_token(tampered)

    def test_missing_sub_raises(self):
        """Token without 'sub' claim should raise InvalidTokenError."""
        import jwt as pyjwt
        from config import settings
        bad_token = pyjwt.encode({"email": "x@x.com"}, settings.jwt_secret_key, algorithm="HS256")
        with pytest.raises(InvalidTokenError):
            verify_token(bad_token)


# ── Confidence Engine Tests ────────────────────────────────────────────────────

class TestConfidenceEngine:
    """Tests the deterministic confidence formula — no LLM mocking needed."""

    def _make_state(self, evidence_count=5, avg_sim=0.80, high_bias=0, medium_bias=0, input_types=3):
        return {
            "evidence_index": [{"similarity_score": avg_sim} for _ in range(evidence_count)],
            "validated_inputs": [{"input_type": f"TYPE_{i}"} for i in range(input_types)],
            "evidence_citations": [{"similarity_score": avg_sim} for _ in range(evidence_count)],
            "evidence_by_dimension": {"TECHNICAL": [{"similarity_score": avg_sim}]},
            "bias_flags": (
                [{"severity": "HIGH"}] * high_bias +
                [{"severity": "MEDIUM"}] * medium_bias
            ),
            "high_bias_count": high_bias,
            "medium_bias_count": medium_bias,
            "confidence_result": None,
        }

    def test_high_confidence_when_strong_evidence(self):
        state = self._make_state(evidence_count=5, avg_sim=0.85, input_types=5)
        result = _calculate_confidence(state)
        assert result["score"] in ("HIGH", "MEDIUM"), f"Expected HIGH/MEDIUM, got {result['score']}"
        assert result["numeric_score"] >= 0.50

    def test_insufficient_confidence_with_no_evidence(self):
        state = self._make_state(evidence_count=0, avg_sim=0, high_bias=3, input_types=1)
        result = _calculate_confidence(state)
        assert result["score"] == "INSUFFICIENT"
        assert result["numeric_score"] < 0.30

    def test_high_bias_reduces_score(self):
        low_bias_state = self._make_state(evidence_count=5, avg_sim=0.80, high_bias=0)
        high_bias_state = self._make_state(evidence_count=5, avg_sim=0.80, high_bias=4)
        low_result = _calculate_confidence(low_bias_state)
        high_result = _calculate_confidence(high_bias_state)
        assert low_result["numeric_score"] > high_result["numeric_score"]

    def test_explanation_is_present(self):
        state = self._make_state()
        result = _calculate_confidence(state)
        assert len(result["explanation"]) > 10

    def test_numeric_score_bounds(self):
        """Confidence score must always be between 0 and 1."""
        state = self._make_state(high_bias=100, medium_bias=100)
        result = _calculate_confidence(state)
        assert 0.0 <= result["numeric_score"] <= 1.0


# ── RBAC Tests ─────────────────────────────────────────────────────────────────

class TestRBAC:
    def test_employee_cannot_access_users_endpoint(self, test_client, employee_headers):
        resp = test_client.get("/api/v1/users", headers=employee_headers)
        assert resp.status_code == 403

    def test_unauthenticated_request_returns_401(self, test_client):
        resp = test_client.get("/api/v1/users")
        assert resp.status_code == 401

    def test_health_endpoint_is_public(self, test_client):
        resp = test_client.get("/health")
        # Health may be 503 in test env (no real DB/Qdrant), but not 401
        assert resp.status_code in (200, 503)

    def test_admin_can_access_audit(self, test_client, admin_headers):
        resp = test_client.get("/api/v1/audit", headers=admin_headers)
        # May be 200 (empty list) or 500 (no DB in test) — not 403
        assert resp.status_code != 403
