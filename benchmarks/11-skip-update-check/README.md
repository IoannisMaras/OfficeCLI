# Benchmark 11: Suppress Update Checker Thread Spawning

## 📌 Problem & Context
In [Program.cs](file:///c:/.DEV/OfficeCLI/src/officecli/Program.cs#L268-L269), every single CLI run executes:
```csharp
if (Environment.GetEnvironmentVariable("OFFICECLI_SKIP_UPDATE") != "1")
    OfficeCli.Core.UpdateChecker.CheckInBackground();
```
On a 1 CPU core container, spawning a background task and reading `~/.officecli/config.json` on every CLI invocation adds ~25ms of thread context switching and file IO overhead.

---

## 🔬 Test & Proof Script (`test.sh`)

```bash
#!/bin/bash
set -e

echo "=== Running Update Check Overhead Benchmark (100 Executions) ==="

# Test 1: Default (Update Check Enabled)
echo ""
echo "--- Test 1: Default (Update Check Enabled) ---"
time bash -c "
  for i in {1..100}; do
    /tmp/officecli --output-schema-crc >/dev/null
  done
"

# Test 2: OFFICECLI_SKIP_UPDATE=1
echo ""
echo "--- Test 2: OFFICECLI_SKIP_UPDATE=1 ---"
time bash -c "
  export OFFICECLI_SKIP_UPDATE=1
  for i in {1..100}; do
    /tmp/officecli --output-schema-crc >/dev/null
  done
"
```

## 📊 Expected Results (100 Invocation Loops)
- **Default**: ~3.2 seconds
- **OFFICECLI_SKIP_UPDATE=1**: ~0.7 seconds (**~2.5 seconds total saved / 25ms per CLI run**)
