# SiteOn AI CLI Bridge

This bridge lets the browser-based builder send the current SiteOn project JSON to a local AI CLI. It does not call an API from the builder.

## Start

```bat
node tools\siteon-ai-cli-bridge.mjs
```

Then open the builder and use **AI CLI 보강**.

With no CLI configured, the bridge only saves request files to `ai-requests/`. This is useful for checking the prompt before connecting a CLI.

## Connect a CLI

Set the CLI command before starting the bridge.

For a CLI that reads the prompt from stdin:

```bat
set SITEON_AI_CLI=codex.cmd
set SITEON_AI_ARGS=exec
node tools\siteon-ai-cli-bridge.mjs
```

For a CLI that expects the prompt as the final command argument:

```bat
set SITEON_AI_CLI=claude.cmd
set SITEON_AI_ARGS=-p
set SITEON_AI_PROMPT_MODE=arg
node tools\siteon-ai-cli-bridge.mjs
```

Exact CLI arguments can differ by installed tool version. If the CLI does not return a JSON object, the builder will keep the request file and show that it could not apply the response.

## Required AI Output

The CLI must return only valid JSON. A full project response is safest:

```json
{
  "project": {
    "v": 4,
    "fields": {},
    "state": {}
  }
}
```

The `project` value should be the complete updated project JSON, not a partial patch.

For smaller edits, the builder also accepts a patch response:

```json
{
  "patch": {
    "fields": {
      "f_slogan": "New hero headline"
    },
    "state": {},
    "customCode": {
      "css": ".siteon-page { scroll-behavior: smooth; }",
      "headHtml": "",
      "bodyHtml": ""
    }
  },
  "imagePrompts": [
    {
      "target": "hero",
      "prompt": "Korean clinic reception...",
      "recommendedAspectRatio": "16:9",
      "alt": "Clinic reception",
      "negativePrompt": "blurry, distorted text"
    }
  ],
  "geo": {
    "summary": "Local SEO suggestions"
  }
}
```

The builder sends `siteon/ai-cli-edit-v2` requests with task types for copy, image prompts, GEO optimization, and HTML/CSS custom code.

## Local Settings

- `SITEON_AI_PORT`: default `4627`
- `SITEON_AI_CLI`: CLI executable, for example `codex.cmd`
- `SITEON_AI_ARGS`: CLI arguments before the prompt
- `SITEON_AI_PROMPT_MODE`: `stdin` or `arg`, default `stdin`
- `SITEON_AI_TIMEOUT_MS`: default `180000`
- `SITEON_AI_MAX_BODY_MB`: default `80`

The server binds to `127.0.0.1` only.
