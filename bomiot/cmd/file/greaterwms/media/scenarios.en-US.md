# Use Cases

The manual answers "how to use it"; this page answers "should you use it". Five short judgments below: what the pain is, which Bomiot mechanisms catch it, and where to read the details.

---

## Delivering Projects to Clients

Suppose you took on a project that needs to run on a few of the client's computers — and nobody on their side knows the tech.

Three things will happen: their machines can't set up the environment; the source code can't ship with the package; and every bug fix means remotely walking them through an upgrade, machine by machine.

Bomiot's corresponding mechanisms:

- Package into an environment-free application — the client double-clicks and it runs: build
- Compilation protection — deliver without handing over source code: build
- build.json authorization and device-count control — know who is using it and on how many machines
- Incremental updates — clients upgrade automatically, no more sending installers one by one: publish

Licensing tiers and device counts are commercial rules — see "Sponsor Us" under the Pricing tab; not covered here.

---

## Intranet, Offline, and On-site Environments

Suppose your system has to live in a factory workshop, a hospital intranet, or a client's server room — no internet, or a network so poor that installing a dependency is a struggle.

- Single-package delivery: no Python, no dependencies on the target machine
- Update packages can be carried in offline (USB) and applied
- Same story for ARM devices and multi-site rollouts: build one package, copy it anywhere, it runs

Details in build and deploy.

---

## One Person, Many Projects

Suppose you maintain several systems for several clients at once. The worst outcome is code crossing over and data mixing together.

- Switch projects from the top-right corner; the page fully reloads, leaving no state from the previous project
- Every request carries a `project` header; the backend isolates data per project and routes `api.py` per project

See Multi-Project under the Frontend tab, and Interaction under the Signals tab.

---

## After AI Writes the Code

Suppose AI generated a working tool for you in an afternoon, and you want it in someone's hands tomorrow.

Code generation has been compressed to minutes, but delivery has barely moved. Bomiot fills exactly that gap: `init` to initialize, `run` to run locally, `build` to package — one chain end to end. See Quick Start.

---

## What It's Not For

Honest boundaries. If your situation is on this list, don't force it:

- A pure web service users only reach through a browser — there is no delivery problem to solve
- Extreme sensitivity to size and memory — packaged artifacts are larger than native applications
- A requirement for absolute crack-proofing — compilation protection raises the bar; it is not unbreakable
- A project that never needs to be handed to anyone — it cannot help you there

The full attitude behind these boundaries lives in the Inscription.

---

Fits your case? Start from Quick Start.
