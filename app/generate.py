import random
import math
import torch
from app import socketio
from .pipeline import load_pipeline
from .outputs import save_image
from threading import Event

def start_generation(data):
    # Extract scheduler
    scheduler_name = data.get("scheduler")
    if not scheduler_name:
        socketio.emit("generation_failed", {"error": "Missing 'scheduler' parameter"})
        return

    try:
        pipeline = load_pipeline(scheduler_name)
    except Exception as e:
        socketio.emit("generation_failed", {"error": f"Failed to load pipeline: {e}"})
        return

    # Ensure that required parameters have been recieved
    prompt = data.get("prompt")
    if not prompt:
        socketio.emit("generation_failed", {"error": "Missing 'prompt' parameter"})
        return
    
    num_inference_steps = data.get("num_inference_steps")
    if not num_inference_steps:
        socketio.emit("generation_failed", {"error": "Missing 'num_inference_steps' parameter"})
        return
    num_inference_steps = int(num_inference_steps)

    guidance_scale = data.get("guidance_scale")
    if not guidance_scale:
        socketio.emit("generation_failed", {"error": "Missing 'guidance_scale' parameter"})
        return
    guidance_scale = float(guidance_scale)

    width = data.get("width")
    if not width:
        socketio.emit("generation_failed", {"error": "Missing 'width' parameter"})
        return
    width = int(width)

    height = data.get("height")
    if not height:
        socketio.emit("generation_failed", {"error": "Missing 'height' parameter"})
        return
    height = int(height)

    # Optional parameters may be empty
    negative_prompt = data.get("negative_prompt", "low quality, watermark")
    seed = data.get("seed", None)

    if seed is None or seed == '' or math.isnan(seed):
        seed = random.randint(0, 2**32 - 1)
    generator = torch.Generator().manual_seed(seed)

    try:
        print("Starting generation...")
        output = pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            generator=generator,
        )

        filename = save_image(output, seed)
        socketio.emit("generation_completed", {"filename": filename})
    except Exception as e:
        print(f"Generation failed: {e}")
        socketio.emit("generation_failed", {"error": str(e)})
