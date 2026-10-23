---
name: dsh-magpie
display_name: "dsh-magpie"
display_name_en: "dsh-magpie"
description: Explain how to use a local magpie gateway from DeepSeek Harness, including the model list, quota, and routing groups.
description_zh: 说明怎样从 DeepSeek Harness 使用本机 magpie 网关，查看可用模型、额度和路由组。
description_en: Use a local magpie gateway from DeepSeek Harness, including the model list, quota, and routing groups.
category: data-analysis
version: 1.0.0
author: Hylouis233
---
# Using magpie from DeepSeek Harness

magpie is a local gateway that puts every subscription you already pay for —
coding plans, chat plans, model providers — behind one OpenAI-compatible
endpoint, and picks the account that serves each call.
This skill explains how to work with it from a DSH session.

## Check what is available first

The gateway lists every model your signed-in plans can serve:

```bash
curl -s -H "Authorization: Bearer $MAGPIE_GATEWAY_KEY" http://127.0.0.1:3425/v1/models \
  | jq -r '.data[] | "\(.id)\t\(.magpie_label // "")"'
```

Model ids are `<provider>/<model>`, for example `acme-code/glm-5.3` or
`acme-cloud/gpt-6.1-sol`. The prefix names the subscription the call is billed
to, so picking a model is picking which plan pays.

## Read what is left before a long run

```bash
magpie quota            # every subscription's remaining allowance
magpie quota <provider> --json
```

A provider with a spent window answers with an error rather than silently
falling back, so check quota before starting something long.

## Prefer the routing groups when you have no reason to pick

A model id that starts with `auto/` (or `group/`) is a routing group: magpie
sends it to whichever member is healthy and has room. This is the right default
for unattended work where you do not care which plan serves it.

## Shape of a call

```bash
curl -s http://127.0.0.1:3425/v1/chat/completions \
  -H "Authorization: Bearer $MAGPIE_GATEWAY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/auto",
    "stream": true,
    "messages": [{"role": "user", "content": "hello"}]
  }'
```

The gateway streams server-sent events and accepts the OpenAI-compatible fields:
`messages`, `tools`, `temperature`, `max_tokens`, `stop` and
`reasoning_effort`.

## Reasoning effort

Models that reason accept `reasoning_effort`. Ask the listing for the levels a
given model takes — they differ per model:

```bash
curl -s -H "Authorization: Bearer $MAGPIE_GATEWAY_KEY" http://127.0.0.1:3425/v1/models \
  | jq -r '.data[] | select(.id=="auto/auto") | .reasoning_levels'
```

Sending an effort the model does not list is refused by the upstream provider, so
read the list rather than guessing.

## Multiple computers

A gateway can be shared on a local network. Point another machine's DSH at it by
setting `baseURL` to that machine's address and using a gateway key from the
Gateway page; keys are per-caller and can be scoped to specific models or
accounts:

```bash
magpie gateway-key add laptop
magpie gateway-key models <id> acme-code/* auto/*
```

## Troubleshooting

| Symptom | What it means |
| --- | --- |
| HTTP 401 | The gateway key is wrong or was revoked. Read it from the Gateway page. |
| `ECONNREFUSED` | Nothing is listening at that address. Start magpie, or check the port. |
| `Illegal API invocation from an unapproved channel` (11128) | The upstream vendor refused the request because of the words in the prompt. Change the wording, or route the same request to a different provider. |
| An empty reply, no error | Read the gateway's own log; a spent allowance usually explains it. |

---

[![](https://img.shields.io/badge/powered_by-dsh-4D6BFE?style=flat-square&logo=deepseek&logoColor=white)](https://github.com/deepseek-ai/deepseek-harness)
