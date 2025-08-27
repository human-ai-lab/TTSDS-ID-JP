<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#ttdsdidjp">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li>
          <a href="#ftcd">Fine-tuning Custom Dataset</a>
          <ul>
            <li><a href="#pcd">Preparing Custom Dataset</a></li>
            <li><a href="#ftp">Fine-tuning Process</a></li>
          </ul>
        </li>
        <li><a href="#iuftm">Inference using Fine-tuned Model</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
<a id="ttdsdidjp"></a>
## About TTSDS-ID-JP

This **Indonesian Folklore Storytelling in Japanese with Text-to-Speech** project proposes an integrated framework for cross-lingual folklore preservation by automating the conversion of Indonesian folk narratives into Japanese speech. The system combines machine translation and text-to-speech (TTS) synthesis: Google Translate converts Indonesian text into Japanese, and a fine-tuned Style-Bert-VITS2 model generates high-quality, expressive speech. The models in this project were fine-tuned on a dataset sourced from the YouTube channel of the virtual YouTuber (VTuber) [Suo Sango](https://www.youtube.com/@SuoSango). 

This work is intended for use within the private research community of the Human-AI Interaction Laboratory at Nara Institute of Science and Technology University (NAIST).

**Note:** As this repository contains models fine-tuned on a custom dataset, you must provide your own tokens and credentials to clone and use it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This guide outlines the process for fine-tuning a new model with your own custom dataset using the [Style-Bert-VITS2](https://github.com/litagin02/Style-Bert-VITS2) model. It also covers how to perform inference (generate speech) using our provided model, which was fine-tuned on data from [Suo Sango](https://www.youtube.com/@SuoSango).

*   **To fine-tune a model with your own dataset**, follow the steps in the "Fine-Tuning a Custom Dataset" section.
*   **To only generate speech using our pre-fine-tuned model**, jump directly to the [Inference using Fine-tuned Model](#iuftm) section.

<a id="ftcd"></a>
## Fine-tuning a Custom Dataset

Fine-tuning the model is computationally intensive. It is highly recommended to use a machine with a GPU possessing **more than 16 GB of VRAM**.

To provide a reference for expected fine-tuning times and Google Drive storage usage:
*   Our model was fine-tuned on the Suo Sango dataset (~2.5 hours of audio) for 100 epochs.
*   **Training Time on Various GPUs:**
    *   **Google Colab Pro T4 GPU** (16 GB VRAM): ~**12 hours**.
    *   **L4 GPU** (extrapolated): Estimated **4-6 hours** (2-3x faster than T4).
    *   **A100 GPU** (extrapolated): Estimated **1.5-3 hours** (4-8x faster than T4).
*   **Storage Considerations:**
    *   For every 1000 steps (where 1 epoch ≈ 375 steps), the process saves:
        *   A final model file (`*.safetensors`) of ~**240 MB**.
        *   A full training checkpoint of ~**1.4 GB+**, required to resume fine-tuning.
    *   **Important:** While only the latest checkpoint is kept in the target folder, previous checkpoints are moved to your Google Drive's trash. **You must manually empty your trash** to free up this storage space during long training runs.

If you already have a prepared custom dataset, you can proceed to the [Fine-tuning Process](#ftp).

<a id="pcd"></a>
### Preparing Custom Dataset

The custom dataset preparation process begins by sourcing audio from a YouTube video, downloaded as a `*.wav` file using the `yt-dlp` library. To ensure high-quality results, it is crucial to select videos focused on clear storytelling without background music or sound effects. The resulting audio file is then segmented based on manually annotated timestamps created in Audacity, using the `pydub` library to accurately split the audio at precise phrase boundaries. For the text transcript, Japanese novels can be sourced from [Aozora Bunko](https://www.aozora.gr.jp/); this text is subsequently split into sentences using standard Python string operations based on punctuation. 

**Note:** `yt-dlp` cannot download videos marked as "Members Only" without providing YouTube account cookies from an account that has access to the corresponding channel's membership.

The following sections detail the methodology and provide code references for each step in this workflow.

1. Download youtube video as a `*.wav` file using yt-dlp (to ensure clean dependency management, it is recommended to create a new Conda environment before installing `yt-dlp`.)
  ```sh
  pip install yt-dlp
  pip install ffmpeg
  yt-dlp --extract-audio --audio-format wav "youtube-link"
  ```

2. Split the text transcript
  ```sh
  filenames = ["file_name"] ### CHANGE HERE ###
  index = 0
  size = 120
  
  for filename in filenames:
      title = 1
      with open(f"./path/to/{filename}.txt", "r", encoding="utf-8") as read_file: ### CHANGE HERE ###
          with open(f"./path/to/model_name_{filename}.txt", "w", encoding="utf-8") as write_file: ### CHANGE HERE ###
              buffer = ''
              for row in read_file:
                  row = row.strip()
                  row = row.split("。")
                  for part in row:
                      text = buffer + part
                      if len(text) >= 10 or title:
                          write_file.write(f"dataset/model_name/model_name{index//size+1:03d}_{index%size+1:03d}.wav|0|{text}\n") ### CHANGE HERE ###
                          index += 1
                          buffer = ''
                          title = 0
                      elif text != '':
                          buffer = text + '。'                            
  ```

3. Split the audio file (each audio file has a different optimal silence threshold; always experiment to find the right `silence_threshold` value.)
  ```sh
  pip install pydub
  ```
  ```sh
  from pydub import AudioSegment
  from pydub.silence import detect_leading_silence
  
  audio = AudioSegment.from_file("./path/to/model_name_filename.wav", format="wav") ### CHANGE HERE ###
  size = 120
  
  with open("./path/to/corresponding_filename_timestamp_text.txt", "r", encoding="utf-8") as read_file: ### CHANGE HERE ###
      timestamps_in_seconds = [float(timestamp.split('\t')[0]) for timestamp in read_file]
  timestamps_ms = [t * 1000 for t in timestamps_in_seconds]
  start_ms, timestamps_ms = timestamps_ms[0], timestamps_ms[1:]
  print(f"Timestamps size: {len(timestamps_ms)}")
  
  for i, end_ms in enumerate(timestamps_ms):
      print("Exporting chunk{0}.wav.".format(i+1))
      segment = audio[start_ms:end_ms]
      leading_silence = detect_leading_silence(
          segment, 
          silence_threshold=-80, ### CHANGE HERE ###
          chunk_size=10
      )
      if leading_silence > 0:
          print(f"Chunk {i+1}: Trimmed {leading_silence}ms of leading silence")
          segment = segment[leading_silence:]
      
      silence_chunk = AudioSegment.silent(duration=500)
      audio_chunk = silence_chunk + segment + silence_chunk
      audio_chunk.export(f"./path/to/model_name{i//size+1:03d}_{i%size+1:03d}.wav", format="wav") ### CHANGE HERE ###
      start_ms = end_ms
  ```

<a id="ftp"></a>
### Fine-tuning Process
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xPZeCKeJKevm_pEavow_54CnER_DIqsK?usp=sharing)

1. Clone `Style-Bert-VITS2` repo

<a id="iuftm"></a>
## Inference using Fine-tuned Model
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XUIlCzJQfIi2hFJwTtE1VUr67ax4qJYX?usp=sharing)

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REFERENCES -->
## References
+ [suo-sango/Storytelling-Voice](https://youtube.com/@suosango?si=0GXrUXLqZsP7NgOT)
+ [litagin02/Style-Bert-VITS2](https://github.com/litagin02/Style-Bert-VITS2)
+ [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
+ [jiaaro/pydub](https://github.com/jiaaro/pydub)
+ [Aozora Bunko](https://www.aozora.gr.jp/)
+ [ttsds/TTSDS-benchmark](https://github.com/ttsds/ttsds)
+ [othneildrew/README-Template](https://github.com/othneildrew/Best-README-Template)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
