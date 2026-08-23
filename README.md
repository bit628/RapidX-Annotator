<p align="center">
  <a href="http://znhj.tz-ndt.com/">
    <img src="docs/rapidx-cover.png" alt="RapidX Annotator — Industrial Radiographic Image Annotation & Enhancement" width="100%">
  </a>
</p>

<p align="center">
  <strong>A desktop workspace for industrial radiographic image inspection, enhancement, and annotation.</strong><br>
  面向工业射线图像查看、增强与缺陷标注的科研桌面工具。
</p>

<p align="center">
  <a href="https://www.microsoft.com/windows/"><img alt="Platform: Windows" src="https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows11&logoColor=white"></a>
  <a href="https://www.python.org/"><img alt="Source: Python" src="https://img.shields.io/badge/Source-Python-3776AB?logo=python&logoColor=white"></a>
  <a href="https://www.qt.io/qt-for-python"><img alt="GUI: PyQt5" src="https://img.shields.io/badge/GUI-PyQt5-41CD52?logo=qt&logoColor=white"></a>
  <a href="https://doi.org/10.1016/j.softx.2025.102328"><img alt="SoftwareX paper" src="https://img.shields.io/badge/SoftwareX-10.1016%2Fj.softx.2025.102328-0A66C2"></a>
  <a href="https://doi.org/10.1007/s10921-025-01186-w"><img alt="SWRD dataset paper" src="https://img.shields.io/badge/SWRD-Dataset%20Paper-F59E0B"></a>
</p>

<p align="center">
  <a href="http://znhj.tz-ndt.com/"><strong>Research Group Website / 课题组官网</strong></a>
  &nbsp;·&nbsp;
  <a href="https://drive.google.com/drive/folders/1LNUt101wufTBJpRAgrZAU1h-Tfx629wO?usp=sharing"><strong>SWRD Dataset / 数据集</strong></a>
  &nbsp;·&nbsp;
  <a href="#quick-start"><strong>Quick Start</strong></a>
  &nbsp;·&nbsp;
  <a href="#publications-and-citation"><strong>Publications</strong></a>
  &nbsp;·&nbsp;
  <a href="CONTRIBUTING.md"><strong>Contributing</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/bit628/RapidX-Annotator/issues/new/choose"><strong>Report an Issue</strong></a>
</p>

---

## Overview

RapidX Annotator supports a practical human-in-the-loop workflow for non-destructive testing (NDT): open industrial radiographs, improve defect visibility, create or refine annotations, and save structured labels for downstream analysis and model development.

| At a glance | Details |
| --- | --- |
| **Platform** | Windows desktop; several modules depend on `pywin32` |
| **Image input** | TIFF/TIF, DICOM/DICONDE, PNG, JPEG, and BMP |
| **Annotation** | Bounding boxes and polygon regions |
| **Label output** | Pascal VOC XML and JSON |
| **Companion data** | SWRD: 3,675 seam-weld radiographs with six defect classes |
| **Project status** | Research source release; model modules and trained weights are not bundled |

> [!NOTE]
> The public source tree includes the batch-prediction interface, but not every referenced model implementation or trained weight. Manual annotation and image-processing code are included; AI-assisted pre-annotation requires a compatible local model setup.

## Highlights

| Capability | What RapidX provides |
| --- | --- |
| **Radiography workspace** | Large-image viewing, zooming, rotation, flipping, and local signal-to-noise inspection |
| **Flexible annotation** | Rectangle and polygon tools with configurable defect classes |
| **Image enhancement** | Contrast adjustment, denoising, sharpening, grayscale, pseudo-color, and positive/negative display |
| **Research workflow** | XML/JSON export, user management, operation logs, and an interface for model-assisted pre-annotation |

## Quick start

RapidX Annotator is currently distributed as a **research source snapshot**, not as a packaged Windows installer.

> [!IMPORTANT]
> `requirements.txt` preserves legacy and model-specific dependency pins, including both Qt generations and PaddleX-related packages. It has not yet been normalized into a portable lock file. Use an isolated Windows environment and review the dependency versions for your Python and model stack before installation.

```powershell
git clone https://github.com/bit628/RapidX-Annotator.git
cd RapidX-Annotator

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

cd src
python main.py
```

If the full dependency snapshot conflicts with your environment, install the application dependencies in a dedicated environment and configure PaddleX/model dependencies separately. See [Contributing](CONTRIBUTING.md) before proposing dependency changes.

## Companion SWRD dataset

The **SWRD (Seam Weld Radiographic Dataset)** is the companion resource for weld-defect research.

| **3,675 images** | **2 weld forms** | **6 defect classes** | **3 research tasks** |
| :---: | :---: | :---: | :---: |
| Original X-ray images | Standard and T-joint seam welds | Porosity, inclusion, crack, undercut, lack of fusion, lack of penetration | Classification, detection, segmentation |

