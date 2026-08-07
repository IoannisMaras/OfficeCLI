import subprocess
import time
import os

print("=========================================================")
echo_banner = "EMPIRICAL BENCHMARK IN LINUX DOCKER (1 CPU / 2 GB RAM)"
print(echo_banner)
print("=========================================================\n")

os.environ["OFFICECLI_SKIP_UPDATE"] = "1"

jit_bin = "/app/bin-jit/officecli"
r2r_bin = "/app/bin-r2r/officecli"

def run_cmd(binary, args):
    start = time.perf_counter()
    res = subprocess.run([binary] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    return (end - start) * 1000  # ms

commands = [
    ("1. Create Document", ["create", "/tmp/test.docx"]),
    ("2. Add Paragraph 1", ["add", "/tmp/test.docx", "/body", "--type", "paragraph", "--prop", "text=Title"]),
    ("3. Add Paragraph 2", ["add", "/tmp/test.docx", "/body", "--type", "paragraph", "--prop", "text=Intro"]),
    ("4. Get Body Elements", ["get", "/tmp/test.docx", "/body"]),
    ("5. View Text", ["view", "/tmp/test.docx", "text"])
]

print(f"{'Command Step':<25} | {'JIT Time (ms)':<15} | {'R2R Time (ms)':<15} | {'Speedup':<10}")
print("-" * 72)

total_jit = 0
total_r2r = 0

for label, args in commands:
    t_jit = run_cmd(jit_bin, args)
    t_r2r = run_cmd(r2r_bin, args)
    total_jit += t_jit
    total_r2r += t_r2r
    speedup = t_jit / t_r2r if t_r2r > 0 else 0
    print(f"{label:<25} | {t_jit:>12.2f} ms | {t_r2r:>12.2f} ms | {speedup:>8.1f}x")

print("-" * 72)
total_speedup = total_jit / total_r2r if total_r2r > 0 else 0
print(f"{'TOTAL DURATION':<25} | {total_jit:>12.2f} ms | {total_r2r:>12.2f} ms | {total_speedup:>8.1f}x\n")
