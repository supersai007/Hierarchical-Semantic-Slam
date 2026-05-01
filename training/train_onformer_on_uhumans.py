# !pip install transformers torch torchvision

import os
import pandas as pd


from transformers import (
    OneFormerProcessor,
    OneFormerForUniversalSegmentation,
    OneFormerConfig
)
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import torch
from pathlib import Path

# remap sub_id = simulator label --> super_id = uHumans2 office label based on lookup table from uhumans2_office.yaml
REMAP = {
    10: 1,   # air_vent
    5:  2,   # books
    14: 3,   # floor
    202: 0,  # unknown
    128: 4,  # ceiling_light
    191: 19, # wall
    100: 9,  # cabinet
    28: 5,   # chair
    36: 7,   # couch
    163: 16, # desk
    151: 10, # computer
    71: 3,   # floor
    86: 11,  # lamp
    93: 6,   # bench
    198: 12, # painting
    130: 13, # plant
    131: 14, # sign
    148: 20, # human
    161: 17, # cubicle
    193: 18, # trashcan
    203: 15, # stairs
    204: 0,  # unknown
}
NUM_CLASSES = 21  # from uHumans2 office labelspace

REMAP_LUT = np.zeros(256, dtype=np.uint8)
for raw_id, remapped_id in REMAP.items():
    if raw_id < 256:
        REMAP_LUT[raw_id] = remapped_id

def apply_remap(seg_array: np.ndarray) -> np.ndarray:
    clipped = np.clip(seg_array, 0, 255).astype(np.uint8)
    return REMAP_LUT[clipped]

# check if remap works on sample data
drive_path = "/lustre/nvwulf/home/admanoharan/semantics/dataset/uhumans"
model_dir = "/lustre/nvwulf/home/admanoharan/semantics/models/oneformer_ade20k_swin_large/trained_on_uhumans/"
sample_seg = next(Path(f"{drive_path}/tesse_seg_cam_converted_image_raw/tesse_seg_cam_converted_image_raw").glob("*.jpg"))
raw = np.array(Image.open(sample_seg))
remapped = apply_remap(raw)

print(f"Raw labels:      {sorted(np.unique(raw).tolist())}")
print(f"Remapped labels: {sorted(np.unique(remapped).tolist())}")
print(f"All remapped IDs within 0-20: {remapped.max() <= 20}")

# Load model config
model_config = OneFormerConfig.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
model_config.num_queries= 250
model_config.text_encoder_n_ctx = 16
model_config.num_text = model_config.num_queries - model_config.text_encoder_n_ctx
processor = OneFormerProcessor.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
processor.image_processor.num_text = model_config.num_text
processor.task_seq_length = 77

model_config.num_labels = NUM_CLASSES
model_config.is_training=True

UHUMANS2_CLASSES = [
    "unknown", "air_vent", "books", "floor", "ceiling_light",
    "chair", "bench", "couch", "stairs", "cabinet",
    "computer", "lamp", "painting", "plant", "sign",
    "stairs", "desk", "cubicle", "trashcan", "wall", "human"
]
model_config.id2label = {i: name for i, name in enumerate(UHUMANS2_CLASSES)}
model_config.label2id = {name: i for i, name in enumerate(UHUMANS2_CLASSES)}

# Load pretrained weights then replace the classification head with the new one for 21 classes. The rest of the weights are kept and will be fine-tuned.
model = OneFormerForUniversalSegmentation.from_pretrained(
    "shi-labs/oneformer_ade20k_swin_large",
    config=model_config,
    ignore_mismatched_sizes=True
)


