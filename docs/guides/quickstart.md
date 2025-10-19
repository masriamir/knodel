# Quick Start Guide

Get up and running with `knodel` in 5 minutes.

## Prerequisites

- Python 3.13
- [uv](https://github.com/astral-sh/uv) for dependency management

## Installation

### Quick Setup

The project uses a Makefile for a streamlined development workflow:

```bash
# Install uv if not already available
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Set up the development environment
make install

# Run the example session
make run

# View the generated Tidal code
cat demo.tidal
```

### Manual Setup (Alternative)

Instead of using the Makefile, to set up manually:

```bash
uv sync --all-groups
```

## Running the Example Session

The `examples` directory contains a minimal session that layers a supersaw,
and a super pulse-width modulation synthesizer pattern.
The Makefile allows transpiling the pattern into Tidal code:

```bash
make run                    # Creates demo.tidal
make run OUTPUT=my.tidal    # Creates my.tidal
```

Or directly with the CLI:

```bash
uv run python -m knodel examples.basic_session:create_session --output demo.tidal
cat demo.tidal
```

The generated file is ready to be loaded into a running Tidal Cycles interpreter.

## Writing The First Session

1. Import the provided primitives:
   ```python
   from knodel.patterns import Pattern
   from knodel.session import TidalSession
   from knodel.synths import SuperSaw
   ```

2. Instantiate synthesizer wrappers, optionally configuring their controls.

3. Use the pattern helpers (e.g., `stack`, `fast`, `slow`) to build complex layers.

4. Add the resulting patterns to a `TidalSession` and transpile using `TidalTranspiler`.

### Example

```python
from knodel.patterns import Pattern
from knodel.session import TidalSession
from knodel.synths import SuperPWM, SuperSaw

session = TidalSession()
supersaw = SuperSaw(cutoff=1200, detune=0.4).to_pattern()
pwm = SuperPWM(pwidth=0.7).to_pattern().fast(2)
session.configure(setcps="0.6")
session.set_stream("d1", Pattern.stack([supersaw, pwm]))
```

Finally, call `TidalTranspiler` to generate the Haskell snippet:

```python
from pathlib import Path
from knodel.transpiler import TidalTranspiler

transpiler = TidalTranspiler()
output = transpiler.transpile(session)
Path("session.tidal").write_text(output, encoding="utf-8")
```

## Next Steps

- Explore [detailed installation options](installation.md)
- Learn more about [contributing](../contributing/CONTRIBUTING.md)
- Check out the [testing guide](../development/testing.md)
