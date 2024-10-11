import streamlit as st
import os

# Liste des langues disponibles
language_options = {
    "Français": "fr-FR",
    "Anglais": "en-US"
}

# Fonction JavaScript pour la reconnaissance vocale
def load_speech_recognition_js(language):
    return f"""
    <script>
    const startRecognition = () => {{
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = '{language}'; // Choisissez votre langue ici
        recognition.interimResults = false;

        recognition.onstart = () => {{
            console.log('Reconnaissance vocale en cours...');
            document.getElementById('status').innerHTML = 'Parlez maintenant...';
        }};

        recognition.onresult = (event) => {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('transcript').value = transcript;
            document.getElementById('status').innerHTML = 'Reconnaissance terminée.';
            // On peut aussi utiliser Streamlit pour afficher le texte
            const streamlitEvent = new Event('transcript-update');
            streamlitEvent.transcript = transcript;
            document.dispatchEvent(streamlitEvent);
        }};

        recognition.onerror = (event) => {{
            document.getElementById('status').innerHTML = 'Erreur de reconnaissance : ' + event.error;
        }};

        recognition.start();
    }};
    </script>
    <button onclick="startRecognition()">Démarrer la reconnaissance vocale</button>
    <p id="status"></p>
    <input type="text" id="transcript" style="width: 100%;" placeholder="Transcription ici..." />
    """

# Fonction principale de l'application
def main():
    st.title("Application de Reconnaissance Vocale Améliorée")

    # Sélection de la langue
    language_choice = st.selectbox("Choisissez la langue :", list(language_options.keys()))
    language_code = language_options[language_choice]

    # Charger le script JavaScript
    st.components.v1.html(load_speech_recognition_js(language_code), height=200)

    # Initialiser une session pour stocker la transcription
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""

    # Écouter les événements du JavaScript pour la transcription
    def update_transcript():
        transcript = st.text_input("Transcription :", st.session_state.transcript)
        if transcript:
            st.session_state.transcript = transcript
            st.success(f"Texte transcrit : {transcript}")

    # Afficher le texte transcrit
    update_transcript()

    # Écouter les mises à jour de la transcription
    st.components.v1.html(
        """
        <script>
        document.addEventListener('transcript-update', function(event) {
            const transcript = event.transcript;
            const streamlitElement = document.querySelector('input[id="transcript"]');
            if (streamlitElement) {
                streamlitElement.value = transcript;
            }
        });
        </script>
        """, height=0)

    # Option pour sauvegarder la transcription dans un fichier
    if st.button("Enregistrer la transcription"):
        save_transcription(st.session_state.transcript)

    # Vérifier si le fichier existe et permettre le téléchargement
    if os.path.exists("voix.txt"):
        with open("voix.txt", "rb") as file:
            st.download_button(label="Télécharger la transcription", data=file, file_name="voix.txt")


# Fonction pour sauvegarder la transcription dans un fichier
def save_transcription(text):
    if text:  # Vérification si le texte n'est pas vide
        file_name = "voix.txt"  # Nom du fichier
        # Écrire la transcription dans le fichier (mode écriture pour écraser le contenu)
        with open(file_name, "w") as f:  # "w" remplace le contenu
            f.write(text + "\n")  # Ajout d'un retour à la ligne
        st.success(f"Texte enregistré avec succès dans {file_name}")


if __name__ == "__main__":
    main()
