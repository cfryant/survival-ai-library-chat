# Low-power offline models by hardware

**Last verified 2026-10-28.** Every repo was checked with the Hugging Face API: it exists, it is not gated, the exact
filename is in its file list, and the size comes from the API. Every `resolve/main` link returned HTTP 302, which is
the normal redirect to the download CDN. Every app, store and release URL returned HTTP 200. Machine-readable copy:
[`models.json`](models.json).

Rules used: battery life first; when in doubt, go one size smaller. Only official sources: the model maker's own
Hugging Face org, or unsloth / bartowski / ggml-org for GGUF files, plus official app stores and GitHub releases. Every
model listed is **Apache-2.0** and instruction-tuned. The kit runs Qwen3.5 with reasoning (thinking) **off**.
Sizes are the file size in GB (1 GB = 10^9 bytes). RAM figures are rough estimates for 4096 tokens of context.

## Model files

| ID | File (exact) | Size | ~RAM | Download | Why |
|---|---|---|---|---|---|
| `qwen35-0.8b-q4km` | `Qwen3.5-0.8B-Q4_K_M.gguf` | 0.53 GB | ~1 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_K_M.gguf) | Smallest Qwen3.5. Runs on almost anything, but only manages short summaries. |
| `qwen35-0.8b-q40` | `Qwen3.5-0.8B-Q4_0.gguf` | 0.51 GB | ~1 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_0.gguf) | llama.cpp repacks Q4_0 for ARM, so this is the fastest choice on old ARM chips, a Raspberry Pi or a phone. |
| `qwen35-2b-q4km` | `Qwen3.5-2B-Q4_K_M.gguf` | 1.28 GB | ~2 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/resolve/main/Qwen3.5-2B-Q4_K_M.gguf) | Main pick for low-RAM machines. |
| `qwen35-2b-q40` | `Qwen3.5-2B-Q4_0.gguf` | 1.21 GB | ~2 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/resolve/main/Qwen3.5-2B-Q4_0.gguf) | The 2B as Q4_0, for ARM processors. |
| `qwen35-4b-q4km` ★ | `Qwen3.5-4B-Q4_K_M.gguf` | 2.74 GB | ~3.5 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/resolve/main/Qwen3.5-4B-Q4_K_M.gguf) | The kit's battery model. Best quality for the power it draws, and it stays accurate when summarizing passages from the library. |
| `qwen35-4b-q40` | `Qwen3.5-4B-Q4_0.gguf` | 2.58 GB | ~3.3 GB | [repo](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF) · [file](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/resolve/main/Qwen3.5-4B-Q4_0.gguf) | The 4B as Q4_0, for ARM processors. |
| `qwen35-9b-q4km` ★ | `Qwen_Qwen3.5-9B-Q4_K_M.gguf` | 6.17 GB | ~7 GB (8k ctx) | [repo](https://huggingface.co/bartowski/Qwen_Qwen3.5-9B-GGUF) · [file](https://huggingface.co/bartowski/Qwen_Qwen3.5-9B-GGUF/resolve/main/Qwen_Qwen3.5-9B-Q4_K_M.gguf) | The kit's plugged-in model. Reasons noticeably better than the 4B. |
| `gemma4-12b-qat` (optional) | `gemma-4-12b-it-qat-q4_0.gguf` | 6.98 GB | ~9 GB (8k ctx) | [repo](https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf) · [file](https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf/resolve/main/gemma-4-12b-it-qat-q4_0.gguf) | Google's own QAT quant. A strong summarizer, but heavier. An alternative for plugged-in use only. |
| `gemma4-e2b-litert` | `gemma-4-E2B-it.litertlm` | 2.59 GB | ~3 GB | [repo](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm) · [file](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm/resolve/main/gemma-4-E2B-it.litertlm) | Google AI Edge Gallery only, not a GGUF. Uses the GPU on phones. |
| `gemma4-e4b-litert` | `gemma-4-E4B-it.litertlm` | 3.66 GB | ~4.5 GB | [repo](https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm) · [file](https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm/resolve/main/gemma-4-E4B-it.litertlm) | Google AI Edge Gallery only, for phones with 12 GB+. |
| `qwen35-4b-litert` | `Qwen3.5-4B_mixed_int4.litertlm` | 2.75 GB | ~3.5 GB | [repo](https://huggingface.co/litert-community/Qwen3.5-4B) · [file](https://huggingface.co/litert-community/Qwen3.5-4B/resolve/main/Qwen3.5-4B_mixed_int4.litertlm) | Qwen3.5-4B for Edge Gallery, text only. Needs LiteRT-LM 0.15 or newer. |

★ = the two models the Windows launchers use. Their exact filenames are hard-coded in the `.bat` files.

Gemma 4 E2B/E4B **GGUF** files were left out on purpose. Their per-layer embeddings make them bigger than Qwen3.5-4B:
E2B Q4_K_M is 3.1 GB and E4B is 5.0 GB, which means more RAM and more battery for no gain here.

## 1. NVIDIA (CUDA): llama.cpp `win-cuda-12.4` build + `cudart`

| VRAM | Primary | Fallback | Notes |
|---|---|---|---|
| 4–6 GB | `qwen35-4b-q4km` | `qwen35-2b-q4km` | On a 4 GB card, keep context at 4096. If it runs out of memory, use the 2B. |
| 8 GB | `qwen35-9b-q4km` (plugged in) | `qwen35-4b-q4km` (battery) | This is what the kit's two launchers already do. |
| 12 GB+ | `qwen35-9b-q4km` | `qwen35-4b-q4km` | Optional plugged-in alternative: `gemma4-12b-qat`. |

Use the CUDA **12.4** zip for the widest GPU support. The 13.4 zip needs a newer driver and drops older GPUs.

## 2. AMD / Intel GPU (Vulkan): llama.cpp `win-vulkan` build

| GPU | Primary | Fallback | Notes |
|---|---|---|---|
| Integrated GPU, 16 GB system RAM | `qwen35-4b-q4km` | `qwen35-2b-q4km` | The kit's "lowest power" launcher. |
| Integrated GPU, 8 GB system RAM | `qwen35-2b-q4km` | `qwen35-0.8b-q4km` | An integrated GPU's memory comes out of system RAM. |
| Discrete GPU, 8 GB+ | `qwen35-9b-q4km` | `qwen35-4b-q4km` | |

## 3. CPU only: llama.cpp `win-cpu` / `ubuntu-x64` build

| RAM | Primary | Fallback | Notes |
|---|---|---|---|
| 16 GB+ | `qwen35-4b-q4km` | `qwen35-2b-q4km` | The 9B works but is slow on a CPU and drains the battery. |
| 8 GB | `qwen35-4b-q4km` | `qwen35-2b-q4km` | Use context 4096 and `--cache-ram 0`, and close the browser. |
| 4 GB | `qwen35-2b-q4km` | `qwen35-0.8b-q4km` | |
| Very old / no AVX2 | `qwen35-0.8b-q4km` | `qwen35-0.8b-q40` | Expect a few tokens per second. LM Studio requires AVX2; the llama.cpp CPU build picks a matching CPU variant when it starts. |

## 4. Apple Silicon Mac: llama.cpp `macos-arm64` (Metal) or LM Studio

| Unified memory | Primary | Fallback | Notes |
|---|---|---|---|
| 8 GB | `qwen35-4b-q4km` | `qwen35-2b-q4km` | macOS keeps a large share of memory for itself. |
| 16 GB | `qwen35-9b-q4km` | `qwen35-4b-q4km` | Use the 4B on battery. |
| 24 GB+ | `qwen35-9b-q4km` | `qwen35-4b-q4km` | Optional: `gemma4-12b-qat`. |

Install notes:

- **llama.cpp:** extract `llama-bXXXX-bin-macos-arm64.tar.gz` (a `.tar.gz` now, not a `.zip`). The binaries are
  unsigned, so run `xattr -dr com.apple.quarantine <folder>` once. Then start the server with
  `./llama-server -m model.gguf -c 4096 --port 8080`. Metal is on by default.
- **LM Studio:** download from <https://lmstudio.ai/download>. It needs macOS 14+ on Apple Silicon. It is a normal
  installed app, not a portable one. Once the models are on disk it works fully offline. It can load your own GGUF files
  (`lms import` or drag-and-drop) and has built-in "Chat with Documents".

## 5. Intel Mac: llama.cpp `macos-x64` build (CPU)

LM Studio does **not** support Intel Macs ([system requirements](https://lmstudio.ai/docs/app/system-requirements)).

| RAM | Primary | Fallback |
|---|---|---|
| 8 GB | `qwen35-2b-q4km` | `qwen35-0.8b-q4km` |
| 16 GB+ | `qwen35-4b-q4km` | `qwen35-2b-q4km` |

## 6. iPhone / iPad

| Device RAM | Primary | Fallback | Notes |
|---|---|---|---|
| 4 GB (e.g. iPhone 12/13, older iPads) | `qwen35-0.8b-q4km` | `qwen35-0.8b-q40` | iOS limits each app to well under total RAM. |
| 6 GB (e.g. iPhone 13 Pro–15) | `qwen35-2b-q4km` | `qwen35-0.8b-q4km` | The 4B may load, but iOS may kill the app. |
| 8 GB+ (iPhone 15 Pro and later, M-series iPad) | `qwen35-4b-q4km` | `qwen35-2b-q4km` | |

Apps:

- **[PocketPal AI](https://apps.apple.com/us/app/pocketpal-ai/id6502579498)** (iOS 15.1+, free). Loads your own GGUF
  files from the Files app or from Hugging Face. It has **no PDF/document chat**, so paste in the passages you need.
- **[Locally AI](https://apps.apple.com/us/app/locally-ai-by-lm-studio/id6741426692)** (by LM Studio; iOS 18.1+,
  free). Uses its own curated MLX catalog, which includes Qwen3.5 and Apple's on-device Foundation Model, and **cannot
  load GGUF files**. A third-party comparison says it reads PDF/Word/CSV files, but the official listing doesn't say so.
- **[Google AI Edge Gallery](https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337)** (iOS 17+, iPhone
  only). Gemma 4 downloads inside the app. No PDF chat.

## 7. Android

| Device RAM | Primary | Fallback | Notes |
|---|---|---|---|
| 4 GB | `qwen35-0.8b-q40` | `qwen35-0.8b-q4km` | Q4_0 is the fastest format on ARM. |
| 6 GB | `qwen35-2b-q40` | `qwen35-0.8b-q40` | |
| 8 GB | `qwen35-4b-q40` | `qwen35-2b-q40` | Edge Gallery alternative: `gemma4-e2b-litert`. |
| 12 GB+ | `qwen35-4b-q40` | `qwen35-2b-q40` | Edge Gallery: `gemma4-e4b-litert` or `qwen35-4b-litert`. |

Apps:

- **PocketPal AI:** [Google Play](https://play.google.com/store/apps/details?id=com.pocketpalai) or
  [APK on GitHub](https://github.com/a-ghorbani/pocketpal-ai/releases). Loads your own GGUF files. No document chat.
- **[ChatterUI](https://github.com/Vali-98/ChatterUI/releases)** (APK only; v0.10.0 from 2026-09-22). Its
  "Use External Model" option runs a GGUF straight from storage. No PDF support; its keyword "Lorebooks" are the only
  retrieval feature. The developer recommends Q4_0 on Snapdragon 8 Gen 1+ and Exynos 2200+.
- **Google AI Edge Gallery:** [Google Play](https://play.google.com/store/apps/details?id=com.google.ai.edge.gallery)
  (Android 12+) or [APK on GitHub](https://github.com/google-ai-edge/gallery/releases). It does **not** load GGUF. To
  add your own model, copy a `.litertlm` file into Download, then tap **+** and import it. No PDF chat.
- **MLC Chat:** not recommended. It was last updated in 2024 (iOS 1.6, 2024-09-27), uses its own model format and
  can't run Qwen3.5.

## 8. Raspberry Pi 5 (64-bit OS): llama.cpp `ubuntu-arm64` build

| RAM | Primary | Fallback |
|---|---|---|
| 4 GB | `qwen35-0.8b-q40` | `qwen35-0.8b-q4km` |
| 8 GB | `qwen35-2b-q40` | `qwen35-0.8b-q40` |
| 16 GB | `qwen35-4b-q40` (slow) | `qwen35-2b-q40` |

## llama.cpp builds

Releases: <https://github.com/ggml-org/llama.cpp/releases>. The kit was tested with
[b11669](https://github.com/ggml-org/llama.cpp/releases/tag/b11669). The newest build on 2026-10-28 was
[b11971](https://github.com/ggml-org/llama.cpp/releases/tag/b11971). The `bNNNN` builds are now flagged
"pre-release", and GitHub's "Latest" badge points at a `v0.8.0` entry with no binaries, so **pick a `bNNNN` tag, not
"Latest"**.

| Target | Asset name pattern |
|---|---|
| Windows x64, NVIDIA | `llama-bXXXX-bin-win-cuda-12.4-x64.zip` **+** `cudart-llama-bin-win-cuda-12.4-x64.zip` (13.4 variants also exist) |
| Windows x64, Vulkan | `llama-bXXXX-bin-win-vulkan-x64.zip` |
| Windows x64, CPU | `llama-bXXXX-bin-win-cpu-x64.zip` |
| macOS Apple Silicon | `llama-bXXXX-bin-macos-arm64.tar.gz` |
| macOS Intel | `llama-bXXXX-bin-macos-x64.tar.gz` |
| Linux x64 (CPU) | `llama-bXXXX-bin-ubuntu-x64.tar.gz` (Vulkan: `llama-bXXXX-bin-ubuntu-vulkan-x64.tar.gz`) |
| Linux ARM64 / Raspberry Pi | `llama-bXXXX-bin-ubuntu-arm64.tar.gz` |

## Dropped during verification

These returned 401 from the Hugging Face API (missing or private) on 2026-10-28, so they were left out:
`ggml-org/Qwen3.5-4B-GGUF`, `bartowski/google_gemma-4-12B-it-GGUF`, `microsoft/Phi-4-mini-instruct-gguf`.
Also skipped: LFM3 (non-Apache "other" license) and Qwen3.8-27B (16 GB, far too big).
