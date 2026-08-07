# Benchmark 05: Single-Pass Zip Header Parsing

## 📌 Problem & Context
In [DocumentHandlerFactory.cs](file:///c:/.DEV/OfficeCLI/src/officecli/Handlers/DocumentHandlerFactory.cs#L63-L98), opening any document executes `GuardDecompressionBomb(filePath)` which opens the Zip container (`ZipFile.OpenRead`) and reads all entries. Immediately after, `OpenHandler()` opens the exact same file from disk and parses the zip directory a second time.

---

## 🔬 Code Fix Comparison

### BEFORE (Double Open & Double Scan)
```csharp
if (IsNativeOoxml(ext))
    GuardDecompressionBomb(filePath); // ❌ Zip Open #1

var handler = OpenHandler(openTarget, ext, editable); // ❌ Zip Open #2
```

### AFTER (Single Pass Stream Re-use)
```csharp
if (IsNativeOoxml(ext))
{
    using var zipStream = ZipFile.OpenRead(filePath);
    GuardDecompressionBombStream(zipStream);
    var handler = OpenHandlerFromArchive(zipStream, ext, editable); // ✅ Zip Open #1 Only
    return handler;
}
```

---

## 📊 Expected Results
- **Before (Double Zip Scan)**: ~60ms file open latency
- **After (Single Pass)**: ~15ms file open latency (**45ms saved per invocation**)
