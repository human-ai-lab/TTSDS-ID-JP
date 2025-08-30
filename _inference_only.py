from style_bert_vits2.constants import (
    DEFAULT_ASSIST_TEXT_WEIGHT,
    DEFAULT_LENGTH,
    DEFAULT_LINE_SPLIT,
    DEFAULT_NOISE,
    DEFAULT_NOISEW,
    DEFAULT_SDP_RATIO,
    DEFAULT_SPLIT_INTERVAL,
    DEFAULT_STYLE,
    DEFAULT_STYLE_WEIGHT,
)
from style_bert_vits2.nlp.japanese import pyopenjtalk_worker as pyopenjtalk
from style_bert_vits2.tts_model import TTSModelHolder
from pathlib import Path
import soundfile as sf
import torch

pyopenjtalk.initialize_worker()

def generate_audio(text: str):
    
    assets_root = "model_assets"
    assets_root = Path(assets_root)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_holder = TTSModelHolder(assets_root, device)
    
    model_name = "suo_sango_otona"
    model_path = assets_root / model_name / "suo_sango_otona_e100.safetensors"
    model_holder.get_model(model_name, str(model_path))
    assert model_holder.current_model is not None

    speaker_id = model_holder.current_model.spk2id["suo_sango"]
    
    sr, audio = model_holder.current_model.infer(
        text=text,
        language="JP",
        reference_audio_path=None,
        sdp_ratio=DEFAULT_SDP_RATIO,
        noise=DEFAULT_NOISE,
        noise_w=DEFAULT_NOISEW,
        length=DEFAULT_LENGTH,
        line_split=DEFAULT_LINE_SPLIT,
        split_interval=DEFAULT_SPLIT_INTERVAL,
        assist_text=None,
        assist_text_weight=DEFAULT_ASSIST_TEXT_WEIGHT,
        use_assist_text=False,
        style=DEFAULT_STYLE,
        style_weight=DEFAULT_STYLE_WEIGHT,
        given_tone=None,
        speaker_id=speaker_id,
        pitch_scale=1.0,
        intonation_scale=1.0,
    )
        
    sf.write("./_connector/generated_output.wav", audio, sr)

TRANSLATED_TEXT_PATH = "./_connector/translated_text.txt"

with open(TRANSLATED_TEXT_PATH, "r", encoding="utf-8") as f:
    translated_text = f.read()

generate_audio(translated_text)
