import re

def sanitize_filename(name):
    """Cleans the topic to make it a safe filename."""
    clean_name = re.sub(r'[^\w\s-]', '', name).strip()
    return clean_name.replace(' ', '_')

def split_text_smart(text):
    """
    Parses text into segments based on either "quotation marks" (for stories)
    or "Speaker Label:" prefixes (for scripts). Returns (text, is_speaker2).
    """
    # 1. Normalize quotes
    normalized = text.replace('“', '"').replace('”', '"').replace('«', '"').replace('»', '"')
    
    # Check if this is a Label-based script (Speaker1: / Speaker2:)
    if re.search(r'^\s*Speaker\d+:', normalized, re.MULTILINE):
        segments = []
        for line in normalized.split('\n'):
            line = line.strip()
            if not line: continue
            
            if 'Speaker2:' in line:
                segments.append((line.replace('Speaker2:', '').strip(), True))
            elif 'Speaker1:' in line:
                segments.append((line.replace('Speaker1:', '').strip(), False))
            else:
                # If no label but script-like, treat as Narrator/Speaker1
                segments.append((line, False))
        return segments

    # 2. Fallback to Quote-based splitting (for Narrator vs Character)
    segments = []
    current_chunk = []
    in_quote = False
    
    for char in normalized:
        if char == '"':
            chunk_str = "".join(current_chunk).strip()
            if chunk_str:
                segments.append((chunk_str, in_quote)) # in_quote=True means it's a character dialogue
            current_chunk = []
            in_quote = not in_quote
        else:
            current_chunk.append(char)
            
    final_chunk = "".join(current_chunk).strip()
    if final_chunk:
        segments.append((final_chunk, in_quote))
        
    return segments

def strip_speaker_labels(text):
    """Removes labels like 'Speaker 1:', 'Narrator:', etc."""
    return re.sub(r'^\s*\w+(\s*\d+)?:\s*', '', text, flags=re.MULTILINE)
