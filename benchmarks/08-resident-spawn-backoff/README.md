# Benchmark 08: Adaptive Backoff for Resident Server Connection

## 📌 Problem & Context
When spawning a resident process in the background, [CommandBuilder.cs](file:///c:/.DEV/OfficeCLI/src/officecli/CommandBuilder.cs#L312) polls connection using a hardcoded 100ms sleep:
```csharp
for (int i = 0; i < 50; i++)
{
    Thread.Sleep(100);
    if (ResidentClient.TryConnect(filePath, out _)) return true;
}
```
Even if the background server process starts up in **3ms**, the client wastes a full **100ms** before checking connection on the first loop iteration.

---

## 🔬 Code Fix Comparison

### BEFORE (Hardcoded 100ms Sleep)
```csharp
for (int i = 0; i < 50; i++)
{
    Thread.Sleep(100); // ❌ Mandatory 100ms Delay
    if (ResidentClient.TryConnect(filePath, out _)) return true;
}
```

### AFTER (Adaptive Micro-Sleep Backoff)
```csharp
int[] delays = [1, 2, 5, 10, 25, 50, 100];
for (int i = 0; i < 50; i++)
{
    int sleepMs = i < delays.Length ? delays[i] : 100;
    Thread.Sleep(sleepMs); // ✅ Connects as soon as 3ms!
    if (ResidentClient.TryConnect(filePath, out _)) return true;
}
```

---

## 📊 Expected Results
- **Before (Hardcoded Sleep)**: ~100ms connection delay
- **After (Adaptive Micro-Sleep)**: ~5ms connection delay (**95ms latency saved per spawn**)
