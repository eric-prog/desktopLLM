# DesktopLLM - A Lightning fast setup to run any model on a Desktop native app

If you seek an effortlessly immersive chat experience with an LLM model directly on your desktop, DesktopLLM is for you. Interact with an LLM of your choice, have your entire chat history saved locally, search to find answers, and swap betweel models of your choice! 

## ☀️ Features

✅ Access to full chat history <br>
✅ Easy search history (no more scrolling) <br>
✅ Model and token settings (yes you can swap between different models that you have and customize the number of tokens in the responses!) <br>
✅ Interactive chat <br>
✅ Simple UI (trivial) <br>

## ⚙️ Setup

1. Clone the repository:

```
git clone https://github.com/eric-prog/desktopLLM
```

2. Install dependencies:

```
npm run setup
```

3. Choosing the model:

If you're on a device that has around 8gb of RAM, smaller language models like [Phi-2](https://huggingface.co/TheBloke/phi-2-GGUF) are great.

## 💻 Running the Application 

To run the application: 

```
npm run llm
```

## 📁 Folder Structure 

- `app` folder: contains our main file, `desktopllm.py`
- `example_models` folder: contains the quantized dolphin Phi-2 model (great for devices with small RAM i.e. 8gb)

> **_NOTE:_**  The application is purely written in Python

## ⚠️ Issue Reporting

For any issues or suggestions, feel free to open an issue in the GitHub repository.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/eric-prog/desktopLLM/blob/main/LICENSE) file for details.