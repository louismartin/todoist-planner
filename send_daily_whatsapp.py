#!/usr/bin/env python3
"""CLI entry point for sending daily WhatsApp task summaries."""

import argparse
import sys
from pathlib import Path

from todoist_planner.config import load_config
from todoist_planner.whatsapp_summary import send_daily_summary, send_test_message


def main():
    parser = argparse.ArgumentParser(
        description="Send daily WhatsApp summary of top priority tasks."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview message without sending",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send a test message to verify setup",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: config.yaml)",
    )
    args = parser.parse_args()

    config_path = Path(args.config) if args.config else None
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.test:
        print("Sending test message...")
        try:
            message_sid = send_test_message(config)
            print(f"Test message sent successfully! SID: {message_sid}")
        except Exception as e:
            print(f"Failed to send test message: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.dry_run:
        print("=== DRY RUN - Message preview ===\n")

    try:
        message, message_sid = send_daily_summary(config, dry_run=args.dry_run)
        print(message)
        if not args.dry_run:
            print(f"\n=== Message sent! SID: {message_sid} ===")
    except Exception as e:
        print(f"Failed to send daily summary: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
