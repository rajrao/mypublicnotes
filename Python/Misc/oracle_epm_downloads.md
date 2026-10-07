# Downloading Oracle EPM Files with Concurrent Partial Downloads

A guide to downloading application-snapshot files from **Oracle EPM Cloud**
(Planning / PBCS / EPBCS / FCCS and related services) faster, by combining
the EPM Interop REST API with concurrent HTTP range requests.

This code can speed up the download of files from Oracle EPM dramatically. I found that it could potentially speed up downloads by over 4 times and could potentially be speed up by increasing number of workers.

The code snippets are illustrative. They show the shape of each step, not a
drop-in library.

---

## Why EPM needs special handling

With an ordinary file server you issue one `GET` and read the body. Oracle
EPM is different in two ways that matter here:

1. **A download is an asynchronous job.** You don't download the file
   directly. You ask EPM to prepare the application snapshot, it runs a
   job, and only when that job finishes does it give you a link to the
   actual bytes.
2. **The responses are JSON "envelopes," not files.** Until the bytes are
   ready, every response is a small JSON document describing job status and
   carrying links to follow — not the file content.

So an EPM download is really three phases:

```
Start the export job  ->  Poll until it finishes  ->  Download the bytes
```

Concurrent partial downloads apply only to the **third** phase. The first
two are a request/poll loop against JSON envelopes.

---

## The EPM Interop REST API

Downloads use the Interop (migration / lifecycle) REST API and the
`applicationsnapshots` resource. The entry point is the `/contents`
sub-resource of a snapshot:

```
GET {base_url}/interop/rest/v1/applicationsnapshots/{file}/contents
```

Notes on the URL:

- `v1` is a version-agnostic alias; EPM also accepts dated versions such as
  `11.1.2.3.600`. Prefer `v1` unless you have a reason to pin a build.
- `{file}` must be **URL-encoded**. A path like `inbox/Actuals.csv` becomes
  `inbox%2FActuals.csv`.
- Authentication is HTTP Basic (an EPM identity-domain user), typically
  over the service's standard HTTPS endpoint.

---

## The JSON envelope

Every job/status response is a small JSON document with a `status` field
and a `links` array:

```json
{
  "details": null,
  "status": -1,
  "links": [
    { "rel": "self",       "href": "https://.../contents" },
    { "rel": "Job Status", "href": "https://.../contents/7049...6910165" }
  ]
}
```

The `status` field is a tri-state signal:

| `status` | Meaning                               | What to do            |
|---------:|---------------------------------------|-----------------------|
| `-1`     | Job accepted / still running (async)  | Poll the status link  |
| `0`      | Completed successfully                | Follow the download link |
| `> 0`    | Error (see `details`)                 | Fail with the message |

You navigate by **link relation (`rel`)**, not by hard-coded URLs:

- `rel = "Job Status"` — the URL to poll while the job runs.
- `rel = "Download link"` — the URL that serves the file bytes once ready.

```python
def get_link(body, rel):
    for link in body.get("links", []):
        if link.get("rel") == rel:
            return link.get("href")
    return None
```

> **Important:** EPM often returns HTTP `200` even for a *failed* request —
> the real outcome is inside the JSON (`status > 0` with a `details`
> message). Treat the envelope's `status`, not just the HTTP code, as the
> source of truth.

---

## Phase 1 + 2: start the job and poll

Call `/contents`. If the envelope says `status == -1`, follow the
`Job Status` link and poll it until the job stops being in-progress, then
read the `Download link`.

```python
def resolve_download_link(base_url, file_name, auth):
    url = f"{base_url}/interop/rest/v1/applicationsnapshots/{encode(file_name)}/contents"
    body = get_json(url, auth)

    if command_status(body) > 0:
        raise EpmError(body.get("details"))

    # Some responses include the download link immediately.
    link = get_link(body, "Download link")
    if link:
        return link

    # Otherwise poll the Job Status link until the job finishes.
    status_url = get_link(body, "Job Status")
    return poll_until_ready(status_url, auth)


def poll_until_ready(status_url, auth):
    while True:
        body = get_json(status_url, auth)
        status = command_status(body)

        if status > 0:
            raise EpmError(body.get("details"))     # job failed
        if status != -1:                            # finished
            return get_link(body, "Download link")

        sleep(POLL_INTERVAL)                        # still running
```

Give the poll loop an overall timeout so a stuck job can't block forever.

---

## Phase 3: the download link and the finalize gotcha

Once you have the `Download link`, it serves the file bytes and — this is
the useful part — it **supports HTTP range requests**. That is what lets
you download pieces concurrently.

But there is one trap worth stating plainly:

