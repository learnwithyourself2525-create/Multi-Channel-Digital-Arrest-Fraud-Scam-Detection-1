# utils/download_assets.py

from huggingface_hub import hf_hub_download
import os

def download_all_models():
    """
    Downloads and caches all required pre-trained models from Hugging Face Hub.
    """
    print("--- Downloading Required ML Models ---")
    
    # Models for Text Classification
    text_model_name = "distilbert-base-uncased"
    print(f"Downloading: {text_model_name}...")
    hf_hub_download(repo_id=text_model_name, filename="config.json")
    hf_hub_download(repo_id=text_model_name, filename="pytorch_model.bin")
    hf_hub_download(repo_id=text_model_name, filename="tokenizer_config.json")
    hf_hub_download(repo_id=text_model_name, filename="vocab.txt")
    print(f"Successfully downloaded {text_model_name}.")

    # Models for Audio Classification
    audio_model_name = "facebook/wav2vec2-base"
    print(f"\nDownloading: {audio_model_name}...")
    hf_hub_download(repo_id=audio_model_name, filename="config.json")
    hf_hub_download(repo_id=audio_model_name, filename="pytorch_model.bin")
    hf_hub_download(repo_id=audio_model_name, filename="preprocessor_config.json")
    print(f"Successfully downloaded {audio_model_name}.")
    
    print("\n--- All assets downloaded successfully! ---")
    print("Note: The 'deepface' library will download its models on first use.")

if __name__ == "__main__":
    download_all_models()