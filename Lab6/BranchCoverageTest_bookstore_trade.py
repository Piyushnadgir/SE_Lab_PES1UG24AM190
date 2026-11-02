
import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration,
)


def test_empty_batches():
    result = process_book_buybacks([], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1)


def test_unapproved_batch():
    result = process_book_buybacks(
        [{"intake_approved": False}], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_all_formats():
    batches = [
        {"intake_approved": True, "format": "textbook",
         "books": [{}]},
        {"intake_approved": True, "format": "hardcover",
         "books": [{}]},
        {"intake_approved": True, "format": "paperback",
         "books": [{}]},
        {"intake_approved": True, "format": "magazine",
         "books": [{}]},
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 63.0


def test_empty_books():
    result = process_book_buybacks(
        [{"intake_approved": True, "books": []}], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_missing_pages():
    result = process_book_buybacks(
        [{"intake_approved": True,
          "books": [{"missing_pages": 2}]}], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_stops_batch():
    result = process_book_buybacks(
        [{"intake_approved": True, "format": "textbook",
          "books": [{"counterfeit": True}, {}]}], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_non_textbook_continues():
    result = process_book_buybacks(
        [{"intake_approved": True, "format": "paperback",
          "books": [{"counterfeit": True}, {}]}], 5.0
    )
    assert result["total_payout"] == 8.0


def test_mint_condition():
    result = process_book_buybacks(
        [{"intake_approved": True,
          "books": [{"condition": "mint"}]}], 5.0
    )
    assert result["total_payout"] == 10.0


def test_poor_condition():
    result = process_book_buybacks(
        [{"intake_approved": True,
          "books": [{"condition": "poor"}]}], 5.0
    )
    assert result["total_payout"] == 3.2


def test_default_good_condition():
    result = process_book_buybacks(
        [{"intake_approved": True, "books": [{}]}], 5.0
    )
    assert result["total_payout"] == 8.0


def test_store_credit_bonus():
    result = process_book_buybacks(
        [{"intake_approved": True, "payout_in_credit": True,
          "books": [{}]}], 5.0
    )
    assert result["total_payout"] == 13.0


def test_audit_rejected():
    result = process_book_buybacks(
        [{"intake_approved": True,
          "books": [{"missing_pages": 1} for _ in range(5)]}],
        5.0,
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_no_scanner_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_empty_scanner_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"


def test_scanner_readings_at_threshold():
    assert inspect_scanner_calibration([[5, 5, 5]]) == "CALIBRATED"


def test_one_high_reading():
    assert inspect_scanner_calibration([[6]]) == "CALIBRATED"


def test_two_consecutive_high_readings():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_high_reading_streak_resets():
    assert inspect_scanner_calibration([[6, 2, 7, 3]]) == "CALIBRATED"


def test_scanner_recalibration_in_later_device():
    assert inspect_scanner_calibration([[6, 2], [7, 8]]) == "RECALIBRATE"
