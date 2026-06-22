#!/usr/bin/env python3
"""
Sentry Tax Calculator — CLI version

Usage:
    python calculator.py
    python calculator.py 250000         # pass events directly
    python calculator.py --csv          # output CSV for all breakpoints
"""

import sys


# ---------------------------------------------------------------------------
# Pricing models
# ---------------------------------------------------------------------------

def sentry_price(events: int) -> float:
    """
    Sentry Team plan:
      - Free up to 5,000 errors/month
      - $26/month base for up to 50,000 errors
      - ~$0.000290 per additional error above 50k
    Source: https://sentry.io/pricing/ (as of 2026)
    """
    if events <= 5_000:
        return 0.0
    overage = max(0, events - 50_000)
    return 26.0 + overage * 0.000290


def ravn_price(events: int) -> float:
    """
    Ravn flat-rate tiers:
      Free   → 0 $/mo    (up to  5,000 events)
      Solo   → 9.99 $/mo (up to  50,000 events)
      Team   → 19.99 $/mo (up to 250,000 events)
      Business → 49.99 $/mo (up to 1,000,000 events)
    Source: https://getravn.com/pricing
    """
    if events <= 5_000:
        return 0.0
    if events <= 50_000:
        return 9.99
    if events <= 250_000:
        return 19.99
    if events <= 1_000_000:
        return 49.99
    return 49.99  # Business plan; custom pricing above 1M


def sentry_plan(events: int) -> str:
    if events <= 5_000:
        return "Developer (Free)"
    if events <= 50_000:
        return "Team"
    return "Team + overage"


def ravn_plan(events: int) -> str:
    if events <= 5_000:     return "Free"
    if events <= 50_000:    return "Solo"
    if events <= 250_000:   return "Team"
    return "Business"


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_events(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".rstrip("0").rstrip(".")  + "M"
    if n >= 1_000:
        s = f"{n / 1_000:.0f}k"
        return s
    return str(n)


def fmt_price(p: float) -> str:
    if p == 0:
        return "$0"
    return f"${p:.2f}"


# ---------------------------------------------------------------------------
# CLI output
# ---------------------------------------------------------------------------

BREAKPOINTS = [1_000, 5_000, 10_000, 50_000, 100_000, 250_000,
               500_000, 1_000_000, 2_000_000, 5_000_000]

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def print_table(highlight: int | None = None) -> None:
    header = f"{'Events/mo':>10}  {'Sentry':>10}  {'Ravn':>10}  {'You save/mo':>12}  {'You save/yr':>12}"
    print(f"\n{BOLD}{header}{RESET}")
    print("─" * 60)
    for events in BREAKPOINTS:
        s = sentry_price(events)
        r = ravn_price(events)
        save_mo = s - r
        save_yr = save_mo * 12
        marker = "  ◀ you" if events == highlight else ""
        save_str = f"–{fmt_price(save_mo)}" if save_mo > 0 else "—"
        save_yr_str = f"–${save_yr:,.0f}" if save_mo > 0 else "—"
        color = YELLOW if events == highlight else ""
        print(
            f"{color}{fmt_events(events):>10}  "
            f"{RED}{fmt_price(s):>10}{RESET}{color}  "
            f"{GREEN}{fmt_price(r):>10}{RESET}{color}  "
            f"{GREEN}{save_str:>12}{RESET}{color}  "
            f"{GREEN}{save_yr_str:>12}{RESET}{color}{marker}{RESET}"
        )
    print()


def print_single(events: int) -> None:
    s = sentry_price(events)
    r = ravn_price(events)
    annual_tax = (s - r) * 12

    print(f"\n{BOLD}Sentry Tax Calculator{RESET}")
    print(f"Events per month: {BOLD}{fmt_events(events)}{RESET}\n")
    print(f"  {'Sentry ':.<30} {RED}{fmt_price(s)}/mo  ({sentry_plan(events)}){RESET}")
    print(f"  {'Ravn ':.<30} {GREEN}{fmt_price(r)}/mo  ({ravn_plan(events)}){RESET}")
    print()
    if annual_tax > 0:
        print(f"  {BOLD}{RED}Your Sentry Tax: ${annual_tax:,.0f}/year ({fmt_price(s - r)}/month){RESET}")
        print(f"  {DIM}That's ${annual_tax:,.0f} for the exact same error monitoring.{RESET}")
    else:
        print(f"  {GREEN}Both tools are free at this volume.{RESET}")
    print()


def print_csv() -> None:
    print("events_per_month,sentry_monthly,ravn_monthly,monthly_savings,annual_savings")
    for events in BREAKPOINTS:
        s = sentry_price(events)
        r = ravn_price(events)
        save_mo = s - r
        save_yr = save_mo * 12
        print(f"{events},{s:.2f},{r:.2f},{save_mo:.2f},{save_yr:.2f}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def interactive() -> None:
    print(f"\n{BOLD}Sentry Tax Calculator — Python Error Monitoring{RESET}")
    print(f"{DIM}How much are you really paying? Let's find out.{RESET}\n")
    try:
        raw = input("How many error events per month? (e.g. 50000): ").strip()
        events = int(raw.replace(",", "").replace("k", "000").replace("m", "000000"))
    except (ValueError, EOFError):
        print("Please enter a number.")
        sys.exit(1)

    print_single(events)
    print_table(highlight=min(BREAKPOINTS, key=lambda x: abs(x - events)))
    print(f"  Try Ravn free → {BLUE}https://app.getravn.com/register{RESET}")
    print(f"  Full comparison → {BLUE}https://getravn.com/sentry-alternative.html{RESET}\n")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--csv" in args:
        print_csv()
    elif args and args[0].isdigit():
        events = int(args[0])
        print_single(events)
        print_table(highlight=min(BREAKPOINTS, key=lambda x: abs(x - events)))
    else:
        interactive()
