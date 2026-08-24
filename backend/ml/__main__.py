from __future__ import annotations

import argparse
from pathlib import Path

from ml.training import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train and save the Smart Hotel reservation model."
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to the CSV dataset used for training.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("models/smart_hotel_model.pkl"),
        help="Destination path for the trained model artifact.",
    )

    args = parser.parse_args()
    metrics = train_and_save(args.dataset, args.output)

    print(f"Model saved to: {args.output}")
    for name, value in metrics.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()