> **Do not send `q={download:complete}` on your data requests.**
>
> That query parameter is EPM's server-side *finalize / cleanup* signal.
> When present, EPM responds `206` with an **empty body** (`Content-Length:
> 0`). Sent on a data range, it produces a perfectly "successful" download
> of **zero bytes**. Use it only as a deliberate end-of-transfer cleanup
> call, never on the chunks that carry data.

A plain ranged request against the download link (no `q` parameter) returns
the data and the total size:

```
GET {download_link}
Range: bytes=0-10485759

HTTP/1.1 206 Partial Content
Content-Type: application/octet-stream
Content-Range: bytes 0-10485759/164626432
```

The `/164626432` is the total file size — the number you need to plan all
the ranges.

---

## Phase 3, continued: concurrent partial download

With a range-capable download link, this phase is the standard concurrent
partial download:

1. **Probe** one range to learn the total size from `Content-Range`.
2. **Plan** every `(start, end)` range from that size.
3. **Pre-allocate** the output file to the full size.
4. **Fetch ranges concurrently**, each with its own retry/backoff.
5. **Write each piece at its offset** (positioned write under a lock).

```python
def download_bytes(download_link, output_path, auth):
    total, first = probe_total_size(download_link, auth)   # one range GET

    if total is None:                      # server ignored Range -> 200
        save(output_path, first)           # single-stream fallback
        return

    preallocate(output_path, total)
    lock = Lock()

    with open(output_path, "r+b") as f:
        write_at(f, 0, first, lock)        # reuse the probe's bytes

        def worker(byte_range):
            start, end = byte_range
            offset, data = fetch_range(download_link, start, end, auth)
            write_at(f, offset, data, lock)

        ranges = plan_ranges(total, RANGE_SIZE, len(first))
        run_in_parallel(worker, ranges, max_workers=MAX_WORKERS)
```

Everything you'd do for a generic file applies here: retry each range
independently with exponential backoff, bound memory at
`workers x range size`, and fall back to a single stream if the link ever
answers `200` instead of `206`.

---

## End-to-end flow

```mermaid
flowchart TD
    A[Start] --> B[GET /applicationsnapshots/{file}/contents<br/>Basic auth]
    B --> C[Parse JSON envelope]
    C --> D{status value}
    D -->|status greater than 0| E[Error: read details, fail]
    D -->|status 0 or link present| H[Read Download link]
    D -->|status -1| F[Follow Job Status link]
    F --> G[Poll status URL]
    G --> G2{Job finished?}
    G2 -->|No, status -1| G
    G2 -->|Failed, status greater than 0| E
    G2 -->|Yes| H

    H --> I[Probe one range on download link<br/>no q parameter]
    I --> J{206 with Content-Range?}
    J -->|No, got 200| K[No range support<br/>single-stream fallback]
    J -->|Yes| L[Read total size<br/>Pre-allocate output file]
    L --> M[Plan ranges and dispatch to workers]

    subgraph Pool [Concurrent range workers]
        W1[Fetch range A, retry] --> X1[Write A at offset]
        W2[Fetch range B, retry] --> X2[Write B at offset]
        W3[Fetch range C, retry] --> X3[Write C at offset]
    end

    M --> Pool
    Pool --> N{All ranges done?}
    N -->|Some failed| O[Report failure]
    N -->|Yes| P[File complete]
    K --> P
```

---

## EPM-specific guidance and trade-offs

| Topic | Guidance |
|---|---|
| **status vs HTTP code** | Trust the envelope's `status`. EPM returns `200` even on logical failures; the real error is `status > 0` + `details`. |
| **Link navigation** | Follow links by `rel` (`Job Status`, `Download link`), never by assembling URLs by hand. |
| **The `q` parameter** | Keep `q={download:complete}` off every data range. It is a finalize signal that returns an empty body. |
| **Range size** | A range of a few MB (e.g. 10 MB) is a reasonable unit; it matches EPM's own tooling defaults. |
| **Worker count** | EPM links are often latency-bound and jittery. A handful of workers (e.g. 4) usually overlaps enough wait time; measure before pushing higher. |
| **Poll interval & timeout** | Poll every few seconds and cap the total wait. Large snapshot exports can take a while to prepare. |
| **Fallback** | Always handle a `200` on the download link as "no range support" and stream normally. |
| **Does parallel always help?** | Not always. If the EPM link serializes or rate-limits concurrent requests, parallelism won't speed it up. Benchmark sequential vs concurrent on a representative file. |

### Error cases to handle explicitly

- **File not found / invalid file** — comes back as an envelope with
  `status > 0` and a `details` message, usually on the very first
  `/contents` call. Surface the `details` text; don't treat the `200` as
  success.
