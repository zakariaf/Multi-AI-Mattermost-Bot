from openai_client import generate_chat_response, generate_image, transcribe_audio

def test_generate_chat_response():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    response = generate_chat_response(messages)
    print("Chat Response:", response)

def test_generate_image():
    prompt = "A serene landscape with mountains and a river during sunset."
    image_b64 = generate_image(prompt)
    if image_b64:
        with open("test_image.png", "wb") as image_file:
            import base64
            image_file.write(base64.b64decode(image_b64))
        print("Image generated and saved as test_image.png")
    else:
        print("Failed to generate image.")

def test_transcribe_audio():
    audio_file_path = "./src/sample_audio.wav"  # Replace with an actual audio file path
    transcript = transcribe_audio(audio_file_path)
    print("Transcribed Text:", transcript)

if __name__ == "__main__":
    print("Testing Chat Response...")
    test_generate_chat_response()
    print("\nTesting Image Generation...")
    test_generate_image()
    print("\nTesting Audio Transcription...")
    test_transcribe_audio()