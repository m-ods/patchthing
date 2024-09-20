import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# Your Streamlit app code here
st.title("Audio Playback with Word Highlighting")

# Make a GET request to localhost for the transcript
try:
    response = requests.get("http://127.0.0.1:8000/a5d413dc-9b20-41db-9ae0-53efbd610de4")  # Adjust the port if necessary
    if response.status_code == 200:
        transcript = response.json()['transcript']
    else:
        st.error(f"Failed to fetch transcript. Status code: {response.status_code}")
        transcript = {'words': []}
except requests.RequestException as e:
    st.error(f"Error fetching transcript: {e}")
    transcript = {'words': []}

# Assume you have the audio file
audio_file = "https://storage.googleapis.com/linkthing/uploaded_files/Michael%2C%20Jim%2C%20Dwight%20epic%20scene%20%5BqHrN5Mf5sgo%5D.mp4"

# Create the custom HTML component
html_string = f"""
<audio id="audio-player" controls>
    <source src="{audio_file}" type="audio/mpeg">
</audio>
<div id="transcript"></div>
<script>
    const transcript = {json.dumps(transcript['words'])};
    const audioPlayer = document.getElementById('audio-player');
    const transcriptDiv = document.getElementById('transcript');

    // Populate transcript
    transcript.forEach((word, index) => {{
        const span = document.createElement('span');
        span.textContent = word.text + ' ';
        span.id = `word-${{index}}`;
        transcriptDiv.appendChild(span);
    }});

    let lastHighlightedIndex = -1;

    // Highlight words as audio plays
    audioPlayer.ontimeupdate = function() {{
        const currentTime = Math.floor(audioPlayer.currentTime * 1000);
        
        // Binary search to find the current word
        let low = 0;
        let high = transcript.length - 1;
        let currentIndex = -1;

        while (low <= high) {{
            const mid = Math.floor((low + high) / 2);
            const word = transcript[mid];

            if (currentTime >= word.start && currentTime <= word.end) {{
                currentIndex = mid;
                break;
            }} else if (currentTime < word.start) {{
                high = mid - 1;
            }} else {{
                low = mid + 1;
            }}
        }}

        // Update highlighting only if necessary
        if (currentIndex !== lastHighlightedIndex) {{
            if (lastHighlightedIndex !== -1) {{
                document.getElementById(`word-${{lastHighlightedIndex}}`).style.backgroundColor = 'transparent';
            }}
            if (currentIndex !== -1) {{
                document.getElementById(`word-${{currentIndex}}`).style.backgroundColor = 'yellow';
            }}
            lastHighlightedIndex = currentIndex;
        }}
    }};
</script>
"""

# Render the custom component
components.html(html_string, height=300)

# Display the full transcript for debugging (optional)
st.subheader("Full Transcript")
st.json(transcript)