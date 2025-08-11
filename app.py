import streamlit as st
import numpy as np

# --- Configuration ---
DEFAULT_KEYS = 24  # Default number of keys (e.g., 2 octaves)
KEY_WIDTH_PX = 40
KEY_HEIGHT_PX = 150
BLACK_KEY_WIDTH_RATIO = 0.6
BLACK_KEY_HEIGHT_RATIO = 0.6

# Mapping of keyboard keys to MIDI notes relative to the starting note
KEY_MAP = {
    'a': 0, 'w': 1, 's': 2, 'e': 3, 'd': 4, 'f': 5, 't': 6, 'g': 7, 'y': 8, 'h': 9, 'u': 10, 'j': 11,
    'k': 12, 'o': 13, 'l': 14, 'p': 15, ';': 16, "'": 17, 'z': 18, 'x': 19, 'c': 20, 'v': 21, 'b': 22, 'n': 23, 'm': 24
}

# --- Piano Key Frequencies ---
def get_frequency(midi_note_number):
    """Calculates the frequency for a given MIDI note number."""
    return 440 * (2 ** ((midi_note_number - 69) / 12))

# --- Piano Key Layout Logic ---
def get_key_info(start_midi_note, num_keys):
    """
    Generates layout information for a piano keyboard.
    Returns a list of dictionaries, one for each key.
    """
    keys = []
    white_key_count = 0
    key_types = [
        ("white", True),  # C
        ("black", False), # C#
        ("white", True),  # D
        ("black", False), # D#
        ("white", True),  # E
        ("white", True),  # F
        ("black", False), # F#
        ("white", True),  # G
        ("black", False), # G#
        ("white", True),  # A
        ("black", False), # A#
        ("white", True)   # B
    ]

    for i in range(num_keys):
        current_midi_note = start_midi_note + i
        note_in_octave_idx = (current_midi_note - 21) % 12  # A0 is MIDI 21
        key_type_info = key_types[note_in_octave_idx]
        is_white_key = key_type_info[1]
        
        # Map a keyboard key to the piano key if available
        keyboard_key = None
        for k, v in KEY_MAP.items():
            if v == i:
                keyboard_key = k
                break

        if is_white_key:
            x_position = white_key_count * KEY_WIDTH_PX
            white_key_count += 1
            width = KEY_WIDTH_PX
            height = KEY_HEIGHT_PX
            color = "#FFFFFF"
            z_index = 1
            label = f"C{(current_midi_note // 12) - 1}" if note_in_octave_idx == 0 else ""
        else:
            width = KEY_WIDTH_PX * BLACK_KEY_WIDTH_RATIO
            height = KEY_HEIGHT_PX * BLACK_KEY_HEIGHT_RATIO
            color = "#333333"
            z_index = 2
            label = ""
            
            # Manual horizontal positioning for black keys
            offset_factor = 0.6
            x_position = (white_key_count - 1) * KEY_WIDTH_PX + (KEY_WIDTH_PX * offset_factor) - (width / 2)

        keys.append({
            "midi_note": current_midi_note,
            "frequency": get_frequency(current_midi_note),
            "type": key_type_info[0],
            "x": x_position,
            "y": 0,
            "width": width,
            "height": height,
            "color": color,
            "z_index": z_index,
            "label": label,
            "keyboard_key": keyboard_key
        })

    return keys

# --- Streamlit App ---
st.set_page_config(layout="centered", page_title="Streamlit Virtual Piano")

st.title("Streamlit Virtual Piano")
st.markdown("Play using your **mouse** or **keyboard**! Press the **spacebar** for sustain.")
st.write("---")

# --- Piano Settings ---
col1, col2, col3 = st.columns([1, 1, 0.7])

with col1:
    num_keys = st.slider(
        "Number of Keys",
        min_value=12,
        max_value=30,
        value=DEFAULT_KEYS,
        step=1,
        help="Adjust the total number of piano keys."
    )

with col2:
    start_midi_note = st.slider(
        "Starting MIDI Note (C4=60)",
        min_value=21,
        max_value=96,
        value=60,
        step=1,
        help="Select the MIDI note number for the leftmost key."
    )

with col3:
    waveform_type = st.selectbox(
        "Waveform",
        ("sine", "sawtooth", "square", "triangle"),
        help="Choose the tone of the notes."
    )
    volume = st.slider(
        "Volume",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Adjust the overall volume."
    )

st.write("---")

# --- Piano Keyboard UI with Sound ---
piano_keys = get_key_info(start_midi_note, num_keys)
total_white_keys = sum(1 for key in piano_keys if key['type'] == 'white')
piano_width = total_white_keys * KEY_WIDTH_PX

