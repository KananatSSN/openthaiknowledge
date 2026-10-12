# Explorer

A website for exploring the problem sets, and nothing else. It has the same
curriculum board as TutorRank's `/skills` page: a column per subject, a row per
level, a card per unit. Open a unit to see its sets, then pick a set to see its
example questions with answers and hints, the mistake behind each wrong choice,
where the set came from, and a link to its code. You can search by name, topic,
key or indicator code, filter by subject, and switch the labels between Thai
and English. A link such as `/?set=math.polynomial_area_m2` opens that set.

`/contribute` shows the repository's `README.md`, rendered at build time, with
a copy button on every code block, including the set-up prompt contributors
paste into their agent. Edit the README, not the page.

There are no accounts, no progress tracking and no practice; those stay in
TutorRank.

It has no server. `python -m otk.tools.explorer_data` writes everything the
site shows into `static/data/` (git-ignored, about 30 MB), and the build is
plain files.

## Develop

```bash
# from the repository root, with otk installed (uv pip install -e .)
python -m otk.tools.explorer_data     # catalog, examples and pictures -> explorer/static/data
cd explorer
npm ci
npm run dev                           # http://localhost:5173
npm run check
```

## Host it (Docker and Cloudflare Tunnel)

The image builds the data from the checked-out release, builds the site, and
serves it with nginx. It listens on this machine only, at
`127.0.0.1:8090`, so nothing is exposed until a tunnel points at it.

On the machine that serves it (the Mac mini), once:

```bash
git clone https://github.com/KananatSSN/openthaiknowledge.git
```

Then, for each release:

```bash
openthaiknowledge/explorer/deploy.sh          # checks out the newest tag, builds, starts, waits until it answers
openthaiknowledge/explorer/deploy.sh v0.4.0   # or a given tag
openthaiknowledge/explorer/deploy.sh stop
```

Put it on the internet with the Cloudflare Tunnel TutorRank already runs on that
machine. In Cloudflare: **Zero Trust → Networks → Tunnels → your tunnel →
Public hostnames → Add**, with

| Field | Value |
|---|---|
| Subdomain / domain | e.g. `explore` . `yourdomain` |
| Service | `HTTP` · `host.docker.internal:8090` |

`host.docker.internal` is how the tunnel's container (Docker Desktop) reaches a
port on the Mac itself. TutorRank's own containers and configuration are not
touched, and the explorer keeps running when TutorRank is stopped. Only the
tunnel is shared. To give the explorer its own tunnel instead, run a
`cloudflare/cloudflared` container with that tunnel's token and the same
service URL.

Set `EXPLORER_PORT` to use another port; change the tunnel's service URL to
match.

## GitHub Pages

The `Explorer site` workflow can publish the same build to GitHub Pages
(`BASE_PATH=/openthaiknowledge npm run build`; Settings → Pages → Source:
GitHub Actions). It is disabled: the explorer is hosted through the tunnel
instead.
