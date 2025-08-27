<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#ftcd">Fine-tuning Custom Dataset</a></li>
        <li><a href="#iuftm">Inference using Fine-tuned Model</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- GOOGLE COLAB -->
[Open Notebook on Google Drive](https://colab.research.google.com/drive/1xPZeCKeJKevm_pEavow_54CnER_DIqsK?usp=sharing)

<!-- ABOUT THE PROJECT -->
## About The Project

This project **Indonesian Folklore Storytelling in Japanese using Text-to-Speech Technology** proposes an integrated framework for cross-lingual folklore preservation by automating the conversion of Indonesian folk narratives into Japanese speech. The system combines machine translation and text-to-speech (TTS) synthesis: Google Translate converts Indonesian text into Japanese, and a fine-tuned Style-Bert-VITS2 model generates high-quality, expressive speech. The models in this project were fine-tuned on a dataset sourced from the YouTube channel of the virtual YouTuber (VTuber) [Suo Sango](https://www.youtube.com/@SuoSango). 

This work is intended for use within the private research community of the Human-AI Interaction Laboratory at Nara Institute of Science and Technology University (NAIST).

**Note:** As this repository contains models fine-tuned on a custom dataset, you must provide your own tokens and credentials to clone and use it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Fine-tuning Custom Dataset
<a id="ftcd"></a>

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Inference using Fine-tuned Model
<a id="iuftm"></a>

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
+ [ttsds/TTSDS-benchmark](https://github.com/ttsds/ttsds)
+ [othneildrew/README-Template](https://github.com/othneildrew/Best-README-Template)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
