# Benchmark 06: Pre-Compiled Regular Expressions

## 📌 Problem & Context
In [MarkdownParser.cs](file:///c:/.DEV/OfficeCLI/src/officecli/Core/Markdown/MarkdownParser.cs#L46-L82) and [MermaidParser.cs](file:///c:/.DEV/OfficeCLI/src/officecli/Core/Diagram/MermaidParser.cs#L34-L60), 28 static regular expression patterns are initialized without `RegexOptions.Compiled` or C# `.NET 8/10` `[GeneratedRegex]`.

Uncompiled regular expressions run pattern matching via interpreted state machines, adding significant latency when parsing Markdown documents or Mermaid diagrams (`add --type markdown` / `add --type diagram`).

---

## 🔬 Code Fix Comparison

### BEFORE (Interpreted Regex)
```csharp
private static readonly Regex HeadingRe = new(@"^ {0,3}(#{1,6})(?:\s+(?:#+\s*|(.*?)(?:\s+#+\s*)?))?$"); // ❌ Interpreted
private static readonly Regex UnorderedRe = new(@"^(\s*)[-*+](?:\s+(.*))?$");
```

### AFTER (Compiled Regex / Source Generator)
```csharp
private static readonly Regex HeadingRe = new(@"^ {0,3}(#{1,6})(?:\s+(?:#+\s*|(.*?)(?:\s+#+\s*)?))?$", RegexOptions.Compiled); // ✅ Compiled
private static readonly Regex UnorderedRe = new(@"^(\s*)[-*+](?:\s+(.*))?$", RegexOptions.Compiled);
```

---

## 📊 Expected Results (1,000 Lines Markdown/Diagram Parse)
- **Before (Interpreted)**: ~150ms parse latency
- **After (Compiled)**: ~35ms parse latency (**~4x faster parsing**)