# Dataset class
class UHumans2Dataset(Dataset):
    def __init__(self, rgb_dir, seg_dir, processor):
        self.rgb_files = sorted(Path(rgb_dir).glob("*.jpg"))
        self.seg_dir = Path(seg_dir)
        self.processor = processor
        missing = [f.name for f in self.rgb_files if not self._find_seg(f)]
        if missing:
            print(f"{len(missing)} files missing seg pair. First 3: {missing[:3]}")
        print(f"Dataset: {len(self.rgb_files)} samples")

    def _find_seg(self, rgb_path):
        for ext in [".jpg", ".png"]:
            p = self.seg_dir / (rgb_path.stem + ext)
            if p.exists():
                return p
        return None

    def __len__(self):
        return len(self.rgb_files)

    def __getitem__(self, idx):
        rgb_path = self.rgb_files[idx]
        seg_path = self._find_seg(rgb_path)
        if seg_path is None:
            raise FileNotFoundError(f"No seg for {rgb_path.name}")

        image = Image.open(rgb_path).convert("RGB")

        # Load and remap labels
        raw_seg = np.array(Image.open(seg_path))
        if raw_seg.ndim == 3:
            raw_seg = raw_seg[:, :, 0]
        remapped_seg = apply_remap(raw_seg)
        seg = Image.fromarray(remapped_seg)

        inputs = self.processor(
            images=image,
            segmentation_maps=seg,
            task_inputs=["panoptic"],
            return_tensors="pt"
        )

        processed_inputs = {}
        for k, v in inputs.items():
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], torch.Tensor):
                processed_inputs[k] = v[0]
            elif isinstance(v, torch.Tensor):
                processed_inputs[k] = v.squeeze(0)
            else:
                processed_inputs[k] = v

        return processed_inputs
'''
mask_labels and class_labels stay as lists — variable targets per image. 
Model's forward expects them as lists of tensors, so we keep them as lists and move to device in training loop. 
The rest are fixed-size tensors that can be stacked in collate_fn.
'''
def collate_fn(batch):
    collated = {}
    for key in batch[0].keys():
        if key in ["pixel_values", "pixel_mask", "text_inputs", "task_inputs"]:
            collated[key] = torch.stack([b[key] for b in batch])
        else:
            collated[key] = [b[key] for b in batch]
    return collated

# Training
dataset = UHumans2Dataset(
    rgb_dir=f"{drive_path}/tesse_left_cam_rgb_image_raw/tesse_left_cam_rgb_image_raw",
    seg_dir=f"{drive_path}/tesse_seg_cam_converted_image_raw/tesse_seg_cam_converted_image_raw",
    processor=processor
)

# Test sample before training
print("\nTesting single sample...")
sample = dataset[0]
print("Keys:", list(sample.keys()))
print("pixel_values shape:", sample["pixel_values"].shape)
print("Single sample OK ")

loader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=2, collate_fn=collate_fn)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\nTraining on: {device}")
model = model.to(device)

# lower LR for backbone, higher for the new head
backbone_params, head_params = [], []

for name, param in model.named_parameters():
    if "backbone" in name:
        backbone_params.append(param)
    else:
        head_params.append(param)

optimizer = torch.optim.AdamW(
    [
        {"params": backbone_params, "lr": 1e-5},
        {"params": head_params, "lr": 1e-4},
    ]
)


scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=7 * len(loader)
)

best_loss = float("inf")
model.train()

for epoch in range(7):
    epoch_loss = 0.0
    for i, batch in enumerate(loader):
        batch_on_device = {}
        for k, v in batch.items():
            if isinstance(v, torch.Tensor):
                batch_on_device[k] = v.to(device)
            elif isinstance(v, list):
                batch_on_device[k] = [
                    item.to(device) if isinstance(item, torch.Tensor) else item
                    for item in v
                ]
            else:
                batch_on_device[k] = v

        outputs = model(**batch_on_device)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        epoch_loss += loss.item()

        if i % 20 == 0:
            print(f"  Epoch {epoch+1} [{i}/{len(loader)}] loss: {loss.item():.4f}")

    avg = epoch_loss / len(loader)
    print(f"Epoch {epoch+1} avg loss: {avg:.4f}")

    if avg < best_loss:
        best_loss = avg
        model.save_pretrained(model_dir + "/oneformer_uhumans2_best")
        processor.save_pretrained(model_dir + "/oneformer_uhumans2_best")
        print(f" Saved best model (loss={avg:.4f})")

model.save_pretrained(model_dir)
processor.save_pretrained(model_dir)
print("Training complete.")
