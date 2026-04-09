import anthropic
import os
from pathlib import Path

client = anthropic.Anthropic()

def generate_post(platform: str, topic: str, photo_dir: str = None):
    """
    Genereert een social media post met Claude.
    
    platform: 'instagram' of 'linkedin'
    topic: beschrijving van de post
    photo_dir: pad naar fotomap (optioneel)
    """
    
    # Zoek beschikbare foto's
    photos = []
    if photo_dir:
        photo_path = Path(photo_dir)
        if photo_path.exists():
            photos = list(photo_path.glob("*.jpg")) + list(photo_path.glob("*.png"))
    
    # Bouw de prompt op
    photo_info = f"Beschikbare foto's: {[p.name for p in photos]}" if photos else "Geen foto's gevonden."
    
    prompt = f"""
    Maak een {platform} post over: {topic}
    
    {photo_info}
    
    Geef terug:
    1. Welke foto je zou kiezen (als er foto's zijn) en waarom
    2. De tekst voor de post
    3. Relevante hashtags
    """
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test
    result = generate_post(
        platform="linkedin",
        topic="ons nieuwe product launch",
        photo_dir="photos/linkedin"
    )
    print(result)
