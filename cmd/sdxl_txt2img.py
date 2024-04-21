import time

import modal
import util

app = modal.Stub("run-stable-diffusion-cli")
app.run_inference = modal.Function.from_name("stable-diffusion-cli", "SDXLTxt2Img.run_inference")


@app.local_entrypoint()
def main(
    prompt: str,
    n_prompt: str,
    height: int = 1024,
    width: int = 1024,
    samples: int = 5,
    steps: int = 20,
    seed: int = -1,
    upscaler: str = "",
    use_face_enhancer: str = "False",
    output_format: str = "png",
):
    """
    This function is the entrypoint for the Runway CLI.
    The function pass the given prompt to StableDiffusion on Modal,
    gets back a list of images and outputs images to local.
    """
    directory = util.make_directory()
    seed_generated = seed
    for i in range(samples):
        if seed == -1:
            seed_generated = util.generate_seed()
        start_time = time.time()
        images = app.run_inference.remote(
            prompt=prompt,
            n_prompt=n_prompt,
            height=height,
            width=width,
            steps=steps,
            seed=seed_generated,
            upscaler=upscaler,
            use_face_enhancer=use_face_enhancer == "True",
            output_format=output_format,
        )
        util.save_images(directory, images, seed_generated, i, output_format)
        total_time = time.time() - start_time
        print(f"Sample {i} took {total_time:.3f}s ({(total_time)/len(images):.3f}s / image).")

    prompts: dict[str, int | str] = {
        "prompt": prompt,
        "height": height,
        "width": width,
        "samples": samples,
    }
    util.save_prompts(prompts)
