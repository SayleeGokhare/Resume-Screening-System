import re

COMMON_SKILLS = [
    'python', 'django', 'sql', 'html', 'css', 'javascript', 'react', 'node', 'java', 'c++', 'aws', 'docker', 'kubernetes',
    'machine learning', 'data science', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'flask', 'fastapi',
    'git', 'linux', 'agile', 'scrum', 'communication', 'leadership', 'problem solving', 'teamwork'
]

def extract_skills(text):
    found = []
    text = text.lower()
    for skill in COMMON_SKILLS:
        # Escape special characters like C++
        skill_pattern = re.escape(skill)
        
        # Pattern to match potential versions (e.g. html5, css3, python 3.10)
        # We look for the skill followed optionally by version numbers or just as a word
        # But for simpler matching, let's just use the word boundary or non-word char check
        
        # Regex explanation:
        # \b{skill}\b -> Matches 'python' but not 'python3'
        # \b{skill} -> Matches 'python' and 'python3'
        # But we want to be careful not to match 'java' in 'javascript' if javascript is also in the list.
        # Since our list has specific skills, we can check for them.
        
        # Better approach: 
        # 1. Direct match with word boundaries
        # 2. Or match with version numbers appended
        
        pattern = r'\b' + skill_pattern + r'(?:\d+(\.\d+)?)?\b'
        
        # Special case for C++ which doesn't work well with \b at the end
        if '+' in skill or '#' in skill:
            pattern = re.escape(skill)
            
        if re.search(pattern, text):
            found.append(skill)
            
    return ','.join(found)
