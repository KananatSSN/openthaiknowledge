# The explorer as one image: build the data from this checkout of otk, build the
# static site, and serve it with nginx. Build from the repository root:
#
#   docker compose -f explorer/compose.yml up -d --build

FROM python:3.12-slim AS data
WORKDIR /src
COPY pyproject.toml README.md LICENSE LICENSE-CONTENT ./
COPY otk ./otk
RUN pip install --no-cache-dir . && python -m otk.tools.explorer_data --out /data

FROM node:22-slim AS site
WORKDIR /site
COPY explorer/package.json explorer/package-lock.json ./
RUN npm ci
COPY explorer/ ./
# The contribute page renders the repository's README.
COPY README.md README.th.md /
COPY --from=data /data ./static/data
RUN npm run build

FROM nginx:1.29-alpine
COPY explorer/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=site /site/build /usr/share/nginx/html
