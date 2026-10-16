# The explorer: build the data from this checkout of otk, build the static site,
# and serve it with nginx; a second image ("sheets") draws the PDF sheets. Build
# from the repository root:
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

# The PDF sheets behind the "download PDF" button: otk's own renderer, with the
# TLWG Loma Thai font for matplotlib (its line height fits the renderer's layout). Built as its own image
# (compose's "sheets" service, target "sheets"); nginx forwards /api/ to it.
FROM python:3.12-slim AS sheets
RUN apt-get update \
 && apt-get install -y --no-install-recommends fonts-tlwg-loma-ttf \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY pyproject.toml README.md LICENSE LICENSE-CONTENT ./
COPY otk ./otk
RUN pip install --no-cache-dir . && rm -rf /src
WORKDIR /
ENV MPLCONFIGDIR=/tmp/matplotlib GENERATOR_DIAGRAM_DIR=/tmp/diagrams PYTHONUNBUFFERED=1
USER nobody
EXPOSE 8000
CMD ["python", "-m", "otk.tools.explorer_pdf", "--serve", "--port", "8000"]

FROM nginx:1.29-alpine
COPY explorer/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=site /site/build /usr/share/nginx/html
