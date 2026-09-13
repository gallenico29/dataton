"""SVG charts for docs/violencia_crs04_si_no_missing.md (GitHub-renderable)."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "img"
N = 1_419_491

YES = "#c2410c"
NO = "#d6d3d1"
INK = "#1c1917"
MUTED = "#78716c"
GRID = "#e7e5e4"
BG = "#fafaf9"
LIFE = "#a8a29e"
YEAR = "#0369a1"
IDX = ["#a8a29e", "#ca8a04", "#ea580c", "#b91c1c"]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write(name: str, body: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(body, encoding="utf-8")


def stacked_h(
    name: str,
    rows: list[tuple[str, int, int]],
    caption: str,
    width: int = 920,
) -> None:
    left, right, top, row_h, gap = 168, 36, 28, 36, 18
    bar_w = width - left - right
    height = top + len(rows) * (row_h + gap) + 52
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f"<title>{esc(caption)}</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="18" fill="{MUTED}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(caption)}</text>',
    ]
    y = top + 8
    for label, yes, no_n in rows:
        total = yes + no_n
        yw = bar_w * yes / total
        nw = bar_w - yw
        yp = 100 * yes / total
        parts += [
            f'<text x="{left - 10}" y="{y + 24}" text-anchor="end" fill="{INK}" '
            f'font-size="13" font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{esc(label)}</text>",
            f'<rect x="{left}" y="{y}" width="{yw:.2f}" height="{row_h}" '
            f'fill="{YES}" rx="3"/>',
            f'<rect x="{left + yw:.2f}" y="{y}" width="{nw:.2f}" height="{row_h}" '
            f'fill="{NO}" rx="3"/>',
            f'<text x="{left + 8}" y="{y + 24}" fill="#fff7ed" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{yp:.1f}%</text>",
        ]
        y += row_h + gap
    ly = height - 18
    parts += [
        f'<rect x="{left}" y="{ly - 9}" width="12" height="12" fill="{YES}" rx="2"/>',
        f'<text x="{left + 18}" y="{ly}" fill="{INK}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">Sí 12m</text>',
        f'<rect x="{left + 90}" y="{ly - 9}" width="12" height="12" fill="{NO}" rx="2"/>',
        f'<text x="{left + 108}" y="{ly}" fill="{INK}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">No</text>',
        "</svg>",
    ]
    write(name, "\n".join(parts))


def index_bar(name: str) -> None:
    segs = [
        (484842, "0 ninguno", IDX[0]),
        (465436, "1 tipo", IDX[1]),
        (332215, "2 tipos", IDX[2]),
        (136998, "3 tipos", IDX[3]),
    ]
    width, height = 920, 120
    left, right, top = 24, 24, 40
    bar_w, bar_h = width - left - right, 28
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        "<title>Índice 0–3: cuántos tipos a la vez</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="22" fill="{INK}" font-size="13" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">'
        f"65.8% con al menos un tipo · 485 mil / 465 mil / 332 mil / 137 mil</text>",
    ]
    x = left
    for value, label, color in segs:
        w = bar_w * value / N
        parts.append(
            f'<rect x="{x:.2f}" y="{top}" width="{w:.2f}" height="{bar_h}" fill="{color}"/>'
        )
        x += w
    x = left
    for value, label, color in segs:
        w = bar_w * value / N
        pct = 100 * value / N
        parts.append(
            f'<text x="{x + 8:.2f}" y="{top + bar_h + 20}" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{esc(label)} {pct:.1f}%</text>"
        )
        x += w
    parts.append("</svg>")
    write(name, "\n".join(parts))


def grouped_v(name: str) -> None:
    cats = [
        ("Psic. hogar", 887811, 549841),
        ("Fís. hogar", 735865, 289076),
        ("Psic. colegio", 904996, 636673),
        ("Fís. colegio", 226911, 144992),
        ("Sexual", 569769, 325900),
    ]
    width, height = 920, 320
    left, right, top, bottom = 64, 24, 36, 56
    plot_w = width - left - right
    plot_h = height - top - bottom
    ymax = 1_000_000
    group_w = plot_w / len(cats)
    bar_w = 28
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        "<title>Vida vs últimos 12 meses</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="22" fill="{MUTED}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">'
        f"Mujeres SEXO = 1 · N = 1,419,491 · FACTOR_ALUMNOS</text>",
    ]
    for tick in (0, 250_000, 500_000, 750_000, 1_000_000):
        y = top + plot_h * (1 - tick / ymax)
        label = "0" if tick == 0 else f"{tick // 1000}K"
        parts += [
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
            f'stroke="{GRID}" stroke-width="1"/>',
            f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" fill="{MUTED}" '
            f'font-size="11" font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{label}</text>",
        ]
    for i, (label, life, year) in enumerate(cats):
        cx = left + group_w * (i + 0.5)
        for val, color, dx in ((life, LIFE, -bar_w - 2), (year, YEAR, 2)):
            h = plot_h * val / ymax
            x = cx + dx
            y = top + plot_h - h
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" '
                f'fill="{color}" rx="2"/>'
            )
        parts.append(
            f'<text x="{cx:.1f}" y="{height - 28}" text-anchor="middle" fill="{INK}" '
            f'font-size="12" font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{esc(label)}</text>"
        )
    parts += [
        f'<rect x="{left}" y="{height - 16}" width="12" height="12" fill="{LIFE}" rx="2"/>',
        f'<text x="{left + 18}" y="{height - 6}" fill="{INK}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">Algún sí de por vida</text>',
        f'<rect x="{left + 180}" y="{height - 16}" width="12" height="12" fill="{YEAR}" rx="2"/>',
        f'<text x="{left + 198}" y="{height - 6}" fill="{INK}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">Algún sí en últimos 12 meses</text>',
        "</svg>",
    ]
    write(name, "\n".join(parts))


def kpis(name: str) -> None:
    cards = [
        ("59.7%", "Psicológica 12m (sí, ponderado)"),
        ("25.9%", "Física 12m (sí, ponderado)"),
        ("23.0%", "Sexual 12m (sí, ponderado)"),
        ("0", "Missing en ítems madre"),
    ]
    width, height, gap = 920, 110, 16
    cw = (width - 24 - 3 * gap) / 4
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        "<title>Prevalencia 12 meses ponderada</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
    ]
    for i, (value, label) in enumerate(cards):
        x = 12 + i * (cw + gap)
        parts += [
            f'<rect x="{x:.1f}" y="10" width="{cw:.1f}" height="90" fill="#fff" '
            f'stroke="{GRID}" rx="8"/>',
            f'<text x="{x + cw / 2:.1f}" y="52" text-anchor="middle" fill="{INK}" '
            f'font-size="28" font-weight="700" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(value)}</text>',
            f'<text x="{x + cw / 2:.1f}" y="80" text-anchor="middle" fill="{MUTED}" '
            f'font-size="12" font-family="Segoe UI, Helvetica, Arial, sans-serif">'
            f"{esc(label)}</text>",
        ]
    parts.append("</svg>")
    write(name, "\n".join(parts))


def main() -> None:
    kpis("crs04_kpis.svg")
    stacked_h(
        "crs04_targets_12m.svg",
        [
            ("Psicológica (casa o colegio)", 847389, 572102),
            ("Física (casa o colegio)", 367572, 1051919),
            ("Sexual", 325900, 1093592),
        ],
        "% sí en 12 meses · mujeres SEXO = 1 · FACTOR_ALUMNOS · N = 1,419,491 · n = 9,608",
    )
    stacked_h(
        "crs04_ambito.svg",
        [
            ("Psic. hogar", 549841, 869650),
            ("Psic. colegio", 636673, 782818),
            ("Fís. hogar", 289076, 1130415),
            ("Fís. colegio", 144992, 1274499),
            ("Sexual", 325900, 1093592),
        ],
        "Sí = algún ítem del bloque = 1 y filtro 12m = 1. Sexual usa C4P248C_i.",
        width=920,
    )
    index_bar("crs04_indice.svg")
    grouped_v("crs04_vida_vs_12m.svg")
    print(f"wrote {len(list(OUT.glob('crs04_*.svg')))} svgs in {OUT}")


if __name__ == "__main__":
    main()
