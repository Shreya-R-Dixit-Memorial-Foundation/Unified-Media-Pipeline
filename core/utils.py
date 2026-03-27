import re

def sanitize_filename(name):
    """Cleans the topic to make it a safe filename."""
    clean_name = re.sub(r'[^\w\s-]', '', name).strip()
    return clean_name.replace(' ', '_')

def split_text_by_quotes(text):
    """Parses text to separate narration from dialogue segments."""
    # Normalize quotes
    normalized = text.replace('“', '"').replace('”', '"').replace('«', '"').replace('»', '"')
    
    segments = []
    current_chunk = []
    in_quote = False
    
    for char in normalized:
        if char == '"':
            chunk_str = "".join(current_chunk).strip()
            if chunk_str:
                segments.append((chunk_str, in_quote))
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
