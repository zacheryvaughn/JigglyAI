from .device import device, precision
from diffusers import (
    # PIPELINES
    StableDiffusionPipeline,
    StableDiffusion3Pipeline,
    StableDiffusionXLPipeline,
    FluxPipeline,
    # SCHEDULERS
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    HeunDiscreteScheduler,
    DPMSolverMultistepScheduler,
    KDPM2DiscreteScheduler,
    KDPM2AncestralDiscreteScheduler,
    UniPCMultistepScheduler,
    LMSDiscreteScheduler
)
from app.detect_model import detect_model_type

model_path = "models/EvaClausMixPonyXL-V35.safetensors"

SCHEDULER_DICT = {
    'Euler': EulerDiscreteScheduler,
    'Euler Karras': EulerDiscreteScheduler,  # Standard Euler with Karras sigmas enabled
    'Euler Ancestral': EulerAncestralDiscreteScheduler,
    'Heun': HeunDiscreteScheduler,  # Standard Heun
    'Heun Karras': HeunDiscreteScheduler,  # Standard Heun with Karras sigmas enabled
    'DPM++ 2M': DPMSolverMultistepScheduler,  # Base DPM++ Scheduler
    'DPM++ 2M Karras': DPMSolverMultistepScheduler,  # Needs Karras sigmas enabled
    'DPM++ 2M SDE': DPMSolverMultistepScheduler,  # Needs sde-dpmsolver++ algorithm
    'DPM++ 2M SDE Karras': DPMSolverMultistepScheduler,  # Needs sde-dpmsolver++ and Karras sigmas
    'K DPM 2': KDPM2DiscreteScheduler,  # Standard K DPM 2
    'K DPM 2 Karras': KDPM2DiscreteScheduler,  # Standard K DPM 2 with Karras sigmas
    'K DPM 2 Ancestral': KDPM2AncestralDiscreteScheduler,  # K DPM 2 Ancestral
    'UniPC 2M': UniPCMultistepScheduler,
    'UniPC 2M Karras': UniPCMultistepScheduler,  # Needs Karras sigmas enabled
    'LMS': LMSDiscreteScheduler,
    'LMS Karras': LMSDiscreteScheduler  # Needs Karras sigmas enabled
}
# Schedulers incompatible with MPS
incompatible_mps_schedulers = ['Heun Karras', 'K DPM 2', 'K DPM 2 Karras', 'UniPC 2M', 'UniPC 2M Karras', 'LMS Karras']
second_order_schedulers = ['Heun', 'Heun Karras', 'K DPM 2', 'K DPM 2 Karras', 'K DPM 2 Ancestral']

def load_pipeline(scheduler_name):
    model_type = detect_model_type(model_path)

    if model_type == "SD1.5":
        required_pipeline = StableDiffusionPipeline

    elif model_type == "SDXL":
        required_pipeline = StableDiffusionXLPipeline

    # elif model_type == "SD3.5-large":
    #     required_pipeline = StableDiffusion3Pipeline

    # elif model_type == "Flux.1-dev":
    #     required_pipeline = FluxPipeline

    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    pipeline = required_pipeline.from_single_file(
        model_path,
        use_safetensors=True,
        variant="fp16",
        requires_safety_checker=False,
        safety_checker=None,
        torch_dtype=precision
    ).to(device)

    # Fallback for MPS Incompatible Schedulers
    if device == "mps" and scheduler_name in incompatible_mps_schedulers:
        print(f"Scheduler '{scheduler_name}' is incompatible with MPS. Defaulting to 'Euler'.")
        scheduler_name = "Euler"

    # Configure Scheduler Algorithm and Karras Sigmas
    if scheduler_name in SCHEDULER_DICT:
        scheduler_class = SCHEDULER_DICT[scheduler_name]
        if scheduler_name in ['Euler Karras', 'Heun Karras', 'K DPM 2 Karras']:
            pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config, use_karras_sigmas=True)
        elif scheduler_name == 'DPM++ 2M SDE':
            pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config, algorithm_type="sde-dpmsolver++")
        elif scheduler_name == 'DPM++ 2M SDE Karras':
            pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config, algorithm_type="sde-dpmsolver++", use_karras_sigmas=True)
        elif scheduler_name in ['DPM++ 2M Karras', 'UniPC 2M Karras', 'LMS Karras']:
            pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config, use_karras_sigmas=True)
        else:
            pipeline.scheduler = scheduler_class.from_config(pipeline.scheduler.config)
        
        # Print Pipeline Configurations
        print(f"Model Path: {model_path}")
        print(f"Model Type: {model_type}")
        print(f"Scheduler: {scheduler_name}")
        print(f"Algorithm Type: {pipeline.scheduler.config.get('algorithm_type', 'N/A')}")
        print(f"Use Karras Sigmas: {pipeline.scheduler.config.get('use_karras_sigmas', 'N/A')}")
    else:
        raise ValueError(f"Scheduler {scheduler_name} is not supported.")
    
    return pipeline