# RapidX Annotator
*Industrial radiographic image annotation & enhancement toolkit*

![build](https://img.shields.io/github/actions/workflow/status/yourname/rapidx-annotator/ci.yml?label=CI)
![license](https://img.shields.io/github/license/yourname/rapidx-annotator)

> **Made with ❤️ for non‑destructive testing (NDT) researchers and practitioners.**

---

## ✨ Features

- **One‑click YOLO pre‑annotation** – batch infer bounding boxes or segmentation masks with any YOLOv5/v8 weights.
- **Flexible manual annotation** – rectangle, polygon, point; copy‑paste, snapping, length/area overlay.
- **Real‑time enhancement panel** – contrast‑stretch, gamma, pseudo‑color, denoise, sharpen … instant preview without altering raw data.
- **Ultra‑large radiograph tiling** – slice >10 k × k images, annotate patch‑wise, then auto‑merge to original coordinates.
- **Multi‑format export** – Pascal‑VOC XML, COCO JSON, YOLO txt, PNG mask.
- **Bilingual UI** – English / 中文 with editable class‑name mapping.
- **Action log & optional user login** – traceable annotation history for QA.


## 🖼️ Screenshot

![Main window](docs/screenshot_main.png)


## 🗂️ Directory structure
```text
github/
├─ main.py                # application entry (PyQt)
├─ classes.txt            # default defect classes (中文)
├─ classes_en2ch.txt      # EN ↔ ZH label map
├─ libs/                  # core libraries
│  ├─ predict.py          # YOLO / PaddleX inference wrapper
│  ├─ enhance.py          # image‑enhancement ops
│  ├─ divideimage.py      # large‑image tiling
│  ├─ lab/                # I/O for XML / JSON / mask
│  └─ view/               # QGraphics items & scene
└─ wins/                  # GUI windows + Qt Designer *.ui
```

---

## ⚡ Installation

### Prerequisites
* Python ≥ 3.8
* Git
* (Optional) NVIDIA GPU + CUDA 11.x for faster inference

### 1 · Clone & install dependencies
```bash
git clone https://github.com/yourname/rapidx-annotator.git
cd rapidx-annotator

pip install -r requirements.txt  # PyQt5, opencv-python, ultralytics …

# Windows‑specific: install pywin32
pip install pywin32   # auto‑skipped on Linux / macOS
```
> For GPU inference install **torch** matching your CUDA version *before* `ultralytics`.

### 2 · Launch GUI
```bash
python main.py
```

### 3 · (Optional) Conda virtual environment
```bash
conda create -n rapidx python=3.10
conda activate rapidx
```

---

## 🚀 Typical workflow
1. **Create / edit classes** – *Class Window* → save `classes.txt`.
2. **Import images** – *File ▸ Open folder…*.
3. *(Optional)* **Run YOLO pre‑label** – *Tools ▸ Predict…*.
4. **Refine labels** – draw / edit with mouse & keyboard shortcuts.
5. **Export annotations** – *File ▸ Export…* choose VOC, COCO, YOLO or Seg.

---

## 🔧 Configuration
Adjust defaults in `libs/config.py` (paths, tiling size, enhancement presets, language).  
Most options can be overridden via environment variables – see inline comments.

---

---

## 📄 License

Source code released under the **GNU Affero General Public License v3.0** – see `LICENSE`.

### Patent notice
Algorithm covered by Chinese patent **ZL 2023 1 0448168.8** is **free for academic and research purposes**.  
**Commercial use** (including deployment in proprietary products or cloud services) **requires a separate written license** from the patent holder. Contact <your-email@example.com> for details.

---

## 📝 Citation
```bibtex
@software{yu_rapidx_annotator_2025,
  author = {Xinghua Yu and Contributors},
  title  = {RapidX Annotator: Industrial Radiographic Image Annotation & Enhancement Toolkit},
  year   = 2025,
  url    = {https://github.com/yourname/rapidx-annotator},
}
```

---

## 🙏 Acknowledgements
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [PaddleX](https://github.com/PaddlePaddle/PaddleX)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt)
- [OpenCV](https://opencv.org/)

---
<sub>© 2025 Xinghua Yu & Contributors · Released under AGPL‑3.0 · All trademarks are property of their respective owners.</sub>

