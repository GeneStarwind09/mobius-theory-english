using System;
using System.Text;

// This method is copied into the game's existing formatter by TextPatch.
// The helper assembly is used during patching only, not installed into the game.
public static class EnglishWrap {
    public static string SetString(string text, int chineseColumns) {
        if (String.IsNullOrEmpty(text)) return text ?? "";
        int width = Math.Max(12, chineseColumns * 2);
        var result = new StringBuilder();
        string[] paragraphs = text.Replace("\r", "").Split('\n');
        // Individual stores avoid compiler-generated static data in this helper
        // assembly: the copied method must depend only on the game and mscorlib.
        char[] separators = new char[3];
        separators[0] = ' '; separators[1] = '\t'; separators[2] = '\u3000';
        for (int p = 0; p < paragraphs.Length; p++) {
            if (p > 0) result.Append('\n');
            int used = 0;
            foreach (string word in paragraphs[p].Split(separators, StringSplitOptions.RemoveEmptyEntries)) {
                if (used > 0 && used + 1 + word.Length > width) { result.Append('\n'); used = 0; }
                if (used > 0) { result.Append(' '); used++; }
                result.Append(word); used += word.Length;
            }
        }
        return result.ToString();
    }
}
