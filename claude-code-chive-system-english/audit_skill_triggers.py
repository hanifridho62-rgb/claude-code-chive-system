import os
import glob
import re

skills_dir = "/tmp/claude_chive_system/.claude/skills"
skills = sorted(os.listdir(skills_dir))

print("=" * 70)
print("  AUDIT FRONTMATTER & TRIGGER METRICS FOR CLAUDE CODE")
print("=" * 70)

for s in skills:
    s_path = os.path.join(skills_dir, s, "SKILL.md")
    if not os.path.exists(s_path):
        print(f"[FAIL] {s}: SKILL.md not found!")
        continue
    
    with open(s_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check frontmatter fences
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        print(f"[FAIL] {s}: Line 1 is not '---'!")
        continue
        
    closing_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_idx = i
            break
            
    if closing_idx == -1:
        print(f"[FAIL] {s}: Closing '---' fence missing!")
        continue
        
    fm_text = "\n".join(lines[1:closing_idx])
    desc_match = re.search(r'description:\s*(.*?)(?=\n\w|\Z)', fm_text, re.DOTALL)
    when_match = re.search(r'when_to_use:\s*(.*?)(?=\n\w|\Z)', fm_text, re.DOTALL)
    
    desc_len = len(desc_match.group(1).strip()) if desc_match else 0
    when_len = len(when_match.group(1).strip()) if when_match else 0
    total_len = desc_len + when_len
    
    status = "OK" if total_len <= 1536 else "TRUNCATED (> 1536 chars)"
    print(f"{s:26s} | Desc+When: {total_len:4d} chars | Cap <= 1536: {status}")

print("=" * 70)
