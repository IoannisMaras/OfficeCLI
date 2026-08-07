# Benchmark 10: Single-Pass Batch Command Execution

## 📌 Problem & Context
In non-MCP direct CLI mode, running 10 separate commands (`officecli add` x 10) launches 10 processes, opens the file 10 times, parses OpenXML 10 times, and deflates zip 10 times (**~3.5 seconds total**).

Running 1 `officecli batch` command processes all 10 items in memory with one DOM load and one zip write.

---

## 🔬 Test & Proof Script (`test.sh`)

```bash
#!/bin/bash
set -e

echo "=== Running 10-Item Edit Benchmark (Individual CLI vs Batch CLI) ==="

# Test 1: 10 Individual CLI Calls
echo ""
echo "--- Test 1: 10 Individual CLI Calls ---"
time bash -c "
  /tmp/officecli create /tmp/test1.docx
  for i in {1..10}; do
    /tmp/officecli add /tmp/test1.docx /body --type paragraph --prop text=\"Item \$i\"
  done
"

# Test 2: 1 Single Batch Command
echo ""
echo "--- Test 2: 1 Single Batch Command ---"
time bash -c "
  /tmp/officecli create /tmp/test2.docx
  /tmp/officecli batch /tmp/test2.docx --commands '[
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 1\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 2\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 3\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 4\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 5\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 6\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 7\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 8\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 9\"}},
    {\"command\":\"add\",\"parent\":\"/body\",\"type\":\"paragraph\",\"props\":{\"text\":\"Item 10\"}}
  ]'
"
```

## 📊 Expected Results
- **10 Individual CLI Calls**: ~3,500ms total
- **1 Single Batch Command**: ~320ms total (**~10x speedup**)
