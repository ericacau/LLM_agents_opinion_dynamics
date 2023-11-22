# Python Project Template
[![SBD++](https://img.shields.io/badge/Available%20on-SoBigData%2B%2B-green)](https://sobigdata.d4science.org/group/sobigdata-gateway/explore?siteId=20371853)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Server

To start the LLM server 

```bash
python -m llama_cpp.server --model mistral-7b-instruct-v0.1.Q4_K_M.gguf --n_gpu_layers 40 --host 10.8.0.1 --port 8081
```

#### Server parameters:
[--model MODEL] [--model_alias MODEL_ALIAS] [--n_ctx N_CTX] [--n_gpu_layers N_GPU_LAYERS] [--tensor_split TENSOR_SPLIT]
                   [--rope_freq_base ROPE_FREQ_BASE] [--rope_freq_scale ROPE_FREQ_SCALE] [--seed SEED] [--n_batch N_BATCH] [--n_threads N_THREADS]
                   [--f16_kv F16_KV] [--use_mlock USE_MLOCK] [--use_mmap USE_MMAP] [--embedding EMBEDDING] [--low_vram LOW_VRAM]
                   [--last_n_tokens_size LAST_N_TOKENS_SIZE] [--logits_all LOGITS_ALL] [--cache CACHE] [--cache_type CACHE_TYPE] [--cache_size CACHE_SIZE]
                   [--vocab_only VOCAB_ONLY] [--verbose VERBOSE] [--host HOST] [--port PORT] [--interrupt_requests INTERRUPT_REQUESTS] [--n_gqa N_GQA]
                   [--rms_norm_eps RMS_NORM_EPS] [--mul_mat_q MUL_MAT_Q]

## License
This project is licensed under the terms of the BSD-2-Clause license.

## Acknowledgements
This repository was developed within the [SoBigData++](https://sobigdata.d4science.org/group/sobigdata-gateway/explore?siteId=20371853) H2020 project training activities (WP4) to support "Social Mining and Big Data resources Integration" (WP8).

## Contact(s)
[Giulio Rossetti](mailto:giulio.rossetti@gmail.com) - CNR-ISTI 

Twitter: [@giuliorossetti](https://twitter.com/GiulioRossetti)

Mastodon: [@giuliorossetti@mastodon.uno](https://mastodon.uno/@giuliorossetti)

