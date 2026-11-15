> Historical design/deployment note. This portfolio does not include the full deployment, referenced services, or all scripts. These notes are not a current security certification or runnable setup guide.

# Orbit local model benchmark

This bounded check exercises the two selected local Ollama models with a fixed read-only prompt. It measures elapsed time and records the returned text. It does not call the network beyond the existing loopback Ollama endpoint and does not enable tools or external actions.

Run inside Orbit:

```text
python3 scripts/orbit-model-benchmark.py
```

The benchmark is observational only. It is not a quality evaluation or permission to route consequential work to either model.