- **Download:** [SWRD dataset on Google Drive](https://drive.google.com/drive/folders/1LNUt101wufTBJpRAgrZAU1h-Tfx629wO?usp=sharing)
- **Cite:** [SWRD: A Dataset of Radiographic Image of Seam Weld for Defect Detection](https://doi.org/10.1007/s10921-025-01186-w)

Please review the dataset provider's terms and cite the dataset paper when using the data in research.

## Typical workflow

1. Define or edit defect categories in the class manager.
2. Open one radiograph or a folder of supported images.
3. Apply display enhancement to improve the visibility of low-contrast indications.
4. Draw or refine rectangular and polygon annotations.
5. Save annotations as XML or JSON.
6. Optionally configure a compatible model for batch pre-annotation.

## Architecture and source layout

<details>
<summary><strong>View the system architecture and annotation workflow</strong></summary>

### System architecture

![Flowchart of the RapidX Annotator system architecture](docs/Fig%202%20Flowchart%20of%20System%20Architecture.jpg)

### Annotation workflow and deep-learning integration

![RapidX Annotator annotation workflow and deep-learning integration](docs/Fig%204%20Annotation%20Workflow%20and%20Deep%20Learning%20Integration.jpg)

</details>

<details>
<summary><strong>View the repository structure</strong></summary>

```text
RapidX-Annotator/
├── demo_data/              # Small radiographic-image examples
├── docs/                   # Architecture figures and project artwork
├── requirements.txt        # Research dependency snapshot
└── src/
    ├── main.py             # PyQt application entry point
    ├── classes.txt         # Default defect classes
    ├── classes_en2ch.txt   # English-to-Chinese class mapping
    ├── libs/
    │   ├── enhance.py      # Image-enhancement algorithms
    │   ├── predict.py      # Batch prediction integration
    │   ├── label.py        # Annotation save/load workflow
    │   ├── divideimage.py  # Large-image tiling utilities
    │   ├── lab/            # XML/JSON and image I/O
    │   └── view/           # Annotation graphics and scenes
    └── wins/               # Application windows and generated UI code
```

</details>

## Publications and citation

GitHub users can select **Cite this repository** in the sidebar, powered by [`CITATION.cff`](CITATION.cff). If RapidX Annotator supports your work, please cite the SoftwareX article:

```bibtex
@article{li2025rapidx,
  title   = {RapidX annotator: A specialized software tool for industrial radiographic image annotation and enhancement},
  author  = {Li, Yan and Qiu, Hao and Wang, Xu and Dong, Na and Yu, Xinghua},
  journal = {SoftwareX},
  volume  = {31},
  pages   = {102328},
  year    = {2025},
  doi     = {10.1016/j.softx.2025.102328}
}
```

For the companion dataset:

```bibtex
@article{zhao2025swrd,
  title   = {SWRD: A Dataset of Radiographic Image of Seam Weld for Defect Detection},
  author  = {Zhao, Xuefeng and Wu, Juntao and Zhang, Baoxin and Wen, Haoyu and Wang, Xiaopeng and Li, Yan and Yu, Xinghua},
  journal = {Journal of Nondestructive Evaluation},
  volume  = {44},
  number  = {2},
  pages   = {50},
  year    = {2025},
  doi     = {10.1007/s10921-025-01186-w}
}
```

## Community and support

| Need | Where to go |
| --- | --- |
| Report a reproducible bug | [Open a structured bug report](https://github.com/bit628/RapidX-Annotator/issues/new?template=01_bug_report.yml) |
| Suggest an improvement | [Open a feature request](https://github.com/bit628/RapidX-Annotator/issues/new?template=02_feature_request.yml) |
| Contribute code or documentation | Read [CONTRIBUTING.md](CONTRIBUTING.md) |
| Report a vulnerability privately | Follow [SECURITY.md](SECURITY.md) |
| Learn about the research group | Visit the [official website / 课题组官网](http://znhj.tz-ndt.com/) |

## Research group

RapidX Annotator and SWRD are research outputs from the **Institute of Arc Cognitive Manufacturing, Chongqing Innovation Center, Beijing Institute of Technology**.

- [Research group website / 课题组官网](http://znhj.tz-ndt.com/)
- [Institute website / 电弧认知制造技术研究所](https://cqic.bit.edu.cn/kjcx/yjsgk/59d317c8119d4b49974700f9dd24e1cf.htm)
- [Chongqing Innovation Center, Beijing Institute of Technology](https://cqic.bit.edu.cn/)

## License

The repository's `LICENSE.txt` is currently empty, so reuse terms are not yet stated clearly in this source tree. Please contact the maintainers before redistribution or commercial use. This notice should be replaced when the research group approves an open-source license.

## Acknowledgements

RapidX Annotator builds on the Python scientific-computing ecosystem, including PyQt, OpenCV, NumPy, SciPy, pydicom, nibabel, and PaddleX.