- **Job never completes** — guard the poll loop with a deadline.
- **Empty download** — if a "successful" download produces 0 bytes, the
  prime suspect is a stray `q={download:complete}` on a data request.

---

## A simple complete example

A minimal, self-contained illustration using the `requests` library. It
performs all three phases: start the export job, poll until ready, then
download the bytes with four concurrent range workers writing at offsets.
Error handling is kept light for clarity.

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://<your-epm-host>"      # e.g. https://planning-xxxx.epm.<region>.ocs.oraclecloud.com
RANGE_SIZE = 10 * 1024 * 1024             # 10 MB per range
MAX_WORKERS = 4
POLL_INTERVAL = 3                         # seconds between job-status polls
POLL_TIMEOUT = 30 * 60                    # give up on the job after 30 min


class EpmError(Exception):
    pass


def _get_link(body, rel):
    for link in body.get("links", []) or []:
        if link.get("rel") == rel:
            return link.get("href")
    return None


def resolve_download_link(file_name, auth):
    """Phase 1 + 2: start the export job and poll for the download link."""
    url = (f"{BASE_URL}/interop/rest/v1/applicationsnapshots/"
           f"{quote(file_name, safe='')}/contents")

    body = requests.get(url, auth=auth, timeout=300).json()
    if int(body.get("status", 0)) > 0:
        raise EpmError(body.get("details"))

    link = _get_link(body, "Download link")
    if link:
        return link

    status_url = _get_link(body, "Job Status")
    if not status_url:
        raise EpmError("no Job Status or Download link in response")

    deadline = time.time() + POLL_TIMEOUT
    while True:
        if time.time() > deadline:
            raise EpmError("timed out waiting for the export job")
        body = requests.get(status_url, auth=auth, timeout=300).json()
        status = int(body.get("status", 0))
        if status > 0:
            raise EpmError(body.get("details"))
        if status != -1:                                  # job finished
            return _get_link(body, "Download link")
        time.sleep(POLL_INTERVAL)


def fetch_range(download_link, start, end, auth):
    """Fetch one byte range. Note: NO q parameter on data requests."""
    headers = {"Range": f"bytes={start}-{end}"}
    resp = requests.get(download_link, auth=auth, headers=headers, timeout=300)
    resp.raise_for_status()
    return start, resp.content


def download(file_name, output_path, auth):
    """Phase 3: concurrent partial download of the resolved link."""
    download_link = resolve_download_link(file_name, auth)

    # Probe one range to learn the total size (reuse its bytes).
    probe = requests.get(download_link, auth=auth,
                         headers={"Range": f"bytes=0-{RANGE_SIZE - 1}"},
                         timeout=300)

    if probe.status_code != 206 or "/" not in probe.headers.get("Content-Range", ""):
        # Server did not honor the range: fall back to a single stream.
        with open(output_path, "wb") as f:
            f.write(probe.content)
        print(f"Downloaded {len(probe.content)} bytes (single stream).")
        return

    total = int(probe.headers["Content-Range"].split("/")[-1])
    first = probe.content

    # Pre-allocate the file so each worker can write at its own offset.
    with open(output_path, "wb") as f:
        f.truncate(total)

    # Plan the remaining ranges (the first piece is already in hand).
    ranges = []
    pos = len(first)
    while pos < total:
        end = min(pos + RANGE_SIZE - 1, total - 1)
        ranges.append((pos, end))
        pos = end + 1

    lock = threading.Lock()
    with open(output_path, "r+b") as f:
        with lock:
            f.seek(0)
            f.write(first)

        def worker(byte_range):
            start, data = fetch_range(download_link, *byte_range, auth)
            with lock:
                f.seek(start)
                f.write(data)
            return len(data)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            for _ in pool.map(worker, ranges):
                pass

    print(f"Downloaded {total} bytes to {output_path} "
          f"using {MAX_WORKERS} workers.")


if __name__ == "__main__":
    auth = HTTPBasicAuth("user@example.com", "<password>")
    download("new_export.csv", "new_export.csv", auth)
```

**What to notice**

1. `resolve_download_link` handles the EPM job lifecycle — start, poll on
   `status == -1`, fail on `status > 0`, then read the `Download link`.
2. Links are followed by `rel`, and the envelope's `status` (not the HTTP
   code) decides success or failure.
3. The data requests send **no `q` parameter** — that avoids the empty-body
   finalize behavior.
4. The download link is probed once for the total size, the file is
   pre-allocated, and ranges are fetched concurrently and written at their
   offsets.
5. If the link answers `200` instead of `206`, it falls back to a plain
   single-stream download.
```
