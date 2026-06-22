# The Sentry Tax Calculator

> **How much are you really paying for Python error monitoring?**

A transparent, open-source pricing calculator that shows the cost difference between Sentry and [Ravn](https://getravn.com) for Python developers.

**[→ Open the interactive calculator](https://kosevskey.github.io/sentry-tax/)**

---

## The numbers

| Events/month | Sentry (Team) | Ravn | You save |
|---|---|---|---|
| 5,000 | $0 | $0 | — |
| 50,000 | **$26/mo** | $9.99/mo | **$192/yr** |
| 100,000 | **$40/mo** | $9.99/mo | **$361/yr** |
| 250,000 | **$84/mo** | $19.99/mo | **$769/yr** |
| 500,000 | **$157/mo** | $19.99/mo | **$1,644/yr** |
| 1,000,000 | **$276/mo** | $49.99/mo | **$2,712/yr** |

*Sentry prices estimated from the Team plan base ($26/mo, 50k events) with $0.000290/additional event. See [methodology](#methodology).*

---

## Use it

### Interactive (browser)

Open [`index.html`](index.html) locally or visit the [GitHub Pages version](https://kosevskey.github.io/sentry-tax/).

Move the slider. Watch the Sentry Tax update in real time.

### CLI (terminal)

```bash
# Interactive mode
python calculator.py

# Pass events directly
python calculator.py 250000

# Export as CSV (for spreadsheets, dashboards)
python calculator.py --csv
```

Example output:

```
Sentry Tax Calculator
Events per month: 250k

  Sentry ......................... $84.00/mo  (Team + overage)
  Ravn ........................... $19.99/mo  (Team)

  Your Sentry Tax: $769/year ($64.01/month)
  That's $769 for the exact same error monitoring.
```

---

## Methodology

This calculator uses publicly available pricing as of 2026.

**Sentry (Team plan)**
- Base: $26/month for up to 50,000 errors
- Overage: ~$0.000290 per error above 50k
- Source: [sentry.io/pricing](https://sentry.io/pricing/)

**Ravn**
- Free: $0/month — 5,000 events
- Solo: $9.99/month — 50,000 events
- Team: $19.99/month — 250,000 events
- Business: $49.99/month — 1,000,000 events
- Source: [getravn.com/pricing](https://getravn.com/pricing)

**This is an estimate.** Sentry's actual pricing depends on your plan, add-ons, annual vs. monthly billing, and negotiated contracts. Always check current prices before making a decision.

The goal here is transparency — all formulas are in [`calculator.py`](calculator.py) and [`index.html`](index.html). If anything is wrong, open an issue.

---

## What is Ravn?

[Ravn](https://getravn.com) is a lightweight Python error monitoring tool. Two lines of code:

```python
import ravn
ravn.init(api_key="your_key")

# That's it. Every exception is captured automatically.
```

- Automatic exception capture
- AI root cause analysis on every error
- Performance tracking via `@ravn.measure`
- Email alerts, error grouping, team management

[Try it free →](https://app.getravn.com/register)

---

## Contributing

Found an error in the pricing data? Open a PR. The methodology is intentionally public so anyone can verify or correct it.

---

*Sentry is a trademark of Functional Software, Inc. This project is not affiliated with Sentry.*
