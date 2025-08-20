import json
from pathlib import Path
from huggingface_hub import hf_hub_download
from style_bert_vits2.logging import logger

def download_bert_models():
    with open("bert/bert_models.json", encoding="utf-8") as fp:
        models = json.load(fp)
    for k, v in models.items():
        local_path = Path("bert").joinpath(k)
        for file in v["files"]:
            if not Path(local_path).joinpath(file).exists():
                logger.info(f"Downloading {k} {file}")
                hf_hub_download(v["repo_id"], file, local_dir=local_path)

def download_models():
    model_files  = {
        "MichaelJP/TTSDS-ID-JP": [
            "suo_sango_otona/config.json",
            "suo_sango_otona/style_vectors.npy",
            "suo_sango_otona/suo_sango_otona_e100.safetensors",
        ],
    }
    Path("model_assets").mkdir(exist_ok=True)
    for repo_id, files in model_files.items():
        for file in files:
            if not Path(f"model_assets/{file}").exists():
                logger.info(f"Downloading {file}")
                hf_hub_download(
                    repo_id,
                    file,
                    local_dir="model_assets",
                )

if __name__ == "__main__":
    download_bert_models()
    download_models()
