import streamlit as st
import speech_recognition as sr
import os

# Liste des API disponibles
api_options = {
    "Google": "google",
    "Sphinx (offline)": "sphinx"
}

# Liste des langues disponibles
language_options = {
    "Français": "fr-FR",
    "Anglais": "en-US"
}

# Fonction pour la transcription de la parole
def transcribe_speech(api_choice, language):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Parlez maintenant...")

        try:
            # Ajustement pour réduire le bruit ambiant
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source)
            st.info("Transcription en cours...")

            # Transcription selon l'API choisie
            if api_choice == "google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "sphinx":
                text = r.recognize_sphinx(audio_text)
            else:
                text = "API non prise en charge."

            return text

        except sr.UnknownValueError:
            return "Erreur : Impossible de comprendre l'audio."
        except sr.RequestError as e:
            return f"Erreur de requête : {e}"
        except Exception as e:
            return f"Erreur inattendue : {e}"

# Fonction pour sauvegarder la transcription dans un fichier
def save_transcription(text):
    if text:  # Vérification si le texte n'est pas vide
        file_name = "voix.txt"  # Nom du fichier
        # Écrire la transcription dans le fichier (mode écriture pour écraser le contenu)
        with open(file_name, "w") as f:  # "w" remplace le contenu
            f.write(text + "\n")  # Ajout d'un retour à la ligne
        st.success(f"Texte enregistré avec succès dans {file_name}")

# Fonction principale de l'application
def main():
    st.title("Application de Reconnaissance Vocale Améliorée")

    # Sélection de l'API
    api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale :", list(api_options.keys()))
    api_key = api_options[api_choice]

    # Sélection de la langue
    language_choice = st.selectbox("Choisissez la langue :", list(language_options.keys()))
    language_code = language_options[language_choice]

    # Initialiser une session pour stocker la transcription
    if "transcription" not in st.session_state:
        st.session_state.transcription = ""  # Initialisation à vide

    # Ajout du bouton pour démarrer la reconnaissance
    if st.button("Commencer l'enregistrement"):
        text = transcribe_speech(api_key, language_code)
        st.session_state.transcription = text  # Mettre à jour la transcription dans session_state
        st.write("Transcription :", text)

    # Option pour sauvegarder la transcription
    if st.session_state.transcription and st.button("Enregistrer la transcription"):
        save_transcription(st.session_state.transcription)

    # Vérifier si le fichier existe et permettre le téléchargement
    if os.path.exists("voix.txt"):
        with open("voix.txt", "rb") as file:
            st.download_button(label="Télécharger la transcription", data=file, file_name="voix.txt")


if __name__ == "__main__":
    main()
