[日本語版 README はこちら](README_ja.md)

# Stable Diffusion CLI on Modal

This is a Diffusers-based script for running Stable Diffusion on [Modal](https://modal.com/). This script has no WebUI and only works with CLI. It can perform txt2img inference and has the ability to increase resolution using ControlNet Tile and Upscaler.

## Features

1. Image generation using txt2img or img2img.
   ![](assets/20230902_tile_imgs.png)

2. Upscaling

| Before upscaling                                                 | After upscaling                                                  |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| <img src="assets/20230708204347_1172778945_0_0.png" width="300"> | <img src="assets/20230708204347_1172778945_0_2.png" width="300"> |

## Requirements

The app requires the following to run:

- python: > 3.10
- modal
- A token for Modal.

The `modal` is the Python library. In order to install that:

```bash
pip install modal
```

And you need a modal token to use this script:

```bash
modal token new
```

Please see [the documentation of Modal](https://modal.com/docs/guide) for modals and tokens.

## Getting Started

To use the script, execute the below.

1. git clone the repository.
2. Copy `./app/config.sample.yml` to `./app/config.yml`
3. Open the Makefile and set prompts.
4. Execute `make app` command. An application will be deployed to Modal.
5. Execute `make img_by_sd15_txt2img` command.

Images are generated and output to the `outputs/` directory.

## Directory structure

```txt
.
├── .env                        # Secrets manager
├── Makefile
├── README.md
├── cmd/                      # A directory with scripts to run inference.
│   ├── outputs/                # Images are outputted this directory.
│   ├── sd15_img2img.py         # A script to run sd15_img2img inference.
│   ├── sd15_txt2img.py         # A script to run sd15_txt2img inference.
│   ├── sdxl_txt2img.py         # A script to run sdxl_txt2img inference.
│   └── util.py
└── app/                # A directory with config files.
    ├── __main__.py             # A main script to run inference.
    ├── Dockerfile              # To build a base image.
    ├── config.yml              # To set a model, vae and some tools.
    ├── requirements.txt
    ├── setup.py                # Build an application to deploy on Modal.
    ├── stable_diffusion_1_5.py # There is a class to run inference about sd15.
    └── stable_diffusion_xl.py  # There is a class to run inference about sdxl.
```

## How to use

### 1. `git clone` the repository

```bash
git clone https://github.com/hodanov/stable-diffusion-modal.git
cd stable-diffusion-modal
```

### 2. Add hugging_face_token to .env file

Add hugging_face_token to .env file.

This script downloads and uses a model from HuggingFace, but if you want to use a model in a private repository, you will need to set this environment variable.

```txt
HUGGING_FACE_TOKEN="Write your hugging face token here."
```

### 3. Add the model to ./app/config.yml

Add the model used for inference. Use the Safetensors file as is. VAE, LoRA, and Textual Inversion are also configurable.

```yml
# ex)
model:
  name: stable-diffusion-1-5
  url: https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned.safetensors # Specify URL for the safetensor file.
vae:
  name: sd-vae-ft-mse
  url: https://huggingface.co/stabilityai/sd-vae-ft-mse-original/blob/main/vae-ft-mse-840000-ema-pruned.safetensors
controlnets:
  - name: control_v11f1e_sd15_tile
    repo_id: lllyasviel/control_v11f1e_sd15_tile
```

If you want to use LoRA and Textual Inversion, configure as follows.

```yml
# Example
loras:
  - name: lora_name.safetensors # Specify the LoRA file name. Any name is fine, but the extension `.safetensors` is required.
    url: download_link_here # Specify the download link for the safetensor file.
```

### 4. Setting prompts

Set the prompt to Makefile.

```makefile
# ex)
run:
 cd ./cmd && modal run txt2img.py \
 --prompt "hogehoge" \
 --n-prompt "mogumogu" \
 --height 768 \
 --width 512 \
 --samples 1 \
 --steps 30 \
 --seed 12321 |
 --upscaler "RealESRGAN_x2plus" \
 --use-face-enhancer "False" \
 --fix-by-controlnet-tile "True" \
 --output-fomart "avif"
```

### 5. Deploy an application

Execute the below command. An application will be deployed on Modal.

```bash
make app
```

### 6. Run inference

The txt2img inference is executed with the following command.

```bash
make img_by_sd15_txt2img
```

Thank you.
