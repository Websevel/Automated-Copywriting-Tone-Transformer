"""
main.py
-------
CLI entry point. Two modes:

1. Single generation:
   python main.py --product "Wireless Earbuds" --platform instagram --tone witty

2. Batch generation from a CSV:
   python main.py --batch products.csv
"""

import argparse
from generator import generate_copy
from batch_processor import run_batch_sync


def build_parser():
    parser = argparse.ArgumentParser(
        description="Automated Copywriting & Tone Transformer (DecodeLabs Project 2)"
    )
    parser.add_argument("--product", type=str, help="Product name / raw description")
    parser.add_argument("--platform", type=str, choices=["linkedin", "instagram", "twitter", "email"],
                         help="Target platform")
    parser.add_argument("--tone", type=str, help="Desired tone, e.g. witty, professional, urgent")
    parser.add_argument("--temperature", type=float, default=0.7,
                         help="Creativity control (0.0 = safe/factual, 1.0+ = more varied)")
    parser.add_argument("--top_p", type=float, default=0.9,
                         help="Word diversity control (lower = more focused)")
    parser.add_argument("--batch", type=str, default=None,
                         help="Path to a CSV file for batch mode (columns: product_name,platform,tone)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.batch:
        run_batch_sync(args.batch)
        return

    if not (args.product and args.platform and args.tone):
        parser.error("For single-mode generation you must pass --product, --platform, and --tone "
                      "(or use --batch <file.csv> instead).")

    result = generate_copy(
        product_name=args.product,
        platform=args.platform,
        tone=args.tone,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    print("\n----- GENERATED COPY -----")
    print(result.generated_copy)
    print("---------------------------")
    print(f"Characters: {result.char_count} | Within platform limit: {result.within_limit}")


if __name__ == "__main__":
    main()
