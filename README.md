# Streamlit Virtual Piano 🎹
An interactive virtual piano application built with Streamlit and the Web Audio API, allowing users to play notes using their mouse or keyboard and customize the sound in real-time.

---

## ✨ Features
- **Responsive Design:** The piano keyboard automatically adjusts to fit any screen size, from desktop to mobile, ensuring all keys are always visible.
- **Real-time Sound Customization:** Use interactive sliders to adjust the ADSR (Attack, Decay, Sustain, Release) envelope, giving you full control over the sound's character.
- **Multiple Waveforms:** Choose from four different waveforms (sine, sawtooth, square, and triangle) to change the instrument's tone.
- **Mouse and Keyboard Input:** Play notes by clicking the keys or by using a dedicated keyboard mapping.
- **Sustain Pedal Functionality:** Press and hold the spacebar to activate a sustain pedal, allowing notes to ring out after the key is released.
- **Scalable Keyboard:** Easily change the number of keys and the starting MIDI note to create a keyboard of any size.

---

## 🚀 How to Run the App Locally
To get this project up and running on your local machine, follow these steps:
### Prerequisites
You'll need Python 3.7 or newer installed.
### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/AlienMinus/Piano
cd Piano
```
### Install the required Python library:
```bash
pip install streamlit
```
### Execution
Run the application using the Streamlit command:
```bash
streamlit run app.py
```
Your web browser should automatically open a new tab with the Streamlit app. If not, navigate to http://localhost:8501.

---

## 🛠️ Technologies Used
- **Python:** The core programming language for the Streamlit backend.
- **Streamlit:** The framework used to create the interactive web application and its user interface components.
- **JavaScript (Web Audio API):** Handles all audio synthesis, key presses, and sound generation directly in the browser for low-latency performance.
- **HTML/CSS:** Structures and styles the piano keyboard, making it responsive and visually appealing.
