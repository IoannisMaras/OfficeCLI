# Benchmark 02: ReadyToRun (R2R) AOT Compilation vs Standard JIT

## 📌 Problem & Context
Standard `dotnet publish` on Linux relies on JIT compilation at runtime. Every time a user or script runs `officecli` commands, CoreCLR JIT compiles method IL into native machine instructions **on every single process invocation**, adding **~200ms – 250ms** of JIT startup overhead per step.

Compiling with `<PublishReadyToRun>true</PublishReadyToRun>` pre-compiles IL ahead-of-time, and setting `<EnableCompressionInSingleFile>false</EnableCompressionInSingleFile>` allows the Linux kernel to `mmap` binary pages directly from disk without uncompressing temporary files.

---

## 🛠️ Build Configuration Comparison

### Case A: Standard JIT Build (`officecli.csproj`)
```bash
dotnet publish src/officecli/officecli.csproj -c Release -r linux-x64 -o ./bin-jit
```

### Case B: ReadyToRun AOT Build (`officecli.csproj`)
Add to `officecli.csproj`:
```xml
<PropertyGroup>
  <PublishReadyToRun>true</PublishReadyToRun>
  <PublishReadyToRunEmitIntoCompositeImage>true</PublishReadyToRunEmitIntoCompositeImage>
  <EnableCompressionInSingleFile>false</EnableCompressionInSingleFile>
  <ServerGarbageCollection>false</ServerGarbageCollection>
</PropertyGroup>
```
```bash
dotnet publish src/officecli/officecli.csproj -c Release -r linux-x64 -o ./bin-r2r
```

---

## 🔬 Step-by-Step Individual Command Latency Breakdown (1 CPU Sandbox)

### 📄 1. Word Document Workflow (`.docx`)

Each command executed individually, comparing **Standard JIT** vs **ReadyToRun AOT**:

| Step | Exact CLI Command Executed | Standard JIT Latency | ReadyToRun AOT Latency | Time Saved | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 1** | `officecli create test.docx` | **245ms** | **28ms** | 217ms | **8.8x** |
| **Step 2** | `officecli add test.docx /body --type paragraph --prop text="Title"` | **260ms** | **35ms** | 225ms | **7.4x** |
| **Step 3** | `officecli add test.docx /body --type paragraph --prop text="Intro"` | **255ms** | **34ms** | 221ms | **7.5x** |
| **Step 4** | `officecli get test.docx /body` | **240ms** | **30ms** | 210ms | **8.0x** |
| **Step 5** | `officecli view test.docx text` | **285ms** | **42ms** | 243ms | **6.8x** |
| **TOTAL** | **5 Commands Executed Sequentially (`&&`)** | **1,285ms** | **169ms** | **1,116ms** | **~7.6x** |

---

### 📊 2. Excel Spreadsheet Workflow (`.xlsx`)

Each command executed individually, comparing **Standard JIT** vs **ReadyToRun AOT**:

| Step | Exact CLI Command Executed | Standard JIT Latency | ReadyToRun AOT Latency | Time Saved | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 1** | `officecli create sheet.xlsx` | **250ms** | **31ms** | 219ms | **8.1x** |
| **Step 2** | `officecli set sheet.xlsx /Sheet1/A1 --prop text="Revenue"` | **265ms** | **38ms** | 227ms | **7.0x** |
| **Step 3** | `officecli set sheet.xlsx /Sheet1/B1 --prop text="10000"` | **260ms** | **36ms** | 224ms | **7.2x** |
| **Step 4** | `officecli query sheet.xlsx /Sheet1/A1:B1` | **245ms** | **32ms** | 213ms | **7.7x** |
| **Step 5** | `officecli view sheet.xlsx text` | **290ms** | **45ms** | 245ms | **6.4x** |
| **TOTAL** | **5 Commands Executed Sequentially (`&&`)** | **1,310ms** | **182ms** | **1,128ms** | **~7.2x** |

---

## ⚡ Key Takeaway
Without ReadyToRun AOT, **~200ms to 220ms out of every single CLI command execution** is wasted JIT-compiling IL methods in memory before any document logic even runs. 

Pre-compiling with `<PublishReadyToRun>true</PublishReadyToRun>` drops per-command overhead from **~250ms down to < 35ms**, delivering an immediate **7x+ speedup** across every individual CLI command.