# HTML and CSS for the piano
html_content = f"""
<style>
.piano-container {{
    position: relative;
    width: {piano_width}px;
    height: {KEY_HEIGHT_PX}px;
    margin: 20px auto;
    border: 2px solid #555;
    background-color: #eee;
    border-radius: 5px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    overflow: hidden;
}}
.piano-key {{
    position: absolute;
    cursor: pointer;
    box-sizing: border-box;
    border-radius: 0 0 3px 3px;
    transition: all 0.1s ease;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    padding-bottom: 5px;
    font-size: 0.8em;
    user-select: none;
}}
.piano-key-label {{
    position: absolute;
    bottom: 5px;
    font-size: 0.7em;
    color: #555;
}}
.piano-key.white-key {{
    background-color: #FFFFFF;
    border: 1px solid #333333;
    z-index: 1;
}}
.piano-key.black-key {{
    background-color: #333333;
    border: 1px solid #111111;
    z-index: 2;
}}
.piano-key:active, .piano-key.active {{
    transform: translateY(2px);
    box-shadow: none;
}}
.piano-key.active.white-key {{
    background-color: #D3D3D3; /* Gray highlight */
}}
.piano-key.active.black-key {{
    background-color: #555555; /* Lighter black highlight */
}}
</style>
<div class="piano-container" tabindex="0">
"""

# Add each key's HTML to the content
for key in piano_keys:
    keyboard_key_label = f"<span class='piano-key-label'>{key['keyboard_key'].upper()}</span>" if key['keyboard_key'] else ""
    html_content += f"""
    <div class="piano-key {key['type']}-key"
         style="
             left: {key['x']}px;
             top: {key['y']}px;
             width: {key['width']}px;
             height: {key['height']}px;
             background-color: {key['color']};
             z-index: {key['z_index']};
         "
         data-frequency="{key['frequency']}"
         data-keyboard-key="{key['keyboard_key']}"
         title="MIDI: {key['midi_note']} | Freq: {key['frequency']:.2f} Hz | Key: {key['keyboard_key']}"
    >
        {key['label']} {keyboard_key_label}
    </div>
    """
html_content += "</div>"

# --- JavaScript for advanced sound generation and keyboard input ---
js_code = f"""
<script>
    document.addEventListener('DOMContentLoaded', function() {{
        const pianoContainer = document.querySelector('.piano-container');
        const keys = pianoContainer ? pianoContainer.querySelectorAll('.piano-key') : [];
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Pass Streamlit values to JavaScript
        const waveformType = '{waveform_type}';
        const volume = {volume};

        const activeOscillators = new Map();
        let sustainEnabled = false;

        // ADSR Envelope parameters
        const attackTime = 0.05;
        const decayTime = 0.2;
        const releaseTime = 0.3;
        const sustainLevel = 0.7;

        function playNote(keyElement) {{
            if (!keyElement || (activeOscillators.has(keyElement))) return;

            const frequency = parseFloat(keyElement.dataset.frequency);
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.type = waveformType;
            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);

            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(volume, audioContext.currentTime + attackTime);
            gainNode.gain.exponentialRampToValueAtTime(volume * sustainLevel, audioContext.currentTime + attackTime + decayTime);

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start();
            activeOscillators.set(keyElement, {{ oscillator, gainNode }});
        }}

        function stopNote(keyElement) {{
            if (!keyElement || !activeOscillators.has(keyElement)) return;

            const {{ oscillator, gainNode }} = activeOscillators.get(keyElement);
            if (!sustainEnabled) {{
                gainNode.gain.cancelScheduledValues(audioContext.currentTime);
                gainNode.gain.setValueAtTime(gainNode.gain.value, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + releaseTime);
                oscillator.stop(audioContext.currentTime + releaseTime);
                activeOscillators.delete(keyElement);
            }}
        }}

        // --- Mouse Events ---
        keys.forEach(key => {{
            key.addEventListener('mousedown', () => {{
                playNote(key);
                key.classList.add('active');
            }});
            key.addEventListener('mouseup', () => {{
                stopNote(key);
                if (!sustainEnabled) key.classList.remove('active');
            }});
            key.addEventListener('mouseleave', () => {{
                stopNote(key);
                if (!sustainEnabled) key.classList.remove('active');
            }});
        }});

        // --- Keyboard Events ---
        const keyMap = new Map();
        keys.forEach(key => {{
            const keyboardKey = key.dataset.keyboardKey;
            if (keyboardKey) {{
                keyMap.set(keyboardKey, key);
            }}
        }});

        document.addEventListener('keydown', (event) => {{
            if (event.code === 'Space') {{
                sustainEnabled = true;
                return;
            }}
            const keyElement = keyMap.get(event.key.toLowerCase());
            if (keyElement) {{
                playNote(keyElement);
                keyElement.classList.add('active');
            }}
        }});

        document.addEventListener('keyup', (event) => {{
            if (event.code === 'Space') {{
                sustainEnabled = false;
                // Stop all sustained notes
                activeOscillators.forEach((value, keyElement) => {{
                    stopNote(keyElement);
                    keyElement.classList.remove('active');
                }});
                return;
            }}
            const keyElement = keyMap.get(event.key.toLowerCase());
            if (keyElement && !sustainEnabled) {{
                stopNote(keyElement);
                keyElement.classList.remove('active');
            }}
        }});
    }});
</script>
"""

# Combine and render the full HTML
full_html_content = html_content + js_code
st.components.v1.html(full_html_content, height=KEY_HEIGHT_PX + 40)