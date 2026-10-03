#!/usr/bin/env python3
"""用 GitHub Git Data API 把本地仓库目录全量推成一个 commit。

为什么不用 git push: 某些环境下 github.com:443 不可达而 api.github.com 可达
(本机就是: git push 会 134s 超时 + gnutls_handshake)。本脚本走 REST。
另注: 空仓库第一次调用 POST /git/blobs 会 409 — 必须先用 Contents API
落一个初始 commit，本脚本假定远程已有 ref。

用法:
  GITHUB_TOKEN_FILE=~/.github_token TARGET_OWNER=SymonChu \
  TARGET_REPO=design-md-templates REPO_DIR=/path/to/repo \
      python3 push-templates-to-github.py "commit message"
"""
import os, sys, json, time, base64, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OWNER = os.environ.get("TARGET_OWNER", "SymonChu")
REPO = os.environ.get("TARGET_REPO", "design-md-templates")
ROOT = os.environ.get("REPO_DIR",
                      os.path.join(HERE, "..", "..", "..", "design-md-collection"))
TOKEN_FILE = os.environ.get("GITHUB_TOKEN_FILE", os.path.expanduser("~/.github_token"))
BRANCH = os.environ.get("TARGET_BRANCH", "main")
API = f"https://api.github.com/repos/{OWNER}/{REPO}"
MSG = sys.argv[1] if len(sys.argv) > 1 else "sync: templates"
TOK = open(os.path.expanduser(TOKEN_FILE)).read().strip()


def api(method, url, payload=None, tries=3):
    last = None
    for _ in range(tries):
        try:
            data = json.dumps(payload).encode() if payload is not None else None
            req = urllib.request.Request(url, data=data, method=method, headers={
                "User-Agent": "hermes", "Accept": "application/vnd.github+json",
                "Authorization": "token " + TOK, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
                return json.loads(b) if b else {}
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (409, 502, 503):
                time.sleep(1.5)
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(1.5)
    raise last


def main():
    paths = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != ".git"]
        for f in sorted(fn):
            paths.append(os.path.relpath(os.path.join(dp, f), ROOT))
    print(f"repo dir: {ROOT}\nfiles: {len(paths)}")
    t0 = time.time()
    tree = []
    for i, p in enumerate(paths, 1):
        c = base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()
        sha = api("POST", f"{API}/git/blobs", {"content": c, "encoding": "base64"})["sha"]
        tree.append({"path": p, "mode": "100644", "type": "blob", "sha": sha})
        if i % 25 == 0:
            print(f"  blobs {i}/{len(paths)} ({time.time()-t0:.0f}s)")
    tsha = api("POST", f"{API}/git/trees", {"tree": tree})["sha"]
    parent = api("GET", f"{API}/git/ref/heads/{BRANCH}")["object"]["sha"]
    csha = api("POST", f"{API}/git/commits",
               {"message": MSG, "tree": tsha, "parents": [parent]})["sha"]
    api("PATCH", f"{API}/git/refs/heads/{BRANCH}", {"sha": csha})
    print(f"parent: {parent[:10]}  ->  new commit: {csha[:10]}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
