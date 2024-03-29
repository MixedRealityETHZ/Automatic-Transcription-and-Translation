# ATT: Automatic Transcription & Translation with Magic Leap 2

Welcome to the repository for the ATT project, an application designed for the Magic Leap 2 (ML2) glasses, facilitating real-time multilingual communication through transcription and translation. This project was developed by Alejandro Cuadron Lafuente, Elisa Martinez Abad, Ruben Schenk, and Sophya Tsubin at ETH Zürich in cooperation with Lukas Bernreiter from Magic Leap Switzerland.

## Demo Video

[![ATT Demo Video](https://img.youtube.com/vi/7M1DDJBEqbE/0.jpg)](https://www.youtube.com/watch?v=7M1DDJBEqbE)

## Project Overview

ATT (Automatic Transcription & Translation) leverages the capabilities of the Magic Leap 2 glasses, combined with OpenAI's Whisper model, to provide an unobtrusive mixed reality experience in multilingual communication. This repository contains all the components of our project, including the Unity project, the compiled application, the Flask API, the final project report, the poster, and a demo video. For an in-depth explanation of how the project works, check our [final report](./MR-ATT-final-report.pdf).

## Contents

- **att.unitypackage**: Package of our Unity project.
- **MRATT.apk**: Compiled application for the ML2 glasses.
- **api.py**: Flask API script to be run on a server.
- **MR-ATT-final-report.pdf**: Comprehensive project report detailing the development process and findings.
- **MR-ATT-poster-presentation.pdf**: Poster of the poster presentation.

## Prerequisites

- Magic Leap 2 glasses
- A server for running the Flask API with CUDA

In case you want to modify some aspects of the project, you will also need:
- Windows
- Magic Leap Hub
- Unity v2022.3.10f1 (we do not guarantee it works if another version is used)

## Installation and Setup

### Flask server application
The [requirements.txt](requirements.txt) file lists all the packages required for running the project. To create an environment in the server and install the packages run:

```bash
python -m venv .venv
cd .venv/Scripts
activate.bat # If using Windows
activate # If using Unix
```

Then, install all necessary packages:

```bash
cd ../..
python -m pip install -r requirements.txt
```

Now, you can launch the Flask application by executing the `api.py` script:

```bash
python api.py
```

By default, the server runs Whisper with the `large-v3` model. In case you want to use a different one, simply use the following options:
```bash
python api.py -m [tiny|small|medium|large|large-v2|large-v3]
```

#### Error: CUDA unavailable
To fix this, uninstall all `torch` libraries and reinstall them with this command:
```
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

### Unity project

Currently, the server's IP is hardcoded in the Unity scripts. Because of this, you'll need to change the IP to your own and rebuild the app.

First, create an empty Unity project and set it up to work with Magic Leap by following these [tutorials](https://developer-docs.magicleap.cloud/docs/guides/unity/getting-started/unity-getting-started/): "Create a Project", "Configure Project Settings", and "Render Pipeline Settings".

Once the project is set up with ML2, proceed to install MRTK3 in the project. Follow this [tutorial](https://developer-docs.magicleap.cloud/docs/guides/third-party/mrtk3/mrtk3-new-project/) and when prompted to select MRTK3 components for installation, choose "MRTK Input", "MRTK UX Components", and "MRTK UX Components (Non-canvas)". Make sure you check the `RECORD_AUDIO` permission in the final step!

To import the ATT project, go to `Assets -> Import Package -> Custom Package`, and then import the project package `att.unitypackage`. Once imported, a prompt will appear asking you to `Import TMP essentials`. Click on it to finish Unity's setup.

Finally, to change the IP to yours, navigate inside the Unity project to `Assets -> Scripts` and open `TranslationAPI.cs` and `AppStart.cs`. Change the IP to your desired one at `line 8`.

Now that the project is set up, feel free to modify it as much as you want and have fun :D

## Usage

To start the app, start the server as it was mentioned in the previous section and upload the apk to the glasses via the Magic Leap Hub. Once installed, just open the app and follow the on-screen instructions to start transcribing and translating speech in real-time. In case you want to stop the translation, just exit the app using the `HOME` button in the ML2 controller.

## Demo Video, Final Report, and Poster

- **Demo Video**: Take a look at our short [demo video](https://youtu.be/7M1DDJBEqbE) to get a quick overview of the project.
- **Final Report**: Read our [final report](./MR-ATT-final-report.pdf) for detailed insights into the project.
- **Poster**: Check out our [poster](./MR-ATT-poster-presentation.pdf) for a concise summary of the project.

## Contributors

- Alejandro Cuadron Lafuente
- Elisa Martinez Abad
- Ruben Schenk
- Sophya Tsubin

For any queries, please contact us at: `{acuadron,emartine,rschenk,stsubin}@ethz.ch`

## Licenses

The ATT project's original content, developed at ETH Zürich, is licensed under the MIT License. This includes all the source code created by our team.

Additionally, this project uses several open-source components under different licenses:
- Mixed Reality Toolkit 3 (MRTK3) - BSD 3-Clause License
- WavUtility - MIT License
- fast-whisper - MIT License

For the full text of these licenses, see the `LICENSE` file in this repository.
