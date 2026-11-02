
import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration,
)


def test_invalid_batches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1)


def test_unapproved_batch():
    result = process_book_buybacks(
        [{"intake_approved": False, "books": []}], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_textbook_mint():
    batches = [{
        "intake_approved": True,
        "format": "textbook",
        "books": [{"condition": "mint"}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 50.0


def test_hardcover_poor():
    batches = [{
        "intake_approved": True,
        "format": "hardcover",
        "books": [{"condition": "poor"}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 6.0


def test_paperback_default_format_and_condition():
    batches = [{
        "intake_approved": True,
        "books": [{}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0


def test_unknown_format():
    batches = [{
        "intake_approved": True,
        "format": "unknown",
        "books": [{}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_missing_pages_rejected():
    batches = [{
        "intake_approved": True,
        "format": "paperback",
        "books": [{"missing_pages": 2}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook():
    batches = [{
        "intake_approved": True,
        "format": "textbook",
        "books": [{"counterfeit": True}, {"condition": "mint"}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback():
    batches = [{
        "intake_approved": True,
        "format": "paperback",
        "books": [{"counterfeit": True}, {"condition": "good"}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0


def test_store_credit_bonus():
    batches = [{
        "intake_approved": True,
        "format": "paperback",
        "payout_in_credit": True,
        "books": [{}],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 13.0


def test_audit_rejected():
    batches = [{
        "intake_approved": True,
        "format": "paperback",
        "books": [{"missing_pages": 1} for _ in range(5)],
    }]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_calibrated():
    assert inspect_scanner_calibration([[1, 2, 3, 5]]) == "CALIBRATED"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_scanner_streak_resets():
    assert inspect_scanner_calibration([[6, 2, 7, 3]]) == "CALIBRATED"
