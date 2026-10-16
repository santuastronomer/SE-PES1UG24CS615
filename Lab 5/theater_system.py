
"""Manage movie seat reservations and save reservation data."""

import json
import secrets
from pathlib import Path

SHOWS = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}
RESERVATION_FILE = Path("seats.json")


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a seat and record the result in the log."""
    if system_logs is None:
        system_logs = []

    if show_id not in SHOWS:
        system_logs.append(f"Unknown show: {show_id}")
        return False

    show = SHOWS[show_id]

    if (
        isinstance(seat_number, bool)
        or not isinstance(seat_number, (int, str))
    ):
        system_logs.append("Invalid seat number.")
        return False

    if isinstance(seat_number, str):
        seat_number = seat_number.strip()
        if not seat_number:
            system_logs.append("Invalid seat number.")
            return False

    if (
        isinstance(seat_number, int)
        and not 1 <= seat_number <= show["seats"]
    ):
        system_logs.append(f"Seat number out of range for {show_id}")
        return False

    if seat_number in show["booked"]:
        system_logs.append(
            f"Seat {seat_number} already taken for {show_id}"
        )
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat if it exists."""
    if show_id not in SHOWS:
        return False

    try:
        SHOWS[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False

    return True


def ticket_code(show_id, seat_number):
    """Generate a random eight-character ticket reference."""
    del show_id, seat_number
    return secrets.token_hex(4)


def dump_reservations(file=RESERVATION_FILE):
    """Save reservation data to a JSON file."""
    with open(file, "w", encoding="utf-8") as reservation_file:
        json.dump(SHOWS, reservation_file, indent=2)


def load_reservations(file=RESERVATION_FILE):
    """Load saved reservations for known shows."""
    if not Path(file).exists():
        return

    with open(file, "r", encoding="utf-8") as reservation_file:
        data = json.load(reservation_file)

    if not isinstance(data, dict):
        raise ValueError("Reservation data must be a JSON object.")

    for show_id, saved_show in data.items():
        if show_id in SHOWS and isinstance(saved_show, dict):
            booked = saved_show.get("booked", [])
            if isinstance(booked, list):
                SHOWS[show_id]["booked"] = booked


def print_seating_summary():
    """Print available and booked seats for every show."""
    for show in SHOWS.values():
        free_seats = show["seats"] - len(show["booked"])
        print(
            f'{show["title"]}: {free_seats} seats free, '
            f'booked = {show["booked"]}'
        )


def main():
    """Run the sample movie reservation workflow."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    reserve_seat("SHOW-2", "A7", logs)
    release_seat("SHOW-2", 3)

    print(f"Ticket code: {ticket_code('SHOW-1', 5)}")
    seat = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    reserve_seat("SHOW-2", seat, logs)

    dump_reservations()
    load_reservations()
    print_seating_summary()


if __name__ == "__main__":
    main()
