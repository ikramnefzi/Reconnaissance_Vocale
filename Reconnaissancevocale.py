import streamlit as st

# Fonction JavaScript pour la reconnaissance vocale
def load_speech_recognition_js():
    return """
    <script>
    const startRecognition = () => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'fr-FR'; // Choisissez votre langue ici
        recognition.interimResults = false;

        recognition.onstart = () => {
            console.log('Reconnaissance vocale en cours...');
            document.getElementById('status').innerHTML = 'Parlez maintenant...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('transcript').value = transcript;
            document.getElementById('status').innerHTML = 'Reconnaissance terminée.';
            // On peut aussi utiliser Streamlit pour afficher le texte
            const streamlitEvent = new Event('transcript-update');
            streamlitEvent.transcript = transcript;
            document.dispatchEvent(streamlitEvent);
        };

        recognition.onerror = (event) => {
            document.getElementById('status').innerHTML = 'Erreur de reconnaissance : ' + event.error;
        };

        recognition.start();
    };
    </script>
    <button onclick="startRecognition()">Démarrer la reconnaissance vocale</button>
    <p id="status"></p>
    <input type="text" id="transcript" style="width: 100%;" placeholder="Transcription ici..." />
    """

# Fonction principale de l'application
def main():
    st.title("Application de Reconnaissance Vocale")

    # Charger le script JavaScript
    st.components.v1.html(load_speech_recognition_js(), height=200)

    # Afficher le texte de la transcription
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""

    # Écouter les événements du JavaScript
    def update_transcript():
        transcript = st.text_input("Transcription :", st.session_state.transcript)
        if transcript:
            st.session_state.transcript = transcript
            st.success(f"Texte transcrit : {transcript}")

    # Afficher le texte transcrit
    st.write("Transcription :", st.session_state.transcript)

    # Écouter les mises à jour de la transcription
    st.components.v1.html(
        f"""
        <script>
        document.addEventListener('transcript-update', function(event) {{
            const transcript = event.transcript;
            const streamlitElement = document.querySelector('input[id="transcript"]');
            if (streamlitElement) {{
                streamlitElement.value = transcript;
            }}
        }});
        </script>
        """, height=0)

if __name__ == "__main__":
    main()
